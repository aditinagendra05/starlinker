import networkx as nx
import numpy as np

class SatelliteNetwork:
    def __init__(self, isl_threshold=2000, gs_threshold=2500):
        self.graph = nx.Graph()
        self.isl_threshold = isl_threshold
        self.gs_threshold = gs_threshold

    def update_topology(self, sat_positions, ground_stations):
        self.graph.clear()
        
        # Add Satellite Nodes
        for sat_id, pos in sat_positions.items():
            self.graph.add_node(sat_id, pos=pos, type='satellite')

        # Add Ground Station Nodes
        for name, pos in ground_stations.items():
            self.graph.add_node(name, pos=pos, type='ground_station')

        # Create ISLs (Satellite to Satellite)
        sats = list(sat_positions.keys())
        for i in range(len(sats)):
            for j in range(i + 1, len(sats)):
                d = np.linalg.norm(sat_positions[sats[i]] - sat_positions[sats[j]])
                if d < self.isl_threshold:
                    self.graph.add_edge(sats[i], sats[j], weight=d)

        # Connect Ground Stations to visible Satellites
        for name, gs_pos in ground_stations.items():
            for sat_id, s_pos in sat_positions.items():
                d = np.linalg.norm(gs_pos - s_pos)
                if d < self.gs_threshold:
                    self.graph.add_edge(name, sat_id, weight=d)

    def get_shortest_path(self, start_node, end_node):
        try:
            return nx.shortest_path(self.graph, start_node, end_node, weight='weight')
        except:
            return None