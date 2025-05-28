import geopandas as gpd
import pandas as pd
import overpy
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
import h3
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
import numpy as np
from shapely.ops import transform


def get_service_type(nace_code, nace_dict):
    for service_type, codes in nace_dict.items():
        if nace_code in codes:
            return service_type
    return None


def get_nace_code(service_type, nace_dict):
    for type, codes in nace_dict.items():
        if service_type == type:
            return codes[0]  # return the first code in the list
    return None


def remove_z(geometry):
    if geometry.has_z:
        return transform(lambda x, y, z=None: (x, y), geometry)
    return geometry


def drop_duplicates_custom(gdf, subset_columns, value_column):
    """
    Drop duplicates in a GeoDataFrame based on a subset of columns and custom criteria.

    Parameters:
    - gdf: GeoDataFrame
      The input GeoDataFrame.
    - subset_columns: list of str
      The columns to consider for identifying duplicates.
    - value_column: str
      The column to use for determining which duplicate row to keep.

    Returns:
    - GeoDataFrame
      The GeoDataFrame with duplicates dropped according to the specified criteria.
    """
    # Sort the GeoDataFrame by the value_column to prioritize rows with 'E', then '2', then the lowest value
    gdf = gdf.sort_values(by=value_column, key=lambda x: x.map({"E": 1, "2": 2}.get))

    # Drop duplicates based on the subset_columns, keeping the first occurrence
    gdf = gdf.drop_duplicates(subset=subset_columns, keep="first")

    return gdf


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


# def drop_intersecting_nodes(nodes_gdf, ways_gdf):

#     # Function to check if a node intersects with any linestring
#     def node_intersects(node):
#         return ways_gdf.intersects(node).any()

#     # Filter nodes that do not intersect with any linestring
#     filtered_nodes_gdf = nodes_gdf[~nodes_gdf.geometry.apply(node_intersects)].copy()

#     return filtered_nodes_gdf


def combine_points_within_distance(points_gdf, distance=200, inherit_columns=None):
    """
    Combines all point geometries within a specified distance into one point.

    Parameters:
    points_gdf (geopandas.GeoDataFrame): GeoDataFrame containing the point geometries.
    distance (float): The distance in the same unit as the CRS of the GeoDataFrame.
    inherit_columns (list of str): Columns whose values will be inherited from the first point within each buffer.

    Returns:
    geopandas.GeoDataFrame: GeoDataFrame with combined points.
    """
    if inherit_columns is None:
        inherit_columns = []

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

            # Create a new row with the combined point and inherited values
            combined_row = {
                "geometry": combined_point,
                **{column: points_within[column].iloc[0] for column in inherit_columns},
            }
            combined_points.append(combined_row)

            # Remove the combined points from the original GeoDataFrame
            points_gdf = points_gdf.drop(points_within.index)

    # Create a new GeoDataFrame with the combined points
    combined_points_gdf = gpd.GeoDataFrame(combined_points, crs=points_gdf.crs)

    return combined_points_gdf


def aggregate_points_by_distance(
    gdf,
    distance_threshold=50,
    destination_type_column="destination_type_main",
    inherit_columns=None,
):
    """
    Aggregates point geometries in a GeoDataFrame into one point if they are within a user-specified distance threshold
    and share the same value for the column "destination-type".

    Parameters:
    gdf (geopandas.GeoDataFrame): The input GeoDataFrame containing point geometries.
    distance_threshold (float): The distance threshold for aggregating points.
    destination_type_column (str): The column name for the destination type.
    inherit_columns (list of str): Columns whose values will be inherited from the first point within each buffer.

    Returns:
    geopandas.GeoDataFrame: The aggregated GeoDataFrame.
    """
    if inherit_columns is None:
        inherit_columns = []

    # Ensure the GeoDataFrame is in a projected coordinate system
    if gdf.crs is None or gdf.crs.is_geographic:
        raise ValueError("GeoDataFrame must be in a projected coordinate system.")

    aggregated_points = []

    # Group by destination-type
    for destination_type, group in gdf.groupby(destination_type_column):
        # Combine points within the distance threshold for each group
        combined_gdf = combine_points_within_distance(
            group, distance=distance_threshold, inherit_columns=inherit_columns
        )

        # Add the destination-type column to the combined points
        combined_gdf[destination_type_column] = destination_type

        # Append the combined points to the aggregated points list
        aggregated_points.append(combined_gdf)

    # Concatenate all aggregated points into a single GeoDataFrame
    aggregated_gdf = gpd.GeoDataFrame(
        pd.concat(aggregated_points, ignore_index=True), crs=gdf.crs
    )

    return aggregated_gdf


# Define the styling function for NaN values
def highlight_nan(x):
    return ["color: grey" if pd.isna(v) else "" for v in x]


def highlight_zero(x):
    return ["color: red" if v == 0 else "" for v in x]


# Define the styling function for max values in each row
def highlight_max(x):
    is_max = x == x.max()
    return ["background-color: yellow" if v else "" for v in is_max]


def replace_nan_with_dash(val):
    return "-" if pd.isna(val) else val


def highlight_next_max(row, color="lightyellow"):
    attr = f"background-color: {color}"
    sorted_values = row.sort_values(ascending=False)
    if len(sorted_values) > 1:
        second_highest_value = sorted_values.iloc[1]
        return [attr if val == second_highest_value else "" for val in row]
    return [""] * len(row)


def count_destinations_in_municipalities(
    municipalities, muni_id_col, destinations, destination_col, csv_fp, html_fp
):

    muni_destinations = municipalities.sjoin(
        destinations, how="inner", predicate="intersects"
    )

    muni_service_counts = (
        muni_destinations.groupby([muni_id_col, destination_col])
        .size()
        .reset_index(name="count")
    )

    muni_service_pivot = muni_service_counts.pivot(
        index="navn", columns=destination_col, values="count"
    ).fillna(0)

    muni_service_pivot.loc["Total"] = muni_service_pivot.sum()

    muni_service_pivot = muni_service_pivot.astype(int)
    df_styled = (
        muni_service_pivot.style.apply(
            highlight_zero, subset=muni_service_pivot.columns, axis=1
        )
        .set_table_styles(
            [
                {"selector": "th", "props": [("font-weight", "bold")]},
            ]
        )
        .set_properties(
            **{"text-align": "right", "font-size": "12px", "width": "100px"}
        )
        .set_caption("Municipal service counts")
    )
    df_styled = df_styled.set_table_attributes(
        'style="width: 50%; border-collapse: collapse;"'
    )

    # muni_subset_with_counts = muni_subset.merge(
    #     muni_service_pivot, left_on="navn", right_index=True, how="left"
    # )

    # muni_subset_with_counts = muni_subset_with_counts.fillna(0)

    muni_service_pivot.to_csv(csv_fp, index=True)

    df_styled.to_html(
        html_fp,
    )

    return df_styled


def plot_destinations(
    data,
    study_area,
    destination_col,
    destination,
    color,
    font_size,
    fp,
    attribution_text,
    title,
    figsize=(7, 7),
    markersize=10,
):

    _, ax = plt.subplots(figsize=figsize)

    label = destination.replace("_", " ").title()

    study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

    data[data[destination_col] == destination].plot(
        ax=ax, color=color, markersize=markersize, label=label, legend=True
    )

    # TODO: fix legend position so that it is aligned with scale bar and attribution text
    ax.legend(
        loc="lower left",
        fontsize=font_size,
        # title_fontsize=10,
        # title="OSM",
        markerscale=2,
        frameon=False,
        bbox_to_anchor=(-0.1, -0.01),
    )

    ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

    ax.set_axis_off()

    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower center",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )
    cx.add_attribution(ax=ax, text=attribution_text, font_size=font_size)
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    plt.savefig(
        fp,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()
    plt.close()


def plot_destinations_combined(
    data1,
    data2,
    data1_label,
    data2_label,
    study_area,
    destination_col,
    destination,
    color1,
    color2,
    font_size,
    fp,
    attribution_text,
    title,
    figsize=(7, 7),
    markersize=6,
):

    _, ax = plt.subplots(figsize=figsize)

    label1 = destination.replace("_", " ").title() + " - " + data1_label
    label2 = destination.replace("_", " ").title() + " - " + data2_label

    study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

    data1[data1[destination_col] == destination].plot(
        ax=ax, color=color1, markersize=markersize, label=label1, legend=True, alpha=0.5
    )

    data2[data2[destination_col] == destination].plot(
        ax=ax, color=color2, markersize=markersize, label=label2, legend=True, alpha=0.5
    )

    # TODO: fix legend position so that it is aligned with scale bar and attribution text
    ax.legend(
        loc="lower left",
        fontsize=font_size,
        # title_fontsize=10,
        # title="OSM",
        markerscale=2,
        frameon=False,
        bbox_to_anchor=(-0.1, -0.01),
    )

    ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

    ax.set_axis_off()

    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower center",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )
    cx.add_attribution(ax=ax, text=attribution_text, font_size=font_size)
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    plt.savefig(
        fp,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    plt.close()


def plot_destinations_combined_subplot(
    data1,
    data2,
    data1_label,
    data2_label,
    study_area,
    destination_col,
    color1,
    color2,
    font_size,
    fp,
    attribution_text,
    figsize=(15, 10),
    markersize=6,
):

    unique_destinations = set(data1[destination_col].unique()).union(
        data2[destination_col].unique()
    )

    unique_destinations = sorted(unique_destinations)

    _, axes = plt.subplots(
        nrows=2, ncols=math.ceil(len(unique_destinations) / 2), figsize=figsize
    )

    axes = axes.flatten()

    if len(axes) > len(unique_destinations):

        axes[-1].axis("off")

    for i, destination in enumerate(unique_destinations):

        title = f"{destination.replace('_', ' ').title()}"

        ax = axes[i]

        study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

        data1[data1[destination_col] == destination].plot(
            ax=ax,
            color=color1,
            markersize=markersize,
            label=data1_label,
            legend=True,
            alpha=0.5,
        )

        data2[data2[destination_col] == destination].plot(
            ax=ax,
            color=color2,
            markersize=markersize,
            label=data2_label,
            legend=True,
            alpha=0.5,
        )

        ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

        ax.set_axis_off()

    # TODO: fix legend position so that it is aligned with scale bar and attribution text
    middle_ax = axes[(len(axes) // 2) - 1]
    middle_ax.legend(
        loc="upper right",
        fontsize=font_size,
        # title_fontsize=10,
        # title="OSM",
        markerscale=3,
        frameon=False,
        bbox_to_anchor=(1, 1),
    )

    axes[len(axes) // 2].add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower left",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )

    cx.add_attribution(
        ax=axes[len(unique_destinations) - 1],
        text=attribution_text,
        font_size=font_size,
    )
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    plt.savefig(
        fp,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    plt.close()


def create_hex_grid(polygon_gdf, hex_resolution, crs, buffer_dist):

    # Inspired by https://stackoverflow.com/questions/51159241/how-to-generate-shapefiles-for-h3-hexagons-in-a-particular-area

    poly_bounds = polygon_gdf.buffer(buffer_dist).to_crs("EPSG:4326").total_bounds

    latlng_poly = h3.LatLngPoly(
        [
            (poly_bounds[0], poly_bounds[1]),
            (poly_bounds[0], poly_bounds[3]),
            (poly_bounds[2], poly_bounds[3]),
            (poly_bounds[2], poly_bounds[1]),
        ]
    )

    hex_list = []
    hex_list.extend(h3.polygon_to_cells(latlng_poly, res=hex_resolution))

    # Create hexagon data frame
    hex_pd = pd.DataFrame(hex_list, columns=["hex_id"])

    # Create hexagon geometry and GeoDataFrame
    hex_pd["latlng_geometry"] = [
        h3.cells_to_h3shape([x], tight=True) for x in hex_pd["hex_id"]
    ]

    hex_pd["geometry"] = hex_pd["latlng_geometry"].apply(lambda x: Polygon(x.outer))

    grid = gpd.GeoDataFrame(hex_pd)

    grid.set_crs("4326", inplace=True).to_crs(crs, inplace=True)

    grid["grid_id"] = grid.hex_id

    grid = grid[["grid_id", "geometry"]]

    return grid


def count_destinations_in_hex_grid(gdf, hex_grid, destination_col):

    joined = gpd.sjoin(hex_grid, gdf, how="left", predicate="intersects")

    counts = (
        joined.groupby(["grid_id", destination_col])[destination_col]
        .count()
        .reset_index(name="count")
    )

    # Pivot the counts DataFrame to create a column for each destination type
    counts_pivot = counts.pivot(
        index="grid_id", columns=destination_col, values="count"
    ).fillna(0)

    # Merge the pivoted counts back into the hex grid
    hex_grid = hex_grid.merge(
        counts_pivot, left_on="grid_id", right_index=True, how="left"
    )

    # Fill NaN values with 0 for missing destination counts
    hex_grid = hex_grid.fillna(0)

    return hex_grid


def plot_hex_summaries(
    combined_grid,
    study_area,
    destination,
    fp,
    figsize=(20, 10),
    font_size=14,
    attribution_text="(C) OSM, CVR",
    titles=[
        "OSM",
        "CVR",
        "Difference (OSM - CVR)",
    ],
    cmaps=[
        "viridis",
        "viridis",
        "RdBu_r",
    ],
):

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=figsize)

    axes = axes.flatten()

    suptitle = f"{destination.replace('_', ' ').title()}"

    viridis_norm = plt.Normalize(
        vmin=0,
        vmax=max(
            combined_grid[destination + "_osm"].max(),
            combined_grid[destination + "_cvr"].max(),
        ),
    )

    largest_abs_value = combined_grid[destination + "_diff"].abs().max()
    divnorm = colors.TwoSlopeNorm(
        vmin=-largest_abs_value,
        vcenter=0,
        vmax=largest_abs_value,
    )

    norms = [viridis_norm, viridis_norm, divnorm]

    for j, col in enumerate(["_osm", "_cvr", "_diff"]):

        ax = axes[j]

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3.5%", pad="1%")
        cax.tick_params(labelsize=font_size)

        study_area.plot(ax=ax, color="white", edgecolor="black")

        grid_subset = combined_grid[
            (combined_grid[destination + "_osm"] > 0)
            | (combined_grid[destination + "_cvr"] > 0)
        ].copy()

        grid_subset[destination + "_osm"] = grid_subset[destination + "_osm"].replace(
            {0: np.nan}
        )

        grid_subset[destination + "_cvr"] = grid_subset[destination + "_cvr"].replace(
            {0: np.nan}
        )

        grid_subset.plot(
            cax=cax,
            ax=ax,
            column=destination + col,
            cmap=cmaps[j],
            norm=norms[j],
            # legend=True,
            alpha=0.5,
            # legend_kwds={
            #     "shrink": 0.9,
            #     "aspect": 30,
            # },
        )

        sm = plt.cm.ScalarMappable(
            cmap=cmaps[j],
            norm=norms[j],
        )
        sm._A = []
        cbar = fig.colorbar(sm, cax=cax)
        cbar.outline.set_visible(False)

        if j == 2:
            min_val = -largest_abs_value
            max_val = largest_abs_value
            cbar.set_ticks(
                [min_val, round(min_val / 2), 0, round(max_val / 2), max_val]
            )

        ax.set_axis_off()
        ax.set_title(titles[j], fontsize=font_size)

    fig.suptitle(
        suptitle,
        fontsize=font_size + 4,
        fontdict={"fontweight": "bold"},
    )

    axes[0].add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower left",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )

    cx.add_attribution(ax=axes[-1], text=attribution_text, font_size=font_size)
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    plt.savefig(
        fp,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    plt.close()


def linestring_to_polygon(geom):
    # Only convert if LineString is closed
    if geom.is_ring:
        return Polygon(geom)
    else:
        return None  # or raise a warning / try to close it manually


def drop_contained_polygons(gdf, drop=True):
    """
    Find polygons that are fully contained by another polygon in the same GeoDataFrame.
    """
    contained_indices = set()

    for idx, geom in gdf.geometry.items():
        others = gdf.drop(idx)
        for other_idx, other_geom in others.geometry.items():
            if geom.within(other_geom):
                contained_indices.add(idx)
                break

    if drop:
        return gdf.drop(index=contained_indices)
    else:
        return list(contained_indices)
