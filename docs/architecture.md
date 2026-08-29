# Technische architectuur

## Keten

Ontwerpeisen → configuratie → Blender Python-generator → `.blend` → validatie/renders → `.glb` → webviewer.

## Bronnen van waarheid

1. Goedgekeurde requirements en besluiten.
2. Machineleesbare huisconfiguratie.
3. Reproduceerbare Python-generators.
4. Gegenereerde `.blend` en exports.

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
