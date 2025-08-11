# Vejledning

Guiden indeholder en vejledning til at installere og downloade alle nødvendige programmer og datasæt, samt en kort vejledning til at køre analysen. 

Se ***[LINK TIL RAPPORT]*** for baggrund for projektet og en detaljeret oversigt over datakilder og databehandling.

## Installation :computer:

Modellen kan *enten* installeres manuelt (metode A) eller ved hjælp af Docker (metode B).
Modellen og installationsvejledningen er udviklet på Windows 11, Intel(R) Core(TM) Ultra 5 125U.

***

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

*Guiden til manuel installation antager at værktøjer markeret med * allerede er installeret.

For at installere de resterende værktøjer køres nedenstående i et terminalvindue:

#### A1. Klon GitHub repository

````bash
git clone https://github.com/anerv/innotech
cd innotech
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
pip install --use-pep517 -e .
````

#### A4. Installer DuckDB
````bash
winget install DuckDB.cli
````

#### A5. Installer OpenTripPlanner

Følg instruktionerne for installation af OpenTripPlanner (OTP) her: https://docs.opentripplanner.org/en/dev-2.x/Basic-Tutorial/.

OTP-programmet skal placeres i ``otp``-mappen, eksempelvis:
``innotech/otp/otp-shaded-2.7.0.jar``.

#### A6. Klargør mapper til data og resultater

Naviger til hovedmappen (``innotech``) i en terminal, hvis du ikke allerede har gjort det, og kør:

````bash
python setup_folders.py
````

#### A7. Anvend Python-environment

* Åben den første notebook (se anvendelsesguiden ``user_guide.md``) i din Python IDE (f.eks. Visual Studio Code).
* Brug conda environment ``innotech`` som Python interpreter.


***

### B. Installation med Docker

* Kræver en installation af [Git](https://git-scm.com/downloads).

#### B1. Klon GitHub repository

````bash
git clone https://github.com/anerv/innotech
cd innotech
````

#### B2. Installer Docker Desktop

* Installer Docker Desktop fra: https://docs.docker.com/desktop/setup/install/windows-install/
* Start Docker Desktop

#### B3. Download Docker image

* Download docker imaget fra Docker Hub:

```bash
docker pull anerv/innotech-env:latest
```

#### B4. Kør Docker container

* Naviger til hovedmappen (``innotech``) i en terminal, hvis du ikke allerede har gjort det.

* Kør Docker containeren:

```bash
docker run -it --name innotech-container -p 8888:8888 -p 8080:8080 -v ${PWD}:/home/jovyan/work anerv/innotech-env:latest
```

#### B5. Anvend Docker Python environment

* Åben et browservindue og gå til http://localhost:8888
* Kør analysen (se anvendelsesguiden ``user_guide.md``), brug ``Python Innotech`` som kernel.


## Inputdata :file_folder:

Grundelementerne i tilgængelighedsanalysen er data på husstandsadresser og destinationer samt data på vejnetværket og offentlig transport.

### Destinationer og adresser :house:

- Adresse-data fra DAR (adresser, husnumre, og adressepunkter) for den ønskede region.
- BBR-data (enheder) for den ønskede region: 
- CVR-data (produktionsenheder, CVR-enheder med brancher, og CVR-enheder med adresser) for den ønskede region.
- Afgrænsning af studieområdet (data med danske administrative områder (regioner eller kommuner). Opdater config.yml hvis et andet område end Region Sjælland ønskes.). 

Alle data kan downloades fra Datafordeler.dk.

Se ``config.yml`` for forventede filnavne og placeringer.

For en oversigt over dataspecifikationer og databehandling, se modelbeskrivelsen her: LINK TIL RAPPORT.


### Inputdata til OTP :globe_with_meridians:

- OpenStreetMap: A pbf-file for det pågældende land, downloadet fra eksempelvis https://download.geofabrik.de/.

- NeTEx rejseplansdata: I Danmark kan rejseplansdata i NeTEx-formattet downloades fra det Nationale Access Point: https://du-portal-ui.dataudveksler.app.vd.dk/data/242/overview.


Se [anvendelsesguiden](user_guide.md) for instruktioner til at køre analysen.

