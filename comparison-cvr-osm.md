# Comparison of CVR and OSM destination data

- Large data hetereogeneity in number of destinations *and* their locations - suggests data conflation/using both data sources might be most appropriate.
- Data aggregation to a grid or by collapsing nearby destinations could speed up computation.
- CVR data has a few missing addresses/locations for all destinations categories.
- The data comparison could be improved by including more CVR codes (for fitness, libraries, theaters, ungdomsuddannelser, dagpleje, etc.) - is there a reason these are not included in the parameter list?
- Why not include dagplejer in child care (often used in rural areas instead of vuggestue)?
- There are some supermarkets and day cares (and possibly other categories) that are not in the CVR data set but searchable on the CVR website.
(Daycare: Sølyst in Jyderup; Børnehuset Elverhøj, Holbæk. Supermarkets: Supermarkets in Kirke Hvalsø)

## Data completeness

### Subcategories

- Comparison across subcategories is difficult, as the CVR categories and OSM tagging does not align - for example, OSM tagging is often more detailed for leisure than CVR, with OSM categories divided into detailed purpuses such as 'bowling' and 'swimming', while the OSM category supermarket correspond to both 'grocery store' and 'supermarket' in CVR.
- The subcategories could be made more comparable (e.g. by including libraries, theaters, and fitness centers/gyms when subsetting data from CVR).
<style type="text/css">
#T_face3 th {
  font-weight: bold;
}
#T_face3 .col0 {
  font-weight: bold;
}
#T_face3 .col0 {
  font-weight: bold;
}
#T_face3_row0_col0, #T_face3_row0_col3, #T_face3_row1_col0, #T_face3_row2_col0, #T_face3_row2_col3, #T_face3_row3_col0, #T_face3_row3_col3, #T_face3_row4_col0, #T_face3_row4_col3, #T_face3_row5_col0, #T_face3_row5_col3, #T_face3_row6_col0, #T_face3_row6_col3, #T_face3_row7_col0, #T_face3_row7_col1, #T_face3_row8_col0, #T_face3_row9_col0, #T_face3_row9_col1, #T_face3_row10_col0 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_face3_row0_col1, #T_face3_row1_col1, #T_face3_row2_col1, #T_face3_row3_col1, #T_face3_row4_col1, #T_face3_row5_col1, #T_face3_row6_col1, #T_face3_row7_col2, #T_face3_row9_col2 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_face3_row0_col2, #T_face3_row1_col2, #T_face3_row2_col2, #T_face3_row3_col2, #T_face3_row4_col2, #T_face3_row5_col2, #T_face3_row6_col2, #T_face3_row7_col3, #T_face3_row8_col3, #T_face3_row9_col3, #T_face3_row10_col3 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_face3_row1_col3, #T_face3_row8_col1, #T_face3_row8_col2, #T_face3_row10_col1, #T_face3_row10_col2 {
  color: grey;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_face3" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_face3_level0_col0" class="col_heading level0 col0" >service_type</th>
      <th id="T_face3_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_face3_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_face3_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_face3_row0_col0" class="data row0 col0" >dentist</td>
      <td id="T_face3_row0_col1" class="data row0 col1" >388.0</td>
      <td id="T_face3_row0_col2" class="data row0 col2" >400.0</td>
      <td id="T_face3_row0_col3" class="data row0 col3" >20.0</td>
    </tr>
    <tr>
      <td id="T_face3_row1_col0" class="data row1 col0" >discount_supermarket</td>
      <td id="T_face3_row1_col1" class="data row1 col1" >232.0</td>
      <td id="T_face3_row1_col2" class="data row1 col2" >237.0</td>
      <td id="T_face3_row1_col3" class="data row1 col3" >-</td>
    </tr>
    <tr>
      <td id="T_face3_row2_col0" class="data row2 col0" >doctor-gp</td>
      <td id="T_face3_row2_col1" class="data row2 col1" >401.0</td>
      <td id="T_face3_row2_col2" class="data row2 col2" >406.0</td>
      <td id="T_face3_row2_col3" class="data row2 col3" >41.0</td>
    </tr>
    <tr>
      <td id="T_face3_row3_col0" class="data row3 col0" >kindergarten</td>
      <td id="T_face3_row3_col1" class="data row3 col1" >200.0</td>
      <td id="T_face3_row3_col2" class="data row3 col2" >206.0</td>
      <td id="T_face3_row3_col3" class="data row3 col3" >153.0</td>
    </tr>
    <tr>
      <td id="T_face3_row4_col0" class="data row4 col0" >library</td>
      <td id="T_face3_row4_col1" class="data row4 col1" >56.0</td>
      <td id="T_face3_row4_col2" class="data row4 col2" >58.0</td>
      <td id="T_face3_row4_col3" class="data row4 col3" >48.0</td>
    </tr>
    <tr>
      <td id="T_face3_row5_col0" class="data row5 col0" >nursery</td>
      <td id="T_face3_row5_col1" class="data row5 col1" >14.0</td>
      <td id="T_face3_row5_col2" class="data row5 col2" >15.0</td>
      <td id="T_face3_row5_col3" class="data row5 col3" >11.0</td>
    </tr>
    <tr>
      <td id="T_face3_row6_col0" class="data row6 col0" >pharmacy</td>
      <td id="T_face3_row6_col1" class="data row6 col1" >101.0</td>
      <td id="T_face3_row6_col2" class="data row6 col2" >108.0</td>
      <td id="T_face3_row6_col3" class="data row6 col3" >75.0</td>
    </tr>
    <tr>
      <td id="T_face3_row7_col0" class="data row7 col0" >school</td>
      <td id="T_face3_row7_col1" class="data row7 col1" >308.0</td>
      <td id="T_face3_row7_col2" class="data row7 col2" >314.0</td>
      <td id="T_face3_row7_col3" class="data row7 col3" >361.0</td>
    </tr>
    <tr>
      <td id="T_face3_row8_col0" class="data row8 col0" >sports_facility</td>
      <td id="T_face3_row8_col1" class="data row8 col1" >-</td>
      <td id="T_face3_row8_col2" class="data row8 col2" >-</td>
      <td id="T_face3_row8_col3" class="data row8 col3" >88.0</td>
    </tr>
    <tr>
      <td id="T_face3_row9_col0" class="data row9 col0" >supermarket</td>
      <td id="T_face3_row9_col1" class="data row9 col1" >263.0</td>
      <td id="T_face3_row9_col2" class="data row9 col2" >269.0</td>
      <td id="T_face3_row9_col3" class="data row9 col3" >426.0</td>
    </tr>
    <tr>
      <td id="T_face3_row10_col0" class="data row10 col0" >train_station</td>
      <td id="T_face3_row10_col1" class="data row10 col1" >-</td>
      <td id="T_face3_row10_col2" class="data row10 col2" >-</td>
      <td id="T_face3_row10_col3" class="data row10 col3" >73.0</td>
    </tr>
  </tbody>
</table>


### Main destination categories

<style type="text/css">
#T_aa6bb th {
  font-weight: bold;
}
#T_aa6bb .col0 {
  font-weight: bold;
}
#T_aa6bb .col0 {
  font-weight: bold;
}
#T_aa6bb_row0_col0, #T_aa6bb_row0_col3, #T_aa6bb_row1_col0, #T_aa6bb_row1_col3, #T_aa6bb_row2_col0, #T_aa6bb_row2_col3, #T_aa6bb_row3_col0, #T_aa6bb_row3_col3, #T_aa6bb_row4_col0, #T_aa6bb_row4_col1, #T_aa6bb_row5_col0, #T_aa6bb_row5_col1, #T_aa6bb_row6_col0, #T_aa6bb_row6_col3, #T_aa6bb_row7_col0 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_aa6bb_row0_col1, #T_aa6bb_row1_col1, #T_aa6bb_row2_col1, #T_aa6bb_row3_col1, #T_aa6bb_row4_col2, #T_aa6bb_row5_col2, #T_aa6bb_row6_col1 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_aa6bb_row0_col2, #T_aa6bb_row1_col2, #T_aa6bb_row2_col2, #T_aa6bb_row3_col2, #T_aa6bb_row4_col3, #T_aa6bb_row5_col3, #T_aa6bb_row6_col2, #T_aa6bb_row7_col3 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_aa6bb_row7_col1, #T_aa6bb_row7_col2 {
  color: grey;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_aa6bb" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_aa6bb_level0_col0" class="col_heading level0 col0" >service_type_main</th>
      <th id="T_aa6bb_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_aa6bb_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_aa6bb_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_aa6bb_row0_col0" class="data row0 col0" >dentist</td>
      <td id="T_aa6bb_row0_col1" class="data row0 col1" >388.0</td>
      <td id="T_aa6bb_row0_col2" class="data row0 col2" >400.0</td>
      <td id="T_aa6bb_row0_col3" class="data row0 col3" >20</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row1_col0" class="data row1 col0" >doctor</td>
      <td id="T_aa6bb_row1_col1" class="data row1 col1" >401.0</td>
      <td id="T_aa6bb_row1_col2" class="data row1 col2" >406.0</td>
      <td id="T_aa6bb_row1_col3" class="data row1 col3" >41</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row2_col0" class="data row2 col0" >nursery/kindergarten</td>
      <td id="T_aa6bb_row2_col1" class="data row2 col1" >214.0</td>
      <td id="T_aa6bb_row2_col2" class="data row2 col2" >221.0</td>
      <td id="T_aa6bb_row2_col3" class="data row2 col3" >164</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row3_col0" class="data row3 col0" >pharmacy</td>
      <td id="T_aa6bb_row3_col1" class="data row3 col1" >101.0</td>
      <td id="T_aa6bb_row3_col2" class="data row3 col2" >108.0</td>
      <td id="T_aa6bb_row3_col3" class="data row3 col3" >75</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row4_col0" class="data row4 col0" >recreation</td>
      <td id="T_aa6bb_row4_col1" class="data row4 col1" >56.0</td>
      <td id="T_aa6bb_row4_col2" class="data row4 col2" >58.0</td>
      <td id="T_aa6bb_row4_col3" class="data row4 col3" >136</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row5_col0" class="data row5 col0" >school</td>
      <td id="T_aa6bb_row5_col1" class="data row5 col1" >308.0</td>
      <td id="T_aa6bb_row5_col2" class="data row5 col2" >314.0</td>
      <td id="T_aa6bb_row5_col3" class="data row5 col3" >361</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row6_col0" class="data row6 col0" >shop</td>
      <td id="T_aa6bb_row6_col1" class="data row6 col1" >495.0</td>
      <td id="T_aa6bb_row6_col2" class="data row6 col2" >506.0</td>
      <td id="T_aa6bb_row6_col3" class="data row6 col3" >426</td>
    </tr>
    <tr>
      <td id="T_aa6bb_row7_col0" class="data row7 col0" >train_station</td>
      <td id="T_aa6bb_row7_col1" class="data row7 col1" >-</td>
      <td id="T_aa6bb_row7_col2" class="data row7 col2" >-</td>
      <td id="T_aa6bb_row7_col3" class="data row7 col3" >73</td>
    </tr>
  </tbody>
</table>



### Local heterogeneity

For all destination categories, Region Sjælland both has areas with more destinations in OSM and areas with more destinations in CVR. This pattern suggests that the two data sources not only include a different *number* of destinations, but also completely *different* observations.

#### All destinations

![Maps of all CVR and OSM destinations](results/maps/main-all-osm-cvr.png "destinations")


#### Comparison of local destination count

*Red values: More destinations in OSM. Blue: More destinations in CVR.*

![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-doctor.png "doctors")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-dentist.png "dentist")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-pharmacy.png "pharmacies")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-nursery-kindergarten.png "nurseries/kindergartens")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-school.png "schools")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-shop.png "shops")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-recreation.png "recreation")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-train_station.png "train stations")

## Data consistency

### CVR

- Several CVR Penheder does not have an address ID and thus cannot be matched to an address, and some units with an address id cannot be matched to a corresponding address.
- CVR data in csv format needs some initial preprocessing to handle values (typically business names) that include the csv separator (";" or ",").
- The CVR data might include businesses that are no longer operating/open.


### OSM

- OSM tagging can be inconsistent and it is thus expected to miss some locations (e.g. grocery stores tagged with very detailed values instead of just grocery/supermarket)
- While OSM data are updated continuously and generally is up to date, there is no consistent check of whether businesses and other destinations are still open. 
