# Besluitlogboek

## Werkwijze

Gebruik per belangrijk besluit:

```markdown
## DEC-000 — Titel

- Datum:
- Status: Voorgesteld / Goedgekeurd / Vervangen
- Aanleiding:
- Besluit:
- Alternatieven:
- Gevolgen:
- Goedgekeurd door:
```

## DEC-001 — Parametrische modelbesturing

- Datum: 29 augustus 2026
- Status: Goedgekeurd
- Aanleiding: Een binair `.blend`-bestand is slecht vergelijkbaar en moeilijk reproduceerbaar.
- Besluit: Gebruik configuratie en Blender Python-scripts als primaire technische bron; gebruik `.blend` als bewerkbare uitvoer.
- Alternatieven: Volledig handmatig modelleren.
- Gevolgen: Meer initiële structuur, maar betere herhaalbaarheid en controle.
- Goedgekeurd door: Projecteigenaar op 29 augustus 2026.

## DEC-002 — Blender 5.2.1 LTS als projectbasis

- Datum: 29 augustus 2026
- Status: Goedgekeurd
- Aanleiding: Het project heeft een vaste, reproduceerbare Blender-runtime nodig. Op de ontwikkelmachine zijn meerdere Blender-versies aanwezig en `blender` staat niet in `PATH`.
- Besluit: Gebruik Blender 5.2.1 LTS als vastgelegde projectbasis. Scripts mogen later niet automatisch een willekeurige Blender-versie uit `PATH` kiezen, maar gebruiken de omgevingsvariabele `BLENDER_EXECUTABLE`. Het werkelijke lokale installatiepad blijft machineafhankelijk en wordt niet gecommit. `PATH` wordt nu niet gewijzigd en oudere Blender-versies worden nu niet verwijderd.
- Alternatieven: Blender via `PATH` kiezen, een oudere geïnstalleerde Blender-versie gebruiken, of een lokaal absoluut installatiepad in projectconfiguratie vastleggen.
- Gevolgen: Toekomstige automatisering moet controleren of `BLENDER_EXECUTABLE` naar Blender 5.2.1 LTS wijst. Blender 5.2.1 LTS bevat Blender-Python 3.13.13. Ontwikkelaars moeten hun lokale pad buiten Git instellen.
- Goedgekeurd door: Projecteigenaar op 29 augustus 2026.

## DEC-003 — Repositorybrede regelafhandeling

- Datum: 29 augustus 2026
- Status: Goedgekeurd
- Aanleiding: De repository heeft een eenduidig line-endingbeleid nodig dat niet afhankelijk is van lokale Git-instellingen.
- Besluit: Gebruik `.gitattributes` als gezaghebbende projectconfiguratie voor regelafhandeling. Tekstbestanden gebruiken LF. Windows `.bat`- en `.cmd`-bestanden gebruiken CRLF. Binaire bestanden worden expliciet als `binary` behandeld. Lokale `core.autocrlf`-instellingen worden niet gewijzigd.
- Alternatieven: Vertrouwen op lokale Git-configuratie of regelafhandeling pas later bepalen.
- Gevolgen: Toekomstige bestandsnormalisatie moet tegen `.gitattributes` worden gecontroleerd. Renormalisatie wordt afzonderlijk gecontroleerd en niet vermengd met deze besluitcommit.
- Goedgekeurd door: Projecteigenaar op 29 augustus 2026.

## DEC-004 — GitHub-repository en branchconventie

- Datum: 29 augustus 2026
- Status: Goedgekeurd
- Aanleiding: De lokale repository moet reproduceerbaar met de bedoelde private GitHub-repository verbonden zijn.
- Besluit: Gebruik de private GitHub-repository `evdtweel/blender-design` met HTTPS-remote `origin`. `main` is de standaardwerkbranch en de lokale branch `main` volgt `origin/main`.
- Alternatieven: De lokale branch `master` behouden, SSH als remoteprotocol gebruiken, of de remote pas later koppelen.
- Gevolgen: Gewone pushes gaan naar `origin/main`. Pushes gebruiken geen force, tenzij de projecteigenaar daarvoor later expliciet toestemming geeft.
- Goedgekeurd door: Projecteigenaar op 29 augustus 2026.

## DEC-005 — Fase 2-commandoketen, proefwoning en outputbeleid

- Datum: 29 augustus 2026
- Status: Goedgekeurd
- Aanleiding: De verticale Blender-proefopstelling heeft een reproduceerbare, Windows-vriendelijke commandoketen en afgebakend outputbeleid nodig voordat scripts of configuratie worden gemaakt.
- Besluit: Gebruik `scripts/build_phase2.ps1` als primair entrypoint en `scripts/blender/build_phase2_probe.py` als Blender-script. Gebruik `config/phase2_probe.json` als configuratie. Blender wordt via `BLENDER_EXECUTABLE` gestart en moet Blender 5.2.1 LTS zijn. Blender draait headless met `--background --factory-startup`. Edward start de keten primair vanuit de IntelliJ-terminal met `.\scripts\build_phase2.ps1 -Clean`.
- Besluit: `-Clean` mag uitsluitend `out/phase2/` leegmaken of vervangen, na strikte controle dat het doelpad binnen de repository en exact binnen de toegestane outputroot ligt. Gegenereerde uitvoer komt voorlopig uitsluitend onder `out/phase2/`, blijft voorlopig lokaal en wordt niet gecommit. Git LFS wordt nog niet ingericht. Een latere lokale IntelliJ Run Configuration mag hetzelfde gecommitte script aanroepen, maar is niet de technische projectbron.
- Besluit: De tijdelijke proefwoning is uitsluitend technische testdata en geen definitief huisontwerp. Goedgekeurde tijdelijke Fase 2-testdata: buitenmaat 8,00 × 6,00 meter; wandhoogte 2,80 meter; wanddikte 0,20 meter; buitendeur 0,90 × 2,10 meter; ramen 1,20 × 1,20 meter; borstwering ramen 0,90 meter; één eenvoudige binnenwand; symmetrisch zadeldak; dakhelling 30 graden; dakoverstek 0,30 meter; vier controleaanzichten voor, achter, links en rechts.
- Besluit: Plaatsing en aantallen van deur en ramen moeten in de eerste configuratie technisch eenvoudig en valide zijn en vormen geen definitief architectonisch ontwerp.
- Alternatieven: Directe Blender-aanroep vanuit IntelliJ, een externe Python-wrapper buiten Blender, output in de README-hoofdmappen schrijven, of gegenereerde uitvoer direct committen.
- Gevolgen: De volgende implementatiestap mag de minimale projectstructuur, wrapper, Blender-script en proefconfiguratie maken volgens dit besluit. Output onder `out/phase2/` moet lokaal blijven totdat de projecteigenaar anders besluit.
- Goedgekeurd door: Projecteigenaar op 29 augustus 2026.
