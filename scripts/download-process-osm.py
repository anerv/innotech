# %%[markdown]

# Download and process OSM data


# %%
import geopandas as gpd
import pandas as pd
import overpy
from src.helper_functions import (
    create_nodes_gdf,
    create_ways_gdf,
    # create_relations_gdf,
    # drop_intersecting_nodes,
    # combine_points_within_distance,
)

# %%

administrative_boundaries = gpd.read_file(
    "../data/input/DK_AdministrativeUnit/au_inspire.gpkg", layer="administrativeunit"
)

region_sj = administrative_boundaries[
    (administrative_boundaries.nationallevel == "2ndOrder")
    & (administrative_boundaries.name_gn_spell_spellofna_text == "Region Sjælland")
]

region_sj.to_file("../data/processed/adm_boundaries/region_sj.gpkg")

# %%
bbox = region_sj.to_crs("WGS84").total_bounds

bbox_wgs84 = (bbox[1].item(), bbox[0].item(), bbox[3].item(), bbox[2].item())


# %%


queries = {
    "doctor-gp": [
        {"amenity": "doctors"},
        {"amenity": "general_practitioner"},
        {"amenity": "clinic"},
        {"healthcare": "doctor"},
    ],
    # "doctor-specialist": ,
    "dentist": [
        {"amenity": "dentist"},
        {"healthcare": "dentist"},
    ],
    # "physiotherapist": ,
    "pharmacy": [{"amenity": "pharmacy"}],
    "kindergarten": [{"amenity": "kindergarten"}],
    "nursery": [{"amenity": "nursery"}, {"amenity": "childcare"}],
    "school": [{"amenity": "school"}],
    "grocery_store": [{"shop": "grocery"}],
    "supermarket": [{"shop": "supermarket"}, {"amenity": "convenience"}],
    "theatre": [{"amenity": "theatre"}],
    "library": [{"amenity": "library"}],
    "sports_facility": [{"amenity": "sports_centre"}, {"club": "sport"}],
    "fitness": [
        {"leisure": "fitness_centre"},
        {"amenity": "fitness_centre"},
        {"amenity": "gym"},
    ],
    "movie_theater": [{"amenity": "cinema"}, {"amenity": "movie_theater"}],
    "swimming_hall": [
        {"leisure": "swimming_pool"},
        {"amenity": "swimming_pool"},
        {"sport": "swimming"},
    ],
    "football": [{"sport": "football"}, {"sport": "soccer"}],
    "golf_course": [{"sport": "golf"}, {"leisure": "golf_course"}],
    "bowling": [{"leisure": "bowling_alley"}],
    # "forest": [{"landuse": "forest"}, {"natural": "wood"}],
}


# %%

# connect to the overpass API
api = overpy.Overpass()

all_osm = []

for category, query_list in queries.items():
    data_list = []

    for query_dict in query_list:
        for key, value in query_dict.items():
            query = f"""
            (
            node[{key}={value}]({bbox_wgs84[0]},{bbox_wgs84[1]},{bbox_wgs84[2]},{bbox_wgs84[3]});
            way[{key}={value}]({bbox_wgs84[0]},{bbox_wgs84[1]},{bbox_wgs84[2]},{bbox_wgs84[3]});
            relation[{key}={value}]({bbox_wgs84[0]},{bbox_wgs84[1]},{bbox_wgs84[2]},{bbox_wgs84[3]});
            );
            out body;
            >;
            out skel qt;
            """

            # Fetch the data
            result = api.query(query)

            # Create GeoDataFrames
            nodes_gdf = create_nodes_gdf(result.nodes)
            ways_gdf = create_ways_gdf(result.ways)

            # Reproject to EPSG:25832 if necessary
            if not nodes_gdf.empty:
                # Drop nodes where the key is none (these nodes belong to a way)
                nodes_gdf = nodes_gdf[nodes_gdf[key].notna()]
                nodes_gdf = nodes_gdf.to_crs("EPSG:25832")

            if not ways_gdf.empty:

                ways_gdf["geometry"] = ways_gdf.geometry.polygonize()
                ways_gdf = ways_gdf.explode(index_parts=True).reset_index(drop=True)

                ways_gdf = ways_gdf.to_crs("EPSG:25832")
                ways_centroids = ways_gdf.copy()
                ways_centroids["geometry"] = ways_gdf.geometry.centroid
            else:
                ways_centroids = None

            if nodes_gdf.empty and (ways_centroids is None):
                print(f"No data found for {key} = {value}")
                continue

            # Combine nodes and ways if both exist
            if not nodes_gdf.empty and ways_centroids is not None:

                combined_gdf = pd.concat([nodes_gdf, ways_centroids], ignore_index=True)

                assert len(combined_gdf) == len(nodes_gdf) + len(ways_centroids)

            elif not nodes_gdf.empty and ways_centroids is None:
                # Only nodes exist
                combined_gdf = nodes_gdf

            elif nodes_gdf.empty and ways_centroids is not None:
                # Only ways exist
                combined_gdf = ways_centroids

            data_list.append(combined_gdf)

    if not data_list:
        print(f"No data found for {category}")

    if len(data_list) == 0:
        print(f"No data found for {category}")
        continue

    all_data = pd.concat(data_list, ignore_index=True)
    all_data = all_data.reset_index(drop=True)
    # all_data = all_data.drop_duplicates(subset=["geometry"])

    all_data = gpd.clip(all_data, region_sj)

    all_data["destination_type"] = category

    all_data.to_file(f"../data/processed/osm/{category}_osm.gpkg", driver="GPKG")

    all_osm.append(all_data)

all_osm = pd.concat(all_osm, ignore_index=True)
all_osm = all_osm.reset_index(drop=True)
all_osm.to_file("../data/processed/osm/all_osm_destinations.gpkg", driver="GPKG")


# %%
