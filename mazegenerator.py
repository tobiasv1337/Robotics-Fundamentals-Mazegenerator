import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as tkagg

class MazeGenerator:
    def __init__(self, master):
        self.master = master
        self.rows = 6
        self.columns = 6
        self.walls = [[{'R': False, 'T': False, 'L': False, 'B': False} for _ in range(self.columns)] for _ in range(self.rows)]

        self.master.title("Maze Generator")
        self.figure, self.axis = self.create_figure()
        self.canvas = tkagg.FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = tkagg.NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()

        self.draw_maze()

    def create_figure(self):
        figure = fig.Figure(figsize=(5, 5))
        axis = figure.add_subplot(111)
        axis.set_aspect('equal', adjustable='box')
        return figure, axis

    def draw_maze(self):
        self.axis.clear()
        self.axis.set_xlim(0, self.columns)
        self.axis.set_ylim(0, self.rows)
        self.axis.set_xticks(range(self.columns + 1))
        self.axis.set_yticks(range(self.rows + 1))
        self.axis.grid(True, linestyle='-', linewidth=0.5, color='grey')

        for row in range(self.rows):
            for column in range(self.columns):
                cell_walls = self.walls[row][column]
                if cell_walls['R']:
                    self.axis.plot([column + 1, column + 1], [row, row + 1], color='black', linewidth=2)
                if cell_walls['T']:
                    self.axis.plot([column, column + 1], [row, row], color='black', linewidth=2)
                if cell_walls['L']:
                    self.axis.plot([column, column], [row, row + 1], color='black', linewidth=2)
                if cell_walls['B']:
                    self.axis.plot([column, column + 1], [row + 1, row + 1], color='black', linewidth=2)

        self.canvas.draw()


def main():
    root = tk.Tk()
    maze_generator = MazeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()