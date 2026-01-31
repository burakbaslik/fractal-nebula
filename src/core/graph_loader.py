import networkx as nx
import random
import math

class MapGenerator:
    def __init__(self, width=20, height=20, obstacle_prob=0.2):
        self.width = width
        self.height = height
        self.obstacle_prob = obstacle_prob
        self.graph = None

    def generate_grid_map(self):
        """Generates a grid graph with random obstacles."""
        G = nx.grid_2d_graph(self.width, self.height)
        
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
            G[u][v]['traffic_factor'] = 1.0 

        nodes_to_remove = []
        for node in G.nodes():
            if random.random() < self.obstacle_prob:
                nodes_to_remove.append(node)
        
        for node in nodes_to_remove:
            G.remove_node(node)
        
        self.graph = G
        return G

    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))

    def get_cost(self, u, v):
        return self.graph[u][v]['weight'] * self.graph[u][v].get('traffic_factor', 1.0)
