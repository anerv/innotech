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

#### B4. Anvend Python environment

##### Med JupyterLab:

* Åben et browservindue og gå til http://localhost:8888
* Brug den præ-indstillede Python kernel i Jupyter-lab vinduet til at køre analysen (se anvendelsesguiden nedenfor)

##### Med Visual Studio Code

* Åben Visual Studio Code

* Installer *Remote - Containers*-udvidelsen.

* Åben *Command Palette* (`Ctrl+Shift+P` eller `Cmd+Shift+P`) og vælg: ``Remote-Containers: Attach to Running Container...``

* Vælg den aktive container `innotech-env`.

* Inden i ``innotech-enc`` workspace, vælg Python interpreteren ``Python (innotech)``.

* Herfra kan analysen køres (se anvendelsesguiden nedenfor).


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


## Anvendelse

### 1. Opdater indstillinger :pencil2:

``config.yml`` indeholder bl.a. filnavne og placeringer på inputdata og resultater, navnet på studieområdet, samt indstillinger for, visse destinationer analysen indholder.
Hvis andre destinationer, ankomsttider, inputdata, m.m. ønskes opdateres de her.

``build-config.json`` indeholder indstillinger for OpenTripPlanner. Opdater kun, hvis studieområdet er i anden anden tidszone end Danmark eller hvis et andet NeTEx-datasæt anvendes.

***TODO: INKLUDER CONFIG FOR OTP rejsetidsberegning***


### 2. Generer inputdata :arrows_counterclockwise:

- Kør script ``A_prepare_data.py`` (i mappen ``/run``).
Dette script kører en række sub-scripts der klargør input-data og bygger en ``graph.obj`` fil, der senere anvendes i OpenTripPlanner.

### 3. Beregn rejsetider :bus:

**A.** Start OpenTripPlanner:

##### Hvis du har fulgt den manuelle installationsguide:

* Naviger til undermappen ``otp``:

```bash
cd otp
```

* Kør kommandoen:
```bash
java -Xmx2G -jar otp-shaded-2.7.0.jar --load .
```

##### Hvis du bruger Docker-installation:

* Naviger til hovedmappen ``innotech``

* Kør kommandoen:

```bash
java -Xmx2G -jar /usr/src/app/otp-shaded-2.6.0.jar --load .
```

- Tjek eventuelt http://localhost:8080/ i din browser for at bekræfte, at OpenTripPlanner er startet korrekt.

**B.** Kør script ``B_run_otp.py`` (i mappen ``/run``).

- For et område som Region Sjælland med standard-indstillinger vil det tage 8+ timer at køre analysen på en almindelig laptop (testet på  Windows 11, Intel(R) Core(TM) Ultra 5 125U, 32 GB ram)


### 4. Processer resultater :bar_chart:

- Kør script ``C_process_results.py`` (i mappen ``/run``) for at eksportere og opsummere resultaterne på rejsetider.
 
### Sammenlign datakilder [valgfri] :arrow_right::arrow_left:

- Data på destinationer stammer både fra det danske CVR-register og OpenStreetMap. For en sammenligning af det to datakilder for hver destinationstype, kør script ``D00_compare-cvr-osm.py`` (i mappen ``/scripts``). Resultaterne af sammenligningen findes i ``/results/destination_data_evaluation/``.


## Oversigt over resultater :white_check_mark:

- ``/results/maps/`` indeholder illustrationer af rejse- og ventetider til alle destinationer.
- ``/results/data/`` indeholder ``service_access_summary`` (csv og html) med opsummerende statistikker for rejsetider til alle destinationer, samt to parquet-filer per destination: ``[destination]_[nummer]_otp.parquet`` og ``[destination]_[nummer]_otp_geo.parquet``. Destination = navn på destinationstype, f.eks. 'dentist'; nummer angiver om destinationen er den nærmeste, næst-nærmeste, etc. i tilfælde af at rejsetiden beregnes til mere end én destination i hver kategori.


### [destination]_[nummer]_otp.parquet

| Attribut | Indhold |
| - | - |
| source_id | Adresse-id på startpunktet |
| target_id | Adresse-id på slutpunktet (destinationen) |
| startTime | Afgangstid |
| from_lat | Koordinat på startpunktet (latitude) |
| from_lon | Koordinat på slutpunktet (longitude) |
| waitingTime | Ventetid i løbet af turen (sekunder) |
| duration | Rejsetid i sekunder |
| walkDistance | Gåafstand (meter), målt i afstand langs med vejnettet |
| abs_dist | Afstand mellem start og slutpunkter (meter), målt i fugleflugtafstand |

### [destination]_[nummer]_otp_geo.parquet


| Attribut | Indhold |
| - | - |
| source_id | Adresse-id på startpunktet |
| target_id | Adresse-id på slutpunktet (destinationen) |
| startTime | Afgangstid |
| arrival_time | Ankomsttid |
| waitingTime | Ventetid i løbet af turen |
| walkDistance | Gåafstand (meter), målt i afstand langs med vejnettet |
| abs_dist | Afstand mellem start og slutpunkter (meter), målt i fugleflugtafstand |
| duration_min | Rejsetid i minutter |
| wait_time_dest_min | Ventetid på destinationen i minutter |
| total_time_min | Samlet tid (rejse + ventetid) i minutter |
| only_walking | Om turen udelukkende består af gang (sandt/falsk) |
| geometry | Punktgeometri for startpunktet |

