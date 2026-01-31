import random

class TrafficManager:
    def __init__(self, graph):
        self.graph = graph

    def reset_traffic(self):
        """Resets all traffic factors to 1.0."""
        for u, v in self.graph.edges():
            self.graph[u][v]['traffic_factor'] = 1.0

    def apply_random_traffic(self, intensity=0.3, max_factor=5.0):
        """
        Applies random traffic delays to the map.
        intensity: Probability of a road having traffic (0.0 to 1.0).
        max_factor: Maximum multiplier for weight (e.g. 5.0 means 5x slower).
        """
        for u, v in self.graph.edges():
            if random.random() < intensity:
                factor = random.uniform(1.5, max_factor)
                self.graph[u][v]['traffic_factor'] = factor

    def apply_congestion_zone(self, center_node, radius, factor=3.0):
        """Simulates an accident or heavy traffic in a specific area."""
        cx, cy = center_node
        for u, v in self.graph.edges():
            ux, uy = u
            vx, vy = v
            mid_x, mid_y = (ux + vx) / 2, (uy + vy) / 2
            
            dist = ((mid_x - cx)**2 + (mid_y - cy)**2)**0.5
            if dist <= radius:
                self.graph[u][v]['traffic_factor'] = factor
