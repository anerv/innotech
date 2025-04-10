# %%[markdown]

# Download and process OSM data


# %%
import geopandas as gpd
import pandas as pd
import overpy
from src.helper_functions import (
    create_nodes_gdf,
    create_ways_gdf,
    create_relations_gdf,
    drop_intersecting_nodes,
    combine_points_within_distance,
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
    "sports_facility": [{"amenity": "sports_centre"}],
    "fitness": [
        {"leisure": "fitness_centre"},
        {"amenity": "fitness_centre"},
        {"amenity": "gym"},
    ],
    "sports_club": [{"club": "sport"}],
    "movie_theater": [{"amenity": "cinema"}, {"amenity": "movie_theater"}],
    "swimming_hall": [
        {"leisure": "swimming_pool"},
        {"amenity": "swimming_pool"},
        {"sport": "swimming"},
    ],
    "football": [{"sport": "football"}, {"sport": "soccer"}],
    "golf_course": [{"sport": "golf"}, {"leisure": "golf_course"}],
    "bowling": [{"leisure": "bowling_alley"}],
    "forest": [{"landuse": "forest"}, {"natural": "wood"}],
}


# %%

# connect to the overpass API
api = overpy.Overpass()


# Define the query
tag_dict = {"amenity": "school"}

for category, query_list in queries.items():

    data_list = []

    # for key, value in query_dict.items():
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
            # relations_gdf = create_relations_gdf(result, result.relations)

            # filter out nodes that are part of ways
            filtered_nodes_gdf = drop_intersecting_nodes(nodes_gdf, ways_gdf)

            if len(filtered_nodes_gdf) > 0:
                # reproject to EPSG:25832
                filtered_nodes_gdf.to_crs("EPSG:25832", inplace=True)

            else:
                filtered_nodes_gdf.crs = "EPSG:25832"

            if len(ways_gdf) > 0:
                ways_gdf.to_crs("EPSG:25832", inplace=True)
                # relations_gdf.to_crs("EPSG:25832", inplace=True)

                ways_centroids = ways_gdf.copy()
                ways_centroids["geometry"] = ways_gdf.geometry.centroid

            if ways_gdf.empty and filtered_nodes_gdf.empty:

                print(f"No data found for {key} = {value}")
                continue

            else:
                combined_gdf = pd.concat(
                    [filtered_nodes_gdf, ways_centroids], ignore_index=True
                )
                combined_gdf = combined_gdf.reset_index(drop=True)

                # combine nodes within 200 meters
                aggregated_gdf = combine_points_within_distance(
                    combined_gdf, distance=200
                )

                data_list.append(aggregated_gdf)

    if len(data_list) == 0:
        print(f"No data found for {category}")
        continue

    all_data = pd.concat(data_list, ignore_index=True)
    all_data = all_data.reset_index(drop=True)
    all_data["category"] = category
    all_data = all_data.drop_duplicates(subset=["geometry"])
    all_data.to_file(f"../data/processed/osm_data/{category}_osm.gpkg", driver="GPKG")

# %%
