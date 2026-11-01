#!/usr/bin/env python3
"""Räknar fram vilka regionnamn repeatrarna i varje län redan bär, från en MeshMapper-export.

Kör:  python3 scripts/seed.py <export.json>           (skriv data/uppmatt.csv)
      python3 scripts/seed.py <export.json> --apply   (dessutom: föreslå namn i regioner.csv)

Exporten hämtas separat med en egen API-nyckel; skriptet gör inga nätanrop och nyckeln hamnar
aldrig i repot. Varje repeater placeras i ett län efter sin position (data/lan.geojson).

Ett namn räknas som länets när fler än hälften av repeatrarna som bär det står i länet. Namn som
inte hör till ett län (`se`, `eu`, `europe` och `offgrid`) räknas aldrig. Namnen räknas exakt som
de är stavade, eftersom repeatern skiljer på `SE06` och `se06`; bara ett namn i det gemensamma
formatet (små a-z, 0-9, enkla bindestreck, högst 29 tecken) kan bli utgångsläge.

Med --apply får ett län som inte har bestämt sig (beslut = forslag eller uppmatt) det vanligaste
sådana namnet, om minst --min-repeatrar repeatrar bär det (standard 2). Raden märks då `uppmatt`.
Ett län som har bestämt själv (beslut = lokalt) ändras aldrig.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGIONER = ROOT / "data" / "regioner.csv"
LAN_GEOJSON = ROOT / "data" / "lan.geojson"
UPPMATT = ROOT / "data" / "uppmatt.csv"
UPPMATT_KOLUMNER = ["scb_lan", "lan", "region", "repeatrar", "av", "matt"]
NAMN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAMN_MAX = 29
DELADE = {"se", "eu", "europe", "offgrid"}


def repeaters_from_export(data):
    """MeshMapper-exporten som (lat, lon, [regionnamn]) per repeater.

    Det enda stället som känner till exportens fältnamn. Antaget format: en lista, eller
    {"repeaters": [...]}, där varje repeater har `lat`, `lon` och `regions` (lista med namn).
    """
    rows = data.get("repeaters", data) if isinstance(data, dict) else data
    out = []
    for r in rows:
        try:
            lat, lon = float(r["lat"]), float(r["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        regions = r.get("regions") or []
        out.append((lat, lon, [str(n).strip() for n in regions]))
    return out


def load_lan(path=LAN_GEOJSON):
    """[(länsnamn, bbox, [polygon, ...])], polygon = [yttre ring, hål, ...] i (lon, lat)."""
    lan = []
    for f in json.loads(path.read_text(encoding="utf-8"))["features"]:
        polys = f["geometry"]["coordinates"]
        xs = [c[0] for p in polys for c in p[0]]
        ys = [c[1] for p in polys for c in p[0]]
        lan.append((f["properties"]["lan"], (min(xs), min(ys), max(xs), max(ys)), polys))
    return lan


def _in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def lan_for(lat, lon, lan):
    for namn, (x0, y0, x1, y1), polys in lan:
        if not (x0 <= lon <= x1 and y0 <= lat <= y1):
            continue
        for poly in polys:
            if _in_ring(lon, lat, poly[0]) and not any(_in_ring(lon, lat, h) for h in poly[1:]):
                return namn
    return None


def measure(repeaters, lan):
    """{län: Counter(namn -> antal repeatrar)}, {län: antal repeatrar}, {namn: Counter(län)}."""
    per_lan = defaultdict(Counter)
    totalt = Counter()
    var = defaultdict(Counter)
    for lat, lon, names in repeaters:
        l = lan_for(lat, lon, lan)
        if l is None:
            continue
        totalt[l] += 1
        for n in set(names):
            if not n or n == "*" or n.lower() in DELADE:
                continue
            per_lan[l][n] += 1
            var[n][l] += 1
    return per_lan, totalt, var


def lansnamn(per_lan, var):
    """Per län: namn som bärs mest i länet, i fallande ordning (fler än hälften av bärarna)."""
    out = {}
    for l, c in per_lan.items():
        egna = [(n, k) for n, k in c.items() if 2 * var[n][l] > sum(var[n].values())]
        out[l] = sorted(egna, key=lambda t: (-t[1], t[0]))
    return out


def write_uppmatt(rows, egna, totalt, matt, path=UPPMATT):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(UPPMATT_KOLUMNER)
        for r in sorted(rows, key=lambda r: r["scb_lan"]):
            for n, k in egna.get(r["lan"], []):
                w.writerow([r["scb_lan"], r["lan"], n, k, totalt[r["lan"]], matt])


def apply(rows, egna, min_repeatrar):
    """Föreslå det vanligaste uppmätta namnet för län som har utgångsläget. Returnerar ändringarna."""
    tagna = {r["region"] for r in rows if r["beslut"] == "lokalt"}
    andrat = []
    for r in sorted(rows, key=lambda r: r["scb_lan"]):
        if r["beslut"] == "lokalt" or not egna.get(r["lan"]):
            continue
        giltiga = [(n, k) for n, k in egna[r["lan"]] if NAMN.match(n) and len(n) <= NAMN_MAX]
        if not giltiga:
            continue
        namn, k = giltiga[0]
        if k < min_repeatrar or namn in tagna:
            continue
        if namn != r["region"] or r["beslut"] != "uppmatt":
            andrat.append((r["lan"], r["region"], namn, k))
        r["region"], r["beslut"] = namn, "uppmatt"
        tagna.add(namn)
    return andrat


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    min_repeatrar = 2
    for a in argv[1:]:
        if a.startswith("--min-repeatrar="):
            min_repeatrar = int(a.split("=", 1)[1])
    data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    repeaters = repeaters_from_export(data)
    per_lan, totalt, var = measure(repeaters, load_lan())
    egna = lansnamn(per_lan, var)
    with REGIONER.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    write_uppmatt(rows, egna, totalt, date.today().isoformat())
    placerade = sum(totalt.values())
    print(f"{len(repeaters)} repeatrar i exporten, {placerade} placerade i ett län, skrev {UPPMATT.name}")
    if "--apply" in argv:
        for lan, fore, efter, k in apply(rows, egna, min_repeatrar):
            print(f"{lan}: {fore} -> {efter} ({k} repeatrar)")
        with REGIONER.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print("Kör python3 scripts/build.py för att skriva om REGIONER.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
