# Vejledning

Guiden indeholder en vejledning til at installere og downloade alle nødvendige programmer og datasæt, samt en kort vejledning til at køre analysen.

Se [LINK TIL RAPPORT] for baggrund for projektet og en detaljeret oversigt over datakilder og databehandling.

## Installation :computer:

XX-modellen kan *enten* installeres manuelt (metode A) eller ved hjælp af Docker (metode B).

### A. Manuel installation

Projektet kræver at følgende programmer og værktøjer er installeret:

- *DuckDB*
- *OpenTripPlanner*
- *Osmium*
- *Innotech Conda environment*
- *Python**
- *Jupyter**
- *Conda**
- *pip**
- *git**
- *Java 21**

*Guiden antager at værktøjer markeret med * allerede er installeret.

For at installere de resterende værktøjer køres nedenstående i et terminalvindue:

#### A1. Klon GitHub repository

````bash
git clone -b main --single-branch https://github.com/anerv/innotech --depth 1
````

#### A2. Skab Conda environment
```bash
conda create -n innotech geopandas pyyaml pyarrow overpy contextily scikit-learn h3-py python-duckdb ipykernel osmium-tool
```

*ELLER*

```bash
conda env create -f environment.yml
```


#### A3. Aktiver Conda environment og installer sidste elementer
````bash
conda activate innotech
pip install matplotlib-scalebar
pip install -e .
````

#### A4. Installer DuckDB
````bash
winget install DuckDB.cli
````

#### A5. Installer OpenTripPlanner

Følg instruktionerne for installation af OpenTripPlanner (OTP) her: https://docs.opentripplanner.org/en/dev-2.x/Basic-Tutorial/.

#### A6. Klargør mapper til data og resultater

Naviger til hovedmappen (``innotech``) i en terminal og kør:

````bash
python setup_folders.py
````

***Should this be included/after docker option?***

### B. Installation med Docker

***MANGLER***

## Inputdata :globe_with_meridians:

Grundelementerne i tilgængelighedsanalysen er data på husstandsadresser og destinationer samt data på vejnetværket og offentlig transport.

### Destinationer og adresser

- Adresse-data fra DAR (adresser, husnumre, og adressepunkter) for den ønskede region.
- BBR-data (enheder) for den ønskede region: 
- CVR-data (produktionsenheder, CVR-enheder med brancher, og CVR-enheder med adresser) for den ønskede region.
- Afgrænsning af studieområdet (data med danske administrative områder (regioner eller kommuner). Opdater config.yml hvis et andet område end Region Sjælland ønskes.). 

Alle data kan downloades fra Datafordeler.dk.

Se ``config.yml`` for forventede filnavne og placeringer.

For en oversigt over dataspecifikationer og databehandling, se modelbeskrivelsen her: LINK TIL RAPPORT.

***Inkluder input-data i Docker???***

### Inputdata til OTP

- OpenStreetMap: A pbf-file for det pågældende land, downloadet fra eksempelvis https://download.geofabrik.de/.

- NeTEx rejseplansdata: I Danmark kan rejseplansdata i NeTEx-formattet downloades fra det Nationale Access Point: https://du-portal-ui.dataudveksler.app.vd.dk/data/242/overview.


## Anvendelse

### 1. Opdater config.yml

MANGLER

### 2. Generer inputdata

MANGLER

nævn graf

### 3. Beregn rejsetider.

MANGLER

- localhost, etc (se todo)
- advar om langsom process

### 4. Analyser resultater

MANGLER

- forklar kolonne navne og indhold

### Sammenlign datakilder [valgfri]