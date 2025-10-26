import os
import numpy as np

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(ROOT_DIR, "Data")
OPT_DIR = os.path.join(ROOT_DIR, "Optimized Paths")

POINTS_FILE = os.path.join(DATA_DIR, "points_lat_long.npy")
PHOTO_IDX_FILE = os.path.join(DATA_DIR, "photo_indexes.npy")
ROUTES_GLOBAL_FILE = os.path.join(OPT_DIR, "routes_global.npy")

# Load point coordinates (lat/lon)
def _load_points():
    pts = np.load(POINTS_FILE)
    return np.asarray(pts)

# All waypoints to plot
def _load_photo_indexes():
    idx = np.load(PHOTO_IDX_FILE)
    return np.asarray(idx, dtype=int)

# Load all mission routes
def _load_routes_global():
    return np.load(ROUTES_GLOBAL_FILE, allow_pickle=True)

def build_all_waypoints(default_alt=50.0):
    """Return ALL waypoints (from photo_indexes.npy) with lat/lon and ids."""
    pts = _load_points()           # (N,2)
    photo_ids = _load_photo_indexes()  # (M,) -> indices into pts
    coords = pts[photo_ids]        # (M,2)
    # shape to [{"id": <int>, "lat": .., "lon": .., "alt": 50.0}, ...]
    out = []
    for i, (lat, lon) in zip(photo_ids.tolist(), coords.tolist()):
        out.append({"id": int(i), "lat": float(lat), "lon": float(lon), "alt": float(default_alt)})
    return out

def build_mission_view(mission_id: int, default_alt=50.0):
    """
    mission_id is 1-based (1..8).
    Returns:
      {
        "mission_id": int,
        "all_waypoints": [ {id, lat, lon, alt}, ... ]          # from photo_indexes.npy
        "visited_ids":   [int, int, ...],                      # the subset visited in this mission
        "path":          [ [lat, lon, alt], ... ]              # ordered path coordinates for this mission
      }
    """
    routes = _load_routes_global()
    if mission_id < 1 or mission_id > len(routes):
        return None

    pts = _load_points()
    # All waypoints to render (from photo_indexes.npy)
    all_wps = build_all_waypoints(default_alt=default_alt)

    # Mission path indices (into points_lat_long space)
    path_idx = np.asarray(routes[mission_id - 1], dtype=int)

    # Path coords in [lat, lon, alt]
    path_coords = []
    for lat, lon in pts[path_idx]:
        path_coords.append([float(lat), float(lon), float(default_alt)])

    # Visited IDs (intersection with photo indexes is fine; you wanted “turn visited a different color”)
    visited_ids = path_idx.tolist()

    return {
        "mission_id": mission_id,
        "all_waypoints": all_wps,
        "visited_ids": visited_ids,
        "path": path_coords,
    }
