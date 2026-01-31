from typing import Dict

def populate_benchmark_tree(tree, results: Dict):
    """Fill a ttk.Treeview `tree` with benchmark `results`.
    Expects keys: sizes, dijkstra_times, astar_times, greedy_times, dijkstra_nodes, astar_nodes, greedy_nodes,
    dijkstra_mem, astar_mem, greedy_mem, dijkstra_len, astar_len, greedy_len
    """
    for item in tree.get_children():
        tree.delete(item)

    sizes = results.get('sizes', [])
    count = 0
    for i, size in enumerate(sizes):
        tag = 'even' if count % 2 == 0 else 'odd'
        tree.insert("", "end", values=(
            f"{size}", "Dijkstra", 
            f"{results['dijkstra_times'][i]:.4f}", 
            f"{results['dijkstra_nodes'][i]:.0f}",
            f"{results['dijkstra_mem'][i]:.2f}",
            f"{results['dijkstra_len'][i]:.0f}"
        ), tags=(tag,))
        count += 1

        tag = 'even' if count % 2 == 0 else 'odd'
        tree.insert("", "end", values=(
            f"{size}", "A*", 
            f"{results['astar_times'][i]:.4f}", 
            f"{results['astar_nodes'][i]:.0f}",
            f"{results['astar_mem'][i]:.2f}",
            f"{results['astar_len'][i]:.0f}"
        ), tags=(tag,))
        count += 1

        tag = 'even' if count % 2 == 0 else 'odd'
        tree.insert("", "end", values=(
            f"{size}", "Greedy", 
            f"{results['greedy_times'][i]:.4f}", 
            f"{results['greedy_nodes'][i]:.0f}",
            f"{results['greedy_mem'][i]:.2f}",
            f"{results['greedy_len'][i]:.0f}"
        ), tags=(tag,))
        count += 1
