import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
from shapely import wkt

base_dir = Path(__file__).resolve().parent

filepath = base_dir / ".." / "Data" / "polygon_lon_lat.wkt"

# visualize the long and lat of the allowed flight region

# read the whole WKT file as one string
with open(filepath, "r") as f:
    wkt_text = f.read().replace("\n", " ").strip()

# convert the WKT text into Shapely geometry object
geom = wkt.loads(wkt_text)

# create a GeoDataFrame containing that geometry
gdf = gpd.GeoDataFrame(index=[0], geometry=[geom], crs="EPSG:4326")

# plot it
fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, color="lightblue", edgecolor="black")
ax.set_title("Visualized WKT Polygon", fontsize=14)
plt.show()
