from src.benchmark import plot_benchmark_data
from src.gui_components.benchmark.helpers import populate_benchmark_tree


def finish_benchmark_process(app, results):
    """Plot ve table'ı benchmark sonuçlarıyla doldur."""
    plot_benchmark_data(results, app.bench_axs)
    app.bench_canvas.draw()
    populate_benchmark_tree(app.tree, results)
    app.bench_status.set("Benchmark Completed.")
    app.btn_run_bench.config(state="normal")
