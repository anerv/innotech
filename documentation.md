# Dokumentation

## Installation

XX-modellen kan *enten* installeres manuelt eller ved hjælp af Docker.

### Manuel installation

Projektet kræver at følgende programmer og værktøjer er installeret:

- DuckDB
- OpenTripPlanner
- Osmium
- Innotech Conda environment
- Python*
- Jupyter*
- Conda*
- pip*
- git*
- Java 21*

*Guiden antager at værktøjer markeret med * allerede er installeret.

For at installere de resterende værktøjer køres nedenstående i et terminalvindue:

#### Klon GitHub repository

````bash
git clone -b main --single-branch https://github.com/anerv/innotech --depth 1
````

### Skab Conda environment
```bash
conda create -n innotech geopandas pyyaml pyarrow overpy contextily scikit-learn h3-py python-duckdb ipykernel osmium-tool
```

*ELLER*

```bash
conda env create -f environment.yaml
```


#### Aktiver Conda environment og installer sidste elementer
````bash
conda activate innotech
pip install matplotlib-scalebar
pip install -e .
````

### Installer DuckDB
````bash
winget install DuckDB.cli
````

### Installer OpenTripPlanner

Følg instruktionerne for installation af OpenTripPlanner (OTP) her: https://docs.opentripplanner.org/en/dev-2.x/Basic-Tutorial/.

### Klargør mapper til data og resultater

Naviger til hovedmappen (``innotech``) i en terminal og kør:

````bash
python setup_folders.py
````

## Installation med Docker

***MANGLER***

## Inputdata

Grundelementerne i tilgængelighedsanalysen er data på husstandsadresser og destinationer, samt data på vejnetværket og offentlig transport, til brug i OTP.

### Destinationer og adresser

- Adresse-data fra DAR (adresser, husnumre, og adressepunkter) for den ønskede region.
- BBR-data (enheder) for den ønskede region: 
- CVR-data (produktionsenheder, CVR-enheder med brancher, og CVR-enheder med adresser) for den ønskede region.
- Afgrænsning af studieområdet (data med danske administrative områder (regioner eller kommuner). Opdater config.yml hvis et andet område end Region Sjælland ønskes.). 

Alle data kan downloades fra Datafordeler.dk.

Se config.yml for forventede filnavne og placeringer.

For en oversigt over dataspecifikationer og databehandling, se modelbeskrivelsen her: LINK TIL RAPPORT.

***Inkluder input-data i Docker???***

### Inputdata til OTP

- OpenStreetMap: A pbf-file for det pågældende land, downloadet fra eksempelvis https://download.geofabrik.de/.

- NeTEx rejseplansdata: I Danmark kan rejseplansdata i NeTEx-formattet downloades fra det Nationale Access Point: https://du-portal-ui.dataudveksler.app.vd.dk/data/242/overview.


## Anvendelse

### Opdater config.yml

For at køre XX-modellen køres alle py-scripts i mappen ``scripts`` i alfanumerisk rækkefølge.

### Generer inputdata

### Kør OTP

- graf, localhost, etc (se todo)

### Analyser resultater


- forklar kolonne navne og indhold