# Alla regioner

Den här filen genereras från [data/regioner.csv](data/regioner.csv) och
[data/grannlan.csv](data/grannlan.csv) med `python3 scripts/build.py`.
Ändra inte här – ändra i CSV-filerna och kör skriptet.

**Varje län bestämmer sin egen region.** Där *Beslut* är *lokalt* har länet valt namnet själv;
övriga namn är ett utgångsläge: *uppmätt* = det namn länet redan använder i trafiken, enligt
Beacon · *förslag* = tre bokstäver, ingen i länet har sagt något än. Vill ert län ha ett annat
namn, till exempel SCB-koden, ändrar ni det. Se [CONTRIBUTING.md](CONTRIBUTING.md).

**Uppmätt:** länets egna scopes i kanalmeddelanden som hördes i länet, av alla meddelanden med scope där, från Beacon 2026-10-29–2026-11-11.
Se *Utgångsläget kommer från luften* i [README.md](README.md#utgångsläget-kommer-från-luften).

**Grannlän:** län som ligger inom räckhåll från länet, från [data/grannlan.csv](data/grannlan.csv).
En kantrepeater kan bära ett av dem. Se *Grannlän* i [README.md](README.md#grannlän).

| Län | Region | Beslut | Uppmätt | Ersätter | Grannlän |
| --- | --- | --- | --- | --- | --- |
| Stockholms län | `se-sth` | förslag |  | `se01` | `se-upp`, `se-sor`, `se05`, `se-gtl`, `se-vml`, `se-gav` |
| Uppsala län | `se-upp` | förslag |  | `se03` | `se-sth`, `se-sor`, `se-vml`, `se20`, `se-gav` |
| Södermanlands län | `se-sor` | förslag | `se04` 8 av 13 | `se04` | `se-sth`, `se-upp`, `se05`, `se08`, `se18`, `se-vml` |
| Östergötlands län | `se05` | uppmätt | `se05` 147 av 150 | `se05` | `se-sth`, `se-sor`, `se-jkp`, `se08`, `se-vgr`, `se18`, `se-vml` |
| Jönköpings län | `se-jkp` | lokalt | `se-jkp` 3374 av 3429, `se06` 7 av 3429 | `se06` | `se05`, `se-kro`, `se08`, `se13`, `se-vgr`, `se18` |
| Kronobergs län | `se-kro` | förslag | `se07` 43 av 96 | `se07` | `se-jkp`, `se08`, `se-blk`, `se-ska`, `se13`, `se-vgr` |
| Kalmar län | `se08` | uppmätt | `se08` 5274 av 5362 | `se08` | `se-sor`, `se05`, `se-jkp`, `se-kro`, `se-gtl`, `se-blk` |
| Gotlands län | `se-gtl` | förslag |  | `se09` | `se-sth`, `se08` |
| Blekinge län | `se-blk` | förslag | `se10` 85 av 711 | `se10` | `se-kro`, `se08`, `se-ska` |
| Skåne län | `se-ska` | förslag | `se12` 2047 av 4896 | `se12` | `se-kro`, `se-blk`, `se13` |
| Hallands län | `se13` | uppmätt | `se13` 1418 av 1857 | `se13` | `se-jkp`, `se-kro`, `se-ska`, `se-vgr` |
| Västra Götalands län | `se-vgr` | förslag |  | `se14` | `se05`, `se-jkp`, `se-kro`, `se13`, `se17`, `se18` |
| Värmlands län | `se17` | uppmätt | `se17` 531 av 774 | `se17` | `se-vgr`, `se18`, `se20` |
| Örebro län | `se18` | uppmätt | `se18` 1712 av 2386 | `se18` | `se-sor`, `se05`, `se-jkp`, `se-vgr`, `se17`, `se-vml`, `se20` |
| Västmanlands län | `se-vml` | förslag |  | `se19` | `se-sth`, `se-upp`, `se-sor`, `se05`, `se18`, `se20`, `se-gav` |
| Dalarnas län | `se20` | uppmätt | `se20` 735 av 874 | `se20` | `se-upp`, `se17`, `se18`, `se-vml`, `se-gav`, `se23` |
| Gävleborgs län | `se-gav` | förslag |  | `se21` | `se-sth`, `se-upp`, `se-vml`, `se20`, `se-vnl`, `se23` |
| Västernorrlands län | `se-vnl` | förslag |  | `se22` | `se-gav`, `se23`, `se-vbt` |
| Jämtlands län | `se23` | uppmätt | `se23` 274 av 274 | `se23` | `se20`, `se-gav`, `se-vnl`, `se-vbt` |
| Västerbottens län | `se-vbt` | förslag |  | `se24` | `se-vnl`, `se23`, `se-nbt` |
| Norrbottens län | `se-nbt` | förslag |  | `se25` | `se-vbt` |
