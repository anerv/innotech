# %%[markdown]

# Download and process OSM data


# %%
import geopandas as gpd
import pandas as pd
import overpy
import yaml
from src.helper_functions import (
    create_nodes_gdf,
    create_ways_gdf,
    # create_relations_gdf,
    linestring_to_polygon,
    drop_contained_polygons,
    # drop_intersecting_nodes,
    # combine_points_within_distance,
    drop_duplicates_custom,
)

# %%

with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    adm_boundaries_fp = parsed_yaml_file["adm_boundaries_fp"]
    study_area_fp = parsed_yaml_file["study_area_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]

    address_fp_parquet = parsed_yaml_file["address_fp_parquet"]

    hb_codes_dict = parsed_yaml_file["hb_codes_dict"]

# %%

administrative_boundaries = gpd.read_file(adm_boundaries_fp)

region = administrative_boundaries[administrative_boundaries["navn"] == study_area_name]

region = region[["navn", "geometry"]]


region.to_file("../data/processed/adm_boundaries/region.gpkg")

# %%
bbox = region.to_crs("WGS84").total_bounds

bbox_wgs84 = (bbox[1].item(), bbox[0].item(), bbox[3].item(), bbox[2].item())


# %%

queries = {
    "doctor-gp": [
        {"amenity": "doctors"},
        {"amenity": "general_practitioner"},
        {"amenity": "clinic"},
        {"healthcare": "doctor"},
    ],
    "dentist": [
        {"amenity": "dentist"},
        {"healthcare": "dentist"},
    ],
    "pharmacy": [{"amenity": "pharmacy"}],
    "kindergarten": [{"amenity": "kindergarten"}],
    "nursery": [{"amenity": "nursery"}, {"amenity": "childcare"}],
    "school": [{"amenity": "school"}],
    "supermarket": [{"shop": "supermarket"}, {"shop": "grocery"}],
    "discount_supermarket": [{"amenity": "convenience"}],
    "library": [{"amenity": "library"}],
    "sports_facility": [{"amenity": "sports_centre"}, {"club": "sport"}],
    "train_station": [{"railway": "station"}],
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
            joined = api.query(query)

            # Create GeoDataFrames
            nodes_gdf = create_nodes_gdf(joined.nodes)
            ways_gdf = create_ways_gdf(joined.ways)

            # Reproject to EPSG:25832 if necessary
            if not nodes_gdf.empty:
                # Drop nodes where the key is none (these nodes belong to a way)
                nodes_gdf = nodes_gdf[nodes_gdf[key].notna()]
                nodes_gdf = nodes_gdf.to_crs("EPSG:25832")

                nodes_gdf = nodes_gdf[
                    [
                        "id",
                        key,
                        "geometry",
                    ]
                ]

            if not ways_gdf.empty:

                ways_gdf["geometry"] = ways_gdf["geometry"].apply(linestring_to_polygon)
                ways_gdf = ways_gdf[ways_gdf["geometry"].notnull()]

                ways_gdf = ways_gdf.to_crs("EPSG:25832")

                # Drop polygons completely contained by other polygons
                ways_gdf = drop_contained_polygons(ways_gdf, drop=True)

                ways_gdf = ways_gdf[
                    [
                        "id",
                        key,
                        "geometry",
                    ]
                ]
                ways_gdf[key] = value

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

    all_data = gpd.clip(all_data, region)

    all_data["service_type"] = category

    all_data.to_file(f"../data/processed/osm/{category}_osm.gpkg", driver="GPKG")

    all_osm.append(all_data)

all_osm_gdf = pd.concat(all_osm, ignore_index=True)
all_osm_gdf = all_osm_gdf.reset_index(drop=True)

all_osm_gdf = all_osm_gdf[["id", "service_type", "geometry"]]
all_osm_gdf.rename(columns={"id": "osm_id"}, inplace=True)


# %%
# fill out hb codes
all_osm_gdf["hb_kode"] = all_osm_gdf["service_type"].map(
    {k: v for k, v in hb_codes_dict.items()}
)

assert (
    all_osm_gdf["hb_kode"].notnull().all()
), "Some service types are not in the hb_codes_dict"

all_osm_gdf.drop_duplicates(subset=["osm_id", "service_type"], inplace=True)

# %%

#  match to closest addresses
addresses = gpd.read_parquet(address_fp_parquet)  # adresseIdentificerer
# addresses.drop_duplicates(subset=["adresseIdentificerer"], inplace=True)

join_threshold = 300  # meters
assert all_osm_gdf.crs == addresses.crs, "CRS mismatch between all_osm and addresses"

# joined = gpd.sjoin_nearest(
#     all_osm_gdf,
#     addresses,
#     how="left",
#     max_distance=join_threshold,
#     lsuffix="osm",
#     rsuffix="addr",
# )

joined = gpd.sjoin_nearest(
    all_osm_gdf,
    addresses,
    how="left",
    max_distance=join_threshold,
    lsuffix="osm",
    rsuffix="addr",
)

# Handle ties by random selection (many addresses can be close to the same OSM point)
# Group by the index of gdf1 and randomly select one row from each group
joined = joined.groupby(joined.index).apply(lambda x: x.sample(1) if len(x) > 1 else x)

joined.reset_index(drop=True, inplace=True)

joined["Adr_id"] = None
joined.Adr_id = joined.adresseIdentificerer

assert joined["Adr_id"].notnull().all(), "Some OSM data are not matched to addresses"

# %%
joined = joined[
    [
        "osm_id",
        "service_type",
        "hb_kode",
        "Adr_id",
        # "enh023Boligtype",
        "geometry",
    ]
]

# %%

joined.to_file("../data/processed/osm/all_osm_services.gpkg", driver="GPKG")
# %%
