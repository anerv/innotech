# Vejledning

Guiden indeholder en vejledning til at installere og downloade alle nødvendige programmer og datasæt, samt en kort vejledning til at køre analysen. 

Se ***[LINK TIL RAPPORT]*** for baggrund for projektet og en detaljeret oversigt over datakilder og databehandling.

## Installation :computer:

Modellen kan *enten* installeres manuelt (metode A) eller ved hjælp af Docker (metode B).
Modellen og installationsvejledningen er udviklet på Windows 11, Intel(R) Core(TM) Ultra 5 125U.


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
pip install --use-pep517 -e .
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

***TODO: Should this be included/after docker option?***

### B. Installation med Docker

***MANGLER***

#### B1. Installer Docker Desktop

#### B2. 

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

**1.** Naviger til mappen ``/otp`` (ligger i hovedmappen for repository ``innotech``).

**2.** Kør kommandoen ```java -Xmx2G -jar otp-shaded-2.7.0.jar --load .``` for at starte OpenTripPlanner.

- Tjek eventuelt http://localhost:8080/ i din browser for at bekræfte, at OpenTripPlanner er startet korrekt.

**3.** Kør script ``B_run_otp.py`` (i mappen ``/run``).

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

