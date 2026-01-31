import matplotlib.pyplot as plt
import networkx as nx

class Visualizer:
    def __init__(self, graph):
        self.graph = graph
        self.pos = {node: node for node in graph.nodes()} 

    def draw_scenario(self, path=None, title="Route Optimization", ax=None, start_node=None, goal_node=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        else:
            ax.clear()

        edge_colors = []
        for u, v in self.graph.edges():
            factor = self.graph[u][v].get('traffic_factor', 1.0)
            if factor > 3.0:
                edge_colors.append('red') 
            elif factor > 1.5:
                edge_colors.append('orange')
            else:
                edge_colors.append('gray') 
                
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=10, node_color='blue', ax=ax)
        
        nx.draw_networkx_edges(self.graph, self.pos, edge_color=edge_colors, width=1.0, alpha=0.5, ax=ax)

        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges, edge_color='green', width=3.0, ax=ax)
            
            if start_node is None: start_node = path[0]
            if goal_node is None: goal_node = path[-1]

        if start_node:
            nodes = nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[start_node], node_color='lime', node_size=100, label="Start", ax=ax)
            nodes.set_zorder(100)
        if goal_node:
            nodes = nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[goal_node], node_color='red', node_size=100, label="Goal", ax=ax)
            nodes.set_zorder(100)
            
        if start_node or goal_node:
            ax.legend()

        ax.set_title(title)
        ax.grid(True)
        
        if ax is None:
            output_file = "simulation_result.png"
            plt.savefig(output_file)
            print(f"Map saved to {output_file}")
