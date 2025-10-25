import pygame
import numpy as np
from shapely import wkt

# --- Constants ---
WINDOW_SIZE = (1000, 800)
BACKGROUND_COLOR = (240, 240, 255)
POLYGON_COLOR = (100, 100, 100)
ALL_POINTS_COLOR = (180, 180, 180)
ASSET_COLOR = (255, 80, 80)
PHOTO_COLOR = (60, 120, 255)
DEPOT_COLOR = (0, 200, 100)
POINTS_RADIUS = 2
SPECIAL_RADIUS = 4

# --- File Paths ---
DATA_DIR = "../Data"
PATH_POINTS = f"{DATA_DIR}/points_lat_long.npy"
PATH_ASSETS = f"{DATA_DIR}/asset_indexes.npy"
PATH_PHOTOS = f"{DATA_DIR}/photo_indexes.npy"
PATH_POLYGON = f"{DATA_DIR}/polygon_lon_lat.wkt"

# Converts from lon/lat to x/y pixels
def lonlat_to_screen(lon, lat, lon_min, lon_max, lat_min, lat_max):
    lon_span = max(1e-12, lon_max - lon_min)
    lat_span = max(1e-12, lat_max - lat_min)

    x = (lon - lon_min) / lon_span * WINDOW_SIZE[0]
    y = WINDOW_SIZE[1] - (lat - lat_min) / lat_span * WINDOW_SIZE[1]
    return int(x), int(y)

# We receive [start, end], we clamp to 0 and add 1 if inclusive
def slice_inclusive(slc, N):
    start, end = int(slc[0]), int(slc[1])

    if end < N:
        end += 1

    start = max(0, min(start, N)) 
    end = max(0, min(end, N))

    if start > end:
        start, end = end, start

    return slice(start, end)

def load_world():
    # Load the points
    points = np.load(PATH_POINTS)
    assert points.ndim == 2 and points.shape[1] == 2, "Points should be Nx2 array"
    N = points.shape[0]

    # load assets and photos
    asset_idx = np.load(PATH_ASSETS)
    photo_idx = np.load(PATH_PHOTOS)

    # Convert to python slices
    asset_sl = slice_inclusive(asset_idx, N)
    photo_sl = slice_inclusive(photo_idx, N)

    # Load the polygon
    with open(PATH_POLYGON, 'r') as f:
        polygon_wkt = f.read().strip()
    polygon = wkt.loads(polygon_wkt)
    exterior = np.array(polygon.exterior.coords)

    # Bounds
    lon_min, lat_min = exterior.min(axis=0)
    lon_max, lat_max = exterior.max(axis=0)

    # PRINTSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSs
    print(f"[load] points: {points.shape}, N={N}")
    print(f"[load] assets slice -> start={asset_sl.start}, stop={asset_sl.stop} (count={asset_sl.stop - asset_sl.start})")
    print(f"[load] photos slice -> start={photo_sl.start}, stop={photo_sl.stop} (count={photo_sl.stop - photo_sl.start})")
    print(f"[load] polygon vertices: {exterior.shape[0]}")
    print(f"[load] lon range=({lon_min:.6f}, {lon_max:.6f}), lat range=({lat_min:.6f}, {lat_max:.6f})")

    return {
        "points": points,
        "asset_sl": asset_sl,
        "photo_sl": photo_sl,
        "poly_coords": exterior,
        "lon_min": lon_min,
        "lon_max": lon_max,
        "lat_min": lat_min,
        "lat_max": lat_max
    }

# --- Drawing functions ---
def draw_polygon(screen, world):
    polygon = world["poly_coords"]
    points = [lonlat_to_screen(lon, lat, 
                                world["lon_min"], world["lon_max"],
                                world["lat_min"], world["lat_max"])
                for lon, lat in polygon]
    
    # Outline
    if len(points) >= 3:
        pygame.draw.polygon(screen, POLYGON_COLOR, points, width=1)

def draw_points(screen, world):
    for lon, lat in world["points"]:
        x, y = lonlat_to_screen(lon, lat, 
                                world["lon_min"], world["lon_max"],
                                world["lat_min"], world["lat_max"])
        pygame.draw.circle(screen, ALL_POINTS_COLOR, (x, y), 2)

def draw_subsets(screen, world, slice, color, radius):
    points = world["points"][slice]
    for lon, lat in points:
        x, y = lonlat_to_screen(lon, lat, 
                                world["lon_min"], world["lon_max"],
                                world["lat_min"], world["lat_max"])
        pygame.draw.circle(screen, color, (x, y), radius)

def draw_depot(screen, world):
    lon, lat = world["points"][0]
    x, y = lonlat_to_screen(lon, lat, 
                            world["lon_min"], world["lon_max"],
                            world["lat_min"], world["lat_max"])
    pygame.draw.circle(screen, DEPOT_COLOR, (x, y), 8)

# -- Main Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("NextEra Drone Visualization")
    clock = pygame.time.Clock()

    # Load world data
    world = load_world()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # Draw wolrd
        draw_polygon(screen, world)
        draw_points(screen, world)
        draw_subsets(screen, world, world["asset_sl"], ASSET_COLOR, 5)
        draw_subsets(screen, world, world["photo_sl"], PHOTO_COLOR, 3)
        draw_depot(screen, world)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()