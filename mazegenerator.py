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

        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.draw_maze()

    def create_figure(self):
        figure = fig.Figure(figsize=(5, 5))
        axis = figure.add_subplot(111)
        axis.set_aspect('equal', adjustable='box')
        return figure, axis

    def draw_maze(self):
        self.axis.clear()
        self.axis.set_xlim(0, self.columns)
        self.axis.set_ylim(self.rows, 0)
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

    def toggle_wall(self, row, column, direction):
        self.walls[row][column][direction] = not self.walls[row][column][direction]
        if direction == 'R' and column < self.columns - 1:
            self.walls[row][column + 1]['L'] = self.walls[row][column][direction]
        elif direction == 'T' and row > 0:
            self.walls[row - 1][column]['B'] = self.walls[row][column][direction]
        elif direction == 'L' and column > 0:
            self.walls[row][column - 1]['R'] = self.walls[row][column][direction]
        elif direction == 'B' and row < self.rows - 1:
            self.walls[row + 1][column]['T'] = self.walls[row][column][direction]
        self.draw_maze()

    def on_click(self, event):
        if event.inaxes is not None:
            col, row = int(event.xdata), int(event.ydata)
            x, y = event.xdata - col, event.ydata - row
            if x < 0.1:
                self.toggle_wall(row, col, 'L')
            elif x > 0.9:
                self.toggle_wall(row, col, 'R')
            elif y < 0.1:
                self.toggle_wall(row, col, 'T')
            elif y > 0.9:
                self.toggle_wall(row, col, 'B')
            
            self.draw_maze()

def main():
    root = tk.Tk()
    maze_generator = MazeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()