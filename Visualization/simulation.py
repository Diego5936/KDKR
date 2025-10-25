import pygame
import numpy as np
from Visualization.visualize_map import load_world, lonlat_to_screen
from Visualization.path_samples import get_sample_path

DRONE_COLOR = (0, 0, 0)
DRONE_RADIUS = 6
SPEED = 0.002

def interpolate(a, b, t):
    return a + (b - a) * t

def main():
    pygame
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Drone Simulation")
    clock = pygame.time.Clock()

    world = load_world()
    path = get_sample_path()
    points = world["points"]

    # Convert path to lon/lat
    coords = [points[i] for i in path]

    lon_min, lon_max = world["lon_min"], world["lon_max"]
    lat_min, lat_max = world["lat_min"], world["lat_max"]

    # Screen coors for the path
    screen_path = [
        lonlat_to_screen(lon, lat, lon_min, lon_max, lat_min, lat_max)
        for lon, lat in coords
    ]

    seg_index = 0
    t = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((240, 240, 255))

        screen.fill((240, 240, 255))

        # Draw path
        pygame.draw.lines(screen, (0, 0, 255), False, screen_path, 2)

        # Segments
        p1 = np.array(screen_path[seg_index])
        p2 = np.array(screen_path[seg_index + 1])

        drone_pos = interpolate(p1, p2, t)

        # Draw drone
        pygame.draw.circle(screen, DRONE_COLOR, drone_pos.astype(int), DRONE_RADIUS)

        # Update t
        t += SPEED
        if t >= 1.0:
            t = 0.0
            seg_index += 1
            if seg_index >= len(screen_path) - 1:
                seg_index = 0

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()