# Algemene acceptatiecriteria

Een taak is alleen gereed wanneer:

- de afgesproken bestanden bestaan;
- relevante commando's zonder onverwachte fout eindigen;
- validaties aantoonbaar zijn uitgevoerd;
- gegenereerde geometrie visueel is beoordeeld;
- aannames en afwijkingen zijn gedocumenteerd;
- geen onbedoelde bestanden zijn gewijzigd;
- documentatie overeenkomt met het resultaat;
- de projecteigenaar het resultaat heeft goedgekeurd.

Een fase is alleen gereed wanneer:

- alle verplichte taken en criteria zijn afgehandeld;
- blokkades zijn opgelost of expliciet geaccepteerd;
- `STATUS.md`, `PROJECT_PLAN.md` en `CHANGELOG.md` zijn bijgewerkt;
- een herkenbare, werkende Git-versie beschikbaar is.

## Fase 2 — Verticale Blender-proefopstelling

- Eén commando bouwt de proefscène.
- `BLENDER_EXECUTABLE` wordt gecontroleerd.
- Blender 5.2.1 LTS draait headless.
- Scene units zijn meters.
- De goedgekeurde tijdelijke proefwoning wordt uit configuratie gebouwd.
- Verwachte objecten hebben stabiele namen en positieve dimensies.
- Openingen liggen binnen de betreffende wand.
- Uitvoer blijft binnen `out/phase2`.
- Exitcode is 0 bij succes en non-zero bij fout.
- Verwachte bestanden:
  - `out/phase2/blender/house.blend`
  - `out/phase2/exports/house.glb`
  - `out/phase2/renders/front.png`
  - `out/phase2/renders/back.png`
  - `out/phase2/renders/left.png`
  - `out/phase2/renders/right.png`
  - `out/phase2/reports/validation.json`
  - `out/phase2/logs/build.log`
- De projecteigenaar keurt uiteindelijk de vier renders visueel goed.
