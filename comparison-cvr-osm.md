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
#T_12e17 th {
  font-weight: bold;
}
#T_12e17 .col0 {
  font-weight: bold;
}
#T_12e17 .col0 {
  font-weight: bold;
}
#T_12e17_row0_col0, #T_12e17_row0_col3, #T_12e17_row1_col0, #T_12e17_row2_col0, #T_12e17_row2_col3, #T_12e17_row3_col0, #T_12e17_row3_col3, #T_12e17_row4_col0, #T_12e17_row4_col3, #T_12e17_row5_col0, #T_12e17_row5_col3, #T_12e17_row6_col0, #T_12e17_row6_col3, #T_12e17_row7_col0, #T_12e17_row8_col0, #T_12e17_row9_col0, #T_12e17_row10_col0 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_12e17_row0_col1, #T_12e17_row0_col2, #T_12e17_row1_col1, #T_12e17_row1_col2, #T_12e17_row2_col1, #T_12e17_row2_col2, #T_12e17_row3_col1, #T_12e17_row3_col2, #T_12e17_row4_col1, #T_12e17_row4_col2, #T_12e17_row5_col1, #T_12e17_row5_col2, #T_12e17_row6_col1, #T_12e17_row6_col2 {
  background-color: yellow;
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_12e17_row1_col3, #T_12e17_row8_col1, #T_12e17_row8_col2, #T_12e17_row10_col1, #T_12e17_row10_col2 {
  color: grey;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_12e17_row7_col1, #T_12e17_row7_col2, #T_12e17_row9_col1, #T_12e17_row9_col2 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_12e17_row7_col3, #T_12e17_row8_col3, #T_12e17_row9_col3, #T_12e17_row10_col3 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_12e17" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_12e17_level0_col0" class="col_heading level0 col0" >service_type</th>
      <th id="T_12e17_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_12e17_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_12e17_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_12e17_row0_col0" class="data row0 col0" >dentist</td>
      <td id="T_12e17_row0_col1" class="data row0 col1" >397.0</td>
      <td id="T_12e17_row0_col2" class="data row0 col2" >397.0</td>
      <td id="T_12e17_row0_col3" class="data row0 col3" >20.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row1_col0" class="data row1 col0" >discount_supermarket</td>
      <td id="T_12e17_row1_col1" class="data row1 col1" >250.0</td>
      <td id="T_12e17_row1_col2" class="data row1 col2" >250.0</td>
      <td id="T_12e17_row1_col3" class="data row1 col3" >-</td>
    </tr>
    <tr>
      <td id="T_12e17_row2_col0" class="data row2 col0" >doctor-gp</td>
      <td id="T_12e17_row2_col1" class="data row2 col1" >419.0</td>
      <td id="T_12e17_row2_col2" class="data row2 col2" >419.0</td>
      <td id="T_12e17_row2_col3" class="data row2 col3" >41.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row3_col0" class="data row3 col0" >kindergarten</td>
      <td id="T_12e17_row3_col1" class="data row3 col1" >225.0</td>
      <td id="T_12e17_row3_col2" class="data row3 col2" >225.0</td>
      <td id="T_12e17_row3_col3" class="data row3 col3" >152.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row4_col0" class="data row4 col0" >library</td>
      <td id="T_12e17_row4_col1" class="data row4 col1" >64.0</td>
      <td id="T_12e17_row4_col2" class="data row4 col2" >64.0</td>
      <td id="T_12e17_row4_col3" class="data row4 col3" >48.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row5_col0" class="data row5 col0" >nursery</td>
      <td id="T_12e17_row5_col1" class="data row5 col1" >19.0</td>
      <td id="T_12e17_row5_col2" class="data row5 col2" >19.0</td>
      <td id="T_12e17_row5_col3" class="data row5 col3" >11.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row6_col0" class="data row6 col0" >pharmacy</td>
      <td id="T_12e17_row6_col1" class="data row6 col1" >111.0</td>
      <td id="T_12e17_row6_col2" class="data row6 col2" >111.0</td>
      <td id="T_12e17_row6_col3" class="data row6 col3" >76.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row7_col0" class="data row7 col0" >school</td>
      <td id="T_12e17_row7_col1" class="data row7 col1" >330.0</td>
      <td id="T_12e17_row7_col2" class="data row7 col2" >330.0</td>
      <td id="T_12e17_row7_col3" class="data row7 col3" >362.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row8_col0" class="data row8 col0" >sports_facility</td>
      <td id="T_12e17_row8_col1" class="data row8 col1" >-</td>
      <td id="T_12e17_row8_col2" class="data row8 col2" >-</td>
      <td id="T_12e17_row8_col3" class="data row8 col3" >89.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row9_col0" class="data row9 col0" >supermarket</td>
      <td id="T_12e17_row9_col1" class="data row9 col1" >298.0</td>
      <td id="T_12e17_row9_col2" class="data row9 col2" >298.0</td>
      <td id="T_12e17_row9_col3" class="data row9 col3" >426.0</td>
    </tr>
    <tr>
      <td id="T_12e17_row10_col0" class="data row10 col0" >train_station</td>
      <td id="T_12e17_row10_col1" class="data row10 col1" >-</td>
      <td id="T_12e17_row10_col2" class="data row10 col2" >-</td>
      <td id="T_12e17_row10_col3" class="data row10 col3" >73.0</td>
    </tr>
  </tbody>
</table>



### Main destination categories

<style type="text/css">
#T_7c68a th {
  font-weight: bold;
}
#T_7c68a .col0 {
  font-weight: bold;
}
#T_7c68a .col0 {
  font-weight: bold;
}
#T_7c68a_row0_col0, #T_7c68a_row0_col3, #T_7c68a_row1_col0, #T_7c68a_row1_col3, #T_7c68a_row2_col0, #T_7c68a_row2_col3, #T_7c68a_row3_col0, #T_7c68a_row3_col3, #T_7c68a_row4_col0, #T_7c68a_row5_col0, #T_7c68a_row6_col0, #T_7c68a_row6_col3, #T_7c68a_row7_col0 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_7c68a_row0_col1, #T_7c68a_row0_col2, #T_7c68a_row1_col1, #T_7c68a_row1_col2, #T_7c68a_row2_col1, #T_7c68a_row2_col2, #T_7c68a_row3_col1, #T_7c68a_row3_col2, #T_7c68a_row6_col1, #T_7c68a_row6_col2 {
  background-color: yellow;
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_7c68a_row4_col1, #T_7c68a_row4_col2, #T_7c68a_row5_col1, #T_7c68a_row5_col2 {
  background-color: lightyellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_7c68a_row4_col3, #T_7c68a_row5_col3, #T_7c68a_row7_col3 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_7c68a_row7_col1, #T_7c68a_row7_col2 {
  color: grey;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_7c68a" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th id="T_7c68a_level0_col0" class="col_heading level0 col0" >service_type_main</th>
      <th id="T_7c68a_level0_col1" class="col_heading level0 col1" >cvr_addresses</th>
      <th id="T_7c68a_level0_col2" class="col_heading level0 col2" >cvr_all</th>
      <th id="T_7c68a_level0_col3" class="col_heading level0 col3" >osm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_7c68a_row0_col0" class="data row0 col0" >dentist</td>
      <td id="T_7c68a_row0_col1" class="data row0 col1" >397.0</td>
      <td id="T_7c68a_row0_col2" class="data row0 col2" >397.0</td>
      <td id="T_7c68a_row0_col3" class="data row0 col3" >20</td>
    </tr>
    <tr>
      <td id="T_7c68a_row1_col0" class="data row1 col0" >doctor</td>
      <td id="T_7c68a_row1_col1" class="data row1 col1" >419.0</td>
      <td id="T_7c68a_row1_col2" class="data row1 col2" >419.0</td>
      <td id="T_7c68a_row1_col3" class="data row1 col3" >41</td>
    </tr>
    <tr>
      <td id="T_7c68a_row2_col0" class="data row2 col0" >nursery/kindergarten</td>
      <td id="T_7c68a_row2_col1" class="data row2 col1" >244.0</td>
      <td id="T_7c68a_row2_col2" class="data row2 col2" >244.0</td>
      <td id="T_7c68a_row2_col3" class="data row2 col3" >163</td>
    </tr>
    <tr>
      <td id="T_7c68a_row3_col0" class="data row3 col0" >pharmacy</td>
      <td id="T_7c68a_row3_col1" class="data row3 col1" >111.0</td>
      <td id="T_7c68a_row3_col2" class="data row3 col2" >111.0</td>
      <td id="T_7c68a_row3_col3" class="data row3 col3" >76</td>
    </tr>
    <tr>
      <td id="T_7c68a_row4_col0" class="data row4 col0" >recreation</td>
      <td id="T_7c68a_row4_col1" class="data row4 col1" >64.0</td>
      <td id="T_7c68a_row4_col2" class="data row4 col2" >64.0</td>
      <td id="T_7c68a_row4_col3" class="data row4 col3" >137</td>
    </tr>
    <tr>
      <td id="T_7c68a_row5_col0" class="data row5 col0" >school</td>
      <td id="T_7c68a_row5_col1" class="data row5 col1" >330.0</td>
      <td id="T_7c68a_row5_col2" class="data row5 col2" >330.0</td>
      <td id="T_7c68a_row5_col3" class="data row5 col3" >362</td>
    </tr>
    <tr>
      <td id="T_7c68a_row6_col0" class="data row6 col0" >shop</td>
      <td id="T_7c68a_row6_col1" class="data row6 col1" >548.0</td>
      <td id="T_7c68a_row6_col2" class="data row6 col2" >548.0</td>
      <td id="T_7c68a_row6_col3" class="data row6 col3" >426</td>
    </tr>
    <tr>
      <td id="T_7c68a_row7_col0" class="data row7 col0" >train_station</td>
      <td id="T_7c68a_row7_col1" class="data row7 col1" >-</td>
      <td id="T_7c68a_row7_col2" class="data row7 col2" >-</td>
      <td id="T_7c68a_row7_col3" class="data row7 col3" >73</td>
    </tr>
  </tbody>
</table>

## Counts per municipality

<style type="text/css">
#T_d09fa th {
  font-weight: bold;
}
#T_d09fa_row0_col0, #T_d09fa_row0_col1, #T_d09fa_row0_col2, #T_d09fa_row0_col3, #T_d09fa_row0_col4, #T_d09fa_row0_col5, #T_d09fa_row0_col6, #T_d09fa_row0_col7, #T_d09fa_row1_col0, #T_d09fa_row1_col1, #T_d09fa_row1_col2, #T_d09fa_row1_col3, #T_d09fa_row1_col4, #T_d09fa_row1_col5, #T_d09fa_row1_col6, #T_d09fa_row1_col7, #T_d09fa_row2_col0, #T_d09fa_row2_col1, #T_d09fa_row2_col2, #T_d09fa_row2_col3, #T_d09fa_row2_col4, #T_d09fa_row2_col5, #T_d09fa_row2_col6, #T_d09fa_row2_col7, #T_d09fa_row3_col0, #T_d09fa_row3_col1, #T_d09fa_row3_col2, #T_d09fa_row3_col3, #T_d09fa_row3_col4, #T_d09fa_row3_col5, #T_d09fa_row3_col6, #T_d09fa_row3_col7, #T_d09fa_row4_col0, #T_d09fa_row4_col1, #T_d09fa_row4_col2, #T_d09fa_row4_col3, #T_d09fa_row4_col4, #T_d09fa_row4_col5, #T_d09fa_row4_col6, #T_d09fa_row4_col7, #T_d09fa_row5_col0, #T_d09fa_row5_col1, #T_d09fa_row5_col2, #T_d09fa_row5_col3, #T_d09fa_row5_col4, #T_d09fa_row5_col5, #T_d09fa_row5_col6, #T_d09fa_row5_col7, #T_d09fa_row6_col0, #T_d09fa_row6_col1, #T_d09fa_row6_col2, #T_d09fa_row6_col3, #T_d09fa_row6_col4, #T_d09fa_row6_col5, #T_d09fa_row6_col6, #T_d09fa_row6_col7, #T_d09fa_row7_col0, #T_d09fa_row7_col1, #T_d09fa_row7_col2, #T_d09fa_row7_col3, #T_d09fa_row7_col4, #T_d09fa_row7_col5, #T_d09fa_row7_col6, #T_d09fa_row7_col7, #T_d09fa_row8_col0, #T_d09fa_row8_col1, #T_d09fa_row8_col2, #T_d09fa_row8_col3, #T_d09fa_row8_col4, #T_d09fa_row8_col5, #T_d09fa_row8_col6, #T_d09fa_row8_col7, #T_d09fa_row9_col0, #T_d09fa_row9_col1, #T_d09fa_row9_col2, #T_d09fa_row9_col3, #T_d09fa_row9_col4, #T_d09fa_row9_col5, #T_d09fa_row9_col6, #T_d09fa_row9_col7, #T_d09fa_row10_col0, #T_d09fa_row10_col1, #T_d09fa_row10_col2, #T_d09fa_row10_col3, #T_d09fa_row10_col4, #T_d09fa_row10_col5, #T_d09fa_row10_col6, #T_d09fa_row10_col7, #T_d09fa_row11_col0, #T_d09fa_row11_col1, #T_d09fa_row11_col2, #T_d09fa_row11_col3, #T_d09fa_row11_col4, #T_d09fa_row11_col5, #T_d09fa_row11_col6, #T_d09fa_row11_col7, #T_d09fa_row12_col0, #T_d09fa_row12_col1, #T_d09fa_row12_col2, #T_d09fa_row12_col3, #T_d09fa_row12_col4, #T_d09fa_row12_col5, #T_d09fa_row12_col6, #T_d09fa_row12_col7, #T_d09fa_row13_col0, #T_d09fa_row13_col1, #T_d09fa_row13_col2, #T_d09fa_row13_col3, #T_d09fa_row13_col4, #T_d09fa_row13_col5, #T_d09fa_row13_col6, #T_d09fa_row13_col7, #T_d09fa_row14_col0, #T_d09fa_row14_col1, #T_d09fa_row14_col2, #T_d09fa_row14_col3, #T_d09fa_row14_col4, #T_d09fa_row14_col5, #T_d09fa_row14_col6, #T_d09fa_row14_col7, #T_d09fa_row15_col0, #T_d09fa_row15_col1, #T_d09fa_row15_col2, #T_d09fa_row15_col3, #T_d09fa_row15_col4, #T_d09fa_row15_col5, #T_d09fa_row15_col6, #T_d09fa_row15_col7, #T_d09fa_row16_col0, #T_d09fa_row16_col1, #T_d09fa_row16_col2, #T_d09fa_row16_col3, #T_d09fa_row16_col4, #T_d09fa_row16_col5, #T_d09fa_row16_col6, #T_d09fa_row16_col7, #T_d09fa_row17_col0, #T_d09fa_row17_col1, #T_d09fa_row17_col2, #T_d09fa_row17_col3, #T_d09fa_row17_col4, #T_d09fa_row17_col5, #T_d09fa_row17_col6, #T_d09fa_row17_col7 {
  text-align: right;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_d09fa" style="width: 50%; border-collapse: collapse;">
  <caption>Municipal service counts</caption>
  <thead>
    <tr>
      <th class="index_name level0" >service_type_main</th>
      <th id="T_d09fa_level0_col0" class="col_heading level0 col0" >dentist</th>
      <th id="T_d09fa_level0_col1" class="col_heading level0 col1" >doctor</th>
      <th id="T_d09fa_level0_col2" class="col_heading level0 col2" >nursery/kindergarten</th>
      <th id="T_d09fa_level0_col3" class="col_heading level0 col3" >pharmacy</th>
      <th id="T_d09fa_level0_col4" class="col_heading level0 col4" >recreation</th>
      <th id="T_d09fa_level0_col5" class="col_heading level0 col5" >school</th>
      <th id="T_d09fa_level0_col6" class="col_heading level0 col6" >shop</th>
      <th id="T_d09fa_level0_col7" class="col_heading level0 col7" >train_station</th>
    </tr>
    <tr>
      <th class="index_name level0" >navn</th>
      <th class="blank col0" >&nbsp;</th>
      <th class="blank col1" >&nbsp;</th>
      <th class="blank col2" >&nbsp;</th>
      <th class="blank col3" >&nbsp;</th>
      <th class="blank col4" >&nbsp;</th>
      <th class="blank col5" >&nbsp;</th>
      <th class="blank col6" >&nbsp;</th>
      <th class="blank col7" >&nbsp;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_d09fa_level0_row0" class="row_heading level0 row0" >Faxe</th>
      <td id="T_d09fa_row0_col0" class="data row0 col0" >8</td>
      <td id="T_d09fa_row0_col1" class="data row0 col1" >21</td>
      <td id="T_d09fa_row0_col2" class="data row0 col2" >11</td>
      <td id="T_d09fa_row0_col3" class="data row0 col3" >5</td>
      <td id="T_d09fa_row0_col4" class="data row0 col4" >5</td>
      <td id="T_d09fa_row0_col5" class="data row0 col5" >33</td>
      <td id="T_d09fa_row0_col6" class="data row0 col6" >37</td>
      <td id="T_d09fa_row0_col7" class="data row0 col7" >4</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row1" class="row_heading level0 row1" >Greve</th>
      <td id="T_d09fa_row1_col0" class="data row1 col0" >24</td>
      <td id="T_d09fa_row1_col1" class="data row1 col1" >30</td>
      <td id="T_d09fa_row1_col2" class="data row1 col2" >42</td>
      <td id="T_d09fa_row1_col3" class="data row1 col3" >8</td>
      <td id="T_d09fa_row1_col4" class="data row1 col4" >12</td>
      <td id="T_d09fa_row1_col5" class="data row1 col5" >37</td>
      <td id="T_d09fa_row1_col6" class="data row1 col6" >39</td>
      <td id="T_d09fa_row1_col7" class="data row1 col7" >2</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row2" class="row_heading level0 row2" >Guldborgsund</th>
      <td id="T_d09fa_row2_col0" class="data row2 col0" >24</td>
      <td id="T_d09fa_row2_col1" class="data row2 col1" >33</td>
      <td id="T_d09fa_row2_col2" class="data row2 col2" >31</td>
      <td id="T_d09fa_row2_col3" class="data row2 col3" >16</td>
      <td id="T_d09fa_row2_col4" class="data row2 col4" >26</td>
      <td id="T_d09fa_row2_col5" class="data row2 col5" >39</td>
      <td id="T_d09fa_row2_col6" class="data row2 col6" >91</td>
      <td id="T_d09fa_row2_col7" class="data row2 col7" >6</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row3" class="row_heading level0 row3" >Holbæk</th>
      <td id="T_d09fa_row3_col0" class="data row3 col0" >42</td>
      <td id="T_d09fa_row3_col1" class="data row3 col1" >31</td>
      <td id="T_d09fa_row3_col2" class="data row3 col2" >21</td>
      <td id="T_d09fa_row3_col3" class="data row3 col3" >17</td>
      <td id="T_d09fa_row3_col4" class="data row3 col4" >18</td>
      <td id="T_d09fa_row3_col5" class="data row3 col5" >65</td>
      <td id="T_d09fa_row3_col6" class="data row3 col6" >93</td>
      <td id="T_d09fa_row3_col7" class="data row3 col7" >10</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row4" class="row_heading level0 row4" >Kalundborg</th>
      <td id="T_d09fa_row4_col0" class="data row4 col0" >18</td>
      <td id="T_d09fa_row4_col1" class="data row4 col1" >20</td>
      <td id="T_d09fa_row4_col2" class="data row4 col2" >36</td>
      <td id="T_d09fa_row4_col3" class="data row4 col3" >13</td>
      <td id="T_d09fa_row4_col4" class="data row4 col4" >14</td>
      <td id="T_d09fa_row4_col5" class="data row4 col5" >59</td>
      <td id="T_d09fa_row4_col6" class="data row4 col6" >60</td>
      <td id="T_d09fa_row4_col7" class="data row4 col7" >3</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row5" class="row_heading level0 row5" >Køge</th>
      <td id="T_d09fa_row5_col0" class="data row5 col0" >31</td>
      <td id="T_d09fa_row5_col1" class="data row5 col1" >39</td>
      <td id="T_d09fa_row5_col2" class="data row5 col2" >30</td>
      <td id="T_d09fa_row5_col3" class="data row5 col3" >21</td>
      <td id="T_d09fa_row5_col4" class="data row5 col4" >14</td>
      <td id="T_d09fa_row5_col5" class="data row5 col5" >43</td>
      <td id="T_d09fa_row5_col6" class="data row5 col6" >66</td>
      <td id="T_d09fa_row5_col7" class="data row5 col7" >8</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row6" class="row_heading level0 row6" >Lejre</th>
      <td id="T_d09fa_row6_col0" class="data row6 col0" >6</td>
      <td id="T_d09fa_row6_col1" class="data row6 col1" >11</td>
      <td id="T_d09fa_row6_col2" class="data row6 col2" >20</td>
      <td id="T_d09fa_row6_col3" class="data row6 col3" >2</td>
      <td id="T_d09fa_row6_col4" class="data row6 col4" >10</td>
      <td id="T_d09fa_row6_col5" class="data row6 col5" >24</td>
      <td id="T_d09fa_row6_col6" class="data row6 col6" >27</td>
      <td id="T_d09fa_row6_col7" class="data row6 col7" >2</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row7" class="row_heading level0 row7" >Lolland</th>
      <td id="T_d09fa_row7_col0" class="data row7 col0" >21</td>
      <td id="T_d09fa_row7_col1" class="data row7 col1" >20</td>
      <td id="T_d09fa_row7_col2" class="data row7 col2" >13</td>
      <td id="T_d09fa_row7_col3" class="data row7 col3" >14</td>
      <td id="T_d09fa_row7_col4" class="data row7 col4" >12</td>
      <td id="T_d09fa_row7_col5" class="data row7 col5" >34</td>
      <td id="T_d09fa_row7_col6" class="data row7 col6" >60</td>
      <td id="T_d09fa_row7_col7" class="data row7 col7" >6</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row8" class="row_heading level0 row8" >Næstved</th>
      <td id="T_d09fa_row8_col0" class="data row8 col0" >39</td>
      <td id="T_d09fa_row8_col1" class="data row8 col1" >39</td>
      <td id="T_d09fa_row8_col2" class="data row8 col2" >35</td>
      <td id="T_d09fa_row8_col3" class="data row8 col3" >14</td>
      <td id="T_d09fa_row8_col4" class="data row8 col4" >11</td>
      <td id="T_d09fa_row8_col5" class="data row8 col5" >70</td>
      <td id="T_d09fa_row8_col6" class="data row8 col6" >87</td>
      <td id="T_d09fa_row8_col7" class="data row8 col7" >3</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row9" class="row_heading level0 row9" >Odsherred</th>
      <td id="T_d09fa_row9_col0" class="data row9 col0" >15</td>
      <td id="T_d09fa_row9_col1" class="data row9 col1" >16</td>
      <td id="T_d09fa_row9_col2" class="data row9 col2" >10</td>
      <td id="T_d09fa_row9_col3" class="data row9 col3" >7</td>
      <td id="T_d09fa_row9_col4" class="data row9 col4" >10</td>
      <td id="T_d09fa_row9_col5" class="data row9 col5" >37</td>
      <td id="T_d09fa_row9_col6" class="data row9 col6" >50</td>
      <td id="T_d09fa_row9_col7" class="data row9 col7" >8</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row10" class="row_heading level0 row10" >Ringsted</th>
      <td id="T_d09fa_row10_col0" class="data row10 col0" >18</td>
      <td id="T_d09fa_row10_col1" class="data row10 col1" >11</td>
      <td id="T_d09fa_row10_col2" class="data row10 col2" >17</td>
      <td id="T_d09fa_row10_col3" class="data row10 col3" >7</td>
      <td id="T_d09fa_row10_col4" class="data row10 col4" >5</td>
      <td id="T_d09fa_row10_col5" class="data row10 col5" >27</td>
      <td id="T_d09fa_row10_col6" class="data row10 col6" >41</td>
      <td id="T_d09fa_row10_col7" class="data row10 col7" >1</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row11" class="row_heading level0 row11" >Roskilde</th>
      <td id="T_d09fa_row11_col0" class="data row11 col0" >66</td>
      <td id="T_d09fa_row11_col1" class="data row11 col1" >72</td>
      <td id="T_d09fa_row11_col2" class="data row11 col2" >53</td>
      <td id="T_d09fa_row11_col3" class="data row11 col3" >21</td>
      <td id="T_d09fa_row11_col4" class="data row11 col4" >23</td>
      <td id="T_d09fa_row11_col5" class="data row11 col5" >69</td>
      <td id="T_d09fa_row11_col6" class="data row11 col6" >88</td>
      <td id="T_d09fa_row11_col7" class="data row11 col7" >4</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row12" class="row_heading level0 row12" >Slagelse</th>
      <td id="T_d09fa_row12_col0" class="data row12 col0" >37</td>
      <td id="T_d09fa_row12_col1" class="data row12 col1" >41</td>
      <td id="T_d09fa_row12_col2" class="data row12 col2" >28</td>
      <td id="T_d09fa_row12_col3" class="data row12 col3" >13</td>
      <td id="T_d09fa_row12_col4" class="data row12 col4" >13</td>
      <td id="T_d09fa_row12_col5" class="data row12 col5" >65</td>
      <td id="T_d09fa_row12_col6" class="data row12 col6" >95</td>
      <td id="T_d09fa_row12_col7" class="data row12 col7" >2</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row13" class="row_heading level0 row13" >Solrød</th>
      <td id="T_d09fa_row13_col0" class="data row13 col0" >19</td>
      <td id="T_d09fa_row13_col1" class="data row13 col1" >21</td>
      <td id="T_d09fa_row13_col2" class="data row13 col2" >22</td>
      <td id="T_d09fa_row13_col3" class="data row13 col3" >3</td>
      <td id="T_d09fa_row13_col4" class="data row13 col4" >2</td>
      <td id="T_d09fa_row13_col5" class="data row13 col5" >11</td>
      <td id="T_d09fa_row13_col6" class="data row13 col6" >17</td>
      <td id="T_d09fa_row13_col7" class="data row13 col7" >2</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row14" class="row_heading level0 row14" >Sorø</th>
      <td id="T_d09fa_row14_col0" class="data row14 col0" >16</td>
      <td id="T_d09fa_row14_col1" class="data row14 col1" >16</td>
      <td id="T_d09fa_row14_col2" class="data row14 col2" >10</td>
      <td id="T_d09fa_row14_col3" class="data row14 col3" >9</td>
      <td id="T_d09fa_row14_col4" class="data row14 col4" >6</td>
      <td id="T_d09fa_row14_col5" class="data row14 col5" >19</td>
      <td id="T_d09fa_row14_col6" class="data row14 col6" >36</td>
      <td id="T_d09fa_row14_col7" class="data row14 col7" >5</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row15" class="row_heading level0 row15" >Stevns</th>
      <td id="T_d09fa_row15_col0" class="data row15 col0" >8</td>
      <td id="T_d09fa_row15_col1" class="data row15 col1" >11</td>
      <td id="T_d09fa_row15_col2" class="data row15 col2" >7</td>
      <td id="T_d09fa_row15_col3" class="data row15 col3" >5</td>
      <td id="T_d09fa_row15_col4" class="data row15 col4" >6</td>
      <td id="T_d09fa_row15_col5" class="data row15 col5" >12</td>
      <td id="T_d09fa_row15_col6" class="data row15 col6" >23</td>
      <td id="T_d09fa_row15_col7" class="data row15 col7" >5</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row16" class="row_heading level0 row16" >Vordingborg</th>
      <td id="T_d09fa_row16_col0" class="data row16 col0" >25</td>
      <td id="T_d09fa_row16_col1" class="data row16 col1" >28</td>
      <td id="T_d09fa_row16_col2" class="data row16 col2" >21</td>
      <td id="T_d09fa_row16_col3" class="data row16 col3" >12</td>
      <td id="T_d09fa_row16_col4" class="data row16 col4" >14</td>
      <td id="T_d09fa_row16_col5" class="data row16 col5" >48</td>
      <td id="T_d09fa_row16_col6" class="data row16 col6" >64</td>
      <td id="T_d09fa_row16_col7" class="data row16 col7" >2</td>
    </tr>
    <tr>
      <th id="T_d09fa_level0_row17" class="row_heading level0 row17" >Total</th>
      <td id="T_d09fa_row17_col0" class="data row17 col0" >417</td>
      <td id="T_d09fa_row17_col1" class="data row17 col1" >460</td>
      <td id="T_d09fa_row17_col2" class="data row17 col2" >407</td>
      <td id="T_d09fa_row17_col3" class="data row17 col3" >187</td>
      <td id="T_d09fa_row17_col4" class="data row17 col4" >201</td>
      <td id="T_d09fa_row17_col5" class="data row17 col5" >692</td>
      <td id="T_d09fa_row17_col6" class="data row17 col6" >974</td>
      <td id="T_d09fa_row17_col7" class="data row17 col7" >73</td>
    </tr>
  </tbody>
</table>



<style type="text/css">
#T_652f8 th {
  font-weight: bold;
}
#T_652f8_row0_col0, #T_652f8_row0_col1, #T_652f8_row0_col2, #T_652f8_row0_col3, #T_652f8_row0_col4, #T_652f8_row0_col5, #T_652f8_row0_col6, #T_652f8_row0_col7, #T_652f8_row0_col8, #T_652f8_row0_col9, #T_652f8_row0_col10, #T_652f8_row1_col0, #T_652f8_row1_col1, #T_652f8_row1_col2, #T_652f8_row1_col3, #T_652f8_row1_col4, #T_652f8_row1_col5, #T_652f8_row1_col6, #T_652f8_row1_col7, #T_652f8_row1_col8, #T_652f8_row1_col9, #T_652f8_row1_col10, #T_652f8_row2_col0, #T_652f8_row2_col1, #T_652f8_row2_col2, #T_652f8_row2_col3, #T_652f8_row2_col4, #T_652f8_row2_col6, #T_652f8_row2_col7, #T_652f8_row2_col8, #T_652f8_row2_col9, #T_652f8_row2_col10, #T_652f8_row3_col0, #T_652f8_row3_col1, #T_652f8_row3_col2, #T_652f8_row3_col3, #T_652f8_row3_col4, #T_652f8_row3_col6, #T_652f8_row3_col7, #T_652f8_row3_col8, #T_652f8_row3_col9, #T_652f8_row3_col10, #T_652f8_row4_col0, #T_652f8_row4_col1, #T_652f8_row4_col2, #T_652f8_row4_col3, #T_652f8_row4_col4, #T_652f8_row4_col5, #T_652f8_row4_col6, #T_652f8_row4_col7, #T_652f8_row4_col8, #T_652f8_row4_col9, #T_652f8_row4_col10, #T_652f8_row5_col0, #T_652f8_row5_col1, #T_652f8_row5_col2, #T_652f8_row5_col3, #T_652f8_row5_col4, #T_652f8_row5_col5, #T_652f8_row5_col6, #T_652f8_row5_col7, #T_652f8_row5_col8, #T_652f8_row5_col9, #T_652f8_row5_col10, #T_652f8_row6_col0, #T_652f8_row6_col1, #T_652f8_row6_col2, #T_652f8_row6_col3, #T_652f8_row6_col4, #T_652f8_row6_col6, #T_652f8_row6_col7, #T_652f8_row6_col8, #T_652f8_row6_col9, #T_652f8_row6_col10, #T_652f8_row7_col0, #T_652f8_row7_col1, #T_652f8_row7_col2, #T_652f8_row7_col3, #T_652f8_row7_col4, #T_652f8_row7_col6, #T_652f8_row7_col7, #T_652f8_row7_col8, #T_652f8_row7_col9, #T_652f8_row7_col10, #T_652f8_row8_col0, #T_652f8_row8_col1, #T_652f8_row8_col2, #T_652f8_row8_col3, #T_652f8_row8_col4, #T_652f8_row8_col6, #T_652f8_row8_col7, #T_652f8_row8_col8, #T_652f8_row8_col9, #T_652f8_row8_col10, #T_652f8_row9_col0, #T_652f8_row9_col1, #T_652f8_row9_col2, #T_652f8_row9_col3, #T_652f8_row9_col4, #T_652f8_row9_col6, #T_652f8_row9_col7, #T_652f8_row9_col8, #T_652f8_row9_col9, #T_652f8_row9_col10, #T_652f8_row10_col0, #T_652f8_row10_col1, #T_652f8_row10_col2, #T_652f8_row10_col3, #T_652f8_row10_col4, #T_652f8_row10_col5, #T_652f8_row10_col6, #T_652f8_row10_col7, #T_652f8_row10_col8, #T_652f8_row10_col9, #T_652f8_row10_col10, #T_652f8_row11_col0, #T_652f8_row11_col1, #T_652f8_row11_col2, #T_652f8_row11_col3, #T_652f8_row11_col4, #T_652f8_row11_col5, #T_652f8_row11_col6, #T_652f8_row11_col7, #T_652f8_row11_col8, #T_652f8_row11_col9, #T_652f8_row11_col10, #T_652f8_row12_col0, #T_652f8_row12_col1, #T_652f8_row12_col2, #T_652f8_row12_col3, #T_652f8_row12_col4, #T_652f8_row12_col5, #T_652f8_row12_col6, #T_652f8_row12_col7, #T_652f8_row12_col8, #T_652f8_row12_col9, #T_652f8_row12_col10, #T_652f8_row13_col0, #T_652f8_row13_col1, #T_652f8_row13_col2, #T_652f8_row13_col3, #T_652f8_row13_col4, #T_652f8_row13_col5, #T_652f8_row13_col6, #T_652f8_row13_col7, #T_652f8_row13_col9, #T_652f8_row13_col10, #T_652f8_row14_col0, #T_652f8_row14_col1, #T_652f8_row14_col2, #T_652f8_row14_col3, #T_652f8_row14_col4, #T_652f8_row14_col5, #T_652f8_row14_col6, #T_652f8_row14_col7, #T_652f8_row14_col8, #T_652f8_row14_col9, #T_652f8_row14_col10, #T_652f8_row15_col0, #T_652f8_row15_col1, #T_652f8_row15_col2, #T_652f8_row15_col3, #T_652f8_row15_col4, #T_652f8_row15_col6, #T_652f8_row15_col7, #T_652f8_row15_col8, #T_652f8_row15_col9, #T_652f8_row15_col10, #T_652f8_row16_col0, #T_652f8_row16_col1, #T_652f8_row16_col2, #T_652f8_row16_col3, #T_652f8_row16_col4, #T_652f8_row16_col6, #T_652f8_row16_col7, #T_652f8_row16_col8, #T_652f8_row16_col9, #T_652f8_row16_col10, #T_652f8_row17_col0, #T_652f8_row17_col1, #T_652f8_row17_col2, #T_652f8_row17_col3, #T_652f8_row17_col4, #T_652f8_row17_col5, #T_652f8_row17_col6, #T_652f8_row17_col7, #T_652f8_row17_col8, #T_652f8_row17_col9, #T_652f8_row17_col10 {
  text-align: right;
  font-size: 12px;
  width: 100px;
}
#T_652f8_row2_col5, #T_652f8_row3_col5, #T_652f8_row6_col5, #T_652f8_row7_col5, #T_652f8_row8_col5, #T_652f8_row9_col5, #T_652f8_row13_col8, #T_652f8_row15_col5, #T_652f8_row16_col5 {
  color: red;
  text-align: right;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_652f8" style="width: 50%; border-collapse: collapse;">
  <caption>Municipal service counts</caption>
  <thead>
    <tr>
      <th class="index_name level0" >service_type</th>
      <th id="T_652f8_level0_col0" class="col_heading level0 col0" >dentist</th>
      <th id="T_652f8_level0_col1" class="col_heading level0 col1" >discount_supermarket</th>
      <th id="T_652f8_level0_col2" class="col_heading level0 col2" >doctor-gp</th>
      <th id="T_652f8_level0_col3" class="col_heading level0 col3" >kindergarten</th>
      <th id="T_652f8_level0_col4" class="col_heading level0 col4" >library</th>
      <th id="T_652f8_level0_col5" class="col_heading level0 col5" >nursery</th>
      <th id="T_652f8_level0_col6" class="col_heading level0 col6" >pharmacy</th>
      <th id="T_652f8_level0_col7" class="col_heading level0 col7" >school</th>
      <th id="T_652f8_level0_col8" class="col_heading level0 col8" >sports_facility</th>
      <th id="T_652f8_level0_col9" class="col_heading level0 col9" >supermarket</th>
      <th id="T_652f8_level0_col10" class="col_heading level0 col10" >train_station</th>
    </tr>
    <tr>
      <th class="index_name level0" >navn</th>
      <th class="blank col0" >&nbsp;</th>
      <th class="blank col1" >&nbsp;</th>
      <th class="blank col2" >&nbsp;</th>
      <th class="blank col3" >&nbsp;</th>
      <th class="blank col4" >&nbsp;</th>
      <th class="blank col5" >&nbsp;</th>
      <th class="blank col6" >&nbsp;</th>
      <th class="blank col7" >&nbsp;</th>
      <th class="blank col8" >&nbsp;</th>
      <th class="blank col9" >&nbsp;</th>
      <th class="blank col10" >&nbsp;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_652f8_level0_row0" class="row_heading level0 row0" >Faxe</th>
      <td id="T_652f8_row0_col0" class="data row0 col0" >8</td>
      <td id="T_652f8_row0_col1" class="data row0 col1" >9</td>
      <td id="T_652f8_row0_col2" class="data row0 col2" >21</td>
      <td id="T_652f8_row0_col3" class="data row0 col3" >10</td>
      <td id="T_652f8_row0_col4" class="data row0 col4" >3</td>
      <td id="T_652f8_row0_col5" class="data row0 col5" >1</td>
      <td id="T_652f8_row0_col6" class="data row0 col6" >5</td>
      <td id="T_652f8_row0_col7" class="data row0 col7" >33</td>
      <td id="T_652f8_row0_col8" class="data row0 col8" >2</td>
      <td id="T_652f8_row0_col9" class="data row0 col9" >28</td>
      <td id="T_652f8_row0_col10" class="data row0 col10" >4</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row1" class="row_heading level0 row1" >Greve</th>
      <td id="T_652f8_row1_col0" class="data row1 col0" >24</td>
      <td id="T_652f8_row1_col1" class="data row1 col1" >12</td>
      <td id="T_652f8_row1_col2" class="data row1 col2" >30</td>
      <td id="T_652f8_row1_col3" class="data row1 col3" >40</td>
      <td id="T_652f8_row1_col4" class="data row1 col4" >6</td>
      <td id="T_652f8_row1_col5" class="data row1 col5" >2</td>
      <td id="T_652f8_row1_col6" class="data row1 col6" >8</td>
      <td id="T_652f8_row1_col7" class="data row1 col7" >37</td>
      <td id="T_652f8_row1_col8" class="data row1 col8" >6</td>
      <td id="T_652f8_row1_col9" class="data row1 col9" >27</td>
      <td id="T_652f8_row1_col10" class="data row1 col10" >2</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row2" class="row_heading level0 row2" >Guldborgsund</th>
      <td id="T_652f8_row2_col0" class="data row2 col0" >24</td>
      <td id="T_652f8_row2_col1" class="data row2 col1" >20</td>
      <td id="T_652f8_row2_col2" class="data row2 col2" >33</td>
      <td id="T_652f8_row2_col3" class="data row2 col3" >31</td>
      <td id="T_652f8_row2_col4" class="data row2 col4" >12</td>
      <td id="T_652f8_row2_col5" class="data row2 col5" >0</td>
      <td id="T_652f8_row2_col6" class="data row2 col6" >16</td>
      <td id="T_652f8_row2_col7" class="data row2 col7" >39</td>
      <td id="T_652f8_row2_col8" class="data row2 col8" >14</td>
      <td id="T_652f8_row2_col9" class="data row2 col9" >71</td>
      <td id="T_652f8_row2_col10" class="data row2 col10" >6</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row3" class="row_heading level0 row3" >Holbæk</th>
      <td id="T_652f8_row3_col0" class="data row3 col0" >42</td>
      <td id="T_652f8_row3_col1" class="data row3 col1" >20</td>
      <td id="T_652f8_row3_col2" class="data row3 col2" >31</td>
      <td id="T_652f8_row3_col3" class="data row3 col3" >21</td>
      <td id="T_652f8_row3_col4" class="data row3 col4" >10</td>
      <td id="T_652f8_row3_col5" class="data row3 col5" >0</td>
      <td id="T_652f8_row3_col6" class="data row3 col6" >17</td>
      <td id="T_652f8_row3_col7" class="data row3 col7" >65</td>
      <td id="T_652f8_row3_col8" class="data row3 col8" >8</td>
      <td id="T_652f8_row3_col9" class="data row3 col9" >73</td>
      <td id="T_652f8_row3_col10" class="data row3 col10" >10</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row4" class="row_heading level0 row4" >Kalundborg</th>
      <td id="T_652f8_row4_col0" class="data row4 col0" >18</td>
      <td id="T_652f8_row4_col1" class="data row4 col1" >12</td>
      <td id="T_652f8_row4_col2" class="data row4 col2" >20</td>
      <td id="T_652f8_row4_col3" class="data row4 col3" >32</td>
      <td id="T_652f8_row4_col4" class="data row4 col4" >9</td>
      <td id="T_652f8_row4_col5" class="data row4 col5" >4</td>
      <td id="T_652f8_row4_col6" class="data row4 col6" >13</td>
      <td id="T_652f8_row4_col7" class="data row4 col7" >59</td>
      <td id="T_652f8_row4_col8" class="data row4 col8" >5</td>
      <td id="T_652f8_row4_col9" class="data row4 col9" >48</td>
      <td id="T_652f8_row4_col10" class="data row4 col10" >3</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row5" class="row_heading level0 row5" >Køge</th>
      <td id="T_652f8_row5_col0" class="data row5 col0" >31</td>
      <td id="T_652f8_row5_col1" class="data row5 col1" >24</td>
      <td id="T_652f8_row5_col2" class="data row5 col2" >39</td>
      <td id="T_652f8_row5_col3" class="data row5 col3" >28</td>
      <td id="T_652f8_row5_col4" class="data row5 col4" >6</td>
      <td id="T_652f8_row5_col5" class="data row5 col5" >2</td>
      <td id="T_652f8_row5_col6" class="data row5 col6" >21</td>
      <td id="T_652f8_row5_col7" class="data row5 col7" >43</td>
      <td id="T_652f8_row5_col8" class="data row5 col8" >8</td>
      <td id="T_652f8_row5_col9" class="data row5 col9" >42</td>
      <td id="T_652f8_row5_col10" class="data row5 col10" >8</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row6" class="row_heading level0 row6" >Lejre</th>
      <td id="T_652f8_row6_col0" class="data row6 col0" >6</td>
      <td id="T_652f8_row6_col1" class="data row6 col1" >9</td>
      <td id="T_652f8_row6_col2" class="data row6 col2" >11</td>
      <td id="T_652f8_row6_col3" class="data row6 col3" >20</td>
      <td id="T_652f8_row6_col4" class="data row6 col4" >5</td>
      <td id="T_652f8_row6_col5" class="data row6 col5" >0</td>
      <td id="T_652f8_row6_col6" class="data row6 col6" >2</td>
      <td id="T_652f8_row6_col7" class="data row6 col7" >24</td>
      <td id="T_652f8_row6_col8" class="data row6 col8" >5</td>
      <td id="T_652f8_row6_col9" class="data row6 col9" >18</td>
      <td id="T_652f8_row6_col10" class="data row6 col10" >2</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row7" class="row_heading level0 row7" >Lolland</th>
      <td id="T_652f8_row7_col0" class="data row7 col0" >21</td>
      <td id="T_652f8_row7_col1" class="data row7 col1" >11</td>
      <td id="T_652f8_row7_col2" class="data row7 col2" >20</td>
      <td id="T_652f8_row7_col3" class="data row7 col3" >13</td>
      <td id="T_652f8_row7_col4" class="data row7 col4" >6</td>
      <td id="T_652f8_row7_col5" class="data row7 col5" >0</td>
      <td id="T_652f8_row7_col6" class="data row7 col6" >14</td>
      <td id="T_652f8_row7_col7" class="data row7 col7" >34</td>
      <td id="T_652f8_row7_col8" class="data row7 col8" >6</td>
      <td id="T_652f8_row7_col9" class="data row7 col9" >49</td>
      <td id="T_652f8_row7_col10" class="data row7 col10" >6</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row8" class="row_heading level0 row8" >Næstved</th>
      <td id="T_652f8_row8_col0" class="data row8 col0" >39</td>
      <td id="T_652f8_row8_col1" class="data row8 col1" >28</td>
      <td id="T_652f8_row8_col2" class="data row8 col2" >39</td>
      <td id="T_652f8_row8_col3" class="data row8 col3" >35</td>
      <td id="T_652f8_row8_col4" class="data row8 col4" >9</td>
      <td id="T_652f8_row8_col5" class="data row8 col5" >0</td>
      <td id="T_652f8_row8_col6" class="data row8 col6" >14</td>
      <td id="T_652f8_row8_col7" class="data row8 col7" >70</td>
      <td id="T_652f8_row8_col8" class="data row8 col8" >2</td>
      <td id="T_652f8_row8_col9" class="data row8 col9" >59</td>
      <td id="T_652f8_row8_col10" class="data row8 col10" >3</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row9" class="row_heading level0 row9" >Odsherred</th>
      <td id="T_652f8_row9_col0" class="data row9 col0" >15</td>
      <td id="T_652f8_row9_col1" class="data row9 col1" >9</td>
      <td id="T_652f8_row9_col2" class="data row9 col2" >16</td>
      <td id="T_652f8_row9_col3" class="data row9 col3" >10</td>
      <td id="T_652f8_row9_col4" class="data row9 col4" >6</td>
      <td id="T_652f8_row9_col5" class="data row9 col5" >0</td>
      <td id="T_652f8_row9_col6" class="data row9 col6" >7</td>
      <td id="T_652f8_row9_col7" class="data row9 col7" >37</td>
      <td id="T_652f8_row9_col8" class="data row9 col8" >4</td>
      <td id="T_652f8_row9_col9" class="data row9 col9" >41</td>
      <td id="T_652f8_row9_col10" class="data row9 col10" >8</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row10" class="row_heading level0 row10" >Ringsted</th>
      <td id="T_652f8_row10_col0" class="data row10 col0" >18</td>
      <td id="T_652f8_row10_col1" class="data row10 col1" >12</td>
      <td id="T_652f8_row10_col2" class="data row10 col2" >11</td>
      <td id="T_652f8_row10_col3" class="data row10 col3" >16</td>
      <td id="T_652f8_row10_col4" class="data row10 col4" >3</td>
      <td id="T_652f8_row10_col5" class="data row10 col5" >1</td>
      <td id="T_652f8_row10_col6" class="data row10 col6" >7</td>
      <td id="T_652f8_row10_col7" class="data row10 col7" >27</td>
      <td id="T_652f8_row10_col8" class="data row10 col8" >2</td>
      <td id="T_652f8_row10_col9" class="data row10 col9" >29</td>
      <td id="T_652f8_row10_col10" class="data row10 col10" >1</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row11" class="row_heading level0 row11" >Roskilde</th>
      <td id="T_652f8_row11_col0" class="data row11 col0" >66</td>
      <td id="T_652f8_row11_col1" class="data row11 col1" >23</td>
      <td id="T_652f8_row11_col2" class="data row11 col2" >72</td>
      <td id="T_652f8_row11_col3" class="data row11 col3" >41</td>
      <td id="T_652f8_row11_col4" class="data row11 col4" >12</td>
      <td id="T_652f8_row11_col5" class="data row11 col5" >12</td>
      <td id="T_652f8_row11_col6" class="data row11 col6" >21</td>
      <td id="T_652f8_row11_col7" class="data row11 col7" >69</td>
      <td id="T_652f8_row11_col8" class="data row11 col8" >11</td>
      <td id="T_652f8_row11_col9" class="data row11 col9" >65</td>
      <td id="T_652f8_row11_col10" class="data row11 col10" >4</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row12" class="row_heading level0 row12" >Slagelse</th>
      <td id="T_652f8_row12_col0" class="data row12 col0" >37</td>
      <td id="T_652f8_row12_col1" class="data row12 col1" >24</td>
      <td id="T_652f8_row12_col2" class="data row12 col2" >41</td>
      <td id="T_652f8_row12_col3" class="data row12 col3" >27</td>
      <td id="T_652f8_row12_col4" class="data row12 col4" >7</td>
      <td id="T_652f8_row12_col5" class="data row12 col5" >1</td>
      <td id="T_652f8_row12_col6" class="data row12 col6" >13</td>
      <td id="T_652f8_row12_col7" class="data row12 col7" >65</td>
      <td id="T_652f8_row12_col8" class="data row12 col8" >6</td>
      <td id="T_652f8_row12_col9" class="data row12 col9" >71</td>
      <td id="T_652f8_row12_col10" class="data row12 col10" >2</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row13" class="row_heading level0 row13" >Solrød</th>
      <td id="T_652f8_row13_col0" class="data row13 col0" >19</td>
      <td id="T_652f8_row13_col1" class="data row13 col1" >4</td>
      <td id="T_652f8_row13_col2" class="data row13 col2" >21</td>
      <td id="T_652f8_row13_col3" class="data row13 col3" >16</td>
      <td id="T_652f8_row13_col4" class="data row13 col4" >2</td>
      <td id="T_652f8_row13_col5" class="data row13 col5" >6</td>
      <td id="T_652f8_row13_col6" class="data row13 col6" >3</td>
      <td id="T_652f8_row13_col7" class="data row13 col7" >11</td>
      <td id="T_652f8_row13_col8" class="data row13 col8" >0</td>
      <td id="T_652f8_row13_col9" class="data row13 col9" >13</td>
      <td id="T_652f8_row13_col10" class="data row13 col10" >2</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row14" class="row_heading level0 row14" >Sorø</th>
      <td id="T_652f8_row14_col0" class="data row14 col0" >16</td>
      <td id="T_652f8_row14_col1" class="data row14 col1" >11</td>
      <td id="T_652f8_row14_col2" class="data row14 col2" >16</td>
      <td id="T_652f8_row14_col3" class="data row14 col3" >9</td>
      <td id="T_652f8_row14_col4" class="data row14 col4" >4</td>
      <td id="T_652f8_row14_col5" class="data row14 col5" >1</td>
      <td id="T_652f8_row14_col6" class="data row14 col6" >9</td>
      <td id="T_652f8_row14_col7" class="data row14 col7" >19</td>
      <td id="T_652f8_row14_col8" class="data row14 col8" >2</td>
      <td id="T_652f8_row14_col9" class="data row14 col9" >25</td>
      <td id="T_652f8_row14_col10" class="data row14 col10" >5</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row15" class="row_heading level0 row15" >Stevns</th>
      <td id="T_652f8_row15_col0" class="data row15 col0" >8</td>
      <td id="T_652f8_row15_col1" class="data row15 col1" >4</td>
      <td id="T_652f8_row15_col2" class="data row15 col2" >11</td>
      <td id="T_652f8_row15_col3" class="data row15 col3" >7</td>
      <td id="T_652f8_row15_col4" class="data row15 col4" >4</td>
      <td id="T_652f8_row15_col5" class="data row15 col5" >0</td>
      <td id="T_652f8_row15_col6" class="data row15 col6" >5</td>
      <td id="T_652f8_row15_col7" class="data row15 col7" >12</td>
      <td id="T_652f8_row15_col8" class="data row15 col8" >2</td>
      <td id="T_652f8_row15_col9" class="data row15 col9" >19</td>
      <td id="T_652f8_row15_col10" class="data row15 col10" >5</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row16" class="row_heading level0 row16" >Vordingborg</th>
      <td id="T_652f8_row16_col0" class="data row16 col0" >25</td>
      <td id="T_652f8_row16_col1" class="data row16 col1" >18</td>
      <td id="T_652f8_row16_col2" class="data row16 col2" >28</td>
      <td id="T_652f8_row16_col3" class="data row16 col3" >21</td>
      <td id="T_652f8_row16_col4" class="data row16 col4" >8</td>
      <td id="T_652f8_row16_col5" class="data row16 col5" >0</td>
      <td id="T_652f8_row16_col6" class="data row16 col6" >12</td>
      <td id="T_652f8_row16_col7" class="data row16 col7" >48</td>
      <td id="T_652f8_row16_col8" class="data row16 col8" >6</td>
      <td id="T_652f8_row16_col9" class="data row16 col9" >46</td>
      <td id="T_652f8_row16_col10" class="data row16 col10" >2</td>
    </tr>
    <tr>
      <th id="T_652f8_level0_row17" class="row_heading level0 row17" >Total</th>
      <td id="T_652f8_row17_col0" class="data row17 col0" >417</td>
      <td id="T_652f8_row17_col1" class="data row17 col1" >250</td>
      <td id="T_652f8_row17_col2" class="data row17 col2" >460</td>
      <td id="T_652f8_row17_col3" class="data row17 col3" >377</td>
      <td id="T_652f8_row17_col4" class="data row17 col4" >112</td>
      <td id="T_652f8_row17_col5" class="data row17 col5" >30</td>
      <td id="T_652f8_row17_col6" class="data row17 col6" >187</td>
      <td id="T_652f8_row17_col7" class="data row17 col7" >692</td>
      <td id="T_652f8_row17_col8" class="data row17 col8" >89</td>
      <td id="T_652f8_row17_col9" class="data row17 col9" >724</td>
      <td id="T_652f8_row17_col10" class="data row17 col10" >73</td>
    </tr>
  </tbody>
</table>


## Data consistency

### CVR

- Several CVR Penheder does not have an address ID and thus cannot be matched to an address, and some units with an address id cannot be matched to a corresponding address.
- CVR data in csv format needs some initial preprocessing to handle values (typically business names) that include the csv separator (";" or ",").
- The CVR data might include businesses that are no longer operating/open.


### OSM

- OSM tagging can be inconsistent and it is thus expected to miss some locations (e.g. grocery stores tagged with very detailed values instead of just grocery/supermarket)
- While OSM data are updated continuously and generally is up to date, there is no consistent check of whether businesses and other destinations are still open. 
