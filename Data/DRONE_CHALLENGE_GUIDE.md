# NextEra Energy Drone Optimization Challenge

Welcome to the NextEra Energy Drone Optimization Challenge at UCF! This guide gives you enough context to get started quickly while leaving
plenty of room for creative solutions. Everything you need is in the data files provided here - build your own tooling and pipelines on top.

---

## 1. Problem Overview
- NextEra Energy maintains and proactively inspects tens of thousands of miles of lines in our electric grid using autonomous drones. At this scale, it's critical to operate as cost effectively as possible. 
- Your goal is to generate efficient inspection missions that visit every required waypoint while respecting battery constraints and returning to the launch site between missions.
- Success is measured by: full coverage, low total distance/time, clear visualizations, and a well-explained approach.

What we supply:
- Geo-referenced waypoints that include both asset poles and photo locations.
- Precomputed shortest-path distances between waypoints inside the allowed flight zone.
- Helper arrays for decoding paths and mapping indices to coordinates.

What you deliver:
1. Working code (any language) that can reproduce your solution from the provided data.
2. A presentation of your approach, assumptions, and analysis of results.
3. Evidence of coverage and constraint handling (plots, tables, or metrics). Visual output is encouraged.

---

## 2. Data Package
All files live in this folder. Load them with `numpy.load` unless stated otherwise.

| File | Type | Purpose |
| --- | --- | --- |
| `distance_matrix.npy` | NumPy array (N x N) | Symmetric matrix of door-to-door flight distances between waypoints computed inside the polygon. Use this as the cost matrix in your optimizer. |
| `predecessors.npy` | NumPy array (N x N) | For each pair of nodes `(i, j)`, stores the predecessor index on the shortest path from `i` to `j`. Use `scipy.sparse.csgraph.dijkstra` conventions to expand indirect legs back into actual waypoint sequences. |
| `points_lat_long.npy` | NumPy array (N x 2) | Geographic coordinates (longitude, latitude) for every waypoint index. Index into this after planning to obtain real-world coordinates. |
| `asset_indexes.npy` | NumPy array | Subset of waypoint indices corresponding to electrical assets (i.e. poles), formatted as a slice: `[first index, last index]`. |
| `photo_indexes.npy` | NumPy array | Subset of waypoint indices for the 4 photo points around each asset, formatted as a slice: `[first index, last index]`.  |
| `polygon_lon_lat.wkt` | Text (WKT) | WKT polygon describing the allowed flight region. Use Shapely/GeoPandas to visualize or enforce constraints. |
| _You bring the code_ | – | While you are free to use any optimization tooling, we **strongly recommend** [Google OR-Tools](https://developers.google.com/optimization/routing) for this challenge. At the OR Tools link, there is a series of code examples (from "Overview" through "Capacity Constraints") that will help guide you through a successful implementation. You may also explore NetworkX, Pyomo, or heuristics of your choice. |

Helpful hint: a few indices (e.g., in `asset_indexes.npy`) may fall outside the coordinate array. If an issue, filter them out defensively.

---

## 3. Suggested Workflow
This is a scaffold—not a prescription. Feel free to diverge.

1. **Inspect the data**
   - Load arrays with `numpy.load`, confirm shapes, and sanity-check index ranges.
   - Plot the polygon and raw waypoints using any mapping library (Plotly, Folium, GeoPandas, etc.).

2. **Build an unconstrained tour**
   - Treat the problem as a single-vehicle routing/TSP on `distance_matrix.npy` using the optimization toolkit of your choice (We recommend Google OR-Tools, but there is also NetworkX heuristics, simulated annealing, genetic algorithms, etc.).

3. **Decode real paths**
   - Convert the abstract tour into detailed waypoint sequences using `predecessors.npy` and the Dijkstra predecessor conventions. This ensures your missions respect the flight polygon boundaries.

4. **Respect battery limits**
   - Split the route into missions that each start/end at the depot (which is **index 0**, as is typical in routing problems) and stay under a maximum allowed distance. The explicit distance constraint for optimal battery usage is **37,725 feet**. You can design your own heuristics: multi-vehicle VRP formulations, greedy partitioning, or clustering first.

5. **Convert to coordinates**
   - Translate waypoint indices to longitude/latitude via `points_lat_long.npy` to generate deliverables (maps, CSVs, GeoJSON, etc.).

6. **Visualize and validate**
   - Overlay missions on the polygon, check that every asset/photo index is covered, and ensure no segment exits the flight zone.
   - For enhanced visualization, you can use [Plotly Mapbox](https://plotly.com/python/scattermapbox/) (scattermapbox) to display your routes on an actual OpenStreetMap.
   - Evaluate total distance, energy use estimates, or mission counts. Iterate on your algorithm or run your solver longer to improve metrics.

---

## 4. Build Your Own Pipeline
No starter code is provided; part of the challenge is designing and implementing your own pipeline. However, you will be greatly accelerated by starting with the examples provided in the OR Tools documentation, specifically the series from "Overview" through "Capacity Constraints". You are free to use any language or library, as long as the judges can run your solution end-to-end with the supplied data and clear instructions.

---

## 5. Constraints & Assumptions
- **Coverage:** Every required **photo** waypoint must be inspected at least once. Assets are not visited but are marked for visual aid. Multiple visits are allowed but may hurt efficiency.
- **Battery limit:** Each mission should return to the depot before exceeding the provided max distance. You may choose a different threshold if justified.
- **Airspace:** Paths must remain inside the provided polygon. Respect boundaries when generating or smoothing routes. You may see narrow bridges between larger polygons which is approved airspace and whose waypoints are already provided by the distance matrix.
- **Computation time:** Aim for solutions that run in minutes, not hours. Pre-computed caches are fair game.
- **Data is static:** Treat the dataset as a snapshot. No need to handle streaming updates unless you explore bonus ideas.

Clarify any additional assumptions in your report (e.g., wind ignored, constant speed).

---

## 6. Deliverables


### Evaluation Rubric 
Judges will look for:
1. **Correctness/Completion** – all targets covered, constraints respected
2. **Efficiency** – total distance traveled, number of missions required
3. **Clarity** – intentional architecture/pipeline design, meaningful visuals
4. **Communication** – how well you present your approach, solution, and results
4. **Bonus** - Any "above & beyond" tasks or creative approaches taken

Provide any metrics or comparisons that make your argument compelling.

---

## 7. Sample Ideas for Going Further
- Multi-drone scheduling with staggered launches.
- Heterogeneous drones (different battery capacities). 
- Prioritized assets or repeated inspections.
- Avoiding flying over certain residents' homes too often
- Weather/No-fly zones as dynamic constraints.
- Integrating real basemap tiles or 3D planners.

---

## 8. Getting Help
- Official docs: [Google OR-Tools Routing](https://developers.google.com/optimization/routing), [SciPy Dijkstra](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.dijkstra.html), [Plotly](https://plotly.com/python/).
- Ask mentors for clarification on assumptions or for hints—not for full solutions.

Good luck, and thanks for helping NextEra Energy keep Florida’s grid resilient! Powering millions safely and efficiently starts with your great ideas!
