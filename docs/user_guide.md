
## Anvendelse

### 1. Opdater indstillinger :pencil2:

``config.yml`` indeholder bl.a. filnavne og placeringer på inputdata og resultater, navnet på studieområdet, samt indstillinger for, visse destinationer analysen indholder.
Hvis andre destinationer, ankomsttider, inputdata, m.m. ønskes opdateres de her.

``build-config.json`` indeholder indstillinger for OpenTripPlanner. Opdater kun, hvis studieområdet er i anden anden tidszone end Danmark eller hvis et andet NeTEx-datasæt anvendes.

***TODO: INKLUDER CONFIG FOR OTP rejsetidsberegning***


### 2. Generer inputdata :arrows_counterclockwise:

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
java -Xmx2G -jar "the name of your otp.jar file" --load .
```

##### Hvis du bruger Docker-installation:

* Åben en ny terminal

* Naviger til undermappen ``otp``:

```bash
cd innotech/otp
```

* Kør kommandoerne:

```bash
docker exec -it innotech-container bash
java -Xmx2G -jar otp.jar --load .
```

- Tjek eventuelt http://localhost:8080/ i din browser for at bekræfte, at OpenTripPlanner er startet korrekt.

**B.** Kør notebook ``B_run_otp.ipynb`` (i mappen ``/run``).

- For et område som Region Sjælland med standard-indstillinger vil det tage 8+ timer at køre analysen på en almindelig laptop (testet på  Windows 11, Intel(R) Core(TM) Ultra 5 125U, 32 GB ram)


### 4. Processer resultater :bar_chart:

- Kør notebook ``C_process_results.ipynb`` (i mappen ``/run``) for at eksportere og opsummere resultaterne på rejsetider.
 
### Sammenlign datakilder [valgfri] :arrow_right::arrow_left:

- Data på destinationer stammer både fra det danske CVR-register og OpenStreetMap. For en sammenligning af det to datakilder for hver destinationstype, kør notebook ``D00_compare_cvr_osm.ipynb`` (i mappen ``/scripts``). Resultaterne af sammenligningen findes i ``/results/destination_data_evaluation/``.

Se ``results_overview.md`` for en oversigt over, hvilke typer resultater analysen producerer.

