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
- Nog aan te leveren door Edward: verdere doelgroep en gebruikers van het 3D-prototype.

### Kijk- en publicatiedoel

- Bekend: het prototype moet interactief deelbaar zijn.
- Nog aan te leveren door Edward: gewenste kijkervaring.
- Nog aan te leveren door Edward: gewenst publicatiedoel.

### Locatie en noordrichting

- Door Edward bevestigd: het bestaande huis staat in Songkhla.
- Door Edward bevestigd: voorgevel en openbare weg liggen aan de oostzijde.
- Door Edward bevestigd: de achterzijde ligt aan de westzijde.
- Door Edward bevestigd: de noordzijde ligt rechts op de plattegrond.
- Nog aan te leveren door Edward: eventuele situatiegegevens die invloed hebben op oriëntatie, zichtlijnen of plaatsing.

### Perceel

- Rechtstreeks afgelezen tekeningmaat: perceel circa 13,00 meter noord-zuid bij 40,00 meter oost-west.
- Nog aan te leveren door Edward: perceelsgrenzen, rooilijnen, bouwvlak of andere randvoorwaarden.
- Nog aan te leveren door Edward: definitieve perceelmaat en juridische perceelgegevens indien die afwijken van de aangeleverde tekeningset.

### Buitenmaten en bouwvolume

- Rechtstreeks afgelezen tekeningmaat: structureel hoofdraster woning circa 10,50 meter noord-zuid bij 16,00 meter oost-west.
- Rechtstreeks afgelezen tekeningmaat: nokniveau volgens doorsnede circa +4,85 meter.
- Nog aan te leveren door Edward: maximale bouwhoogte of andere volumegrenzen.
- Nog aan te leveren door Edward: definitieve buitenwerkse gevelmaten wanneer die afwijken van het structurele hoofdraster.

### Verdiepingen en niveaus

- Door Edward bevestigd: één verhoogde bouwlaag.
- Rechtstreeks afgelezen tekeningmaat: hoofdvloerniveau circa +1,50 meter boven maaiveld.
- Rechtstreeks afgelezen tekeningmaat: nokniveau volgens doorsnede circa +4,85 meter.
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
- Nog aan te leveren door Edward: plaatsing, afmetingen, draairichting en type van ramen en deuren.

### Trappen en doorloopmaten

- Door Edward bevestigd: buitentrappen zijn onderdeel van het huis.
- Nog aan te leveren door Edward: doorloopmaten.
- Nog aan te leveren door Edward: vrije hoogtes, trapbreedtes of andere maatgevende eisen.

### Dak en hemelwaterafvoer

- Door Edward bevestigd: samengesteld hellend dak.
- Rechtstreeks afgelezen tekeningmaat: dakhelling circa 35 graden.
- Rechtstreeks afgelezen tekeningmaat: dakoverstek circa 1,00 meter.
- Rechtstreeks afgelezen tekeningmaat: nokniveau volgens doorsnede circa +4,85 meter.
- Nog aan te leveren door Edward: hemelwaterafvoer.
- Nog aan te leveren door Edward: nokrichtingen, dakvlakken, goten, regenpijpen en dakdetails.

### Materialen en stijl

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
- Bekend: originele bronbestanden met persoonsgegevens in titelblokken worden voorlopig niet in Git opgenomen.
- Nog aan te leveren door Edward: harde ontwerp-, maatvoerings-, perceel- en publicatie-eisen voor het definitieve huis.

### Aannames

- Bekend: het prototype is geen constructieberekening, vergunningstekening of gecertificeerd BIM-model.
- Bekend: buiten scope zonder apart besluit zijn constructieberekeningen, vergunningsstukken, gecertificeerd BIM/IFC-model, gedetailleerde installatietechniek, kostenraming en bouwoffertes.
- Bekend: de tijdelijke Fase 2-proefwoning is geen definitief huisontwerp.
- Bekend: Fase 2-proefmaten worden niet gebruikt als definitieve eisen.
- Nog aan te leveren door Edward: welke ontbrekende gegevens tijdelijk als aanname mogen worden behandeld.

### Open vragen

- Nog aan te leveren door Edward: verdere doelgroep en gebruikers van het 3D-prototype.
- Nog aan te leveren door Edward: gewenste kijkervaring en publicatiedoel.
- Nog aan te leveren door Edward: definitieve perceelmaat en eventuele juridische perceelrandvoorwaarden.
- Nog aan te leveren door Edward: exacte buitenwerkse gevelmaten wanneer die afwijken van het structurele hoofdraster.
- Nog aan te leveren door Edward: overige niveaus en exacte peilmaten indien nodig voor detaillering.
- Nog aan te leveren door Edward: gewenste netto-oppervlakten.
- Nog aan te leveren door Edward: wand-, vloer- en dakdiktes.
- Nog aan te leveren door Edward: exacte plaatsing, afmetingen, draairichting en type van ramen en deuren.
- Nog aan te leveren door Edward: exacte trappen, doorloopmaten, vrije hoogtes en trapbreedtes.
- Nog aan te leveren door Edward: hemelwaterafvoer, nokrichtingen, dakvlakken, goten, regenpijpen en dakdetails.
- Nog aan te leveren door Edward: gewenste materialen en stijl.
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
