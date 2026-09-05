# Blender Design

Parametrisch Blender-project voor een maatvast 3D-prototype van een huis, bestuurd vanuit IntelliJ met Codex en beheerd met Git/GitHub.

## Dagelijkse werkwijze

1. Open `STATUS.md`.
2. Geef de opdracht onder **Eerstvolgende Codex-opdracht** aan Codex in IntelliJ.
3. Laat Codex eerst `AGENTS.md`, `PROJECT_PLAN.md` en `STATUS.md` lezen.
4. Beoordeel scripts, controles, renders en exports.
5. Laat pas na goedkeuring status, plan en changelog bijwerken.
6. Commit één logisch, getest resultaat.

## Belangrijkste uitvoer

- Bewerkbaar model: `blender/house.blend`
- Deelbaar model: `exports/house.glb`
- Controlebeelden: `renders/`
- Interactieve viewer: `viewer/`

Het Blender-bestand is niet de enige bron van waarheid. De configuratie en Python-scripts moeten het model reproduceerbaar kunnen genereren.

## Wiki

De beginnersintro staat in [docs/wiki-intro-eerste-run.md](docs/wiki-intro-eerste-run.md). Deze pagina is bedoeld voor beginners die het huis willen openen of opnieuw genereren.
