# Technische architectuur

## Keten

Ontwerpeisen → configuratie → Blender Python-generator → `.blend` → validatie/renders → `.glb` → webviewer.

## Bronnen van waarheid

1. Goedgekeurde requirements en besluiten.
2. Machineleesbare huisconfiguratie.
3. Reproduceerbare Python-generators.
4. Gegenereerde `.blend` en exports.

## Runtime

- Doelruntime: Blender 5.2.1 LTS.
- Ingebouwde scriptruntime: Blender-Python 3.13.13.
- Lokale Blender-paden zijn machineafhankelijk en worden niet als projectconfiguratie gecommit.
- Toekomstige commandoscripts lezen de omgevingsvariabele `BLENDER_EXECUTABLE`.
- Scripts kiezen niet automatisch een willekeurige Blender-versie uit `PATH`.

## Fase 2-commandoketen

```text
IntelliJ-terminal
→ scripts/build_phase2.ps1
→ BLENDER_EXECUTABLE
→ Blender 5.2.1 headless
→ scripts/blender/build_phase2_probe.py
→ config/phase2_probe.json
→ out/phase2/
```

De Fase 2-keten gebruikt een gecommit PowerShell-entrypoint en een gecommit Blender-Python-script. Lokale IntelliJ-runconfiguraties mogen dit script later aanroepen, maar zijn niet de technische projectbron. Gegenereerde Fase 2-uitvoer blijft voorlopig lokaal onder `out/phase2/`.

## Beoogde mappen

```text
config/       Machineleesbare parameters
scripts/      Blender-generators, validatie en export
assets/       Goedgekeurde textures en bronbestanden
blender/      Blender-werkbestanden
exports/      Deelbare modellen
renders/      Vaste controlebeelden
reports/      Validatie- en meetrapporten
viewer/       Interactieve webviewer
tests/        Automatische tests
docs/         Requirements, architectuur en besluiten
```

## Ontwerpprincipes

- Configuratie boven hardcoded maten.
- Rebuild boven ongedocumenteerde handmatige wijziging.
- Kleine scripts met duidelijke verantwoordelijkheden.
- Deterministische objectnamen en collections.
- Technische én visuele verificatie.
- Relatieve paden voor overdraagbaarheid.
