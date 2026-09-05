# Projectplan Blender Design

## 1. Doel en definitie van gereed

Een maatvast architectonisch prototype dat vanuit configuratie en Python reproduceerbaar in Blender wordt opgebouwd, technisch wordt gevalideerd, visueel wordt gecontroleerd en als `.glb` in een browser kan worden bekeken. Een projectwiki helpt beginnende gebruikers het huis veilig te bekijken en maakt het project overdraagbaar.

Dit prototype is geen constructieberekening, vergunningstekening of gecertificeerd BIM-model. Bouwkundige en constructieve goedkeuring blijft mensenwerk.

## 2. Voortgang op hoofdlijnen

- [x] Fase 0 — Projectbesturing en uitgangspunten
- [x] Fase 1 — Lokale omgeving en Git/GitHub
- [x] Fase 2 — Verticale Blender-proefopstelling
- [ ] Fase 3 — Eisen, referenties en maatvoering
- [ ] Fase 4 — Parametrisch casco
- [ ] Fase 5 — Architectonische indeling en onderdelen
- [ ] Fase 6 — Materialen, terrein en presentatie
- [ ] Fase 7 — Validatie en kwaliteitscontrole
- [ ] Fase 8 — Interactieve 3D-viewer
- [ ] Fase 9 — Publicatie, documentatie en overdracht

## 3. Mijlpalen

| Mijlpaal | Resultaat | Status |
|---|---|---|
| M0 | Repository bestuurbaar | Voltooid |
| M1 | IntelliJ → Blender automatisering werkt | Voltooid |
| M2 | Eisen en maatvoering goedgekeurd | Niet gestart |
| M3 | Maatvast casco gegenereerd | Niet gestart |
| M4 | Compleet architectonisch prototype | Niet gestart |
| M5 | Kwaliteitscontroles slagen | Niet gestart |
| M6 | Interactief model gepubliceerd | Niet gestart |

M1 wordt pas voltooid na een succesvolle gevalideerde headless end-to-end-uitvoering.

## 4. Detailplan

### Fase 0 — Projectbesturing en uitgangspunten

- [x] Startdocumenten in repository plaatsen.
- [x] Bestanden controleren en eerste documentatiecommit maken.
- [x] Projectdoel, doelgroep en prototype-niveau bevestigen.
- [x] Rollen bevestigen: gebruiker als projecteigenaar, ChatGPT als projectregisseur, Codex als uitvoerder.
- [x] Regels voor goedkeuring en planwijziging bevestigen.
- [x] Eerste risico-inventarisatie vastleggen.

Acceptatie:

- [x] `AGENTS.md`, plan, status en logboeken zijn aanwezig en consistent.
- [x] Codex kan de regels samenvatten zonder bestanden te wijzigen.
- [x] De gebruiker heeft scope en werkwijze goedgekeurd.

### Fase 1 — Lokale omgeving en Git/GitHub

- [x] Windows-, IntelliJ-, Git-, Python- en Blender-versies inventariseren.
- [x] Ondersteunde Blender LTS-versie kiezen en vastleggen.
- [x] Pad naar `blender.exe` detecteren zonder machinepad te committen.
- [x] Padstrategie via `BLENDER_EXECUTABLE` vastleggen.
- [x] `.gitignore` en `.gitattributes` opstellen.
- [x] Renormalisatiecontrole uitvoeren.
- [x] GitHub-remote, branch `main`, upstream en eerste push controleren.
- [x] Branch- en commitconventies vastleggen.

Acceptatie:

- [x] Blender-versie en uitvoerbaar pad zijn aantoonbaar gevonden.
- [x] Repository bevat geen IDE-rommel, secrets of tijdelijke Blender-bestanden.
- [x] Push/pull naar de bedoelde GitHub-repository werkt.

### Fase 2 — Verticale Blender-proefopstelling

- [x] Ontwerpanalyse voor Fase 2 uitvoeren.
- [x] DEC-005 voor commandoketen, proefwoning en outputbeleid goedkeuren.
- [x] Minimale projectmappen aanmaken.
- [x] Configuratie voor een kleine proefwoning maken.
- [x] Script maken dat scène, units en collections initialiseert.
- [x] Vier buitenwanden, één binnenwand, deur, ramen en eenvoudig dak genereren.
- [x] `.blend` automatisch opslaan.
- [x] Vaste controlecamera's en verlichting toevoegen.
- [x] Vier aanzichten renderen.
- [x] `.glb` exporteren.
- [x] Basisvalidatie uitvoeren en rapport schrijven.

Acceptatie:

- [x] Eén commando bouwt de proefscène opnieuw op.
- [x] Blender eindigt zonder Python-fout.
- [x] `.blend`, `.glb`, renders en validatierapport bestaan.
- [x] De gebruiker keurt de zichtbare proefuitvoer goed.

### Fase 3 — Eisen, referenties en maatvoering

- [ ] Doelgroep en kijkervaring bepalen.
- [ ] Situatie, perceel en noordrichting vastleggen.
- [ ] Buitenmaten, niveaus en verdiepingshoogtes vastleggen.
- [ ] Ruimtelijst met gewenste netto-oppervlakten opstellen.
- [ ] Wand-, vloer- en dakdiktes vastleggen.
- [ ] Ramen, deuren, trappen en doorloopmaten specificeren.
- [ ] Dakvorm, overstekken en hemelwaterafvoer beschrijven.
- [ ] Referentiebeelden en tekeningen registreren met bron/status.
- [ ] Onzekerheden en expliciete aannames vastleggen.
- [x] Configuratieschema valideren.
- [x] Beginnerspagina voor de projectwiki opstellen; alleen gereed wanneer `docs/wiki-intro-eerste-run.md` bestaat en Blender 5.2.1, openen, navigeren en veilig afsluiten behandelt.

Acceptatie:

- [ ] Geen kritische maat is impliciet of tegenstrijdig.
- [ ] Ruimten en buitenmaten zijn onderling plausibel.
- [ ] De gebruiker keurt requirements en configuratie goed.

### Fase 4 — Parametrisch casco

- [ ] Assenstelsel, oorsprong en verdiepingsniveaus implementeren.
- [ ] Fundering/plint op conceptniveau modelleren.
- [ ] Vloeren en buitenwanden genereren.
- [ ] Binnenwanden genereren.
- [ ] Openingen op basis van configuratie uitsnijden.
- [ ] Verdiepingen en dakvolume genereren.
- [ ] Collections en objectnamen structureren.
- [ ] Maatlabels of meetrapport genereren.

Acceptatie:

- [ ] Buitenmaten en hoogtes vallen binnen afgesproken toleranties.
- [ ] Het model kan schoon opnieuw worden opgebouwd.
- [ ] Geen onverklaarde handmatige geometrie is noodzakelijk.

### Fase 5 — Architectonische indeling en onderdelen

- [ ] Kozijnen, ramen en deuren uitwerken.
- [ ] Trap en balustrades modelleren.
- [ ] Dakdetails en overstekken modelleren.
- [ ] Plafonds en zichtbare vloerafwerkingen toevoegen.
- [ ] Keuken, sanitair en vast meubilair als schaalobjecten toevoegen.
- [ ] Objecten per categorie zichtbaar/verbergbaar maken.
- [ ] Looproutes en hoofdruimtewerking controleren.

Acceptatie:

- [ ] Alle afgesproken ruimten en verbindingen zijn aanwezig.
- [ ] Deuren, trappen en doorgangen zijn geometrisch plausibel.
- [ ] De gebruiker keurt indeling en volumewerking goed.

### Fase 6 — Materialen, terrein en presentatie

- [ ] Materiaalpalet vastleggen.
- [ ] glTF-compatibele materialen toepassen.
- [ ] Textures optimaliseren en licentie/bronnen registreren.
- [ ] Eenvoudig terrein en context toevoegen.
- [ ] Daglicht, presentatieverlichting en camera's instellen.
- [ ] Exterieur- en interieurbeelden renderen.
- [ ] Prestatiebudget voor polygonen en textures bewaken.

Acceptatie:

- [ ] Materiaalweergave blijft herkenbaar in de GLB-export.
- [ ] Controlebeelden hebben consistente camera's en belichting.
- [ ] Modelgrootte blijft binnen afgesproken budget.

### Fase 7 — Validatie en kwaliteitscontrole

- [ ] Configuratieschema automatisch valideren.
- [ ] Afmetingen, units en objectnamen valideren.
- [ ] Openingen en wandrelaties controleren.
- [ ] Duplicaten, onbedoelde overlap en non-manifold geometrie onderzoeken.
- [ ] Ontbrekende materials/textures detecteren.
- [ ] Headless rebuild en export testen.
- [ ] Visuele regressierenders vergelijken.
- [ ] Prestatie en bestandsgrootte rapporteren.
- [ ] Bekende beperkingen vastleggen.

Acceptatie:

- [ ] Alle verplichte controles slagen of afwijkingen zijn expliciet geaccepteerd.
- [ ] Een schone checkout kan het model reproduceren.
- [ ] De GLB opent in ten minste twee compatibele viewers.

### Fase 8 — Interactieve 3D-viewer

- [ ] Viewer-techniek kiezen.
- [ ] Draaien, zoomen en navigeren implementeren.
- [ ] Camera-reset en laadstatus toevoegen.
- [ ] Verdieping/dak zichtbaar en onzichtbaar kunnen maken.
- [ ] Desktop en mobiel toetsen.
- [ ] Foutafhandeling en toegankelijkheid toevoegen.
- [ ] Productiebuild automatiseren.

Acceptatie:

- [ ] Niet-technische bezoekers kunnen het huis zonder Blender bekijken.
- [ ] Viewer werkt op afgesproken browsers en schermformaten.
- [ ] Gebruikersinstructie is aanwezig.

### Fase 9 — Publicatie, documentatie en overdracht

- [ ] Hostingdoel kiezen en configureren.
- [ ] Viewer en model publiceren.
- [ ] Publieke URL testen.
- [ ] Installatie-, bouw-, export- en herstelhandleiding afronden.
- [ ] Projectwiki afronden en vanuit `README.md` vindbaar maken.
- [ ] Testen dat een beginner het huis met alleen de Wiki kan bekijken.
- [ ] Beslissen of de repositorydocumentatie ook naar GitHub Wiki wordt gepubliceerd.
- [ ] Versie taggen en release notes maken.
- [ ] Back-up- en overdrachtscontrole uitvoeren.
- [ ] Vervolgwensen in backlog plaatsen.

Acceptatie:

- [ ] Gepubliceerde versie is bereikbaar en reproduceerbaar.
- [ ] Repository kan door een andere ontwikkelaar worden gebruikt.
- [ ] Wiki bevat minimaal startinstructies, versie-informatie, probleemoplossing en verwijzingen naar projectdocumentatie.
- [ ] Projecteigenaar accepteert de eindoplevering.

## 5. Voortgangsregels

- Eén taak krijgt tegelijk de status actief.
- Taken worden pas afgevinkt na bewijs en goedkeuring.
- Blokkades worden dezelfde sessie in `STATUS.md` geregistreerd.
- Scopewijzigingen krijgen een beslisrecord in `docs/decisions.md`.
- Iedere mijlpaal krijgt een herkenbare Git-tag.
- Grote wijzigingen worden via een featurebranch uitgevoerd.

## 6. Initiële risico's

| Risico | Gevolg | Maatregel |
|---|---|---|
| Alleen handmatig `.blend` bewerken | Niet reproduceerbaar | Configuratie en Python als bron |
| Onvolledige maten | Verkeerd ontwerp | Stoppen en besluit vragen |
| Binaire bestanden in Git | Grote historie | Selectief Git LFS en releases |
| Blender/API-versieverschil | Scripts breken | LTS-versie vastleggen |
| Model technisch goed, visueel fout | Foute oplevering | Vaste renders en menselijke review |
| Te veel detail te vroeg | Vertraging | Eerst verticale proef en casco |
| Textures/licenties onduidelijk | Publicatierisico | Bronnen- en licentieregister |
| Webmodel te zwaar | Slechte ervaring | Prestatiebudget en optimalisatie |

## 7. Voorlopige besluiten die nog nodig zijn

- Gewenste Blender LTS-versie.
- Conceptmodel of architectonisch maatvast prototype: voorlopig maatvast prototype.
- Doelplatform voor de viewer.
- Openbaar of privé GitHub-project.
- Wel of geen Git LFS voor `.blend` en grote textures.
- Welke tekeningen, maten en referentiebeelden beschikbaar zijn.

## 8. Wiki en gebruikersdocumentatie

- Repositorydocumentatie is de bron van waarheid.
- Doelgroepen zijn beginners, reviewers/projecteigenaar en ontwikkelaars.
- ChatGPT stelt structuur en tekst voor.
- Codex verwerkt goedgekeurde wijzigingen.
- De projecteigenaar keurt inhoud en publicatie goed.
- Wiki-instructies worden bij iedere mijlpaal tegen de echte uitvoer gecontroleerd.
