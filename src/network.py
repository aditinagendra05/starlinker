import networkx as nx
import numpy as np

class SatelliteNetwork:
    def __init__(self, isl_threshold=2200, gs_threshold=2800):
        self.graph = nx.Graph()
        self.isl_threshold = isl_threshold
        self.gs_threshold = gs_threshold

    def update_topology(self, sat_positions, ground_stations, broken_nodes=None, weather="Clear"):
        self.graph.clear()
        broken = broken_nodes if broken_nodes else []
        weather_weights = {"Clear": 1.0, "Cloudy": 1.3, "Rainy": 2.0, "Stormy": 5.0}
        penalty = weather_weights.get(weather, 1.0)

        # Add Active Satellites
        for sat_id, pos in sat_positions.items():
            if sat_id not in broken:
                self.graph.add_node(sat_id, pos=pos)

        # Connect ISLs (Satellite to Satellite)
        active_sats = [n for n in self.graph.nodes if n not in ground_stations]
        for i in range(len(active_sats)):
            for j in range(i + 1, len(active_sats)):
                d = np.linalg.norm(sat_positions[active_sats[i]] - sat_positions[active_sats[j]])
                if d < self.isl_threshold:
                    self.graph.add_edge(active_sats[i], active_sats[j], weight=d)

        # Connect Ground Stations with Weather Penalty
        for name, gs_pos in ground_stations.items():
            self.graph.add_node(name, pos=gs_pos)
            for sat_id, s_pos in sat_positions.items():
                if sat_id in broken: continue
                d = np.linalg.norm(gs_pos - s_pos)
                if d < self.gs_threshold:
                    self.graph.add_edge(name, sat_id, weight=d * penalty)

    def get_shortest_path(self, start, end):
        try:
            return nx.shortest_path(self.graph, start, end, weight='weight')
        except: return None