# %%[markdown]
# Download and process OSM data


# %%
import geopandas as gpd
import overpy

# %%
api = overpy.Overpass()
result = api.query("""node["name"="Gielgen"];out body;""")
# %%
len(result.nodes)
len(result.ways)
len(result.relations)
# %%

# TODO: find extent of the area of interest
administrative_boundaries = gpd.read_file(
    "../data/input/DK_AdministrativeUnit/au_inspire.gpkg", layer="administrativeunit"
)

region_sj = administrative_boundaries[
    (administrative_boundaries.nationallevel == "2ndOrder")
    & (administrative_boundaries.name_gn_spell_spellofna_text == "Region Sjælland")
]

region_sj.to_file("../data/processed/adm_boundaries/region_sj.gpkg")

bbox = region_sj.total_bounds

# %%

# TODO: get the OSM data for the area of interest

# TODO: convert the OSM data to a GeoDataFrame
# TODO: Process data - make sure that locations are active + transform to EPSG:25832 + transform to point geometries

# - [ ] doctors
# - [ ] pharmacies
# - [ ] børnehave
# - [ ] vuggestue
# - [ ] skole
# - [ ] supermarkeder
# - [ ] Swimming halls,
# - [ ] football,
# - [ ] golf courses,
# - [ ] forests,
# - [ ] cinema,
# - [ ] bowling,
# - [ ] sports clubs
