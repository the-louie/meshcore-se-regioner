#!/usr/bin/env python3
"""Räknar fram vilket regionnamn varje län använder, från trafiken i Beacon (beacon.meshat.se).

Kör:  python3 scripts/hamta_beacon.py <från> <till> beacon.jsonl    (hämta, se det skriptet)
      python3 scripts/seed.py beacon.jsonl [fler.jsonl ...]         (skriv data/uppmatt.csv)
      python3 scripts/seed.py beacon.jsonl --apply                  (dessutom: regioner.csv)

Varje län mäts i sitt eget Beacon-område (data/beacon-omraden.csv): kanalmeddelanden
(group_text) som observers i länet har hört, räknade per scope. Länets namn är det mest använda
scope som hör till länet. Ett scope hör till länet när det är länets SCB-kod (se06), namnet på
länets rad i regioner.csv, eller ett annat namn som inte är delat (se, eu, europe, offgrid …),
inte danskt eller norskt, inte ett annat läns eller en kommuns SCB-kod, och har mer än hälften av
sina meddelanden i länets område.

Med --apply får ett län som inte har bestämt sig (beslut = forslag eller uppmatt) sitt namn och
märks `uppmatt`, men bara om
  - namnet har minst --min-meddelanden (standard 50) kanalmeddelanden,
  - namnet är minst --min-andel procent (standard 50) av alla kanalmeddelanden med scope som
    hördes i området, så att ett län vars observers mest hör grannar lämnas orört,
  - namnet följer det gemensamma formatet (små a-z, 0-9, enkla bindestreck, högst 29 tecken).
Ett län som har bestämt själv (beslut = lokalt) ändras aldrig.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGIONER = ROOT / "data" / "regioner.csv"
OMRADEN = ROOT / "data" / "beacon-omraden.csv"
UPPMATT = ROOT / "data" / "uppmatt.csv"
UPPMATT_KOLUMNER = ["scb_lan", "lan", "region", "meddelanden", "av", "matt"]
NAMN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAMN_MAX = 29
DELADE = {"se", "eu", "europe", "offgrid", "nordic", "oresund"}
UTLANDSKA = re.compile(r"^(dk|no|fi)(\d|-|$)", re.I)
SCB_KOD = re.compile(r"^se\d{2}(\d{2})?$", re.I)


def load_omraden(path=OMRADEN):
    """{scb_lan: område}. Ett område kan täcka flera län (STO: Stockholm och Uppsala)."""
    with path.open(newline="", encoding="utf-8") as f:
        return {r["scb_lan"]: r["omrade"] for r in csv.DictReader(f)}


def count(paket):
    """{område: Counter(scope -> kanalmeddelanden)} och mätperioden som (första, sista) datum.

    Ett meddelande räknas en gång per område. Paket utan scope-namn (Beacon känner inte igen
    koden) räknas som "?", så att de syns i andelen men aldrig kan bli ett läns namn.
    """
    per_omrade = defaultdict(Counter)
    sett = set()
    tider = []
    for p in paket:
        nyckel = (p["omrade"], p["packetHash"])
        if p.get("payloadTypeName") != "group_text" or nyckel in sett:
            continue
        sett.add(nyckel)
        per_omrade[p["omrade"]][(p.get("scope") or "?").lstrip("#")] += 1
        tider.append(p["firstHeardAt"])
    dag = lambda ms: datetime.fromtimestamp(ms / 1000, timezone.utc).date().isoformat()
    period = (dag(min(tider)), dag(max(tider))) if tider else None
    return per_omrade, period


def hor_till(namn, scb_lan, rad, omrade, per_omrade, totalt):
    if namn in (f"se{scb_lan}", rad["region"]):
        return True
    if namn == "?" or namn.lower() in DELADE or UTLANDSKA.match(namn) or SCB_KOD.match(namn):
        return False
    return 2 * per_omrade[omrade][namn] > totalt[namn]


def lansnamn(rows, omraden, per_omrade):
    """{scb_lan: ([(namn, meddelanden), ...] i fallande ordning, meddelanden med scope i området)}."""
    totalt = Counter()
    for c in per_omrade.values():
        totalt.update(c)
    out = {}
    for rad in rows:
        omrade = omraden.get(rad["scb_lan"])
        if not omrade:
            continue
        c = per_omrade.get(omrade, Counter())
        egna = [(n, k) for n, k in c.items()
                if hor_till(n, rad["scb_lan"], rad, omrade, per_omrade, totalt)]
        out[rad["scb_lan"]] = (sorted(egna, key=lambda t: (-t[1], t[0])), sum(c.values()))
    return out


def write_uppmatt(rows, egna, period, min_lista=5, path=UPPMATT):
    """Namn som används färre än min_lista gånger listas inte: enstaka namn kan vara en
    persons anropssignal eller ett skrivfel, och säger ändå inget om länet."""
    matt = f"{period[0]}–{period[1]}" if period else ""
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(UPPMATT_KOLUMNER)
        for r in sorted(rows, key=lambda r: r["scb_lan"]):
            namn, scopade = egna.get(r["scb_lan"], ([], 0))
            for n, k in namn:
                if k < min_lista:
                    continue
                w.writerow([r["scb_lan"], r["lan"], n, k, scopade, matt])


def apply(rows, egna, min_meddelanden, min_andel):
    """Sätt länets uppmätta namn där reglerna håller. Returnerar ändringarna."""
    tagna = {r["region"] for r in rows if r["beslut"] == "lokalt"}
    andrat = []
    for r in sorted(rows, key=lambda r: r["scb_lan"]):
        namn, scopade = egna.get(r["scb_lan"], ([], 0))
        if r["beslut"] == "lokalt" or not namn:
            continue
        top, k = namn[0]
        if (k < min_meddelanden or 100 * k < min_andel * scopade
                or not NAMN.match(top) or len(top) > NAMN_MAX or top in tagna):
            continue
        if top != r["region"] or r["beslut"] != "uppmatt":
            andrat.append((r["lan"], r["region"], top, k, scopade))
        r["region"], r["beslut"] = top, "uppmatt"
        tagna.add(top)
    return andrat


def option(argv, namn, standard):
    return int(next((a.split("=", 1)[1] for a in argv if a.startswith(f"--{namn}=")), standard))


def main(argv):
    filer = [a for a in argv[1:] if not a.startswith("--")]
    if not filer:
        print(__doc__)
        return 2
    paket = [json.loads(l) for fil in filer for l in Path(fil).open(encoding="utf-8") if l.strip()]
    per_omrade, period = count(paket)
    with REGIONER.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    egna = lansnamn(rows, load_omraden(), per_omrade)
    write_uppmatt(rows, egna, period, option(argv, "min-lista", 5))
    print(f"{len(paket)} paket, {period[0]}–{period[1]}, skrev {UPPMATT.name}" if period
          else "Inga kanalmeddelanden med scope.")
    if "--apply" in argv:
        for lan, fore, efter, k, scopade in apply(
                rows, egna, option(argv, "min-meddelanden", 50), option(argv, "min-andel", 50)):
            print(f"{lan}: {fore} -> {efter} ({k} av {scopade} meddelanden med scope)")
        with REGIONER.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print("Kör python3 scripts/build.py för att skriva om REGIONER.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
