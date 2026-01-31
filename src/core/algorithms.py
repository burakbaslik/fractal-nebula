import heapq
import math

class RouteFinder:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, goal, step_callback=None):
        """
        Dijkstra's Algorithm.
        Returns: (path, cost, expanded_nodes)
        """
        priority_queue = [(0, start)]
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        parents = {start: None}
        expanded_nodes = 0
        
        visited = set()

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue
            
            visited.add(current_node)
            expanded_nodes += 1
            
            if step_callback: step_callback(current_node)

            if current_node == goal:
                return self._reconstruct_path(parents, goal), current_dist, expanded_nodes

            for neighbor in self.graph.neighbors(current_node):
                edge_data = self.graph[current_node][neighbor]
                weight = edge_data.get('weight', 1.0) * edge_data.get('traffic_factor', 1.0)
                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parents[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_dist, neighbor))
        
        return None, float('inf'), expanded_nodes

    def a_star(self, start, goal, step_callback=None):
        """
        A* Algorithm.
        Returns: (path, cost, expanded_nodes)
        """
        priority_queue = [(0, start)]
        visited = set()
        
        g_scores = {node: float('inf') for node in self.graph.nodes()}
        g_scores[start] = 0
        parents = {start: None}
        expanded_nodes = 0

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue

            visited.add(current_node)
            expanded_nodes += 1

            if step_callback: step_callback(current_node)

            if current_node == goal:
               return self._reconstruct_path(parents, goal), g_scores[current_node], expanded_nodes

            for neighbor in self.graph.neighbors(current_node):
                edge_data = self.graph[current_node][neighbor]
                weight = edge_data.get('weight', 1.0) * edge_data.get('traffic_factor', 1.0)
                
                tentative_g = g_scores[current_node] + weight

                if tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    parents[neighbor] = current_node
                    f_score = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(priority_queue, (f_score, neighbor))
        
        return None, float('inf'), expanded_nodes

    def greedy_bfs(self, start, goal, step_callback=None):
        """
        Greedy Best-First Search.
        Uses heuristic only: f(n) = h(n)
        Returns: (path, cost, expanded_nodes)
        """
        queue = [(0, start)] 
        visited = set()
        parents = {start: None}
        expanded_nodes = 0
        
        while queue:
            _, current_node = heapq.heappop(queue)

            if current_node in visited:
                continue

            visited.add(current_node)
            expanded_nodes += 1

            if step_callback: step_callback(current_node)

            if current_node == goal:
               path = self._reconstruct_path(parents, goal)

               total_cost = 0
               for i in range(len(path)-1):
                   u, v = path[i], path[i+1]
                   edge_data = self.graph[u][v]
                   total_cost += edge_data.get('weight', 1.0) * edge_data.get('traffic_factor', 1.0)
               return path, total_cost, expanded_nodes

            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited and neighbor not in parents:
                    parents[neighbor] = current_node
                    priority = self._heuristic(neighbor, goal)
                    heapq.heappush(queue, (priority, neighbor))
        
        return None, float('inf'), expanded_nodes

    def _heuristic(self, node_a, node_b):
        (x1, y1) = node_a
        (x2, y2) = node_b
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _reconstruct_path(self, parents, current_node):
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = parents[current_node]
        return path[::-1] 
