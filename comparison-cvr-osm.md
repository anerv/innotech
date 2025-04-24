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
#T_1d66f th {
  font-weight: bold;
}
#T_1d66f .col0 {
  font-weight: bold;
}
#T_1d66f .col0 {
  font-weight: bold;
}
#T_1d66f_row0_col0, #T_1d66f_row1_col0, #T_1d66f_row1_col3, #T_1d66f_row2_col0, #T_1d66f_row3_col0, #T_1d66f_row3_col3, #T_1d66f_row4_col0, #T_1d66f_row5_col0, #T_1d66f_row5_col3, #T_1d66f_row6_col0, #T_1d66f_row7_col0, #T_1d66f_row8_col0, #T_1d66f_row8_col3, #T_1d66f_row9_col0, #T_1d66f_row9_col3, #T_1d66f_row10_col0, #T_1d66f_row11_col0, #T_1d66f_row11_col1, #T_1d66f_row12_col0, #T_1d66f_row12_col3, #T_1d66f_row13_col0, #T_1d66f_row13_col3, #T_1d66f_row14_col0, #T_1d66f_row14_col1, #T_1d66f_row15_col0, #T_1d66f_row15_col3, #T_1d66f_row16_col0, #T_1d66f_row16_col1, #T_1d66f_row17_col0, #T_1d66f_row18_col0 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_1d66f_row0_col1, #T_1d66f_row0_col2, #T_1d66f_row2_col3, #T_1d66f_row4_col3, #T_1d66f_row6_col1, #T_1d66f_row6_col2, #T_1d66f_row7_col1, #T_1d66f_row7_col2, #T_1d66f_row10_col1, #T_1d66f_row10_col2, #T_1d66f_row17_col1, #T_1d66f_row17_col2, #T_1d66f_row18_col1, #T_1d66f_row18_col2 {
  color: grey;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_1d66f_row0_col3, #T_1d66f_row1_col2, #T_1d66f_row2_col2, #T_1d66f_row3_col2, #T_1d66f_row4_col2, #T_1d66f_row5_col2, #T_1d66f_row6_col3, #T_1d66f_row7_col3, #T_1d66f_row8_col2, #T_1d66f_row9_col2, #T_1d66f_row10_col3, #T_1d66f_row11_col3, #T_1d66f_row12_col2, #T_1d66f_row13_col2, #T_1d66f_row14_col3, #T_1d66f_row15_col2, #T_1d66f_row16_col3, #T_1d66f_row17_col3, #T_1d66f_row18_col3 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_1d66f_row1_col1, #T_1d66f_row2_col1, #T_1d66f_row3_col1, #T_1d66f_row4_col1, #T_1d66f_row5_col1, #T_1d66f_row8_col1, #T_1d66f_row9_col1, #T_1d66f_row11_col2, #T_1d66f_row12_col1, #T_1d66f_row13_col1, #T_1d66f_row14_col2, #T_1d66f_row15_col1, #T_1d66f_row16_col2 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_1d66f" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_1d66f_level0_col0" class="col_heading level0 col0" >destination_type</th>
      <th id="T_1d66f_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_1d66f_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_1d66f_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_1d66f_row0_col0" class="data row0 col0" >bowling</td>
      <td id="T_1d66f_row0_col1" class="data row0 col1" >-</td>
      <td id="T_1d66f_row0_col2" class="data row0 col2" >-</td>
      <td id="T_1d66f_row0_col3" class="data row0 col3" >13.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row1_col0" class="data row1 col0" >dentist</td>
      <td id="T_1d66f_row1_col1" class="data row1 col1" >387.0</td>
      <td id="T_1d66f_row1_col2" class="data row1 col2" >400.0</td>
      <td id="T_1d66f_row1_col3" class="data row1 col3" >32.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row2_col0" class="data row2 col0" >discount_store</td>
      <td id="T_1d66f_row2_col1" class="data row2 col1" >231.0</td>
      <td id="T_1d66f_row2_col2" class="data row2 col2" >242.0</td>
      <td id="T_1d66f_row2_col3" class="data row2 col3" >-</td>
    </tr>
    <tr>
      <td id="T_1d66f_row3_col0" class="data row3 col0" >doctor-gp</td>
      <td id="T_1d66f_row3_col1" class="data row3 col1" >402.0</td>
      <td id="T_1d66f_row3_col2" class="data row3 col2" >408.0</td>
      <td id="T_1d66f_row3_col3" class="data row3 col3" >56.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row4_col0" class="data row4 col0" >doctor-specialist</td>
      <td id="T_1d66f_row4_col1" class="data row4 col1" >319.0</td>
      <td id="T_1d66f_row4_col2" class="data row4 col2" >327.0</td>
      <td id="T_1d66f_row4_col3" class="data row4 col3" >-</td>
    </tr>
    <tr>
      <td id="T_1d66f_row5_col0" class="data row5 col0" >fitness</td>
      <td id="T_1d66f_row5_col1" class="data row5 col1" >198.0</td>
      <td id="T_1d66f_row5_col2" class="data row5 col2" >200.0</td>
      <td id="T_1d66f_row5_col3" class="data row5 col3" >55.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row6_col0" class="data row6 col0" >football</td>
      <td id="T_1d66f_row6_col1" class="data row6 col1" >-</td>
      <td id="T_1d66f_row6_col2" class="data row6 col2" >-</td>
      <td id="T_1d66f_row6_col3" class="data row6 col3" >633.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row7_col0" class="data row7 col0" >golf_course</td>
      <td id="T_1d66f_row7_col1" class="data row7 col1" >-</td>
      <td id="T_1d66f_row7_col2" class="data row7 col2" >-</td>
      <td id="T_1d66f_row7_col3" class="data row7 col3" >84.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row8_col0" class="data row8 col0" >grocery_store</td>
      <td id="T_1d66f_row8_col1" class="data row8 col1" >105.0</td>
      <td id="T_1d66f_row8_col2" class="data row8 col2" >112.0</td>
      <td id="T_1d66f_row8_col3" class="data row8 col3" >3.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row9_col0" class="data row9 col0" >kindergarten</td>
      <td id="T_1d66f_row9_col1" class="data row9 col1" >201.0</td>
      <td id="T_1d66f_row9_col2" class="data row9 col2" >208.0</td>
      <td id="T_1d66f_row9_col3" class="data row9 col3" >150.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row10_col0" class="data row10 col0" >library</td>
      <td id="T_1d66f_row10_col1" class="data row10 col1" >-</td>
      <td id="T_1d66f_row10_col2" class="data row10 col2" >-</td>
      <td id="T_1d66f_row10_col3" class="data row10 col3" >50.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row11_col0" class="data row11 col0" >movie_theater</td>
      <td id="T_1d66f_row11_col1" class="data row11 col1" >25.0</td>
      <td id="T_1d66f_row11_col2" class="data row11 col2" >26.0</td>
      <td id="T_1d66f_row11_col3" class="data row11 col3" >28.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row12_col0" class="data row12 col0" >nursery</td>
      <td id="T_1d66f_row12_col1" class="data row12 col1" >13.0</td>
      <td id="T_1d66f_row12_col2" class="data row12 col2" >15.0</td>
      <td id="T_1d66f_row12_col3" class="data row12 col3" >10.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row13_col0" class="data row13 col0" >pharmacy</td>
      <td id="T_1d66f_row13_col1" class="data row13 col1" >108.0</td>
      <td id="T_1d66f_row13_col2" class="data row13 col2" >116.0</td>
      <td id="T_1d66f_row13_col3" class="data row13 col3" >75.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row14_col0" class="data row14 col0" >school</td>
      <td id="T_1d66f_row14_col1" class="data row14 col1" >308.0</td>
      <td id="T_1d66f_row14_col2" class="data row14 col2" >314.0</td>
      <td id="T_1d66f_row14_col3" class="data row14 col3" >380.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row15_col0" class="data row15 col0" >sports_facility</td>
      <td id="T_1d66f_row15_col1" class="data row15 col1" >167.0</td>
      <td id="T_1d66f_row15_col2" class="data row15 col2" >174.0</td>
      <td id="T_1d66f_row15_col3" class="data row15 col3" >91.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row16_col0" class="data row16 col0" >supermarket</td>
      <td id="T_1d66f_row16_col1" class="data row16 col1" >262.0</td>
      <td id="T_1d66f_row16_col2" class="data row16 col2" >270.0</td>
      <td id="T_1d66f_row16_col3" class="data row16 col3" >424.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row17_col0" class="data row17 col0" >swimming_hall</td>
      <td id="T_1d66f_row17_col1" class="data row17 col1" >-</td>
      <td id="T_1d66f_row17_col2" class="data row17 col2" >-</td>
      <td id="T_1d66f_row17_col3" class="data row17 col3" >158.0</td>
    </tr>
    <tr>
      <td id="T_1d66f_row18_col0" class="data row18 col0" >theatre</td>
      <td id="T_1d66f_row18_col1" class="data row18 col1" >-</td>
      <td id="T_1d66f_row18_col2" class="data row18 col2" >-</td>
      <td id="T_1d66f_row18_col3" class="data row18 col3" >30.0</td>
    </tr>
  </tbody>
</table>


### Main destination categories

<style type="text/css">
#T_900b3 th {
  font-weight: bold;
}
#T_900b3 .col0 {
  font-weight: bold;
}
#T_900b3 .col0 {
  font-weight: bold;
}
#T_900b3_row0_col0, #T_900b3_row0_col3, #T_900b3_row1_col0, #T_900b3_row1_col3, #T_900b3_row2_col0, #T_900b3_row2_col3, #T_900b3_row3_col0, #T_900b3_row3_col1, #T_900b3_row4_col0, #T_900b3_row4_col1, #T_900b3_row5_col0, #T_900b3_row5_col3 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_900b3_row0_col1, #T_900b3_row1_col1, #T_900b3_row2_col1, #T_900b3_row3_col2, #T_900b3_row4_col2, #T_900b3_row5_col1 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_900b3_row0_col2, #T_900b3_row1_col2, #T_900b3_row2_col2, #T_900b3_row3_col3, #T_900b3_row4_col3, #T_900b3_row5_col2 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_900b3" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_900b3_level0_col0" class="col_heading level0 col0" >destination_type_main</th>
      <th id="T_900b3_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_900b3_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_900b3_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_900b3_row0_col0" class="data row0 col0" >doctors</td>
      <td id="T_900b3_row0_col1" class="data row0 col1" >1108</td>
      <td id="T_900b3_row0_col2" class="data row0 col2" >1135</td>
      <td id="T_900b3_row0_col3" class="data row0 col3" >88</td>
    </tr>
    <tr>
      <td id="T_900b3_row1_col0" class="data row1 col0" >nurseries/kindergartens</td>
      <td id="T_900b3_row1_col1" class="data row1 col1" >214</td>
      <td id="T_900b3_row1_col2" class="data row1 col2" >223</td>
      <td id="T_900b3_row1_col3" class="data row1 col3" >160</td>
    </tr>
    <tr>
      <td id="T_900b3_row2_col0" class="data row2 col0" >pharmacies</td>
      <td id="T_900b3_row2_col1" class="data row2 col1" >108</td>
      <td id="T_900b3_row2_col2" class="data row2 col2" >116</td>
      <td id="T_900b3_row2_col3" class="data row2 col3" >75</td>
    </tr>
    <tr>
      <td id="T_900b3_row3_col0" class="data row3 col0" >recreation</td>
      <td id="T_900b3_row3_col1" class="data row3 col1" >390</td>
      <td id="T_900b3_row3_col2" class="data row3 col2" >400</td>
      <td id="T_900b3_row3_col3" class="data row3 col3" >1142</td>
    </tr>
    <tr>
      <td id="T_900b3_row4_col0" class="data row4 col0" >schools</td>
      <td id="T_900b3_row4_col1" class="data row4 col1" >308</td>
      <td id="T_900b3_row4_col2" class="data row4 col2" >314</td>
      <td id="T_900b3_row4_col3" class="data row4 col3" >380</td>
    </tr>
    <tr>
      <td id="T_900b3_row5_col0" class="data row5 col0" >shops</td>
      <td id="T_900b3_row5_col1" class="data row5 col1" >598</td>
      <td id="T_900b3_row5_col2" class="data row5 col2" >624</td>
      <td id="T_900b3_row5_col3" class="data row5 col3" >427</td>
    </tr>
  </tbody>
</table>


### Local heterogeneity

For all destination categories, Region Sjælland both has areas with more destinations in OSM and areas with more destinations in CVR. This pattern suggests that the two data sources not only include a different *number* of destinations, but also completely *different* observations.

#### All destinations

![Maps of all CVR and OSM destinations](results/maps/main-all-osm-cvr.png "destinations")


#### Comparison of local destination count

*Red values: More destinations in OSM. Blue: More destinations in CVR.*

![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-doctors.png "doctors")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-pharmacies.png "pharmacies")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-nurseries-kindergartens.png "nurseries/kindergartens")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-schools.png "schools")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-shops.png "shops")
![Maps comparing the local count of destinations](results/maps/hex-grid-comparison-recreation.png "recreation")


## Data consistency

### CVR

- Several CVR Penheder does not have an address ID and thus cannot be matched to an address, and some units with an address id cannot be matched to a corresponding address.
- CVR data in csv format needs some initial preprocessing to handle values (typically business names) that include the csv separator (";" or ",").
- The CVR data might include businesses that are no longer operating/open.


### OSM

- OSM tagging can be inconsistent and it is thus expected to miss some locations (e.g. grocery stores tagged with very detailed values instead of just grocery/supermarket)
- While OSM data are updated continuously and generally is up to date, there is no consistent check of whether businesses and other destinations are still open. 
