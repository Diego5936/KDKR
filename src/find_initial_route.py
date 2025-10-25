
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


class RouteFinder:
    def __init__(self, search_time_limit, num_drones):
        self.routes = []
        self.search_time_limit = search_time_limit #Time in seconds
        self.num_drones =  num_drones
        self.load_assets()

    def load_assets(self):
        self.asset_indexes = np.load("../Data/asset_indexes.npy")
        self.distance_matrix = np.load("../Data/distance_matrix.npy")
        self.photo_indexes = np.load("../Data/photo_indexes.npy")
        self.points_lat_long = np.load("../Data/points_lat_long.npy")
        self.predecessors = np.load("../Data/predecessors.npy")
        self.waypoint_indexes = np.load("../Data/waypoint_indexes.npy")
        self.routes = np.load("../Data/routes.npy")

    #Inits OR-tools and finds the shortest path for X amount of drones starting from inital point
    def find_initial_route(self):
        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix), self.num_drones, 0)
        routing = pywrapcp.RoutingModel(manager)

        #Defines how OR-tool checks distances between waypoitns
        def distance_callback(from_index: int, to_index: int):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(self.distance_matrix[from_node][to_node])

    
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = self.search_time_limit
        search_parameters.log_search = True

        #Start our search from best prev route if already exists
        if self.routes.size == 0:
            routes_internal = [[manager.NodeToIndex(n) for n in r] for r in self.routes]

            initial_solution = routing.ReadAssignmentFromRoutes(routes_internal, True)

            solution = routing.SolveFromAssignmentWithParameters(initial_solution, search_parameters)

        #Start search from beginning
        else:
            solution = routing.SolveWithParameters(search_parameters)
        self.getRouteList(routing, manager, solution)

    #Resets the waypoints for all drones and populates it with new shortest routes
    def getRouteList(self, routing, manager, solution) -> None:
        self.routes = [] 
        for vehicle in range(routing.vehicles()):
            if solution:
                print("Total distance:", solution.ObjectiveValue())
                index = routing.Start(0)
                route = []
                while not routing.IsEnd(index):
                    route.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))
                self.routes.append(route)
                print("Route:", route)

            else:
                print("No solution found.")
    #Exports the best routes into a npy file
    def exportRoutesNPY(self, filePath):
        np.save(filePath, np.array(self.routes, dtype=float))

route = RouteFinder(90, 1)
route.find_initial_route()
route.exportRoutesNPY("../Data/routes.npy")