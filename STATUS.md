# Projectstatus

Laatste update: 29 augustus 2026
Huidige fase: Fase 3 — Eisen, referenties en maatvoering
Algemene status: Fase 2 voltooid en goedgekeurd

## Afgerond

- Fase 0 — Projectbesturing en uitgangspunten afgerond.
- Fase 1 — Lokale omgeving en Git/GitHub afgerond.
- Fase 2 — Verticale Blender-proefopstelling afgerond en goedgekeurd op 29 augustus 2026.
- M1 — IntelliJ → Blender automatisering werkt voltooid op 29 augustus 2026.
- Fase 2-ontwerpanalyse uitgevoerd.
- DEC-005 goedgekeurd voor commandoketen, proefwoning en outputbeleid.
- Succesvolle gevalideerde headless end-to-end-uitvoering met Blender 5.2.1 LTS uitgevoerd.
- Werkende Fase 2-build levert `out/phase2/blender/house.blend`, `out/phase2/exports/house.glb`, vier controlerenders, `out/phase2/reports/validation.json` met status `passed` en `out/phase2/logs/build.log`.
- Fase 2-plan voltooid in commit `725dbf8`.
- Fase 2-buildlog vastgelegd in commit `cba4e56`.
- Eerste eenvoudige Songkhla-buitenmodel gegenereerd zonder commit: `out/phase3/blender/songkhla_exterior.blend`, `out/phase3/exports/songkhla_exterior.glb`, vijf renders, `out/phase3/reports/validation.json` met status `passed` en `out/phase3/logs/build.log`.
- Fase 3-configuratie `config/songkhla_exterior.json` gebruikt als bron voor het eerste eenvoudige buitenmodel.
- Fase 3-buildscript `scripts/build_songkhla_exterior.ps1` en Blender-generator `scripts/blender/build_songkhla_exterior.py` lokaal aangemaakt, nog niet gecommit.
- Gegenereerde uitvoer onder `/out/` wordt genegeerd.
- Projectbesturing ingericht.
- `AGENTS.md` actief.
- Resultaatrapportage actief.
- Repository-hygiëne ingericht.
- Eerste gecontroleerde commit gemaakt: `a75ac31`.
- Bewijscommit vóór Fase 1-afsluiting: `c84d938`.
- Lokale omgeving read-only geïnventariseerd.
- Blender 5.2.1 LTS geverifieerd als beoogde projectbasis.
- Blender-Python 3.13.13 geverifieerd.
- `.gitattributes` en DEC-003 voorbereid voor repositorybrede regelafhandeling.
- `.gitattributes` en renormalisatie gecontroleerd; renormalisatie leverde geen bestandswijzigingen op.
- Repository gekoppeld aan GitHub: `https://github.com/evdtweel/blender-design`.
- Branch `main` volgt `origin/main`.
- IntelliJ-project `D:\repo\blender_design` aangemaakt.
- Git-repository zichtbaar in IntelliJ.
- Codex werkt met directory `D:\repo\blender_design` en `workspace-write`.
- Hoofdarchitectuur en beheerwijze besproken.
- Eerste versie van het bestuurbare projectplan opgesteld.
- Startdocumenten zijn lokaal aanwezig en door Codex gelezen.
- Projectdoel, taakverdeling, gefaseerde werkwijze en initiële risico-inventarisatie zijn goedgekeurd.
- DEC-001 is goedgekeurd door de projecteigenaar.
- Repository-hygiëne en permanente resultaatrapportage zijn goedgekeurd.

## Actief

- Fase 3 voorbereiden voor eisen, referenties en maatvoering.
- Eerste eenvoudige Songkhla-buitenmodel beoordelen op basis van de gegenereerde Fase 3-uitvoer.

## Geblokkeerd

- Geen blokkades.

## Aandachtspunten

- `PATH` is bewust nog niet aangepast voor Blender.
- Oudere Blender-installaties 4.1.1 en 4.3.0 zijn aanwezig, maar blokkeren niet omdat toekomstige scripts `BLENDER_EXECUTABLE` gebruiken.
- Systeemwijde `core.autocrlf=true` wordt bewust niet gewijzigd; `.gitattributes` is de projectbrede regelconfiguratie.
- Pushes gebruiken geen force zonder latere expliciete toestemming van de projecteigenaar.
- Fase 3-model gebruikt tijdelijke blockoutwaarden voor nog onbekende diktes en wand-/dakuitwerking; deze zijn niet bevestigd als architectonische maatvoering.
- Blender 5.2.1 LTS meldt tijdens opslaan/exporteren waarschuwingen over niet-relatieve interne Blender assetpaden voor standaardmaterialen; de projectpaden blijven relatief.

## Besluiten nodig

- Fase 3 vereist nog goedgekeurde eisen, referenties en maatvoering.

## Eerstvolgende Codex-opdracht

Start Fase 3 met het verzamelen en vastleggen van eisen, referenties en maatvoering, zonder Fase 3 al als voltooid te markeren.

## Bewijs voor afronding

- Codex rapporteert alle aanwezige startdocumenten.
- Codex vat de belangrijkste projectregels correct samen.
- Codex meldt `git status`, staged bestanden en diff-controles zonder onverwachte bestanden.
- Eerste gecontroleerde documentatiecommit bestaat: `a75ac31`.

## Huidige fase

Fase 3 — Eisen, referenties en maatvoering.
