
## Anvendelse

> **_OBS:_**  De danske NeTEx-data indeholder ikke rute/rejsetidsdata for færgeforbindelser. Rejsetidsberegninger for ikke-brofaste øer fungerer derfor kun internt på øerne og ikke mellem øer og fastland.

> **_OBS:_**  Hvis OTP returnerer *(StreetIndex.java:405) Couldn't link (10.969541647227851, 55.330497255524456, NaN)* kan det skyldes, at enten start- eller slutadressen ikke kan forbindes til vejnettet og der derfor ikke kan beregnes en rute.

### 1. Opdater indstillinger :pencil2:

* ``config.yml`` indeholder bl.a. filnavne og placeringer på inputdata og resultater, navnet på studieområdet, samt indstillinger for, visse destinationer analysen indholder.
Hvis andre destinationer, ankomsttider, inputdata, m.m. ønskes opdateres de her. 

    Brug evt. script ```test/tune_otp_settings.py``` til at teste effekten af ankomsttid m.m.

* ``build-config.json`` indeholder indstillinger for OpenTripPlanner. Opdater kun, hvis studieområdet er i anden anden tidszone end Danmark eller hvis et andet NeTEx-datasæt anvendes.

* Hvis specifikke indstillinger for ruteberegningen ønskes (f.eks. max antal skift, vægtning af ventetid vs. rejsetid, adgang for kørestole etc.) tilføjes en ``router-config.json`` til ``otp``-mappen. Se https://docs.opentripplanner.org/en/latest/RouteRequest/ for eksempel.


### 2. Generer inputdata :arrows_counterclockwise:

> **_OBS:_** Husk at anvende innotech Python environment (manuel installation) eller at starte Docker containeren og vælge ``Python (innotech)`` Jupyter Server (installation med Docker), før du går i gang. Se installationsvejledningen for detaljerede instruktioner.

- Kør notebook ``A_prepare_data.ipynb`` (i mappen ``/run``).
Denne notebook kører en række sub-scripts der klargør input-data og bygger en ``graph.obj`` fil, der senere anvendes i OpenTripPlanner.

### 3. Beregn rejsetider :bus:

**A.** Start OpenTripPlanner:

##### Hvis du har fulgt den manuelle installationsguide:

* Naviger til undermappen ``otp``:

```bash
cd innotech/otp
```

* Kør kommandoen:
```bash
java -Xmx2G -jar otp.jar --load .
```

##### Hvis du bruger Docker-installation:

* Åben en ny terminal

* Kør kommandoen:

```bash
docker exec -it innotech-container bash
```

* Naviger til undermappen ``otp``:

```bash
cd innotech/otp
```

* Kør kommandoen:

```bash
java -Xmx2G -jar otp.jar --load .
```

- Tjek eventuelt http://localhost:8080/ i din browser for at bekræfte, at OpenTripPlanner er startet korrekt.

**B.** Kør notebook ``B_run_otp.ipynb`` (i mappen ``/run``).

- For et område som Region Sjælland med standard-indstillinger vil det tage 8+ timer at køre analysen på en almindelig laptop (testet på  Windows 11, Intel(R) Core(TM) Ultra 5 125U, 32 GB ram)
- Efter at notebook B er kørt successfuldt kan resultaterne findes i mappen ``results``: Se [results_overview](results_overview.md) for en oversigt over output fra analysen.

 
### Sammenlign datakilder [valgfri] :arrow_right::arrow_left:

- Data på destinationer stammer både fra det danske CVR-register og OpenStreetMap. For en sammenligning af det to datakilder for hver destinationstype, kør notebook ``C00_compare_cvr_osm.ipynb`` (i mappen ``/scripts``). Resultaterne af sammenligningen findes i ``/results/destination_data_evaluation/``.

Se ``results_overview.md`` for en oversigt over, hvilke typer resultater analysen producerer.

