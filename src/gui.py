import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
import random
import threading
import networkx as nx

from src.core import MapGenerator, TrafficManager, RouteFinder, Visualizer
from src.benchmark import get_benchmark_data, plot_benchmark_data

# External GUI parts
from src.gui_components.parts.simulation_tab import setup_simulation_tab as _setup_sim_tab
from src.gui_components.parts.benchmark_tab import setup_benchmark_tab as _setup_bench_tab
from src.gui_components.controllers.controller import GUIController

class RouteOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Route Optimization")
        self.root.geometry("1100x800")
        
        self.style = ttk.Style()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_sim = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sim, text="Simulation")
        
        # Tab 2: Benchmark
        self.tab_bench = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bench, text="Benchmark")

        # Attach controller and delegate methods
        self.controller = GUIController(self)
        self.generate_map = self.controller.generate_map
        self.apply_traffic = self.controller.apply_traffic
        self.on_map_click = self.controller.on_map_click
        self.toggle_buttons = self.controller.toggle_buttons
        self.run_simulation_algo = self.controller.run_simulation_algo
        self.start_benchmark_thread = self.controller.start_benchmark_thread

        # --- Simulation Tab Setup ---
        self.setup_simulation_tab()

        # --- Benchmark Tab Setup ---
        self.setup_benchmark_tab()
        
        # Defer layout update to potentiall fix Treeview initial sizing
        self.root.after(200, lambda: self.root.event_generate('<Configure>'))

    def setup_simulation_tab(self):
        # Delegate setup to external module
        _setup_sim_tab(self)
    

    def setup_benchmark_tab(self):
        # Delegate benchmark tab setup to external module
        _setup_bench_tab(self)
    
