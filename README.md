# KDKR
Knowledge Driven Kinetic Routing


# KDKR - Knowledge Driven Kinetic Routing

A drone route optimization system for automated infrastructure inspection using Google OR-Tools and visualization tools.

## Overview

KDKR (Knowledge Driven Kinetic Routing) optimizes multi-drone mission planning for infrastructure inspection. The system uses Vehicle Routing Problem (VRP) algorithms to efficiently route drones to inspection points while respecting battery constraints and minimizing the number of required flights.

## Features

- **Multi-drone route optimization** using Google OR-Tools
- **Battery capacity constraints** for realistic flight planning
- **Visual mission planning** with matplotlib-based route visualization
- **Real-time drone simulation** using pygame
- **Flexible waypoint types**: assets, photo locations, and general waypoints
- **Optimized path reconstruction** using predecessor matrices

## Project Structure

```
KDKR/
├── Data/                          # Data files (not in repo)
│   ├── asset_indexes.npy         # Asset waypoint indices
│   ├── photo_indexes.npy         # Photo location indices
│   ├── waypoint_indexes.npy      # General waypoint indices
│   ├── distance_matrix.npy       # Pairwise distances between points
│   ├── points_lat_long.npy       # All waypoint coordinates (lon, lat)
│   ├── predecessors.npy          # Path reconstruction matrix
│   ├── polygon_lon_lat.wkt       # Inspection area boundary
│   └── routes.npy                # Optimized routes (output)
├── src/
│   └── find_initial_route.py     # Route optimization script
├── Visualization/
│   ├── __init__.py
│   ├── plot_mission.py           # Mission route plotting
│   ├── visualize_map.py          # Interactive map viewer
│   ├── simulation.py             # Drone flight simulator
│   └── path_samples.py           # Sample path generator
└── README.md
```

## Installation

### Requirements

```bash
pip install numpy
pip install ortools
pip install matplotlib
pip install pygame
pip install shapely
```

### Python Version
- Python 3.8 or higher recommended

## Usage

### 1. Route Optimization

Optimize drone routes using the VRP solver:

```python
from src.find_initial_route import RouteFinder

# Initialize with parameters
route_finder = RouteFinder(
    search_time_limit=30,      # Optimization time in seconds
    num_drones=200,            # Maximum drones available
    battery_cap=37725,         # Battery capacity in feet
    vehicle_fixed_cost=5000    # Cost penalty per drone used
)

# Find optimal routes
solution, routing = route_finder.find_initial_route()

# Export results
if solution:
    route_finder.exportRoutesNPY("../Data/routes.npy")
```

### 2. Visualize Routes

Plot individual mission routes:

```python
from Visualization.plot_mission import plot_single_mission

# Plot a single mission
plot_single_mission(
    points_lon_lat=points,
    mission_nodes_global=route_path,
    depot_idx=0,
    title="Mission 1 | len=15000 ft",
    save_path="mission_1.png",  # Optional: save to file
    show=True
)
```

### 3. Interactive Map Viewer

View all waypoints and inspection areas:

```bash
cd Visualization
python visualize_map.py
```

Features:
- View all waypoints (gray dots)
- Asset locations (red dots)
- Photo locations (blue dots)
- Depot location (green dot)
- Inspection area polygon boundary

### 4. Drone Simulation

Run real-time drone flight simulation:

```bash
cd Visualization
python simulation.py
```

## Configuration

### Battery Capacity
Default: `37,725 feet` - Adjust based on your drone specifications

### Vehicle Fixed Cost
Default: `5,000` - Higher values encourage fewer drones, lower values allow more drones

### Search Time Limit
Default: `30 seconds` - Increase for better optimization on large problems

### First Solution Strategy
Default: `SAVINGS` - Best for multi-vehicle VRP problems

Options:
- `SAVINGS` - Best for VRP (recommended)
- `PATH_CHEAPEST_ARC` - Better for single-vehicle TSP
- `AUTOMATIC` - Let OR-Tools decide

## Algorithm Details

### Route Optimization

The system uses Google OR-Tools Constraint Programming solver with:

1. **Distance Dimension**: Tracks cumulative flight distance per drone
2. **Battery Constraints**: Ensures no route exceeds battery capacity
3. **Vehicle Fixed Cost**: Minimizes number of drones needed
4. **Guided Local Search**: Metaheuristic for solution improvement
5. **Warm Start**: Can resume from previous solutions

### Key Parameters

```python
MAX_BATTERY_CAP = 37725        # Maximum flight distance per drone (feet)
SEARCH_TIME_LIMIT_S = 30       # Optimization time limit (seconds)
VEHICLE_FIXED_COST = 5000      # Cost to use each additional drone
NUM_DRONES_MAX = 200           # Maximum drones available
```

## Data Format

### Input Files (all in `Data/`)

- **points_lat_long.npy**: Shape `(N, 2)` array of `[longitude, latitude]`
- **distance_matrix.npy**: Shape `(N, N)` pairwise distances in feet
- **predecessors.npy**: Shape `(N, N)` for path reconstruction
- **asset_indexes.npy**: `[start_idx, end_idx]` for asset waypoints
- **photo_indexes.npy**: `[start_idx, end_idx]` for photo waypoints
- **waypoint_indexes.npy**: `[start_idx, end_idx]` for general waypoints
- **polygon_lon_lat.wkt**: WKT polygon defining inspection boundary

### Output Files

- **routes.npy**: List of routes, where each route is a list of waypoint indices

## Troubleshooting

### "No solution found"

**Causes:**
1. Battery capacity too small for problem size
2. Too few drones available (`num_drones` too low)
3. Incorrect distance matrix values
4. Over-constrained problem

**Solutions:**
```python
# Increase battery capacity
battery_cap = 50000

# Increase available drones
num_drones = 200

# Increase search time
search_time_limit = 180

# Remove global span cost constraint
# distance_dimension.SetGlobalSpanCostCoefficient(100)  # Comment out
```

### Memory Issues

For large problems (>1000 waypoints):
```python
# Reduce number of vehicles
num_drones = 50

# Use faster first solution strategy
search_parameters.first_solution_strategy = \
    routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
```

### Slow Optimization

```python
# Stop at first feasible solution
search_parameters.solution_limit = 1

# Reduce time limit
search_time_limit = 10

# Use simpler metaheuristic
search_parameters.local_search_metaheuristic = \
    routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC
```

## API Reference

### RouteFinder Class

```python
class RouteFinder:
    def __init__(self, search_time_limit, num_drones, battery_cap, 
                 vehicle_fixed_cost=5000, filepath="")
    
    def load_assets(self, filepath)
    # Loads all numpy data files from Data/ directory
    
    def find_initial_route(self)
    # Returns: (solution, routing)
    # Optimizes routes using OR-Tools
    
    def getRouteList(self, routing, manager, solution)
    # Extracts route sequences from OR-Tools solution
    
    def reconstructGlobalPath(self, start, end)
    # Returns: list of waypoint indices
    # Reconstructs path between two points using predecessors
    
    def exportRoutesNPY(self, filepath)
    # Saves optimized routes to numpy file
```

### plot_single_mission()

```python
def plot_single_mission(
    points_lon_lat,          # Nx2 array of coordinates
    mission_nodes_global,    # List of waypoint indices
    depot_idx,               # Depot index (usually 0)
    title=None,              # Plot title
    save_path=None,          # Save location (optional)
    show=True                # Display plot
)
```

## Performance Tips

1. **Pre-compute distance matrix** for faster optimization
2. **Use predecessor matrix** for efficient path reconstruction
3. **Start with warm solutions** by loading previous routes
4. **Adjust vehicle fixed cost** to balance drone count vs route length
5. **Use solution limits** for quick feasibility checks
f
