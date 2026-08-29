# AGENTS.md

## Projectdoel

Bouw een reproduceerbaar, parametrisch en maatvast 3D-prototype van een huis in Blender. Het resultaat moet als `.blend` bewerkbaar en als `.glb` interactief deelbaar zijn.

## Verplichte werkwijze

1. Lees vóór iedere taak `PROJECT_PLAN.md`, `STATUS.md` en relevante bestanden in `docs/`.
2. Voer uitsluitend de actieve, afgebakende taak uit.
3. Meld aannames en ontbrekende informatie; verzin geen architectonische maten.
4. Vraag toestemming voordat scope, eisen, acceptatiecriteria of ontwerpbesluiten worden gewijzigd.
5. Gebruik meters als Blender scene unit en millimeters in gebruikersdocumentatie waar passend.
6. Houd configuratie, scripts, gegenereerde bestanden en documentatie gescheiden.
7. Gebruik stabiele, beschrijvende objectnamen en collections.
8. Bewaar reproduceerbare geometrie in Python/configuratie; voorkom uitsluitend handmatige Blender-wijzigingen.
9. Overschrijf geen goedgekeurd model zonder voorafgaand Git-checkpoint.
10. Voer na iedere modelwijziging relevante validatie, export en controle-renders uit.

## Kwaliteitsregels

- Geen negatieve of nulafmetingen.
- Openingen moeten binnen de bijbehorende wand liggen.
- Objecten mogen niet onbedoeld dubbel of overlappend zijn.
- Exporteerbare materialen gebruiken een glTF-geschikte Principled BSDF-opbouw.
- Relatieve projectpaden gebruiken; geen persoonlijke absolute paden committen.
- Secrets, tokens en lokale IDE-instellingen nooit committen.
- Een taak is alleen gereed als de acceptatiecriteria aantoonbaar zijn gehaald.

## Wijzigingsrapport

Rapporteer na iedere taak:

- gewijzigde bestanden;
- uitgevoerde commando's;
- test- en validatieresultaten;
- gegenereerde uitvoer;
- aannames, risico's en openstaande vragen;
- voorgestelde volgende stap.

Werk `STATUS.md`, `PROJECT_PLAN.md` en `CHANGELOG.md` alleen bij nadat de gebruiker het resultaat heeft goedgekeurd.

## Verplichte resultaatrapportage

- Schrijf na iedere opdracht het volledige eindrapport naar `CODEX_RESULT.md` in de repository-root.
- Overschrijf daarbij het resultaat van de vorige opdracht.
- Het rapport bevat minimaal:
  - datum en naam van de opdracht;
  - uitvoeringsstatus: Geslaagd, Gedeeltelijk geslaagd, Geblokkeerd of Mislukt;
  - samenvatting;
  - gewijzigde bestanden;
  - exact uitgevoerde commando’s;
  - test- en validatieresultaten;
  - gegenereerde uitvoer;
  - aannames en genomen beslissingen;
  - waarschuwingen, fouten en blokkades;
  - nog openstaande vragen;
  - precies één aanbevolen volgende stap.
- Vermeld ook expliciet wanneer geen bestanden zijn gewijzigd.
- Geef in AI Chat daarnaast alleen een korte samenvatting en vermeld dat het volledige rapport in `CODEX_RESULT.md` staat.
- `CODEX_RESULT.md` is een lokaal overdrachtsbestand en wordt niet gecommit.
- Deze rapportage is verplicht, ook bij een mislukte of geblokkeerde opdracht.
- Als Codex het rapportbestand niet kan schrijven, moet het dit expliciet in AI Chat melden.
