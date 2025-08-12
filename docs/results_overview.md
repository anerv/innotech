## Oversigt over resultater :white_check_mark:

- ``/results/maps/`` indeholder illustrationer af rejse- og ventetider til alle destinationer.
- ``/results/data/`` indeholder ``service_access_summary`` (csv og html) med opsummerende statistikker for rejsetider til alle destinationer, samt to parquet-filer per destination: ``[destination]_[nummer]_otp.parquet`` og ``[destination]_[nummer]_otp_geo.parquet``. Destination = navn på destinationstype, f.eks. 'dentist'; nummer angiver om destinationen er den nærmeste, næst-nærmeste, etc. i tilfælde af at rejsetiden beregnes til mere end én destination i hver kategori.


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
| bus_duration | Rejsetid med bus |
| rail_duration | Rejsetid med tog |
| walk_duration | Rejsetid gang |
| geometry | Punktgeometri for startpunktet |