from typing import Optional, Sequence
import numpy as np
import matplotlib.pyplot as plt

"""""
Plots a single mission
Given: (lon, lat) points as array | Sequence of indices mission route | depot index
       Title (optional) | save path (optional) | show boolean
"""
def plot_single_mission(
    points_lon_lat: np.ndarray,
    mission_nodes: Sequence[int],
    depot_idx: int,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True,
):
    if len(mission_nodes) < 2:
        raise ValueError("Mission must have at least depot->depot")

    pts = points_lon_lat
    path = np.array(mission_nodes, dtype=int)

    # Plot all points
    plt.figure(figsize=(8, 7))
    plt.scatter(pts[:, 0], pts[:, 1], s=2, alpha=0.15, label="All waypoints")

    # Mission path
    xs = pts[path, 0]
    ys = pts[path, 1]
    plt.plot(xs, ys, linewidth=1.5, label="Mission path")

    # Depot
    plt.scatter([pts[depot_idx, 0]], [pts[depot_idx, 1]], s=60, c="green", label="Depot")

    # Mark mission middle stops
    if len(path) > 2:
        mid = path[1:-1]
        plt.scatter(pts[mid, 0], pts[mid, 1], s=10, label="Mission waypoints")

    # Labels
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(title or "Mission")
    plt.legend(loc="best")

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    else:
        plt.close()
