# Comparison of CVR and OSM destination data

## Data completeness

- TODO: 2 tables
- Combined map for each category
- Hex map

<style type="text/css">
#T_94799 th {
  font-weight: bold;
}
#T_94799_row0_col0, #T_94799_row0_col2, #T_94799_row1_col0, #T_94799_row1_col2, #T_94799_row2_col0, #T_94799_row2_col2, #T_94799_row3_col0, #T_94799_row3_col1, #T_94799_row4_col0, #T_94799_row4_col1, #T_94799_row5_col0, #T_94799_row5_col2 {
  text-align: left;
  font-size: 12px;
  width: 100px;
}
#T_94799_row0_col1, #T_94799_row1_col1, #T_94799_row2_col1, #T_94799_row3_col2, #T_94799_row4_col2, #T_94799_row5_col1 {
  background-color: yellow;
  text-align: left;
  font-size: 12px;
  width: 100px;
}
</style>
<table id="T_94799" style="width: 50%; border-collapse: collapse;">
  <caption>Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets</caption>
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_94799_level0_col0" class="col_heading level0 col0" >cvr_addresses</th>
      <th id="T_94799_level0_col1" class="col_heading level0 col1" >cvr_all</th>
      <th id="T_94799_level0_col2" class="col_heading level0 col2" >osm</th>
    </tr>
    <tr>
      <th class="index_name level0" >destination_type_main</th>
      <th class="blank col0" >&nbsp;</th>
      <th class="blank col1" >&nbsp;</th>
      <th class="blank col2" >&nbsp;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_94799_level0_row0" class="row_heading level0 row0" >doctors</th>
      <td id="T_94799_row0_col0" class="data row0 col0" >1108</td>
      <td id="T_94799_row0_col1" class="data row0 col1" >1135</td>
      <td id="T_94799_row0_col2" class="data row0 col2" >88</td>
    </tr>
    <tr>
      <th id="T_94799_level0_row1" class="row_heading level0 row1" >nurseries/kindergartens</th>
      <td id="T_94799_row1_col0" class="data row1 col0" >214</td>
      <td id="T_94799_row1_col1" class="data row1 col1" >223</td>
      <td id="T_94799_row1_col2" class="data row1 col2" >160</td>
    </tr>
    <tr>
      <th id="T_94799_level0_row2" class="row_heading level0 row2" >pharmacies</th>
      <td id="T_94799_row2_col0" class="data row2 col0" >108</td>
      <td id="T_94799_row2_col1" class="data row2 col1" >116</td>
      <td id="T_94799_row2_col2" class="data row2 col2" >75</td>
    </tr>
    <tr>
      <th id="T_94799_level0_row3" class="row_heading level0 row3" >recreation</th>
      <td id="T_94799_row3_col0" class="data row3 col0" >390</td>
      <td id="T_94799_row3_col1" class="data row3 col1" >400</td>
      <td id="T_94799_row3_col2" class="data row3 col2" >1142</td>
    </tr>
    <tr>
      <th id="T_94799_level0_row4" class="row_heading level0 row4" >schools</th>
      <td id="T_94799_row4_col0" class="data row4 col0" >308</td>
      <td id="T_94799_row4_col1" class="data row4 col1" >314</td>
      <td id="T_94799_row4_col2" class="data row4 col2" >380</td>
    </tr>
    <tr>
      <th id="T_94799_level0_row5" class="row_heading level0 row5" >shops</th>
      <td id="T_94799_row5_col0" class="data row5 col0" >598</td>
      <td id="T_94799_row5_col1" class="data row5 col1" >624</td>
      <td id="T_94799_row5_col2" class="data row5 col2" >427</td>
    </tr>
  </tbody>
</table>


![alt text](results/maps/hex-grid-comparison-doctors.png "Title")

## Data consistency

### CVR

Several CVR Penheder does not have an address ID and thus cannot be matched to an address, and some units with an address id cannot be matched to a corresponding address. 

Processing of ; 

- TODO: Include fitness centers???

### OSM

Tags

- Document issues (e.g. missing CVR codes, categories that do not map perfectly between CVR and OSM, missing addresses and geometries in CVR)