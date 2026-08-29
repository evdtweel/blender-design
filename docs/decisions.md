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
