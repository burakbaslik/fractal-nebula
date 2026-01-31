# Fractal Nebula - Emergency Route Optimization

![Project Banner](https://via.placeholder.com/1200x300?text=Fractal+Nebula+Project+Banner)

## 📌 Project Overview

**What is this?**  
This project is a **Pathfinding Simulation Application** designed to optimize emergency routes in a complex grid-based environment. By generating random maps with obstacles and simulating dynamic traffic conditions, the model identifies the most efficient path between a start and end point using advanced algorithms.

**Why does it matter?**  
In emergency response scenarios, every second counts. Finding the fastest route in a city map cluttered with static obstacles (buildings) and dynamic factors (traffic congestion) is critical. This simulation provides a visual and analytical comparison of pathfinding algorithms to understand their efficiency in real-world-like scenarios.

**Key Features:**
*   **Dynamic Map Generation:** Automatically creates grid maps with configurable obstacle density.
*   **Traffic Simulation:** Simulates random traffic congestion that affects travel costs dynamically.
*   **Algorithm Comparison:** Real-time benchmarking of **Dijkstra** vs. **A*** algorithms.
*   **Interactive GUI:** A modern, theme-able user interface built with `ttkbootstrap` for easy interaction.
*   **Visual Analytics:** Visualizes the search process and final paths using `matplotlib`.

## 🛠 Technologies Used

This project is built using a robust Python ecosystem:

*   **[Python 3.x](https://www.python.org/)**: Core programming language.
*   **[NetworkX](https://networkx.org/)**: For graph data structures and pathfinding logic.
*   **[Matplotlib](https://matplotlib.org/)**: For static and animated visualization of the maps and routes.
*   **[NumPy](https://numpy.org/)**: For efficient numerical operations and grid management.
*   **[ttkbootstrap](https://ttkbootstrap.readthedocs.io/)**: For creating a modern, responsive GUI.

## 📂 Project Structure

```text
fractal-nebula/
├── src/
│   ├── core/              # Core algorithms and map logic
│   │   ├── generator.py   # Map generation logic
│   │   ├── traffic.py     # Traffic simulation
│   │   └── route.py       # Dijkstra and A* implementations
│   └── gui/               # GUI implementation (Tkinter/ttkbootstrap)
├── gui_app.py             # Main GUI application entry point
├── main.py                # Command-line interface entry point
├── .gitignore             # Files excluded from Git
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## 📊 Simulation Details

The project simulates a city grid where:
*   **Nodes** represent intersections or accessible areas.
*   **Edges** represent roads between nodes.
*   **Obstacles** are removed nodes (blocked paths).
*   **Traffic** introduces weights to edges, simulating delay.

**Algorithms Implemented:**
1.  **Dijkstra's Algorithm**: Guarantees the shortest path but explores more nodes.
2.  **A* (A-Star) Search**: Uses a heuristic (Manhattan distance) to find the path faster, making it ideal for spatial maps.

## ⚙️ Installation & Setup

Follow these steps to set up the project locally.

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/fractal-nebula.git
cd fractal-nebula
```

**2. Create a Virtual Environment (Recommended)**
Isolate project dependencies to avoid conflicts.

*Windows:*
```bash
python -m venv .venv
.venv\Scripts\activate
```

*Mac/Linux:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### 1. GUI Mode (Recommended)
Start the interactive dashboard to generate maps, set parameters, and visualize results instantly.

```bash
python gui_app.py
```
*Tip: Use the GUI controls to adjust map size, obstacle probability, and traffic intensity.*

### 2. CLI Mode
Run the simulation directly from the terminal for quick benchmarks.

```bash
python main.py --width 30 --height 30 --obstacles 0.2 --traffic 0.3
```

**Arguments:**
*   `--width`: Map width (default: 30)
*   `--height`: Map height (default: 30)
*   `--obstacles`: Probability of obstacles (0.0 - 1.0)
*   `--traffic`: Probability of traffic congestion (0.0 - 1.0)
*   `--seed`: Random seed for reproducibility

## 📷 Screenshots

### 🖥️ Interactive Dashboard
![Dashboard Placeholder](https://via.placeholder.com/800x450?text=Dashboard+Screenshot)

### 📊 Route Visualization
![Visualization Placeholder](https://via.placeholder.com/800x450?text=Algorithm+Visualization)

## 📉 Results & Evaluation

The application outputs a comparison table in the console (and visually in the GUI) showing:

*   **Time (ms)**: Execution time for each algorithm.
*   **Path Cost**: The weighted cost of the found path (distance + traffic).
*   **Nodes Expanded**: Efficiency metric showing how many nodes were visited.

Typical results show that **A*** expands significantly fewer nodes than **Dijkstra** while finding the optimal path in grid environments.

## 🔒 Security & Data Privacy

*   **No Personal Data**: This project is a pure simulation and does not process any real-world user data.
*   **Safe Execution**: The code uses standard libraries and does not make external network requests (other than installing dependencies).

---
*Created by [Burak Başlık](https://github.com/burakbaslik)*
