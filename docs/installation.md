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
git clone -b main --single-branch https://github.com/anerv/innotech --depth 1
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

***

### B. Installation med Docker

* Kræver en installation af [Git](https://git-scm.com/downloads) og (valgfrit) [Visual Studio Code](https://code.visualstudio.com/) med *Remote - Containers* udvidelsen.

#### B1. Installer Docker Desktop

* Installer Docker Desktop fra: https://docs.docker.com/desktop/setup/install/windows-install/
* Start Docker Desktop

#### B2. Download Docker image

* Download docker imaget fra Docker Hub:

```bash
docker pull your-dockerhub-username/otp-python-env:latest
```

#### B3. Kør Docker container

* Kør Docker containeren:

```bash
docker run -it --rm -p 8888:8888 -p 8080:8080 -v "$(pwd)":/home/jovyan/work innotech-env:local
```

#### B4. Anvend Docker Python environment

##### Med JupyterLab:

* Åben et browservindue og gå til http://localhost:8888
* Brug den præ-indstillede Python kernel i Jupyter-lab vinduet til at køre analysen (se anvendelsesguiden ``analysis_guide.md``).

##### Med Visual Studio Code

* Åben Visual Studio Code

* Installer *Remote - Containers*-udvidelsen.

* Åben *Command Palette* (`Ctrl+Shift+P` eller `Cmd+Shift+P`) og vælg: ``Remote-Containers: Attach to Running Container...``

* Vælg den aktive container `innotech-env`.

* Inden i ``innotech-enc`` workspace, vælg Python interpreteren ``Python (innotech)``.

* Herfra kan analysen køres (se anvendelsesguiden ``analysis_guide.md``).


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

***TODO: Inkluder input-data i Docker???***

### Inputdata til OTP :globe_with_meridians:

- OpenStreetMap: A pbf-file for det pågældende land, downloadet fra eksempelvis https://download.geofabrik.de/.

- NeTEx rejseplansdata: I Danmark kan rejseplansdata i NeTEx-formattet downloades fra det Nationale Access Point: https://du-portal-ui.dataudveksler.app.vd.dk/data/242/overview.


Se [anvendelsesguiden](user_guide.md) for instruktioner til at køre analysen.

