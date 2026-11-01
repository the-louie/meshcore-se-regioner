#!/usr/bin/env python3
"""Validerar data/regioner.csv och data/grannlan.csv och genererar REGIONER.md.

Kör:  python3 scripts/build.py          (validera + skriv REGIONER.md)
      python3 scripts/build.py --check  (validera + kontrollera att REGIONER.md är aktuell)
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "regioner.csv"
GRANNLAN = ROOT / "data" / "grannlan.csv"
UPPMATT = ROOT / "data" / "uppmatt.csv"
OUT = ROOT / "REGIONER.md"
KOLUMNER = ["scb_lan", "lan", "region", "beslut"]
GRANNLAN_KOLUMNER = ["scb_lan", "lan", "scb_grannlan", "grannlan", "via"]
BESLUT = {"forslag", "uppmatt", "lokalt"}
BESLUT_TEXT = {"forslag": "förslag", "uppmatt": "uppmätt", "lokalt": "lokalt"}
UPPMATT_KOLUMNER = ["scb_lan", "lan", "region", "repeatrar", "av", "matt"]
VIA = {"land", "vatten", "omvand", "lokal"}
# Det gemensamma formatet (CONTRIBUTING.md): små a-z, 0-9 och enkla bindestreck, högst 29 tecken.
# Repeatern skiljer på stora och små bokstäver, så bara små tillåts. Vilket namn länet väljer
# inom formatet bestämmer länet.
NAMN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAMN_MAX = 29
SCB_LAN = re.compile(r"^[0-9]{2}$")
SWEDISH_ORDER = str.maketrans({"å": "{", "ä": "|", "ö": "}"})


def swedish_sort_key(name):
    """Sortera å, ä och ö efter z utan beroende på systemets locale."""
    return name.casefold().translate(SWEDISH_ORDER)


def load(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def saknade_kolumner(rows, kolumner, namn):
    for nr, r in enumerate(rows, start=2):
        saknas = [k for k in kolumner if r.get(k) is None]
        if saknas:
            return [f"{namn} rad {nr}: saknar {', '.join(saknas)}"]
    return []


def validate(rows):
    errors = saknade_kolumner(rows, KOLUMNER, "regioner.csv")
    if errors:
        return errors
    if len(rows) != 21:
        errors.append(f"förväntade 21 län, hittade {len(rows)}")
    for r in rows:
        where = f"{r['lan']} ({r['scb_lan']})"
        if not SCB_LAN.match(r["scb_lan"]):
            errors.append(f"{where}: SCB-länskoden är inte två siffror")
        if not NAMN.match(r["region"]) or len(r["region"]) > NAMN_MAX:
            errors.append(
                f"{where}: '{r['region']}' följer inte det gemensamma formatet "
                f"(små a-z, 0-9 och enkla bindestreck, högst {NAMN_MAX} tecken)"
            )
        if r["beslut"] not in BESLUT:
            errors.append(f"{where}: okänt beslut '{r['beslut']}'")
    for col, vad in (("scb_lan", "SCB-länskoden"), ("lan", "länsnamnet"), ("region", "regionen")):
        for v, n in Counter(r[col] for r in rows).items():
            if n > 1:
                errors.append(f"{vad} '{v}' står på {n} rader")
    return errors


def validate_grannlan(rows, grannlan):
    errors = saknade_kolumner(grannlan, GRANNLAN_KOLUMNER, "grannlan.csv")
    if errors:
        return errors
    lan = {r["scb_lan"]: r["lan"] for r in rows}
    for g in grannlan:
        where = f"grannlan.csv: {g['lan']} ({g['scb_lan']}) → {g['grannlan']}"
        for kod, namn in ((g["scb_lan"], g["lan"]), (g["scb_grannlan"], g["grannlan"])):
            if kod not in lan:
                errors.append(f"{where}: länskoden {kod} finns inte i regioner.csv")
            elif lan[kod] != namn:
                errors.append(f"{where}: län {kod} heter '{lan[kod]}' i regioner.csv")
        if g["scb_grannlan"] == g["scb_lan"]:
            errors.append(f"{where}: det egna länet kan inte vara grannlän")
        if g["via"] not in VIA:
            errors.append(f"{where}: okänt värde i via '{g['via']}'")
    par = Counter((g["scb_lan"], g["scb_grannlan"]) for g in grannlan)
    for (a, b), n in par.items():
        if n > 1:
            errors.append(f"grannlan.csv: {lan.get(a, a)} → {lan.get(b, b)} står {n} gånger")
    for a, b in sorted(par):
        if (b, a) not in par:
            errors.append(f"grannlan.csv: {lan.get(a, a)} når {lan.get(b, b)} men inte tvärtom")
    return errors



def validate_uppmatt(rows, uppmatt):
    errors = saknade_kolumner(uppmatt, UPPMATT_KOLUMNER, "uppmatt.csv")
    if errors:
        return errors
    lan = {r["scb_lan"]: r["lan"] for r in rows}
    for u in uppmatt:
        where = f"uppmatt.csv: {u['lan']} {u['region']}"
        if lan.get(u["scb_lan"]) != u["lan"]:
            errors.append(f"{where}: länet finns inte i regioner.csv")
        if not (u["repeatrar"].isdigit() and u["av"].isdigit()):
            errors.append(f"{where}: repeatrar och av ska vara heltal")
    return errors


def render(rows, grannlan, uppmatt=()):
    region = {r["scb_lan"]: r["region"] for r in rows}
    matt = {}
    for u in uppmatt:
        matt.setdefault(u["scb_lan"], []).append(f"`{u['region']}` {u['repeatrar']} av {u['av']}")
    datum = max((u["matt"] for u in uppmatt), default=None)
    grannar = {}
    for g in grannlan:
        grannar.setdefault(g["scb_lan"], []).append(g["scb_grannlan"])
    out = [
        "# Alla regioner",
        "",
        "Den här filen genereras från [data/regioner.csv](data/regioner.csv) och",
        "[data/grannlan.csv](data/grannlan.csv) med `python3 scripts/build.py`.",
        "Ändra inte här – ändra i CSV-filerna och kör skriptet.",
        "",
        "**Varje län bestämmer sin egen region.** Där *Beslut* är *lokalt* har länet valt namnet själv;",
        "övriga namn är ett utgångsläge: *uppmätt* = det namn länets repeatrar redan bär, enligt",
        "MeshMapper · *förslag* = tre bokstäver, ingen i länet har sagt något än. Vill ert län ha ett annat",
        "namn, till exempel SCB-koden, ändrar ni det. Se [CONTRIBUTING.md](CONTRIBUTING.md).",
        "",
        "**Uppmätt:** namn som repeatrar i länet bär, med antal repeatrar av alla uppmätta i länet"
        + (f", från MeshMapper {datum}." if datum else ". Ingen mätning ännu."),
        "Se *Utgångsläget kommer från luften* i [README.md](README.md#utgångsläget-kommer-från-luften).",
        "",
        "**Grannlän:** län som ligger inom räckhåll från länet, från [data/grannlan.csv](data/grannlan.csv).",
        "En kantrepeater kan bära ett av dem. Se *Grannlän* i [README.md](README.md#grannlän).",
        "",
        "| Län | Region | Beslut | Uppmätt | Ersätter | Grannlän |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in sorted(rows, key=lambda r: r["scb_lan"]):
        grann = ", ".join(f"`{region[g]}`" for g in sorted(grannar.get(r["scb_lan"], [])))
        uppm = ", ".join(matt.get(r["scb_lan"], [])[:3])
        out.append(
            f"| {r['lan']} | `{r['region']}` | {BESLUT_TEXT[r['beslut']]} | {uppm} "
            f"| `se{r['scb_lan']}` | {grann} |"
        )
    out.append("")
    return "\n".join(out)


def main():
    rows = load(CSV)
    grannlan = load(GRANNLAN)
    uppmatt = load(UPPMATT) if UPPMATT.exists() else []
    errors = validate(rows)
    if not errors:
        errors = validate_grannlan(rows, grannlan) + validate_uppmatt(rows, uppmatt)
    if errors:
        print("\n".join(f"FEL: {e}" for e in errors))
        return 1
    text = render(rows, grannlan, uppmatt)
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("FEL: REGIONER.md är inte aktuell – kör python3 scripts/build.py")
            return 1
        print(f"OK: {len(rows)} län, inga krockar, REGIONER.md aktuell")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"OK: {len(rows)} län, inga krockar, skrev {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
