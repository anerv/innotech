# %%
# ILLUSTRATIONS FOR INNNOTECH REPORT


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
import os
import sys

os.environ["GDAL_DATA"] = os.path.join(
    f"{os.sep}".join(sys.executable.split(os.sep)[:-1]), "Library", "share", "gdal"
)

# %%

##### ILLUSTRATIONS OF SERVICES/DESTINATIONS #####


# Plot services for each subcategory for each data set
study_area = gpd.read_file("../data/processed/adm_boundaries/study_area.gpkg")

data = gpd.read_parquet(
    "../results/data/osm-cvr-combined-aggregated.parquet",
)


figsize = (8, 6)

font_size = 10

destination_col = "service_type"

attribution_text = "(C) OSM, CVR"

color = "#009988"

markersize = 5


destination_dict = {
    "dentist": "Tandlæger",
    "doctor": "Læger",
    "nursery/kindergarten": "Daginstitutioner",
    "pharmacy": "Apoteker",
    "recreation": "Fritid",
    "school": "Skoler",
    "shop": "Dagligvareindkøb",
    "train_station": "Togstationer",
}

for destination, title in destination_dict.items():

    fp = f"../illustrations/illustration_{title}.png"

    _, ax = plt.subplots(figsize=figsize)

    label = destination.replace("_", " ").title()

    study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

    data[data[destination_col] == destination].plot(
        ax=ax,
        color=color,
        markersize=markersize,
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
            location="lower left",
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


### HOUSEHOLDS ###

householddata = gpd.read_parquet(
    "../results/data/all_addresses_bbr.parquet",
)


attribution_text = "(C) KDS"

color = "#AA3377"

markersize = 0.01

title = "Adresser"

fp = f"../illustrations/illustration_adresser.png"

_, ax = plt.subplots(figsize=figsize)

label = destination.replace("_", " ").title()

study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

householddata.plot(ax=ax, color=color, markersize=markersize, alpha=0.3)

ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

ax.set_axis_off()

ax.add_artist(
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


# %%

##### RESULTS #####

results = pd.read_parquet("supermarket_1_otp.parquet")
study_area = gpd.read_file("../data/processed/adm_boundaries/study_area.gpkg")

from shapely.geometry import Point

results["geometry"] = results.apply(
    lambda x: Point(x["from_lon"], x["from_lat"]), axis=1
)


results_gdf = gpd.GeoDataFrame(
    results,
    geometry="geometry",
    crs="EPSG:4326",
)

results_gdf = results_gdf.to_crs("EPSG:25832")

results_gdf["duration_min"] = results_gdf["duration"] / 60
# %%

attribution_text = "Data fra Klimadatastyrelsen og OpenStreetMap"
font_size = 10
fp = "illustration_travel_time_supermarket.png"

fig, ax = plt.subplots(figsize=(10, 10))

study_area.plot(ax=ax, color="none", edgecolor="black", linewidth=0.5)

results_gdf.plot(
    ax=ax,
    column="duration_min",
    cmap="viridis",
    scheme="user_defined",
    classification_kwds={"bins": [15, 30, 60, 120, 180]},
    markersize=0.1,
    figsize=(10, 10),
    legend=True,
    # missing_kwds={
    #     "color": "none",
    #     "label": "Ikke tilgængelig",
    #     "edgecolor": "lightgrey",
    #     "hatch": "//",
    #     "linewidth": 0.2,
    #     "alpha": 0.5,
    # },
    legend_kwds={
        "title": "Rejsetid (minutter)",
        # "bbox_to_anchor": (0.5, 1.05),
        # "loc": "lower center",
        "fontsize": font_size,
        "frameon": False,
    },
)


ax.set_axis_off()

ax.add_artist(
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
cx.add_attribution(ax=ax, text=attribution_text, font_size=font_size)
txt = ax.texts[-1]
txt.set_position([0.99, 0.001])
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


# %%
