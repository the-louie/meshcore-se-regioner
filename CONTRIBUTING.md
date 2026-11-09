# Bidra

Varje län bestämmer sin egen region. Listan i [data/regioner.csv](data/regioner.csv) är ett
utgångsläge som går att ändra med en pull request, och den som är aktiv i länet har sista ordet om
länets rad.

## Ändra ert läns region

1. Kom överens i länet. Det är ni som bär namnet på era repeatrar, så det är ni som väljer det.
2. Ändra länets rad i `data/regioner.csv`: skriv namnet i kolumnen `region` och sätt `beslut` till
   `lokalt`.
3. Kör `python3 scripts/build.py`. Skriptet kontrollerar raden och skriver om `REGIONER.md`.
4. Skicka en pull request med båda filerna. Skriv i beskrivningen var beslutet togs, till exempel
   länets Discordkanal eller en träff.

Har du inte Python går det bra att bara ändra CSV-filen – någon annan kör skriptet. Du kan också
öppna ett issue i stället för en pull request.

## Vad namnet måste klara

Länet väljer namnet, men formatet är gemensamt. Ett namn används inte bara i det egna länet:
grannlänets kantrepeatrar, companions i andra län och bottar måste stava det exakt likadant. Därför
gäller samma format för alla, samma som i [MeshCore Canadas standard](https://github.com/MeshCore-ca/MeshCore-Canada/blob/main/docs/config/standard.md#names-and-on-air-tags):

- **Bara små bokstäver `a`–`z`, siffror `0`–`9` och enkla bindestreck,** inget bindestreck först
  eller sist. Å och ä skrivs `a`, ö skrivs `o`.
- **Högst 29 tecken.** En repeater och en companion sparar högst 30.
- **Unikt i landet.** Två län kan inte bära samma namn, eftersom en repeater inte kan se skillnad.

Varför bara små bokstäver: repeatern räknar fram scopets nyckel ur namnet exakt som det är stavat,
utan att göra om stora bokstäver till små ([firmwarekällan](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/RegionMap.cpp)).
Companionen får nyckeln färdig från appen, och appens källkod är inte öppen, så räkna inte med att
den rättar stavningen. MeshCore Canadas guide säger samma sak: skriv namnet med små bokstäver.
`se-jkp`, `SE-JKP` och `Se-Jkp` blir tre olika scopes som aldrig når varandra. Med bara små bokstäver finns det ett sätt
att stava varje namn. Är koden du vill använda skriven med stora bokstäver någon annanstans, som
SCB:s `SE1408`, skriv den med små: `se1408`.

Inom formatet väljer länet fritt: en förkortning (`se-jkp`), SCB-koden (`se06`) eller något annat
som folk i länet känner igen. Utgångsläget i listan är `se-` och tre bokstäver, men det är bara
ett förslag.

## Kolumnen `beslut`

| Värde | Betyder |
| --- | --- |
| `forslag` | Utgångsläget. Ingen i länet har bestämt något än. |
| `lokalt` | Länet har valt namnet själv. |

Ändra inte ett annat läns rad från `lokalt` utan att länet står bakom ändringen.

## Lokala namn utanför listan

En ort eller en grupp repeatrar kan komma överens om ett eget namn för ett mindre område, till exempel
`se-vgr-gbg`, och bära det bredvid länets namn. Det hör till dem som använder det och står inte i
listan här, men det följer samma format som länens namn ovan. Se *Lokala namn* i
[README.md](README.md#lokala-namn).

## Ändra ett grannlän

[data/grannlan.csv](data/grannlan.csv) har en rad per län och grannlän. Listan är framräknad från
avstånd på kartan, se *Grannlän* i [README.md](README.md#grannlän). Vet ni att ert län har kontakt
med ett län som saknas, eller saknar kontakt med ett som står där: ändra filen.

1. Lägg till eller ta bort raden i `data/grannlan.csv`. Sätt `via` till `lokal` på rader du lägger till.
2. Ett par ska gälla åt båda håll. Lägger du till Värmland för Dalarna måste Värmland också ha Dalarna.
3. Kör `python3 scripts/build.py` och skicka en pull request med `data/grannlan.csv` och `REGIONER.md`.

| `via` | Betyder |
| --- | --- |
| `land` | Länens landytor ligger inom 40 km från varandra, fågelvägen. |
| `vatten` | Längre bort än 40 km, men inom 80 km över öppet vatten. |
| `omvand` | Tillagd för att paret ska gälla åt båda håll. |
| `lokal` | Tillagd av någon som känner till trakten. Skriv i pull requesten vad du vet. |

## Ändra själva förslaget

Texten i `README.md` går också att ändra med en pull request. Större ändringar (nivåer, utrullning,
namnformat) är bäst att ta som ett issue först, så att fler hinner tycka till.
