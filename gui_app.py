import ttkbootstrap as tb
from src.gui import RouteOptimizerApp

def main():
    # themename options: cosmo, flatly, darker, superhero, cyborg, vapor, etc.
    root = tb.Window(themename="superhero") 
        
    app = RouteOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
