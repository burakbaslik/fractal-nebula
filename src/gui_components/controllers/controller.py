import threading
import time
import traceback

from src.core import MapGenerator, TrafficManager, RouteFinder, Visualizer
from src.benchmark import get_benchmark_data
from src.gui_components.animation.callback import create_anim_callback
from src.gui_components.benchmark.processor import finish_benchmark_process

class GUIController:
    def __init__(self, app):
        self.app = app

    def on_map_click(self, event):
        if hasattr(self.app, 'is_running') and self.app.is_running: return
        if not self.app.graph or not event.inaxes: return
        col = round(event.xdata)
        row = round(event.ydata)
        node = (col, row)
        if not self.app.graph.has_node(node):
            self.app.sim_result_text.set(f"Invalid position {node} (Obstacle)")
            return
        if event.button == 1:
            self.app.start_node = node
            self.app.sim_result_text.set(f"Start set to {node}")
        elif event.button == 3:
            self.app.goal_node = node
            self.app.sim_result_text.set(f"Goal set to {node}")
        self.app.visualizer.draw_scenario(path=None, ax=self.app.sim_ax, title="Map (Custom Points)", start_node=self.app.start_node, goal_node=self.app.goal_node)
        self.app.sim_canvas.draw()

    def generate_map(self):
        if hasattr(self.app, 'is_running') and self.app.is_running: return
        size = self.app.size_var.get()
        obst = self.app.obst_var.get()
        self.app.sim_result_text.set("Generating map...")
        self.app.root.update_idletasks()
        map_gen = MapGenerator(width=size, height=size, obstacle_prob=obst)
        self.app.graph = map_gen.generate_grid_map()
        self.app.visualizer = Visualizer(self.app.graph)
        nodes = list(self.app.graph.nodes())
        if not nodes: return
        self.app.start_node = nodes[0]
        self.app.goal_node = nodes[-1]
        self.app.visualizer.draw_scenario(ax=self.app.sim_ax, title="Map Generated", start_node=self.app.start_node, goal_node=self.app.goal_node)
        self.app.sim_canvas.draw()
        self.app.sim_result_text.set(f"Map: {size}x{size}")
        self.app.traffic_manager = TrafficManager(self.app.graph)
        self.apply_traffic()

    def apply_traffic(self):
        if hasattr(self.app, 'is_running') and self.app.is_running: return
        if not self.app.graph: return
        self.app.traffic_manager.reset_traffic()
        self.app.traffic_manager.apply_random_traffic(intensity=self.app.traffic_var.get())
        self.app.visualizer.draw_scenario(ax=self.app.sim_ax, title="Traffic Applied", start_node=self.app.start_node, goal_node=self.app.goal_node)
        self.app.sim_canvas.draw()
        self.app.sim_result_text.set("Traffic updated.")

    def toggle_buttons(self, state='normal'):
        self.app.btn_dijkstra['state'] = state
        self.app.btn_astar['state'] = state
        self.app.btn_greedy['state'] = state
        self.app.btn_run_bench['state'] = state

    def run_simulation_algo(self, algo):
        try:
            if hasattr(self.app, 'is_running') and self.app.is_running:
                print("DEBUG: Simulation already running. Ignoring request.")
                return
            if not self.app.graph or not self.app.start_node or not self.app.goal_node:
                self.app.sim_result_text.set("Error: Map, Start, or Goal missing.")
                print("DEBUG: Missing map or nodes.")
                return
            self.app.sim_result_text.set(f"Running {algo}...")
            print(f"DEBUG: Starting {algo}...")
            animate = self.app.var_anim.get()
            self.app.is_running = True
            self.toggle_buttons('disabled')
            if animate:
                threading.Thread(target=self._run_algo_thread, args=(algo,), daemon=True).start()
            else:
                self._run_algo_sync(algo)
                self.app.is_running = False
                self.toggle_buttons('normal')
        except Exception as e:
            print(f"ERROR inside run_simulation_algo: {e}")
            self.app.sim_result_text.set(f"Error: {e}")
            self.app.is_running = False
            self.toggle_buttons('normal')

    def _run_algo_sync(self, algo):
        try:
            t0 = time.time()
            finder = RouteFinder(self.app.graph)
            path, cost, exp = None, 0, 0
            name = ""
            if algo == 'dijkstra':
                path, cost, exp = finder.dijkstra(self.app.start_node, self.app.goal_node)
                name = "Dijkstra"
            elif algo == 'astar':
                path, cost, exp = finder.a_star(self.app.start_node, self.app.goal_node)
                name = "A*"
            else:
                path, cost, exp = finder.greedy_bfs(self.app.start_node, self.app.goal_node)
                name = "Greedy"
            dur = (time.time() - t0) * 1000
            if path:
                self.app.visualizer.draw_scenario(path=path, ax=self.app.sim_ax, title=f"{name}: Cost={cost:.1f}, Nodes={exp}", start_node=self.app.start_node, goal_node=self.app.goal_node)
                self.app.sim_result_text.set(f"{name} Found! Cost: {cost:.2f}, Visited: {exp}")
            else:
                self.app.sim_result_text.set(f"{name} Failed.")
            self.app.sim_canvas.draw()
        except Exception as e:
            print(f"ERROR in _run_algo_sync: {e}")
            traceback.print_exc()

    def _run_algo_thread(self, algo):
        try:
            finder = RouteFinder(self.app.graph)
            self.app.root.after(0, lambda: self.app.visualizer.draw_scenario(path=None, ax=self.app.sim_ax, title=f"Running {algo} (Animating...)", start_node=self.app.start_node, goal_node=self.app.goal_node))
            self.app.root.after(0, self.app.sim_canvas.draw)
            self.app.root.after(0, self.app.sim_canvas.draw)
            step_count_holder = [0]
            anim_callback = create_anim_callback(self.app, step_count_holder)
            t0 = time.process_time()
            if algo == 'dijkstra':
                path, cost, exp = finder.dijkstra(self.app.start_node, self.app.goal_node, step_callback=anim_callback)
                name = "Dijkstra"
            elif algo == 'astar':
                path, cost, exp = finder.a_star(self.app.start_node, self.app.goal_node, step_callback=anim_callback)
                name = "A*"
            else:
                path, cost, exp = finder.greedy_bfs(self.app.start_node, self.app.goal_node, step_callback=anim_callback)
                name = "Greedy"
            dur = (time.process_time() - t0) * 1000
            def finish():
                if path:
                    self.app.visualizer.draw_scenario(path=path, ax=self.app.sim_ax, title=f"{name}: Cost={cost:.1f}, Nodes={exp}", start_node=self.app.start_node, goal_node=self.app.goal_node)
                    self.app.sim_result_text.set(f"{name} Found! Cost: {cost:.2f}, Visited: {exp}")
                else:
                    self.app.sim_result_text.set(f"{name} Failed.")
                self.app.sim_canvas.draw()
                self.app.is_running = False
                self.toggle_buttons('normal')
            self.app.root.after(0, finish)
        except Exception as e:
            print(f"ERROR in _run_algo_thread: {e}")
            self.app.is_running = False
            self.app.root.after(0, lambda: self.toggle_buttons('normal'))
            traceback.print_exc()

    def start_benchmark_thread(self):
        if not self.app.graph:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "Oluşturulmuş bir harita bulunamadı!\nLütfen önce 'Simulation' sekmesinden bir harita oluşturun.")
            return
        self.app.btn_run_bench.config(state="disabled")
        self.app.bench_status.set("Running on active map... Please wait.")
        threading.Thread(target=self.run_benchmark_process, args=(self.app.graph, self.app.start_node, self.app.goal_node), daemon=True).start()

    def run_benchmark_process(self, graph, s, g):
        def update_status(msg):
            self.app.root.after(0, lambda: self.app.bench_status.set(msg))
        results = get_benchmark_data(callback=update_status, custom_graph=graph, start_node=s, goal_node=g)
        self.app.root.after(0, lambda: self.finish_benchmark(results))

    def finish_benchmark(self, results):
        finish_benchmark_process(self.app, results)
