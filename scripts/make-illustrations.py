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


# Plot services for each subcategory for each data set
study_area = gpd.read_file("../data/processed/adm_boundaries/region.gpkg")

data = gpd.read_parquet(
    "../results/data/osm-cvr-combined-aggregated.parquet",
)

# %%

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

# %%

# NOTE: Uses a household data set not included in the repo!
householddata = gpd.read_parquet(
    "../data/input/households/unique_helaars_adresser.parquet"
)

# %%
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
