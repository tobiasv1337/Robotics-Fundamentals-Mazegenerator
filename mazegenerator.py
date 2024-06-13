import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as tkagg

class MazeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Generator")
        self.fig, self.ax = self.create_figure()
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    
    def create_figure(self):
        fig = fig.Figure(figsize=(5, 5))
        ax = self.fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        return fig, ax
        

root = tk.Tk()

root.mainloop()