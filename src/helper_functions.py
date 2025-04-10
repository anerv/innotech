import geopandas as gpd
import pandas as pd
import overpy
from shapely.geometry import Point, Polygon, LineString


# Function to create a GeoDataFrame from nodes
def create_nodes_gdf(nodes):
    if not nodes:
        return gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    data = []
    for node in nodes:
        point = Point(node.lon, node.lat)
        tags = node.tags
        tags["id"] = node.id
        data.append({"geometry": point, **tags})
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


# Function to create a GeoDataFrame from ways
def create_ways_gdf(ways):
    if not ways:
        return gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    data = []
    for way in ways:
        coords = [(node.lon, node.lat) for node in way.nodes]
        line = LineString(coords)
        tags = way.tags
        tags["id"] = way.id
        data.append({"geometry": line, **tags})
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


# Function to create a GeoDataFrame from relations
def create_relations_gdf(overpass_result, relations):
    if not relations:
        return gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    data = []
    for relation in relations:
        coords = []
        for member in relation.members:
            if isinstance(member, overpy.RelationWay):
                way = overpass_result.get_way(member.ref)
                coords.extend([(node.lon, node.lat) for node in way.nodes])
            elif isinstance(member, overpy.RelationNode):
                node = overpass_result.get_node(member.ref)
                coords.append((node.lon, node.lat))
        if len(coords) > 2:
            poly = Polygon(coords)
            tags = relation.tags
            tags["id"] = relation.id
            data.append({"geometry": poly, **tags})
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


def drop_intersecting_nodes(nodes_gdf, ways_gdf):

    # Function to check if a node intersects with any linestring
    def node_intersects(node):
        return ways_gdf.intersects(node).any()

    # Filter nodes that do not intersect with any linestring
    filtered_nodes_gdf = nodes_gdf[~nodes_gdf.geometry.apply(node_intersects)].copy()

    return filtered_nodes_gdf


def combine_points_within_distance(points_gdf, distance=200):
    """
    Combines all point geometries within a specified distance into one point.

    Parameters:
    points_gdf (geopandas.GeoDataFrame): GeoDataFrame containing the point geometries.
    distance (float): The distance in the same unit as the CRS of the GeoDataFrame.

    Returns:
    geopandas.GeoDataFrame: GeoDataFrame with combined points.
    """
    # Create a buffer around each point
    buffered_points = points_gdf.geometry.buffer(distance)

    # Create a list to store the combined points
    combined_points = []

    # Iterate through the buffered points
    for i, buffer in enumerate(buffered_points):
        # Find all points within the current buffer
        points_within = points_gdf[points_gdf.geometry.within(buffer)]

        # If there are points within the buffer, combine them into one point
        if not points_within.empty:
            # Calculate the centroid of the combined points
            combined_point = points_within.geometry.union_all().centroid
            combined_points.append(combined_point)

            # Remove the combined points from the original GeoDataFrame
            points_gdf = points_gdf.drop(points_within.index)

    # Create a new GeoDataFrame with the combined points
    combined_points_gdf = gpd.GeoDataFrame(geometry=combined_points, crs=points_gdf.crs)

    return combined_points_gdf


# Define the styling function for NaN values
def highlight_nan(x):
    return ["color: grey" if pd.isna(v) else "" for v in x]


# Define the styling function for max values in each row
def highlight_max(x):
    is_max = x == x.max()
    return ["background-color: yellow" if v else "" for v in is_max]
