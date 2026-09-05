# Wiki-intro: het huis bekijken en de eerste run uitvoeren

Deze pagina is bedoeld voor iemand die nog niets van Blender weet en het huidige huisontwerp wil bekijken. Het tweede deel legt uit hoe een technisch gebruiker het model opnieuw kan genereren.

Je hoeft het model niet opnieuw te bouwen als je het huis alleen wilt bekijken.

## Wat dit project doet

Dit project maakt een reproduceerbaar 3D-model van een huis in Songkhla. Blender wordt gebruikt als 3D-programma, maar belangrijke wijzigingen worden vastgelegd in configuratiebestanden en Python-scripts. Daardoor kan dezelfde projectversie opnieuw worden opgebouwd en gecontroleerd.

De huidige bruikbare huisweergave staat in Fase 3:

- Blender-bestand: `out/phase3/blender/songkhla_exterior.blend`
- Deelbaar 3D-bestand: `out/phase3/exports/songkhla_exterior.glb`
- Controlebeelden: `out/phase3/renders/`
- Validatierapport: `out/phase3/reports/validation.json`

Let op: dit is nog een buitenmodel in ontwikkeling. Binnenmuren, interieur, materialen en definitieve detaillering zijn nog niet afgerond. Het model is geen constructieberekening, vergunningstekening of definitief bouwadvies.

## Alleen bekijken: wat heb je nodig?

- Blender **5.2.1**;
- bij voorkeur een muis met een indrukbaar scrollwiel;
- deze repository, inclusief het goedgekeurde `.blend`-bestand.

Voor alleen bekijken heb je geen PowerShell, Python of Codex nodig.

## Het bestaande model veilig openen

1. Start Blender 5.2.1.
2. Kies **File > Open**.
3. Open `out/phase3/blender/songkhla_exterior.blend`.
4. Wacht totdat de scène volledig is geladen.
5. Beweeg de muis boven het grote 3D-venster, de **3D Viewport**.
6. Druk op `Home` als het huis niet meteen in beeld staat.

Wil je vrij experimenteren? Maak dan eerst in Windows Verkenner een kopie van het `.blend`-bestand en open de kopie.

## Rond het huis bewegen

| Actie | Bediening |
|---|---|
| Rond het huis draaien | Houd de middelste muisknop ingedrukt en beweeg de muis |
| Beeld verschuiven | Houd `Shift` en de middelste muisknop ingedrukt |
| In- en uitzoomen | Draai het muiswiel |
| Het volledige model in beeld zetten | Druk op `Home` |
| Geselecteerd onderdeel in beeld zetten | Selecteer het onderdeel en druk op numeriek `.` |
| Camerabeeld openen of verlaten | Druk op numeriek `0` |
| Vooraanzicht | Druk op numeriek `1` |
| Zijaanzicht | Druk op numeriek `3` |
| Bovenaanzicht | Druk op numeriek `7` |

Heb je geen numeriek toetsenblok? Gebruik dan **View > Viewpoint** in de 3D Viewport.

## Het huis duidelijk weergeven

Druk op `Z` en kies een weergavemodus:

- **Material Preview** toont materialen en kleuren;
- **Solid** werkt sneller op een minder krachtige computer;
- **Rendered** toont de volledige belichting, maar kan langzaam zijn.

Rechtsboven in de 3D Viewport staan dezelfde weergavemodi als ronde pictogrammen.

## Onderdelen tonen en verbergen

Rechts staat normaal de **Outliner**: een lijst met objecten en verzamelingen. Met het oogpictogram kun je onderdelen tijdelijk zichtbaar of onzichtbaar maken.

Gebruik tijdens het bekijken alleen de oogpictogrammen. Verwijder, verplaats, schaal of hernoem geen objecten. Druk op `Esc` als je per ongeluk een bewerking bent begonnen.

## Veilig afsluiten

1. Kies **File > Quit** of sluit Blender.
2. Vraagt Blender **Save changes?**, kies dan **Don't Save**.

Ook een andere zichtbaarheid, camerapositie of weergavemodus kan door Blender als een wijziging worden gezien. Met **Don't Save** blijft het goedgekeurde model ongewijzigd.

## Eerst naar de controlebeelden kijken

De renders geven snel een vast beeld van alle zijden:

- `out/phase3/renders/east.png`
- `out/phase3/renders/south.png`
- `out/phase3/renders/west.png`
- `out/phase3/renders/north.png`
- `out/phase3/renders/perspective.png`

Gebruik daarna het Blender-bestand om vrij rond het huis te bewegen. Het GLB-bestand kan in een geschikte externe 3D-viewer worden geopend.

## Voor technische gebruikers: model opnieuw genereren

Voor deze stappen heb je daarnaast nodig:

- Windows met PowerShell;
- een correct ingestelde omgevingsvariabele `BLENDER_EXECUTABLE`;
- het volledige project met configuratie en scripts.

Stel voor de huidige PowerShell-sessie het lokale pad naar Blender in:

```powershell
$env:BLENDER_EXECUTABLE = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
```

Dit machinegebonden pad hoort niet in Git.

Open PowerShell in de repository-root:

```powershell
Set-Location D:\repo\blender_design
```

Controleer eerst de configuratie en Blender-koppeling:

```powershell
.\scripts\build_songkhla_exterior.ps1 -ValidateOnly
```

Voer alleen na een geslaagde validatie de build uit:

```powershell
.\scripts\build_songkhla_exterior.ps1 -Clean
```

Na een geslaagde run staan de nieuwe uitvoerbestanden onder `out/phase3/`.

## Als iets niet lukt

- **Het huis is niet zichtbaar:** beweeg de muis boven de 3D Viewport en druk op `Home`.
- **Je zit binnen een muur:** zoom uit of druk opnieuw op `Home`.
- **Alles is grijs:** druk op `Z` en kies **Material Preview**.
- **Blender reageert traag:** kies **Solid** en wacht tot het laden klaar is.
- **Het beeld beweegt niet zoals verwacht:** druk op `Esc` en probeer opnieuw boven de 3D Viewport.
- **`BLENDER_EXECUTABLE` is niet ingesteld:** stel de omgevingsvariabele opnieuw in.
- **De Blender-versie wijkt af:** gebruik de vastgelegde projectversie 5.2.1.
- **Configuratie ontbreekt:** controleer of PowerShell in de repository-root staat.
- **Openen of bouwen geeft een fout:** bewaar de foutmelding en wijzig het bronbestand niet.

De buildlog staat normaal in:

`out/phase3/logs/build.log`

Aanvullende technische oplossingen staan in `docs/troubleshooting.md`.

## Belangrijk om te weten

- De scène-eenheden in Blender zijn meters.
- Gegenereerde bestanden onder `out/` zijn uitvoer en niet de enige bron van waarheid.
- Wijzigingen aan het huis worden via configuratie en scripts reproduceerbaar gemaakt.
- De tijdelijke Fase 2-proefwoning is technische testdata en niet het echte huisontwerp.
- Later komt er een interactieve webviewer waarmee het huis zonder Blender kan worden bekeken.
