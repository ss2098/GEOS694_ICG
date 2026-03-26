#!/usr/bin/env python3
"""
Plot the top 10 global earthquakes by magnitude on a Mollweide map.

This script creates a high-resolution global earthquake figure using a
hardcoded list of the top 10 earthquakes by magnitude from the user's
catalog. Marker size represents magnitude, and marker color represents
depth in kilometers.

Output
------
A PNG figure named "Top10_Global.png" is written to the output directory.
"""

from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd


ARRAY_CENTER_LAT = 63.9
ARRAY_CENTER_LON = -149.1
OUTPUT_DIR = Path("outputs")
OUTPUT_FILE = OUTPUT_DIR / "Top10_Global.png"


TOP10_EVENTS = [
    {
        "rank": 1,
        "time": "2019-02-22 10:17:23.770000+00:00",
        "latitude": -2.1862,
        "longitude": -77.0505,
        "depth_km": 145.0,
        "mag": 7.5,
        "magType": "mww",
        "place": "115 km ESE of Palora, Ecuador",
        "id": "us2000jlfv",
    },
    {
        "rank": 2,
        "time": "2019-03-01 08:50:42.591000+00:00",
        "latitude": -14.7131,
        "longitude": -70.1546,
        "depth_km": 267.0,
        "mag": 7.0,
        "magType": "mww",
        "place": "22 km NNE of Azángaro, Peru",
        "id": "us1000j96d",
    },
    {
        "rank": 3,
        "time": "2019-02-17 14:35:55.840000+00:00",
        "latitude": -3.3412,
        "longitude": 152.1319,
        "depth_km": 368.12,
        "mag": 6.4,
        "magType": "mww",
        "place": "95 km N of Rabaul, Papua New Guinea",
        "id": "us2000jj68",
    },
    {
        "rank": 4,
        "time": "2019-03-06 15:46:14.900000+00:00",
        "latitude": -32.0238,
        "longitude": -177.8845,
        "depth_km": 29.0,
        "mag": 6.4,
        "magType": "mww",
        "place": "South of the Kermadec Islands",
        "id": "us1000jb8d",
    },
    {
        "rank": 5,
        "time": "2019-03-15 05:03:50.060000+00:00",
        "latitude": -17.8744,
        "longitude": -65.9072,
        "depth_km": 359.0,
        "mag": 6.3,
        "magType": "mww",
        "place": "31 km SSE of Tarata, Bolivia",
        "id": "us1000jg5z",
    },
    {
        "rank": 6,
        "time": "2019-03-20 15:23:58.680000+00:00",
        "latitude": -15.5965,
        "longitude": 167.6551,
        "depth_km": 119.0,
        "mag": 6.3,
        "magType": "mww",
        "place": "53 km E of Luganville, Vanuatu",
        "id": "us1000jj9r",
    },
    {
        "rank": 7,
        "time": "2019-03-10 08:12:26.426000+00:00",
        "latitude": -17.8915,
        "longitude": -178.6034,
        "depth_km": 578.19,
        "mag": 6.2,
        "magType": "mww",
        "place": "221 km E of Levuka, Fiji",
        "id": "us1000jd55",
    },
    {
        "rank": 8,
        "time": "2019-02-14 19:57:04.980000+00:00",
        "latitude": 35.4267,
        "longitude": -36.0378,
        "depth_km": 10.0,
        "mag": 6.2,
        "magType": "mww",
        "place": "Northern Mid-Atlantic Ridge",
        "id": "us2000ji4e",
    },
    {
        "rank": 9,
        "time": "2019-03-23 19:21:17.998000+00:00",
        "latitude": 4.5595,
        "longitude": -76.2230,
        "depth_km": 122.0,
        "mag": 6.1,
        "magType": "mww",
        "place": "3 km WSW of Versalles, Colombia",
        "id": "us1000jkrq",
    },
    {
        "rank": 10,
        "time": "2019-03-24 04:37:35.918000+00:00",
        "latitude": 1.6601,
        "longitude": 126.3955,
        "depth_km": 45.0,
        "mag": 6.1,
        "magType": "mww",
        "place": "146 km NW of Ternate, Indonesia",
        "id": "us1000jkwi",
    },
]


def build_dataframe() -> pd.DataFrame:
    """
    Convert the hardcoded earthquake list into a DataFrame.

    Returns
    -------
    pandas.DataFrame
        Table containing the top 10 earthquake events.
    """
    return pd.DataFrame(TOP10_EVENTS)


def compute_marker_sizes(magnitudes: pd.Series) -> pd.Series:
    """
    Convert magnitude values into scatter marker sizes.

    Parameters
    ----------
    magnitudes : pandas.Series
        Earthquake magnitudes.

    Returns
    -------
    pandas.Series
        Marker sizes for plotting.
    """
    return (magnitudes ** 2) * 20.0


def create_top10_global_map(dataframe: pd.DataFrame, output_file: Path) -> None:
    """
    Create and save the top-10 global earthquake map.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame containing top earthquake events.
    output_file : pathlib.Path
        Output path for the PNG figure.
    """
    latitudes = dataframe["latitude"].astype(float)
    longitudes = dataframe["longitude"].astype(float)
    depths = dataframe["depth_km"].astype(float)
    magnitudes = dataframe["mag"].astype(float)
    ranks = dataframe["rank"].astype(int)

    depth_min = 0.0
    depth_max = float(depths.max())

    projection = ccrs.Mollweide(central_longitude=ARRAY_CENTER_LON)

    fig = plt.figure(figsize=(20, 11))
    ax = plt.axes(projection=projection)
    ax.set_global()

    ax.add_feature(cfeature.LAND, facecolor="lightgray", alpha=0.35)
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue", alpha=0.25)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
    ax.add_feature(cfeature.BORDERS, linewidth=0.4, linestyle=":")
    ax.gridlines(linewidth=0.5, alpha=0.4, linestyle="--")

    ax.scatter(
        [ARRAY_CENTER_LON],
        [ARRAY_CENTER_LAT],
        s=150,
        c="black",
        marker="^",
        transform=ccrs.PlateCarree(),
        zorder=11,
        label="Array center",
    )

    scatter = ax.scatter(
        longitudes,
        latitudes,
        s=compute_marker_sizes(magnitudes),
        c=depths,
        cmap="coolwarm",
        marker="o",
        alpha=0.8,
        edgecolors="black",
        linewidth=0.8,
        transform=ccrs.PlateCarree(),
        zorder=8,
        vmin=depth_min,
        vmax=depth_max,
    )

    for rank, latitude, longitude, magnitude in zip(
        ranks, latitudes, longitudes, magnitudes
    ):
        ax.text(
            longitude,
            latitude + 3.5,
            f"#{rank}  M{magnitude:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            weight="bold",
            transform=ccrs.PlateCarree(),
            zorder=9,
            bbox={
                "boxstyle": "round,pad=0.2",
                "facecolor": "white",
                "edgecolor": "black",
                "alpha": 0.85,
                "linewidth": 0.8,
            },
        )

    colorbar = plt.colorbar(
        scatter,
        ax=ax,
        orientation="vertical",
        pad=0.05,
        shrink=0.8,
    )
    colorbar.set_label("Depth (km)", fontsize=13, weight="bold")
    colorbar.ax.invert_yaxis()

    ax.set_title(
        "TOP-10 GLOBAL EVENTS (by Magnitude)\n"
        f"{len(dataframe)} Earthquakes | "
        f"M {magnitudes.min():.1f} – {magnitudes.max():.1f} | "
        f"Depth {depths.min():.0f} – {depths.max():.0f} km",
        fontsize=16,
        weight="bold",
        pad=20,
    )

    ax.legend(loc="lower left", fontsize=10, frameon=True)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Created: {output_file}")


def main() -> None:
    """
    Run the top-10 earthquake plotting workflow.
    """
    dataframe = build_dataframe()
    create_top10_global_map(dataframe, OUTPUT_FILE)


if __name__ == "__main__":
    main()

