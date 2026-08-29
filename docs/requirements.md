# Requirements

## Productdoel

Een interactief deelbaar, maatvast 3D-prototype van een huis.

## Fase 3 — Eisen, referenties en maatvoering

Deze inventarisatie vormt de basis voor Fase 3. De tijdelijke Fase 2-proefwoning is uitsluitend technische testdata en wordt niet gebruikt als definitieve huismaatvoering.

### Doel en gebruikers

- Bekend: het projectdoel is een reproduceerbaar, parametrisch en maatvast 3D-prototype van een huis.
- Bekend: het resultaat moet als `.blend` bewerkbaar en als `.glb` interactief deelbaar zijn.
- Door Edward bevestigd: het te modelleren object is een bestaand huis in Songkhla.
- Door Edward bevestigd: het huis is gebouwd volgens de aangeleverde bouwtekeningen.
- Door Edward bevestigd: het Blender-model dient als geometrisch betrouwbare basis voor een toekomstig verbouwingsontwerp.
- Nog aan te leveren door Edward: verdere doelgroep en gebruikers van het 3D-prototype.

### Kijk- en publicatiedoel

- Bekend: het prototype moet interactief deelbaar zijn.
- Door Edward bevestigd: geometrische juistheid heeft nu voorrang op fotorealisme.
- Nog aan te leveren door Edward: gewenste kijkervaring.
- Nog aan te leveren door Edward: gewenst publicatiedoel.

### Eerste buitenmodelscope

- Door Edward bevestigd: de eerste modelscope omvat uitsluitend de bestaande buitengeometrie.
- Door Edward bevestigd: binnenmuren, ruimtes en interieur worden in een latere stap uitgewerkt.
- Door Edward bevestigd: de bouwtekeningen zijn leidend voor geometrie.
- Door Edward bevestigd: latere actuele foto's zijn alleen nodig voor materiaal- en detailverificatie.
- Minimaal over te nemen: perceeloriëntatie.
- Minimaal over te nemen: verhoogd vloerniveau.
- Minimaal over te nemen: hoofdvorm en buitenwanden.
- Minimaal over te nemen: alle buitenramen en buitendeuren volgens de tekeningen.
- Minimaal over te nemen: voorveranda en overige buitenplatforms.
- Minimaal over te nemen: buitentrappen.
- Minimaal over te nemen: dakvolumes, dakhellingen en overstekken.

### Locatie en noordrichting

- Door Edward bevestigd: het bestaande huis staat in Songkhla.
- Door Edward bevestigd: voorgevel en openbare weg liggen aan de oostzijde.
- Door Edward bevestigd: de achterzijde ligt aan de westzijde.
- Door Edward bevestigd: de noordzijde ligt rechts op de plattegrond.
- Door Edward bevestigd op basis van de noordpijl en voorgevel: gevel 1 is oost/voorgevel.
- Door Edward bevestigd op basis van de noordpijl en voorgevel: gevel 2 is zuid.
- Door Edward bevestigd op basis van de noordpijl en voorgevel: gevel 3 is west/achtergevel.
- Door Edward bevestigd op basis van de noordpijl en voorgevel: gevel 4 is noord.
- Nog aan te leveren door Edward: eventuele situatiegegevens die invloed hebben op oriëntatie, zichtlijnen of plaatsing.

### Perceel

- Rechtstreeks afgelezen tekeningmaat: perceel circa 13,00 meter noord-zuid bij 40,00 meter oost-west.
- Nog aan te leveren door Edward: perceelsgrenzen, rooilijnen, bouwvlak of andere randvoorwaarden.
- Nog aan te leveren door Edward: definitieve perceelmaat en juridische perceelgegevens indien die afwijken van de aangeleverde tekeningset.

### Buitenmaten en bouwvolume

- Rechtstreeks afgelezen tekeningmaat: structureel hoofdraster woning circa 10,50 meter noord-zuid bij 16,00 meter oost-west.
- Bevestigd voorlopig leidend nokpeil: +4.85 m, bronbladen `5.A04-01.pdf` t/m `8.A04-04.pdf` en `10.A05-02.pdf`.
- Onopgeloste tekeningsafwijking: `10.A05-02.pdf` toont ook 4.94 m; deze maat wordt niet voor modellering gebruikt zonder later expliciet besluit.
- Nog aan te leveren door Edward: maximale bouwhoogte of andere volumegrenzen.
- Nog aan te leveren door Edward: definitieve buitenwerkse gevelmaten wanneer die afwijken van het structurele hoofdraster.

### Verdiepingen en niveaus

- Door Edward bevestigd: één verhoogde bouwlaag.
- Rechtstreeks afgelezen tekeningmaat: hoofdvloerniveau circa +1,50 meter boven maaiveld.
- Bevestigd voorlopig leidend nokpeil: +4.85 m, bronbladen `5.A04-01.pdf` t/m `8.A04-04.pdf` en `10.A05-02.pdf`.
- Nog aan te leveren door Edward: overige niveaus en exacte peilmaten indien nodig voor detaillering.

### Ruimtelijst en netto-oppervlakten

- Door Edward bevestigd: drie slaapkamers.
- Door Edward bevestigd: keuken, eetruimte, woonkamer/ontvangstruimte, centrale hal, één badkamer, voorveranda, was-/achterruimte en buitentrappen.
- Nog aan te leveren door Edward: gewenste netto-oppervlakten per ruimte.
- Nog aan te leveren door Edward: gewenste relaties tussen ruimten, looproutes of zonering.

### Constructiediktes

- Nog aan te leveren door Edward: wanddiktes.
- Nog aan te leveren door Edward: vloerdiktes.
- Nog aan te leveren door Edward: dakdiktes.

### Ramen en deuren

- Door Edward bevestigd: ramen en deuren moeten worden gebaseerd op de aangeleverde bouwtekeningen.
- Door Edward bevestigd: de raam- en deurenschemabladen zijn 90 graden gedraaid weergegeven; breedte en hoogte zijn gecorrigeerd geinterpreteerd.

#### Raamtypen

Bronbladen: `11.A06-01.pdf` voor W1 t/m W4 en `12.A06-02.pdf` voor W5 t/m W7.

| Type | Breedte | Hoogte | Borstwering | Aantal | Ligging/functie | Eerste buitenmodelscope | Status |
|---|---:|---:|---:|---:|---|---|---|
| W1 | 2.00 m | 1.40 m | 0.60 m | 4 | Buitenraam | Relevant | Bevestigd |
| W2 | 3.00 m | 1.40 m | 0.60 m | 2 | Buitenraam | Relevant | Bevestigd |
| W3 | 0.50 m | 1.40 m | 0.60 m | 4 | Buitenraam | Relevant | Bevestigd |
| W4 | 1.35 m | 1.15 m | 0.90 m | 1 | Interne opening tussen keuken en eetruimte | Niet relevant | Bevestigd |
| W5 | 1.00 m | 1.10 m | 0.90 m | 2 | Buitenraam | Relevant | Bevestigd |
| W6 | 1.50 m | 1.10 m | 0.90 m | 1 | Buitenraam | Relevant | Bevestigd |
| W7 | 1.00 m | 0.40 m | 1.60 m | 1 | Buitenraam | Relevant | Bevestigd |

#### Deurtypen

Bronbladen: `11.A06-01.pdf` voor D1 t/m D4, `3.A03-01.pdf` voor controle buiten-/binnendeuren en `5.A04-01.pdf` voor de entreepartij D1.

| Type | Breedte | Hoogte | Totaal aantal | Verdeling/functie | Buitenaantal eerste buitenmodelscope | Status |
|---|---:|---:|---:|---|---:|---|
| D1 | 2.80 m | 2.00 m | 1 | Externe entreepartij | 1 | Bevestigd |
| D2 | 0.80 m | 2.00 m | 3 | Binnendeur | 0 | Bevestigd |
| D3 | 0.70 m | 2.00 m | 1 | Binnendeur | 0 | Bevestigd |
| D4 | 0.80 m | 2.00 m | 2 | 1 externe D4 bij keuken/servicezone; 1 interne D4 tussen keuken en eetruimte | 1 | Bevestigd |

- Bevestigd op `3.A03-01.pdf`: D2 en D3 zijn binnendeuren en worden niet meegenomen als buitenopeningen in de eerste buitenmodelscope.
- Bevestigd op `3.A03-01.pdf` en `5.A04-01.pdf`: D1 is de entreepartij aan de oostelijke voorgevel en is relevant voor het buitenmodel.
- Bevestigd op `3.A03-01.pdf`: van type D4 is alleen de D4 bij de keuken/servicezone een buitenopening voor de eerste buitenmodelscope; de andere D4 is intern tussen keuken en eetruimte.
- Bevestigd op `3.A03-01.pdf`: W4 is een interne opening tussen keuken en eetruimte en valt buiten de eerste buitenmodelscope.
- Nog aan te leveren of verder uit te werken: exacte plaatsing per gevel van alle buitenramen en buitendeuren in machineleesbare configuratie.

#### Buitenopeningenmatrix

| Gevel | Buitenopening | Asvak | Aangrenzende ruimte | Bevestiging | Offset binnen asvak |
|---|---|---|---|---|---|
| Oost/gevel 1 | W1 | 1-2 | Woonkamer | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Oost/gevel 1 | D1 | 2-3 | Entree | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Oost/gevel 1 | W1 | 3-4 | Slaapkamer 1 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Zuid/gevel 2 | D4 extern | A-B | Keuken/servicezone | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Zuid/gevel 2 | W5 | B-C | Keuken | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Zuid/gevel 2 | W5 | B-C | Keuken | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Zuid/gevel 2 | W2 | C-D | Eetruimte | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Zuid/gevel 2 | W2 | D-E | Woonkamer | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| West/gevel 3 | W6 | 1-2 | Keuken | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| West/gevel 3 | W1 | 2-3 | Slaapkamer 3 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| West/gevel 3 | W1 | 3-4 | Slaapkamer 2 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Noord/gevel 4 | W3 | B-C | Slaapkamer 2 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Noord/gevel 4 | W3 | B-C | Slaapkamer 2 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Noord/gevel 4 | W7 | C-D | Badkamer | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Noord/gevel 4 | W3 | D-E | Slaapkamer 1 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |
| Noord/gevel 4 | W3 | D-E | Slaapkamer 1 | Gevel, asvak en aangrenzende ruimte bevestigd | Nog niet bemaat; eventueel alleen visueel gecentreerd |

### Trappen en doorloopmaten

- Door Edward bevestigd: buitentrappen zijn onderdeel van het huis.
- Nog aan te leveren door Edward: doorloopmaten.
- Nog aan te leveren door Edward: vrije hoogtes, trapbreedtes of andere maatgevende eisen.

### Dak en hemelwaterafvoer

- Door Edward bevestigd: samengesteld hellend dak.
- Rechtstreeks afgelezen tekeningmaat: dakhelling circa 35 graden.
- Rechtstreeks afgelezen tekeningmaat: dakoverstek circa 1,00 meter.
- Bevestigd voorlopig leidend nokpeil: +4.85 m, bronbladen `5.A04-01.pdf` t/m `8.A04-04.pdf` en `10.A05-02.pdf`.
- Onopgeloste tekeningsafwijking: `10.A05-02.pdf` toont ook 4.94 m; deze maat wordt niet voor modellering gebruikt zonder later expliciet besluit.
- Nog aan te leveren door Edward: hemelwaterafvoer.
- Nog aan te leveren door Edward: nokrichtingen, dakvlakken, goten, regenpijpen en dakdetails.

### Materialen en stijl

- Door Edward bevestigd: de eerste materiaal- en kleurweergave blijft bewust eenvoudig en neutraal.
- Door Edward bevestigd: geometrische juistheid heeft nu voorrang op fotorealisme.
- Door Edward bevestigd: latere actuele foto's zijn alleen nodig voor materiaal- en detailverificatie.
- Nog aan te leveren door Edward: gewenste materialen.
- Nog aan te leveren door Edward: gewenste stijl.
- Nog aan te leveren door Edward: referenties voor gevels, dak, kozijnen, interieur of terrein.

### Referentiebestanden

- Externe bronset buiten Git: `fwdsongkhlahouseplan (1).zip`.
- Door Edward bevestigd: deze bronset bevat 19 PDF-bouw- en constructietekeningen, één SketchUp-model, twee exterieurreferentiebeelden en zes badkamerbeelden.
- Door Edward bevestigd: het huis is volgens deze tekeningen gebouwd.
- Bekend: de originele bronbestanden worden wegens persoonsgegevens in titelblokken voorlopig niet in Git opgenomen.
- Nog aan te leveren door Edward: opgeschoonde of geanonimiseerde bronbestanden als deze later wel in Git mogen worden opgenomen.
- Nog aan te leveren door Edward: bron/status per afzonderlijk referentiebestand wanneer de externe bronset verder wordt uitgesplitst.

### Harde eisen

- Bekend: de primaire technische bron bestaat uit configuratie en Blender Python-scripts.
- Bekend: Blender-scene-units gebruiken meters.
- Bekend: gebruikersdocumentatie gebruikt millimeters waar passend.
- Bekend: relatieve projectpaden gebruiken; persoonlijke absolute paden worden niet gecommit.
- Bekend: gegenereerde uitvoer blijft gescheiden van configuratie, scripts en documentatie.
- Door Edward bevestigd: het definitieve model moet het bestaande huis in Songkhla volgen zoals gebouwd volgens de aangeleverde bouwtekeningen.
- Door Edward bevestigd: de eerste modelscope omvat uitsluitend de bestaande buitengeometrie.
- Door Edward bevestigd: de bouwtekeningen zijn leidend voor geometrie.
- Door Edward bevestigd: geometrische juistheid heeft nu voorrang op fotorealisme.
- Bekend: originele bronbestanden met persoonsgegevens in titelblokken worden voorlopig niet in Git opgenomen.
- Nog aan te leveren door Edward: harde ontwerp-, maatvoerings-, perceel- en publicatie-eisen voor het definitieve huis.

### Aannames

- Bekend: het prototype is geen constructieberekening, vergunningstekening of gecertificeerd BIM-model.
- Bekend: buiten scope zonder apart besluit zijn constructieberekeningen, vergunningsstukken, gecertificeerd BIM/IFC-model, gedetailleerde installatietechniek, kostenraming en bouwoffertes.
- Bekend: de tijdelijke Fase 2-proefwoning is geen definitief huisontwerp.
- Bekend: Fase 2-proefmaten worden niet gebruikt als definitieve eisen.
- Door Edward bevestigd: binnenmuren, ruimtes en interieur vallen buiten de eerste buitenmodelscope en worden later uitgewerkt.
- Nog aan te leveren door Edward: welke ontbrekende gegevens tijdelijk als aanname mogen worden behandeld.

### Open vragen

- Nog aan te leveren door Edward: verdere doelgroep en gebruikers van het 3D-prototype.
- Nog aan te leveren door Edward: gewenste kijkervaring en publicatiedoel.
- Nog aan te leveren door Edward: definitieve perceelmaat en eventuele juridische perceelrandvoorwaarden.
- Nog aan te leveren door Edward: exacte buitenwerkse gevelmaten wanneer die afwijken van het structurele hoofdraster.
- Nog aan te leveren door Edward: overige niveaus en exacte peilmaten indien nodig voor detaillering.
- Nog aan te leveren door Edward: gewenste netto-oppervlakten.
- Nog aan te leveren door Edward: wand-, vloer- en dakdiktes.
- Nog aan te leveren door Edward: exacte plaatsing per gevel en draairichting van ramen en buitendeuren voor machineleesbare configuratie.
- Nog aan te leveren door Edward: exacte trappen, doorloopmaten, vrije hoogtes en trapbreedtes.
- Nog aan te leveren door Edward: hemelwaterafvoer, nokrichtingen, dakvlakken, goten, regenpijpen en dakdetails.
- Nog aan te leveren door Edward: materiaal- en stijldetails voor latere materiaal- en detailverificatie.
- Nog aan te leveren door Edward: geanonimiseerde bronbestanden of toestemming voor opname van opgeschoonde referenties in Git.

## Kwaliteitskenmerken

- Reproduceerbaar.
- Maatvast.
- Controleerbaar.
- Versiebeheerd.
- Interactief deelbaar.
- Uitbreidbaar zonder volledige herbouw.

## Buiten scope zonder apart besluit

- Constructieberekeningen.
- Vergunningsstukken.
- Gecertificeerd BIM/IFC-model.
- Gedetailleerde installatietechniek.
- Kostenraming of bouwoffertes.
