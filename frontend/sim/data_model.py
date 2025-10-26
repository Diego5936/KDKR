"""
KDKR frontend/sim/data_model.py

Loads mission/waypoint data from the project’s Data and Optimized Paths folders
and exposes:
  - build_all_waypoints(default_alt=50.0)
  - build_mission_view(mission_id: int, default_alt=50.0)

Expected files (searched in multiple locations):
  Data/
    - points_lat_long.npy     # shape (N, 2+): [lat, lon, ...]
    - photo_indexes.npy       # bool mask of length N OR integer indices
  Optimized Paths/ OR Optimized_Paths/
    - routes_global.npy       # array/list of missions, each is a sequence of point indices
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import numpy as np

# --- Path resolution ---------------------------------------------------
BASE_DIR = Path(__file__).parent  # .../frontend/sim

# Try frontend/Data first, then project-root/Data
DATA_DIR: Optional[Path] = next(
    (p for p in [
        BASE_DIR.parent / "Data",            # .../frontend/Data
        BASE_DIR.parent.parent / "Data",     # .../Data (project root)
    ] if p.exists()),
    None
)

# Try both spellings and both levels for optimized routes
OPT_DIR: Optional[Path] = next(
    (p for p in [
        BASE_DIR.parent / "Optimized Paths",
        BASE_DIR.parent / "Optimized_Paths",
        BASE_DIR.parent.parent / "Optimized Paths",
        BASE_DIR.parent.parent / "Optimized_Paths",
    ] if p.exists()),
    None
)

POINTS_FILE        = (DATA_DIR / "points_lat_long.npy") if DATA_DIR else None
PHOTO_IDX_FILE     = (DATA_DIR / "photo_indexes.npy")   if DATA_DIR else None
ROUTES_GLOBAL_FILE = (OPT_DIR  / "routes_global.npy")   if OPT_DIR  else None
# ----------------------------------------------------------------------


# --- Helpers -----------------------------------------------------------
def _assert_exists(path: Optional[Path], label: str) -> None:
    p = Path(path) if path is not None else None
    if p is None or not p.exists():
        raise FileNotFoundError(f"{label} not found at {p}")

def _load_points() -> np.ndarray:
    """Returns (N,2) float array of [lat, lon]."""
    _assert_exists(POINTS_FILE, "points_lat_long.npy")
    pts = np.load(str(POINTS_FILE), allow_pickle=True)
    pts = np.asarray(pts, dtype=float)
    if pts.ndim != 2 or pts.shape[1] < 2:
        raise ValueError(f"points_lat_long.npy has unexpected shape {pts.shape}; expected (N,2+).")
    return pts[:, :2]  # (N,2)

def _load_photo_indexes(n_points: int) -> np.ndarray:
    """Returns (M,) int indices into points array."""
    _assert_exists(PHOTO_IDX_FILE, "photo_indexes.npy")
    arr = np.load(str(PHOTO_IDX_FILE), allow_pickle=True)
    arr = np.asarray(arr)

    if arr.dtype == bool:
        if arr.size != n_points:
            raise ValueError(f"photo_indexes mask size {arr.size} != points size {n_points}")
        idx = np.where(arr)[0]
    else:
        idx = np.asarray(arr, dtype=int).ravel()

    # keep only valid indices
    idx = idx[(idx >= 0) & (idx < n_points)]
    return idx

def _load_routes_global():
    """Loads routes_global.npy (array/list of missions)."""
    _assert_exists(ROUTES_GLOBAL_FILE, "routes_global.npy")
    routes = np.load(str(ROUTES_GLOBAL_FILE), allow_pickle=True)
    return routes
# ----------------------------------------------------------------------


# --- Public API --------------------------------------------------------
def build_all_waypoints(default_alt: float = 50.0) -> List[Dict[str, Any]]:
    """
    Returns a flat list of all survey/photo waypoints (from photo_indexes.npy):
      [ {id, lat, lon, alt}, ... ]
    """
    pts = _load_points()                          # (N,2)
    photo_ids = _load_photo_indexes(len(pts))     # (M,)
    coords = pts[photo_ids]                       # (M,2)

    out = []
    for i, (lat, lon) in zip(photo_ids.tolist(), coords.tolist()):
        out.append({
            "id":  int(i),
            "lat": float(lat),
            "lon": float(lon),
            "alt": float(default_alt),
        })
    return out

def build_mission_view(mission_id: int, default_alt: float = 50.0) -> Optional[Dict[str, Any]]:
    """
    mission_id: 1..K (1-based)

    Returns:
      {
        "mission_id":   int,
        "all_waypoints":[ {id, lat, lon, alt}, ... ],  # from photo_indexes.npy
        "visited_ids":  [int, ...],                    # indices visited in this mission
        "path":         [ [lat, lon, alt], ... ]       # ordered path coordinates
      }
    or None if mission_id is out of range.
    """
    pts = _load_points()                 # (N,2)
    routes = _load_routes_global()

    # Normalize routes into a list of missions
    try:
        n_missions = len(routes)
    except TypeError:
        routes = [routes]
        n_missions = 1

    if mission_id < 1 or mission_id > n_missions:
        return None

    raw_idx = routes[mission_id - 1]
    path_idx = np.asarray(raw_idx, dtype=float).astype(int).ravel()
    path_idx = path_idx[(path_idx >= 0) & (path_idx < len(pts))]  # valid only

    path_coords = [[float(lat), float(lon), float(default_alt)]
                   for (lat, lon) in pts[path_idx].tolist()]
    visited_ids = path_idx.astype(int).tolist()

    return {
        "mission_id": mission_id,
        "all_waypoints": build_all_waypoints(default_alt=default_alt),
        "visited_ids": visited_ids,
        "path": path_coords,
    }
# ----------------------------------------------------------------------