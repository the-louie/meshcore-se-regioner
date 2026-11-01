# Förslag: svenska MeshCore-regioner som varje län bestämmer själv

> **Förslag för diskussion – inte antaget.** Varje län avgör själv om och när det antar det.
> Gäller Sverige · repeater-firmware 1.16+ rekommenderas · companion-firmware 1.15+ · MeshCore-appen 1.43+

Regioner (scopes) hindrar lokalt prat från att flooda hela nätet. I dag heter de svenska regionerna
efter SCB:s sifferkoder, till exempel `se06` och `se0680`, som nästan ingen kan utantill. Det här
förslaget har en region per län, och **varje län bestämmer själv vad den heter och hur den används**.
Listan här är bara ett utgångsläge: `se-jkp` för Jönköpings län, `se-vgr` för Västra Götaland.

Upplägget och utrullningen är en svensk anpassning av
[MeshCore Canadas förslag för Ontario och Québec](https://meshcore.ca/proposals/onqc-scopes/).
Länsnivån är den som [meshat.se](https://meshat.se/meshcore/regioner/) redan beskriver.

**Vill ert län ha ett annat namn?** Bra – det är därför det här ligger på GitHub.
Se [CONTRIBUTING.md](CONTRIBUTING.md) och skicka en pull request.

## Vad behöver jag göra?

| Du… | Vad du gör | När |
| --- | --- | --- |
| Använder MeshCore-appen med en companion | **Inget än.** Låt inställningarna vara. [Fas 2](#fas-2-companions) består av två inställningar. | När ditt län har klarat fas 1 |
| Äger en repeater | Inget förrän ditt län har bestämt sig. Sedan [fas 1](#fas-1-repeatrar). | När länet har antagit förslaget |
| Kör en bot | Sätt den till ditt län, se [Bottar](#bottar). | I fas 2, efter länets pilot |
| Är aktiv i ditt län | Kontrollera länets namn i [REGIONER.md](REGIONER.md). Ni bestämmer det. | Nu |

Resten av sidan förklarar hur allt hänger ihop. Du behöver inte förstå det för att följa stegen.

## Kortversionen

Det finns tre nivåer. Varje repeater bär en kod från varje nivå: sitt län, `se` och `eu`.
När du skickar ett meddelande avgör scopet hur långt det färdas.

| Nivå | Exempel | Betyder | Vem bestämmer |
| --- | --- | --- | --- |
| Län | `se-jkp` `se-vgr` `se-kro` | Alla repeatrar i länet. | Länet |
| Sverige | `se` | Alla repeatrar i Sverige. | Alla län tillsammans |
| Europa | `eu` | Reserverad för senare. Bärs nu, används inte än. | Alla län tillsammans |

Om ett län antar förslaget efter pilot och alla faser är klara:

- **Repeatrar** bär sitt län, `se` och `eu`.
- **Bottar** använder länet, så att de håller sig lokala.
- **Companions** har `se` som standard, för att möjliggöra DM på radiovägar som tillåter `se`.
- **Public** använder `se`, om nationell Public antas separat efter pilot.
- **Testkanaler** använder länet, så att tester håller sig inom länet.
- **Meddelanden utan scope** följer länets befintliga trafikpolicy under migrationen. Eventuell
  blockering beslutar länet separat efter pilot: den kan bryta trafik även inom det egna länet.

Det här är utgångsläget. Ett län kan välja annorlunda för det som bara angår länet, till exempel
namnet, takten eller ett [lokalt namn](#lokala-namn) för en ort. Det som angår andra län, som `se`
och `eu`, kräver att länen är överens.

Companions kommer sist, i fas 2. Sätter du ett scope på din companion innan repeatrarna runt dig är
omställda når dina meddelanden **färre**, inte fler.

## Varje län bestämmer

Namnet bestäms där det används. Länets namn angår länet och behöver inget ja ovanifrån.

- **Länet väljer namnet.** En förkortning (`se-jkp`), SCB-koden (`se06`) eller något annat som folk
  i länet känner igen. Det enda som krävs är att namnet fungerar i en repeater och inte redan bärs
  av ett annat län, se [CONTRIBUTING.md](CONTRIBUTING.md#vad-namnet-måste-klara).
- **Länet väljer takten.** Faserna nedan körs per län. Ett län som är klart behöver inte vänta på
  resten av landet, och ett län som inte vill byta behöver inte.
- **Länet väljer sin trafikpolicy.** Om meddelanden utan scope ska blockeras, och var kanterna går,
  avgör länet utifrån sina egna radiovägar.
- **Utgångsläget är en gissning.** Namnen i listan är `se-` och tre bokstäver, valda för att ge
  varje län något att börja med utan att någon behöver fråga. Säger länet något annat är det länet
  som stämmer, och listan som ändras.
- **Gemensamt är bara det som är gemensamt.** `se` och `eu` delas av alla, så där behövs enighet.
  Grannlän som delar kantrepeatrar kommer överens sinsemellan.

[REGIONER.md](REGIONER.md) visar vilka län som har bestämt sitt namn själva och vilka som
fortfarande har utgångsläget.

## Så är namnen uppbyggda

```
se - jkp
│    └──── län, i utgångsläget tre bokstäver
└───────── Sverige
```

Utgångsläget för länens namn:

- **Vedertagen förkortning först.** Jönköping är `jkp`, Stockholm `sth`.
- **Annars en kort förkortning av länsnamnet.** Kronoberg är `kro`, Halland `hal`.
- **Bara `a`–`z`.** Å och ä skrivs `a`, ö skrivs `o`. Inga stora bokstäver.

Ett län som väljer något annat behöver inte följa de här punkterna, bara de tekniska gränserna.

### Länen

| Län | Utgångsläge | Ersätter |
| --- | --- | --- |
| Stockholm | `se-sth` | `se01` |
| Uppsala | `se-upp` | `se03` |
| Södermanland | `se-sor` | `se04` |
| Östergötland | `se-ost` | `se05` |
| Jönköping | `se-jkp` | `se06` |
| Kronoberg | `se-kro` | `se07` |
| Kalmar | `se-kal` | `se08` |
| Gotland | `se-gtl` | `se09` |
| Blekinge | `se-blk` | `se10` |
| Skåne | `se-ska` | `se12` |
| Halland | `se-hal` | `se13` |
| Västra Götaland | `se-vgr` | `se14` |
| Värmland | `se-var` | `se17` |
| Örebro | `se-ore` | `se18` |
| Västmanland | `se-vml` | `se19` |
| Dalarna | `se-dal` | `se20` |
| Gävleborg | `se-gav` | `se21` |
| Västernorrland | `se-vnl` | `se22` |
| Jämtland | `se-jam` | `se23` |
| Västerbotten | `se-vbt` | `se24` |
| Norrbotten | `se-nbt` | `se25` |

Vad varje län faktiskt har valt står i [REGIONER.md](REGIONER.md). Källan är
[data/regioner.csv](data/regioner.csv).

### Lokala namn

Länet är den minsta nivån i förslaget. Vill en ort eller en grupp repeatrar ha ett mindre område,
till exempel Göteborg i ett stort län, kan de komma överens om ett eget namn som `se-vgr-gbg` och
bära det bredvid länets. Det är deras namn och deras beslut: det står inte i listan här och förslaget
har inga regler för det, utöver att det ska fungera i en repeater och inte krocka med ett läns namn.

Ett lokalt namn fungerar bara på de repeatrar som bär det. Bindestrecken betyder ingenting för
repeatern: att bära `se-vgr` betyder inte att bära `se-vgr-gbg`.

### Varför inte kommuner?

Ett tidigare utkast hade en nivå till, en kod för varje kommun. Den är borttagen:

- **Sverige är inte så stort.** Län och land räcker för att hålla lokalt prat lokalt.
- **En kommun har sällan nog med repeatrar** för att ett scope ska avgränsa något. De flesta
  radiovägar går genom flera kommuner.
- **Färre namn blir oftare rätt stavade,** och rätt stavat är det enda som räknas.
- **Kommunkoderna hann knappt användas.** I Jönköpings län syntes ingen av dem i trafiken i oktober
  2026, så det finns lite eller inget att städa bort. Listan ligger kvar i historiken.

Behöver en ort ett eget område används ett [lokalt namn](#lokala-namn).

### Varför inte flygplatskoder, som i Kanada?

Utgångsläget använder inte flygplatskoder, men ett län som hellre vill det kan välja en. Skälen till
utgångsläget:

- De flesta län har ingen flygplats som alla känner till, och vissa har flera.
- Flygplatskoderna är ofta inte det folk säger. Jönköping är `JKG` fast alla skriver Jkpg.
- Svenska repeatrar behöver redan i dag kunna två kodsystem: SCB-siffror för regionen och en
  flygplatskod för MQTT-rapportering. Ett namn som folk kan utantill är enklare än två som ingen kan.

### Varför inte SCB-koderna?

De är kompletta och entydiga, men `se06` säger ingenting, medan `se-jkp` går att gissa. Ett namn som
går att gissa blir oftare rätt stavat. Ett län som redan har vant sig vid sin SCB-kod kan ändå
behålla den: då ändrar länet sin rad till `se06`, och fas 3 hoppar över det namnet.

## Ord som används här

- **Companion:** MeshCore-radion du parar med appen i telefonen eller datorn.
- **Repeater:** en fast radio, ofta på ett tak eller i en mast, som för meddelanden vidare.
- **Flood:** hur ett meddelande sprids när det inte finns någon känd väg: varje repeater som hör det
  skickar det vidare. Kanalmeddelanden floodar alltid, och det gör även det första direktmeddelandet
  till någon.
- **Hopp:** en repeater som skickar ett meddelande vidare.
- **DM:** ett direktmeddelande till en kontakt.
- **Advert:** en radio som annonserar sig själv så att andra hittar den.
- **Kantrepeater:** en repeater som regelbundet pratar med repeatrar i två olika län.

## Vad ett scope är

Ett scope är ett kort namn som sätts på ett meddelande, till exempel `se-jkp`. Repeatrar använder
det för att avgöra om meddelandet ska skickas vidare.

Ett scope är **inte kryptering och inget GPS-staket**. Vem som helst som kan namnet kan använda det,
och det har inget att göra med var du befinner dig. Det är bara en etikett som säger "repeatrar som
bär det här namnet, skicka vidare".

Appen gör om namnet till en liten kod och lägger den i meddelandets huvud. Varje repeater har en
lista över namn den skickar vidare, och jämför koden mot listan.

## Så bestämmer en repeater

En repeater i Mullsjö, i Jönköpings län, bär enligt utgångsläget den här listan: `*`, `se-jkp`, `se`, `eu`.

| Meddelande | Scope | Vad repeatern gör |
| --- | --- | --- |
| Kanal för Jönköpings län | `se-jkp` | Skickar vidare |
| DM till Luleå, skickat med companionens standard | `se` | Skickar vidare |
| Äldre app, inget scope | inget | Skickar vidare |
| Kanal för Västra Götaland | `se-vgr` | Släpper |
| Kanal för ett lokalt namn i Göteborg | `se-vgr-gbg` | Släpper |

- Namnet finns på listan: skicka vidare.
- Namnet finns inte på listan: släpp.
- Inget scope alls: räknas som `*`. Skickas vidare bara om `*` är tillåtet.
- För många hopp: släpps när det passerar `flood.max`, oavsett scope.

Repeatern hör fortfarande alla meddelanden. Scopet avgör bara om den skickar dem vidare.

Fyra saker som folk brukar gå bet på:

- **Stavningen måste vara exakt.** `se-jkp`, `SE-JKP` och `se06` är tre olika namn.
- **Bara floods kontrolleras.** När ett direktmeddelande har en känd väg går det raka vägen, och
  scopet spelar ingen roll.
- **Det finns inget arv.** Att bära `se` betyder inte att bära `se-jkp`. Varje namn måste stå på
  listan för sig. Bindestrecken i namnet är till för människor, inte för repeatern.
- **En repeater utan regioner släpper alla meddelanden med scope.** Från start bär en repeater bara
  `*`. Scope fungerar först när repeatrarna längs vägen är inställda.

## Nivåerna

```
eu                Europa. Reserverad. Bärs nu, används inte än.
└─ se             Alla repeatrar i Sverige.
   ├─ se-jkp      Jönköpings län
   ├─ se-vgr      Västra Götalands län
   └─ …
```

Det en repeater i Jönköpings län faktiskt lagrar är en platt lista:

```
*   se-jkp   se   eu
```

Trädet ovan är till för människor, inte för repeatern.

### Varför `eu`?

Alla repeatrar bär `eu` redan nu, så att ett scope över landsgränser fungerar senare utan att någon
behöver ställa om sin repeater igen. Använd inte `eu` på din companion eller dina kanaler än.

## Utrullning

Varje län rullar ut i sin egen takt. Inom länet gäller ordningen: varje fas börjar först när den förra
är klar i länet. Ett län behöver inte vänta på andra län, utom där en fas berör dem (`se`, `eu` och
kantrepeatrar mot ett grannlän).

| Fas | Vem | Vad |
| --- | --- | --- |
| 1 | Repeatrar | Lägg till nya namn bredvid gamla. Behåll befintlig trafikpolicy, hoppgränser och default scope. |
| 2 | Pilot och migration | Verifiera radiovägar och versioner i länet. Migrera companions och bottar först när deras vägar stöder namnen. Nationell Public beslutas separat, av länen tillsammans. |
| 3 | Städning | Ta bort gamla namn först när berörda användare, kanaler och bottar har migrerat och återställning är förberedd. |
| 4 | Vid behov | Länet beslutar separat om begränsning av trafik utan scope efter mätning och kontroll av beroende radiovägar. |

**Skillnad mot Kanada:** där rensas gamla regioner bort först. Här finns kanaler som redan använder
`se01`-namnen, så de gamla namnen ligger kvar på repeatrarna tills companions har bytt.

### Fas 1: Repeatrar

Fas 1 är förberedande: lägg till länet, `se` och `eu` utan att ta bort gamla namn eller
ändra befintlig trafikpolicy. Companions och bottar ändrar ingenting i den här fasen. Repeaterns
default scope och hoppgränser behålls också.

Skriv kommandona ett i taget i repeaterns kommandorad: i MeshCore-appen öppnar du repeatern, loggar
in som admin och använder kommandorutan, eller så använder du USB-konsolen. Vänta på svaret och kontrollera att det inte börjar med `Err` innan du
skickar nästa. `region def` svarar med regionträdet, inte `OK`.

#### Steg 1: Kontrollera firmware och hitta ditt läns namn

```
ver
```

Slå sedan upp ditt län i [REGIONER.md](REGIONER.md) och använd det namn länet har valt. Exemplen
nedan gäller en repeater i Jönköpings län med utgångsläget `se-jkp`.

Avgör också om din repeater är en vanlig repeater eller en **kantrepeater**. En kantrepeater pratar
regelbundet med repeatrar i ett annat län. Alla andra är vanliga repeatrar, även de som står nära en
länsgräns: om inget på andra sidan kopplar mot den är den en vanlig repeater. En enstaka länk som
setts några gånger, eller inte på flera veckor, räknas inte.

#### Steg 2: Se vad som redan finns

```
region
region default
get flood.max
get flood.max.unscoped
```

Spara svaren före ändringen: namn, föräldrar, `F`-flaggor, hemregion (`^`), default scope och
hoppgränser. Finns `se`, `se06`, `se0642` eller liknande redan: behåll dem och deras trafikpolicy
under migrationen. Anteckningarna behövs för återställning.

#### Steg 3: Lägg till de nya namnen

För både vanliga repeatrar och kantrepeatrar, firmware 1.16 eller nyare, när de angivna namnen
inte redan finns:

```
region def se-jkp|* se|* eu
region save
```

**Granska befintliga namn först.** `region def` tar inte bort andra namn, men flyttar föräldern
för namn som redan finns och tillåter flood för alla namn i kommandot. Finns något av namnen
redan, lägg bara till de saknade med `region put <namn> *` och behåll befintliga föräldrar och
flaggor. Kör inte hela raden ovan över en befintlig konfiguration utan att granska ändringarna.
Ett fel kan lämna en delvis ändrad lista: kontrollera med `region` innan du sparar eller fortsätter.

Har länet valt att behålla sin SCB-kod, till exempel `se06`, finns namnet redan: lägg bara till `se`
och `eu`.

Ändra inte `region allowf *`, `region denyf *`, default scope eller hoppgränser i fas 1.

| Kommando | Vad det gör |
| --- | --- |
| `region def …` | Skapar namn, eller uppdaterar deras föräldrar, och tillåter flood för dem. `\|*` återgår till toppen mellan namnen. Svaret är regionträdet. |
| `region put <namn> *` | Lägger ett namn direkt under `*` och tillåter flood. Kan också ändra ett befintligt namn. |
| `region save` | Sparar regioninställningarna så att de finns kvar efter omstart. |

På firmware 1.15 saknas `region def`: lägg till varje saknat namn med `region put <namn> *`
och kontrollera `F`-flaggan. Kontrollera CLI-stöd på den version som faktiskt används.

**Grannlän (valfritt):** en kantrepeater kan också bära grannlänets namn, till exempel `se-vgr`, så
att folk nära den kan delta i grannlänets kanaler. Det kommer de två länen överens om. Andra kan nå
grannlänet genom en radioväg som tillåter `se`. Vilka län som räknas som grannlän står i
[REGIONER.md](REGIONER.md), se [Grannlän](#grannlän).

**Radiovägar avgör:** att en repeater hör ett grannlän räcker inte som skäl att blockera `*`.
Den kan samtidigt vara den enda förbindelsen mellan två orter inom det egna länet, även om
båda orterna har egna repeatrar. Kontrollera vilka vägar som är beroende av noden i piloten.

#### Steg 4: Kontrollera resultatet

```
region
```

För Jönköpings län ska de nya namnen finnas och tillåta flood. Om `*` tidigare var tillåtet och
hemregionen var `*` kan listan se ut så här:

```
*^ F
se-jkp F
se F
eu F
```

`F` betyder att repeatern skickar vidare det namnet. `^` markerar hemregion, inte default scope.
`*` ska behålla sin tidigare `F`-flagga; om den tidigare saknade `F` ska den fortfarande sakna den.
Kontrollera också med `region default` att standard-scope är oförändrat. Gamla namn som `se06`
behåller sina föräldrar och flaggor tills migrationen är verifierad. Kontrollera igen efter omstart.

#### Tillåt eller släpp, snabbreferens

| Kommando | Vad det gör |
| --- | --- |
| `region allowf <namn>` | Skicka vidare meddelanden med det namnet |
| `region denyf <namn>` | Släpp meddelanden med det namnet. Repeatern tar fortfarande emot dem själv. |
| `<namn>` | Kan vara `*` för meddelanden utan scope, eller ett namn som `se-jkp` |
| `set flood.max.unscoped <hopp>` | En egen hoppgräns för meddelanden utan scope. `0` har samma effekt som `region denyf *`. |
| `region save` | Kör alltid efter `allowf` eller `denyf` |

#### Bottar

Det här görs i fas 2, när länets pilot har verifierat att de radiovägar botten använder bär länets
namn. På companionen som botten använder: sätt **Default Region Scope** till länet, till exempel
`se-jkp`. Sätt också alla kanaler som botten skriver i till länet.

Har orten ett [lokalt namn](#lokala-namn) som repeatrarna runt botten bär kan botten använda det i
stället.

### Fas 2: Companions

**Inte än.** Fas 1 måste vara klar i länet först. En repeater utan de nya namnen släpper alla
meddelanden som har dem. Sätter du din standard till `se` innan repeatrarna på dina vägar bär det
når dina kanalmeddelanden och första DM bara närområdet.

Varje län inleder med en egen pilot. Dokumentera den faktiskt testade kombinationen av appversion,
companion-firmware och repeater-firmware. App 1.43+ och companion-firmware 1.15+ behövs för stegen
nedan; en uppdaterad app räcker inte ensam. Repeater-firmware 1.16+ rekommenderas för kommandona i
fas 1. Ingen kombination är ännu provkörd på fysisk radio i det här förslaget.

- Testa kanaltrafik utan scope och med gamla respektive nya läns- och nationella scopes.
- Testa nya DM med rensade vägar i båda riktningarna, både inom länet och över länsgränsen. Det
  senare görs tillsammans med grannlänet.
- Kontrollera inställningar och leverans efter omstart, och öva återställning enligt nedan.
- Mät paketmängd, airtime och leveransgrad före och efter varje policyändring. Pröva nationell
  Public separat från companionens standard för DM; standarden påverkar även dess egna adverts.

Migrera först när berörda radiovägar är verifierade. Stegen nedan beskriver förslagets val av
standard-scope; nationell Public kräver ett separat beslut efter piloterna. Behåll tidigare
kanalinställning tills det beslutet är taget.

#### Steg 1: Sätt ditt standard-scope

Öppna **Settings** i MeshCore-appen. Under **Network Settings**, tryck på **Default Region Scope**,
lägg till `se` och välj det.

#### Steg 2: Sätt scope på varje kanal

Öppna kanalen, tryck på **⋮** uppe till höger, välj **Set Region Scope** och välj enligt tabellen:

| Kanal | Scope | Varför |
| --- | --- | --- |
| Public | `se`, om nationell Public antas efter pilot | Sprids på sammanhängande radiovägar som tillåter `se`, inom hoppgränsen |
| Testkanaler, som `#test` | Ditt län, till exempel `se-jkp` | Tester håller sig inom länet |
| Bottkanaler | Ditt län | Bottsvar håller sig inom länet |
| Egna kanaler | Län, ett lokalt namn eller `se` | Välj hur långt den ska nå |

Meddelanden med scope är lite kortare. MeshCore Canada såg i sina tester att gränsen på Public sjönk
från 137 till 127 tecken när kanalen fick ett scope.

#### Varför är companionens standard `se`?

Du kan inte välja scope för ett enskilt direktmeddelande. När ett DM saknar känd väg floodar det med
ditt **standard-scope**. Svaret som talar om vägen för din companion kommer tillbaka med din kontakts
standard-scope.

| Din standard | Vad som händer med ett DM från Jönköping till Göteborg |
| --- | --- |
| `se-jkp` | Flood kan stanna vid en repeater som inte tillåter scopet. Även svarsvägen behöver stödja kontaktens standard-scope. |
| `se` | Kan komma fram om en sammanhängande radioväg tillåter `se` inom hoppgränsen åt båda håll. När vägen är känd går senare DM raka vägen. |

Haken: en kanal utan eget scope använder också din standard, `se`, och kan då spridas nationellt
inom hoppgränsen. Det är förslagets val för Public om det antas efter pilot, men inte för
testkanaler och bottar. Därför sätts de till länet i steg 2.

### Fas 3: Städning

Ta bort gamla namn först när berörda companions, kanaler och bottar i länet har migrerat, piloten
har verifierat deras trafik och länet har kommit överens om avslutad övergångstid. Att
telefonappen är uppdaterad räcker inte. Spara konfigurationen och ha återställningskommandon
redo. Använd `region remove <namn>`, ett i taget med det mest indragna först, och sedan `region save`:

```
region remove se0642
region remove se06
region save
region
```

Har länet valt att behålla sin SCB-kod som namn, ta inte bort den. Svarar ett kommando
`Err - not empty` ligger ett annat namn fortfarande under det. Ta bort det först.
`Err - not found` betyder att namnet redan är borta.

### Fas 4: Bara vid behov

Begränsning av trafik utan scope är länets beslut, separat och efter pilot och verifierad migration.
`region denyf *` blockerar vidarebefordran utan scope i alla riktningar, även inom det egna länet.
Kontrollera beroende radiovägar och nya användares möjlighet att nå nätet innan det används.
Efter blockeringen ska `*` sakna `F` i `region`; kör `region save` och kontrollera efter omstart.

Ett alternativ att pröva är `set flood.max.unscoped 3`. Det begränsar trafik utan scope till tre
hopp och kan också bryta nödvändiga vägar. Dokumentera tidigare värde och kontrollera det med
`get flood.max.unscoped` efter ändringen och omstart. `set` sparar inställningen direkt.

### Återställning

Vid försämrad leverans: avbryt nästa steg och återställ senaste policyändringen. Om `*` var
flood-tillåtet före försöket med blockering:

```
region allowf *
region save
region
```

Återställ ändrad hoppgräns med `set flood.max.unscoped <tidigare värde>` och kontrollera med `get`.
Återställ också companionens standard och kanalscopes i appen.

Har gamla namn tagits bort: återskapa dem med `region put <namn> <tidigare förälder>`, föräldrar
först. Återställ varje `allowf`/`denyf`-flagga och hemregion från anteckningarna,
kör `region save` och kontrollera efter omstart. Ta inte bort nya namn som migrerade klienter
fortfarande behöver. Upprepa trafiktesterna, inklusive nya DM åt båda håll.

## Vem hör vad

Exemplet är länken mellan Jönköpings län och Västra Götaland, genom en kantrepeater i Mullsjö som
också bär grannlänets namn `se-vgr`. Tabellen visar en möjlig policy **efter** att båda länen
separat har beslutat att blockera `*`, inte konfigurationen under fas 1. Alla resultat kräver
fungerande radiovägar som tillåter scopet och ryms inom hoppgränsen.

| Meddelande | Repeatrar i Jönköpings län | Kantrepeatern i Mullsjö | Repeatrar i Västra Götaland | Vem får det |
| --- | --- | --- | --- | --- |
| Ny användare i Jönköping, inget scope | Skickar vidare | Släpper | Nås aldrig | Noder som nås utan att passera en repeater som blockerar `*` |
| Ny användare i Falköping, inget scope | Nås aldrig | Släpper | Skickar vidare | Noder som nås utan att passera en repeater som blockerar `*` |
| Länskanal, `se-jkp` | Skickar vidare | Skickar vidare | Släpper | Jönköpings län |
| Länskanal, `se-vgr` | Släpper | Skickar vidare | Skickar vidare | Västra Götaland, plus folk nära Mullsjö |
| DM med companionens standard, `se` | Skickar vidare | Skickar vidare | Skickar vidare | Noder som nås genom radiovägar som tillåter `se` |

En ny användare utan scope når bara den sammanhängande del av nätet som vidarebefordrar `*`.
En kantrepeater som blockerar `*` kan dela det egna länets nät; länsgränsen ger ingen garanti.

## Grannlän

Radio bryr sig inte om länsgränser, och över vatten når den längre än över land. Ett grannlän är
därför inte bara ett län som delar gräns med ditt, utan ett län som ligger **inom räckhåll**.
Listan i [data/grannlan.csv](data/grannlan.csv) är ett utgångsläge, framräknat så här:

- Varje läns landyta utökas **40 km** åt alla håll, och **80 km** där vägen går över öppet vatten
  från länets egen strand. Som vatten räknas havet och de större sjöarna, till exempel Vänern,
  Vättern och Mälaren.
- Varje län vars landyta den utökade ytan når blir grannlän.
- Ett par gäller alltid åt båda håll.

Det ger 50 par av län. Jönköpings län får bland annat `se-vgr` och `se-ost`, Västra Götaland får
`se-var` tvärs över Vänern, och Gotland får `se-kal` och `se-sth`.

Listan säger var en kantrepeater *kan* behövas, inte att den behövs. Den bygger på avstånd på
kartan och vet ingenting om terräng, antennhöjd eller vilka repeatrar som faktiskt hör varandra.
Avgörandet är fortfarande det som står under [Steg 1](#steg-1-kontrollera-firmware-och-hitta-ditt-läns-namn):
pratar repeatern regelbundet med repeatrar i ett annat län? Och om en kantrepeater ska bära
grannlänets namn kommer de två länen överens om.

**Manuella justeringar är välkomna.** Listan är uträknad, inte uppmätt, och de som är på plats vet
bäst. Har ert län kontakt med ett län som saknas, eller står det ett län där som ingen repeater hos er
når: lägg till eller ta bort raden och skicka en pull request. En rad som någon har lagt till för
hand märks `lokal`. Se [CONTRIBUTING.md](CONTRIBUTING.md).

### Så är listan framräknad

Listan är framräknad en gång och ligger som färdig data i [data/grannlan.csv](data/grannlan.csv).
Den räknades först fram per kommun; ett län blev grannlän till ett annat om någon av länets kommuner
nåddes. Så här gick det till:

1. **Kommunernas landyta.** Kommungränserna kommer från OpenStreetMap. De sträcker sig ut i havet,
   så varje kommun skärs mot en landkarta: Natural Earth i skala 1:10 miljoner, land och småöar
   minus sjöar. Länets landyta är kommunernas landytor sammanslagna.
2. **40 km åt alla håll.** Länets landyta utökas med 40 km. Når den utökade ytan en kommun i ett
   annat län blir länen grannlän, med `via` satt till `land`. Avståndet är fågelvägen, så en smal
   sjö eller vik på vägen spelar ingen roll.
3. **80 km över vatten.** Från länets strand utökas vattnet med 80 km, men bara vatten som hänger
   ihop med den stranden räknas. Län som nås den vägen, och inte redan i steg 2, får `via`
   satt till `vatten`.
4. **Båda håll.** Når län A län B, men inte tvärtom, får paret också raden B till A, med `via` satt
   till `omvand`. Det gäller ett enda par: Gävleborg och Stockholms län.

Avstånden är mätta i SWEREF 99 TM, i meter.

Det här förklarar några saker i listan som annars ser konstiga ut:

- **Bara de större sjöarna är vatten.** Natural Earth har Vänern, Vättern, Mälaren, Hjälmaren,
  Siljan, Storsjön, Bolmen, Åsnen och liknande. Mindre sjöar räknas som land.
- **Fri sikt kontrolleras inte.** Öar och uddar mellan två stränder ignoreras.
- **Kustlinjen är grov.** De minsta skären saknas, så avstånd över hav kan vara några kilometer
  för långa.
- **Länkar nära en gräns är känsliga.** Med 10 och 40 km blir det 42 par av län och Gotland får
  inget grannlän, eftersom det är 59 km till Öland. Med 50 och 100 km blir det 56 par. Med 40 och
  80 km blir det 50.

Skriptet som räknade fram filen ligger inte i det här repot, eftersom det behöver kommungränserna
och landkartan. Det som granskas här är resultatet: `scripts/build.py` kontrollerar att varje rad
pekar på län som finns, och att varje par gäller åt båda håll.

## Bra att veta

- **Meddelanden med scope är ungefär tio tecken kortare.**
- **Hoppgränsen gäller `se` också.** Är den verkliga vägen genom landet längre än `flood.max`
  stannar meddelandet på vägen.
- **Versioner:** `region def` kräver repeater-firmware 1.16+. Companionens standard-scope kräver
  firmware 1.15+. Appinstruktionerna förutsätter MeshCore-appen 1.43+.
  CLI-beteendet är kontrollerat mot [firmware 1.16](https://github.com/meshcore-dev/MeshCore/blob/repeater-v1.16.0/src/helpers/CommonCLI.cpp)
  och [CLI-guiden](https://github.com/meshcore-dev/MeshCore/blob/repeater-v1.16.0/docs/cli_commands.md);
  [firmware 1.15](https://github.com/meshcore-dev/MeshCore/blob/companion-v1.15.0/src/helpers/CommonCLI.cpp)
  har stöd för standard-scope. Faktiskt testade versioner ska dokumenteras i piloten.
- **`offgrid`** från meshat.se påverkas inte. Den regionen handlar om strömförsörjning, inte om
  geografi, och kan bäras bredvid de andra.

## Öppna frågor

Det här är inte avgjort, och synpunkter är välkomna som issues eller pull requests.

1. **Länens namn.** Alla 21 namn är ett utgångsläge. Varje län behöver bestämma sitt, se
   [CONTRIBUTING.md](CONTRIBUTING.md).
2. **Kommandona är inte provkörda på fysisk radio.** CLI-beteendet är granskat mot firmwarekällan men
   har inte testats på en repeater med de nya namnen, och inte ihop med befintliga `seXX`-namn.
3. **Var går kanten?** Förslaget lägger kantrepeatrarna vid länsgränserna, och grannlänen avgör
   tillsammans var de står. Gränserna 40 km över land och 80 km över vatten i [Grannlän](#grannlän)
   är en första gissning.
4. **MQTT-koderna.** meshat.se använder flygplatskoder per län för MQTT. Kan länets namn här ersätta
   dem, så att det bara finns ett kodsystem? Det avgör varje län.
5. **`europe`.** meshat.se har både `eu` och `europe`. Förslaget använder bara `eu`.
6. **Tidplan.** Varje län sätter sin egen. Inga datum är satta för `se` och `eu`.

## Nästa steg

- Varje län bestämmer sitt namn.
- Provköra kommandona på riktiga repeatrar.
- Ett verktyg där man väljer län och får färdiga kommandon.
- Bestämma var faserna annonseras i varje län.

## Tack

Texten bygger på [MeshCore Canadas ON/QC-förslag](https://meshcore.ca/proposals/onqc-scopes/)
([källa](https://github.com/MeshCore-ca/MeshCore-Canada), MIT-licens) och på
[meshat.se:s regionguide](https://meshat.se/meshcore/regioner/). Länslistan kommer från SCB.
