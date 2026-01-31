import time
import matplotlib.pyplot as plt
import numpy as np
from src.core import MapGenerator, TrafficManager, RouteFinder
import random
import tracemalloc


def get_benchmark_data(callback=None, custom_graph=None, start_node=None, goal_node=None):
    """
    Runs metrics and returns a dictionary of results.
    If custom_graph is provided, benchmarks that specific map.
    Otherwise, runs the standard suite on varying map sizes.
    """
    
    if custom_graph:
        sizes = ["Current Map"]
        if callback: callback("Benchmarking current map...")
    else:
        sizes = [10, 20, 30, 40, 50]
        if callback: callback("Starting standard suite...")

    results = {
        'sizes': sizes,
        'dijkstra_times': [], 'astar_times': [], 'greedy_times': [],
        'dijkstra_nodes': [], 'astar_nodes': [], 'greedy_nodes': [],
        'dijkstra_mem': [],   'astar_mem': [],   'greedy_mem': [],
        'dijkstra_len': [],   'astar_len': [],   'greedy_len': []
    }

    def run_on_graph(graph, s, g):
        d_t, a_t, g_t = 0, 0, 0
        d_n, a_n, g_n = 0, 0, 0
        d_m, a_m, g_m = 0, 0, 0
        d_l, a_l, g_l = 0, 0, 0
        valid_runs = 0

        for _ in range(10):
            finder = RouteFinder(graph)
            
            # Dijkstra
            tracemalloc.start()
            t0 = time.perf_counter()
            d_path, _, d_exp = finder.dijkstra(s, g)
            t1 = time.perf_counter()
            _, d_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            if d_exp == 0 or not d_path: continue
            
            # A*
            tracemalloc.start()
            t2 = time.perf_counter()
            a_path, _, a_exp = finder.a_star(s, g)
            t3 = time.perf_counter()
            _, a_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Greedy
            tracemalloc.start()
            t4 = time.perf_counter()
            g_path, _, g_exp = finder.greedy_bfs(s, g)
            t5 = time.perf_counter()
            _, g_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            d_t += (t1 - t0) * 1000
            a_t += (t3 - t2) * 1000
            g_t += (t5 - t4) * 1000
            
            d_n += d_exp
            a_n += a_exp
            g_n += g_exp
            
            d_m += d_peak
            a_m += a_peak
            g_m += g_peak
            
            d_l += len(d_path)
            a_l += len(a_path)
            g_l += len(g_path)
            
            valid_runs += 1
            
        return d_t, a_t, g_t, d_n, a_n, g_n, d_m, a_m, g_m, d_l, a_l, g_l, valid_runs

    if custom_graph:
        dt, at, gt, dn, an, gn, dm, am, gm, dl, al, gl, v = run_on_graph(custom_graph, start_node, goal_node)
        if v > 0:
            results['dijkstra_times'].append(dt/v)
            results['astar_times'].append(at/v)
            results['greedy_times'].append(gt/v)
            
            results['dijkstra_nodes'].append(dn/v)
            results['astar_nodes'].append(an/v)
            results['greedy_nodes'].append(gn/v)
            
            results['dijkstra_mem'].append(dm/v/1024)
            results['astar_mem'].append(am/v/1024)
            results['greedy_mem'].append(gm/v/1024)
            
            results['dijkstra_len'].append(dl/v)
            results['astar_len'].append(al/v)
            results['greedy_len'].append(gl/v)

        else:
            for k in results: 
                if isinstance(results[k], list) and k != 'sizes': results[k].append(0)
                
    else:
        for size in sizes:
            if callback: callback(f"Testing Map Size: {size}x{size}")
            
            d_t, a_t, g_t = 0, 0, 0
            d_n, a_n, g_n = 0, 0, 0
            d_m, a_m, g_m = 0, 0, 0
            d_l, a_l, g_l = 0, 0, 0
            valid_count = 0
            
            for _ in range(5):
                 map_gen = MapGenerator(width=size, height=size, obstacle_prob=0.2)
                 G = map_gen.generate_grid_map()
                 TrafficManager(G).apply_random_traffic(0.3)
                 nodes = list(G.nodes())
                 if len(nodes) < 2: continue
                 
                 
                 dt, at, gt, dn, an, gn, dm, am, gm, dl, al, gl, v = run_on_graph(G, nodes[0], nodes[-1])
                 
                 if v > 0:
                     d_t += dt/v 
                     a_t += at/v
                     g_t += gt/v
                     d_n += dn/v
                     a_n += an/v
                     g_n += gn/v
                     d_m += dm/v
                     a_m += am/v
                     g_m += gm/v
                     d_l += dl/v
                     a_l += al/v
                     g_l += gl/v
                     valid_count += 1
            
            if valid_count > 0:
                results['dijkstra_times'].append(d_t/valid_count)
                results['astar_times'].append(a_t/valid_count)
                results['greedy_times'].append(g_t/valid_count)
                
                results['dijkstra_nodes'].append(d_n/valid_count)
                results['astar_nodes'].append(a_n/valid_count)
                results['greedy_nodes'].append(g_n/valid_count)
                
                results['dijkstra_mem'].append(d_m/valid_count/1024)
                results['astar_mem'].append(a_m/valid_count/1024)
                results['greedy_mem'].append(g_m/valid_count/1024)
                
                results['dijkstra_len'].append(d_l/valid_count)
                results['astar_len'].append(a_l/valid_count)
                results['greedy_len'].append(g_l/valid_count)
            else:
                 for k in results: 
                    if isinstance(results[k], list) and k != 'sizes': results[k].append(0)

    if callback: callback("Benchmark complete.")
    return results


def plot_bar_chart(ax, sizes, data1, data2, data3, label1, label2, label3, title, ylabel):
    ax.clear()
    x = np.arange(len(sizes))
    width = 0.08 
    
    rects1 = ax.bar(x - width, data1, width, label=label1)
    rects2 = ax.bar(x, data2, width, label=label2)
    rects3 = ax.bar(x + width, data3, width, label=label3)
    
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(sizes, fontsize=9)
    ax.set_xlim(-0.5, len(sizes) - 0.5) 
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)


def plot_benchmark_data(results, axs):
    sizes = results['sizes']
    (ax1, ax2, ax3, ax4) = axs.flatten()
    
    plot_bar_chart(ax1, sizes, results['dijkstra_times'], results['astar_times'], results['greedy_times'],
                   'Dijkstra', 'A*', 'Greedy', 'Execution Time', 'Time (ms)')

    plot_bar_chart(ax2, sizes, results['dijkstra_nodes'], results['astar_nodes'], results['greedy_nodes'],
                   'Dijkstra', 'A*', 'Greedy', 'Search Space', 'Nodes Expanded')

    plot_bar_chart(ax3, sizes, results['dijkstra_mem'], results['astar_mem'], results['greedy_mem'],
                   'Dijkstra', 'A*', 'Greedy', 'Memory Usage', 'Peak Memory (KB)')

    plot_bar_chart(ax4, sizes, results['dijkstra_len'], results['astar_len'], results['greedy_len'],
                   'Dijkstra', 'A*', 'Greedy', 'Path Length', 'Steps')


def run_benchmark():
    print("Running benchmarks...")
    results = get_benchmark_data(callback=print)
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    plot_benchmark_data(results, axs)
    
    output_file = "benchmark_results.png"
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Benchmark finished. Results saved to {output_file}")


if __name__ == "__main__":
    run_benchmark()
