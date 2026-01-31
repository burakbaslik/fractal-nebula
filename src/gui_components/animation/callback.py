from src.gui_components.animation.helpers import get_batch_and_sleep


def create_anim_callback(app, step_count_holder):
    """
    Animasyon için callback factory. `step_count_holder` = [0] (mutable list).
    Ekranda adım adım düğümleri çizerek animasyonu gösterir.
    """
    def anim_callback(node):
        if node == app.start_node or node == app.goal_node:
            return
        
        speed = app.speed_var.get()
        batch_size, sleep_time = get_batch_and_sleep(speed)
        
        step_count_holder[0] += 1
        
        def draw_step():
            app.sim_ax.plot(node[0], node[1], color='cyan', marker='o', 
                           markersize=6, alpha=0.9, zorder=1000)
            if step_count_holder[0] % batch_size == 0:
                app.sim_canvas.draw()
                app.root.update_idletasks()
        
        app.root.after(0, draw_step)
        
        if step_count_holder[0] % batch_size == 0 and sleep_time > 0:
            import time
            time.sleep(sleep_time)
    
    return anim_callback
