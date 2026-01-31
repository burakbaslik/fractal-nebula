import sys
import argparse
import random
import time
from src.core import MapGenerator, TrafficManager, RouteFinder, Visualizer

def main():
    parser = argparse.ArgumentParser(description="Emergency Route Optimization Simulation")
    parser.add_argument('--width', type=int, default=30, help='Map width')
    parser.add_argument('--height', type=int, default=30, help='Map height')
    parser.add_argument('--obstacles', type=float, default=0.2, help='Obstacle probability (0-1)')
    parser.add_argument('--traffic', type=float, default=0.3, help='Traffic probability (0-1)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("Initializing Map...")
    map_gen = MapGenerator(width=args.width, height=args.height, obstacle_prob=args.obstacles)
    G = map_gen.generate_grid_map()
    print(f"Map created: {len(G.nodes())} nodes, {len(G.edges())} edges.")

    nodes = list(G.nodes())
    if not nodes:
        print("Error: Map is empty!")
        return

    start = nodes[0]
    goal = nodes[-1]
    
    if args.seed is None:
        start = random.choice(nodes)
        goal = random.choice(nodes)
        while start == goal:
            goal = random.choice(nodes)
    
    print(f"Start: {start}, Goal: {goal}")

    print("Applying Traffic...")
    traffic_mgr = TrafficManager(G)
    traffic_mgr.apply_random_traffic(intensity=args.traffic)

    finder = RouteFinder(G)

    print("\nRunning Algorithms...")
    
    # Run Dijkstra
    t0 = time.time()
    d_path, d_cost, d_expanded = finder.dijkstra(start, goal)
    d_time = (time.time() - t0) * 1000
    
    # Run A*
    t0 = time.time()
    a_path, a_cost, a_expanded = finder.a_star(start, goal)
    a_time = (time.time() - t0) * 1000

    print("-" * 50)
    print(f"{'Metric':<20} | {'Dijkstra':<15} | {'A*':<15}")
    print("-" * 50)
    print(f"{'Time (ms)':<20} | {d_time:<15.4f} | {a_time:<15.4f}")
    print(f"{'Path Cost':<20} | {d_cost:<15.4f} | {a_cost:<15.4f}")
    print(f"{'Nodes Expanded':<20} | {d_expanded:<15} | {a_expanded:<15}")
    print(f"{'Path Length':<20} | {len(d_path) if d_path else 'N/A':<15} | {len(a_path) if a_path else 'N/A':<15}")
    print("-" * 50)

    if a_path:
        print("\nPath found! Generating visualization...")
        viz = Visualizer(G)
        viz.draw_scenario(path=a_path, title=f"Route Optimization (A*)\nCost: {a_cost:.2f}")
    else:
        print("\nNo path found between start and goal.")

if __name__ == "__main__":
    main()
