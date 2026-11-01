# Alla regioner

Den här filen genereras från [data/regioner.csv](data/regioner.csv) och
[data/grannlan.csv](data/grannlan.csv) med `python3 scripts/build.py`.
Ändra inte här – ändra i CSV-filerna och kör skriptet.

**Varje län bestämmer sin egen region.** Där *Beslut* är *lokalt* har länet valt namnet själv;
övriga namn är ett utgångsläge: *uppmätt* = det namn länets repeatrar redan bär, enligt
MeshMapper · *förslag* = tre bokstäver, ingen i länet har sagt något än. Vill ert län ha ett annat
namn, till exempel SCB-koden, ändrar ni det. Se [CONTRIBUTING.md](CONTRIBUTING.md).

**Uppmätt:** namn som repeatrar i länet bär, med antal repeatrar av alla uppmätta i länet. Ingen mätning ännu.
Se *Utgångsläget kommer från luften* i [README.md](README.md#utgångsläget-kommer-från-luften).

**Grannlän:** län som ligger inom räckhåll från länet, från [data/grannlan.csv](data/grannlan.csv).
En kantrepeater kan bära ett av dem. Se *Grannlän* i [README.md](README.md#grannlän).

| Län | Region | Beslut | Uppmätt | Ersätter | Grannlän |
| --- | --- | --- | --- | --- | --- |
| Stockholms län | `se-sth` | förslag |  | `se01` | `se-upp`, `se-sor`, `se-ost`, `se-gtl`, `se-vml`, `se-gav` |
| Uppsala län | `se-upp` | förslag |  | `se03` | `se-sth`, `se-sor`, `se-vml`, `se-dal`, `se-gav` |
| Södermanlands län | `se-sor` | förslag |  | `se04` | `se-sth`, `se-upp`, `se-ost`, `se-kal`, `se-ore`, `se-vml` |
| Östergötlands län | `se-ost` | förslag |  | `se05` | `se-sth`, `se-sor`, `se-jkp`, `se-kal`, `se-vgr`, `se-ore`, `se-vml` |
| Jönköpings län | `se-jkp` | förslag |  | `se06` | `se-ost`, `se-kro`, `se-kal`, `se-hal`, `se-vgr`, `se-ore` |
| Kronobergs län | `se-kro` | förslag |  | `se07` | `se-jkp`, `se-kal`, `se-blk`, `se-ska`, `se-hal`, `se-vgr` |
| Kalmar län | `se-kal` | förslag |  | `se08` | `se-sor`, `se-ost`, `se-jkp`, `se-kro`, `se-gtl`, `se-blk` |
| Gotlands län | `se-gtl` | förslag |  | `se09` | `se-sth`, `se-kal` |
| Blekinge län | `se-blk` | förslag |  | `se10` | `se-kro`, `se-kal`, `se-ska` |
| Skåne län | `se-ska` | förslag |  | `se12` | `se-kro`, `se-blk`, `se-hal` |
| Hallands län | `se-hal` | förslag |  | `se13` | `se-jkp`, `se-kro`, `se-ska`, `se-vgr` |
| Västra Götalands län | `se-vgr` | förslag |  | `se14` | `se-ost`, `se-jkp`, `se-kro`, `se-hal`, `se-var`, `se-ore` |
| Värmlands län | `se-var` | förslag |  | `se17` | `se-vgr`, `se-ore`, `se-dal` |
| Örebro län | `se-ore` | förslag |  | `se18` | `se-sor`, `se-ost`, `se-jkp`, `se-vgr`, `se-var`, `se-vml`, `se-dal` |
| Västmanlands län | `se-vml` | förslag |  | `se19` | `se-sth`, `se-upp`, `se-sor`, `se-ost`, `se-ore`, `se-dal`, `se-gav` |
| Dalarnas län | `se-dal` | förslag |  | `se20` | `se-upp`, `se-var`, `se-ore`, `se-vml`, `se-gav`, `se-jam` |
| Gävleborgs län | `se-gav` | förslag |  | `se21` | `se-sth`, `se-upp`, `se-vml`, `se-dal`, `se-vnl`, `se-jam` |
| Västernorrlands län | `se-vnl` | förslag |  | `se22` | `se-gav`, `se-jam`, `se-vbt` |
| Jämtlands län | `se-jam` | förslag |  | `se23` | `se-dal`, `se-gav`, `se-vnl`, `se-vbt` |
| Västerbottens län | `se-vbt` | förslag |  | `se24` | `se-vnl`, `se-jam`, `se-nbt` |
| Norrbottens län | `se-nbt` | förslag |  | `se25` | `se-vbt` |
