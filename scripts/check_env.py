"""Check the geoint environment: imports, versions, and a tiny smoke test.

Run from the repo root:  python scripts/check_env.py
Writes the results to docs/environment.md.
"""
import importlib
import platform
import sys
from datetime import date
from pathlib import Path

PACKAGES = ["pandas", "numpy", "geopandas", "shapely", "pyproj", "rasterio", "matplotlib", "jupyterlab"]

rows, failed = [], []
for name in PACKAGES:
    try:
        mod = importlib.import_module(name)
        rows.append((name, getattr(mod, "__version__", "?"), "ok"))
    except Exception as e:  # noqa: BLE001
        rows.append((name, "-", f"FAILED: {e}"))
        failed.append(name)

extras = {}
smoke = []
if not failed:
    import numpy as np
    import geopandas as gpd
    import pyproj
    import rasterio
    from rasterio.io import MemoryFile
    from rasterio.transform import from_origin
    from shapely.geometry import Point

    extras["GDAL (via rasterio)"] = rasterio.__gdal_version__
    extras["PROJ (via pyproj)"] = pyproj.proj_version_str
    extras["GEOS (via shapely)"] = __import__("shapely").geos_version_string

    # vector: point near Hyannis, reproject to UTM 19N, buffer 1 km
    g = gpd.GeoDataFrame(geometry=[Point(-70.28, 41.65)], crs="EPSG:4326").to_crs("EPSG:26919")
    area_km2 = g.buffer(1000).area.iloc[0] / 1e6
    smoke.append(f"vector: 1 km buffer area = {area_km2:.3f} km² (expect ~3.14)")

    # raster: write + read a tiny in-memory GeoTIFF
    arr = np.arange(16, dtype="float32").reshape(4, 4)
    profile = dict(driver="GTiff", height=4, width=4, count=1, dtype="float32",
                   crs="EPSG:26919", transform=from_origin(390000, 4615000, 30, 30))
    with MemoryFile() as mf:
        with mf.open(**profile) as dst:
            dst.write(arr, 1)
        with mf.open() as src:
            smoke.append(f"raster: read back {src.width}x{src.height}, CRS {src.crs}, sum={src.read(1).sum():.0f} (expect 120)")

lines = [
    "# Environment",
    "",
    f"Checked {date.today()} on {platform.platform()}",
    f"Python {sys.version.split()[0]}",
    "",
    "| Package | Version | Import |",
    "|---|---|---|",
    *[f"| {n} | {v} | {s} |" for n, v, s in rows],
]
if extras:
    lines += ["", "| Library | Version |", "|---|---|", *[f"| {k} | {v} |" for k, v in extras.items()]]
if smoke:
    lines += ["", "Smoke tests:", *[f"- {s}" for s in smoke]]

out = "\n".join(lines) + "\n"
print(out)
Path("docs").mkdir(exist_ok=True)
Path("docs/environment.md").write_text(out)
print("wrote docs/environment.md")
sys.exit(1 if failed else 0)
