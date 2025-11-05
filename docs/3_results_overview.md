## Oversigt over resultater :white_check_mark:

- ``/results/maps/`` indeholder kort med rejse- og ventetider til alle destinationer.
- ``/results/plots/`` indeholder visualiseringer af rejse- og ventetider til alle destinationer.

- ``/results/data/`` indeholder ``[service]_access_summary`` (csv og html) med opsummerende statistikker for rejsetider til alle destinationer, samt tre parquet-filer per destination: ``[destination]_[nummer]_[ankomsttid]_otp.parquet``, ``[destination]_[nummer]_[ankomsttid]_otp_geo.parquet`` og ``[destination]_[nummer]_[ankomsttid]_addresses_otp_geo.parquet``. 

    Destination = navn på destinationstype, f.eks. 'dentist'; nummer angiver om destinationen er den nærmeste, næst-nærmeste, etc. i tilfælde af at rejsetiden beregnes til mere end én destination i hver kategori.


> **_OBS:_** Hvis analysen er indstillet til at filtrere resultater for gåafstand og/eller ventetid vil **_otp_geo** og **_addresses_otp_geo** adresser, hvor gåafstand/ventetid overskrider de fastsatte værdier have 'NaN' som værdi for duration, transfers, ventetid m.m., og altså fremgå som om der ikke er en forbindelse. **_otp_** filerne indeholder det fulde resultatsæt fra OTP og inkluderer også rejsetider m.m. for ture der overskrider værdier for ventetid og gåafstand.

### [destination]_[nummer]_otp.parquet

| Attribut | Indhold |
| - | - |
| source_id | Adresse-id på startpunktet |
| target_id | Adresse-id på slutpunktet (destinationen) |
| from_lat | Koordinat på startpunktet (latitude) |
| from_lon | Koordinat på slutpunktet (longitude) |
| startTime | Afgangstid |
| waitingTime | Ventetid i løbet af turen (sekunder) |
| duration | Rejsetid i sekunder |
| walkDistance | Gåafstand (meter), målt i afstand langs med vejnettet |
| abs_dist | Afstand mellem start og slutpunkter (meter), målt i fugleflugtafstand |
| mode_duration_json | Rejsetid for hvert transportmiddel (sek.) |

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
| transfers | Antal skift |
| bus_duration | Rejsetid med bus  (min) |
| rail_duration | Rejsetid med tog  (min) |
| walk_duration | Rejsetid gang  (min)|
| geometry | Punktgeometri for startpunktet |


### [destination]_[nummer]_addresses_otp_geo.

Indeholder samme attributter som _otp_geo, men knyttet til *adressegeometrier*, i stedet for geometri for startpunktet/adgangspunktet.