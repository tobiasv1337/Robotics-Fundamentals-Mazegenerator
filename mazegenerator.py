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

        self.export_button = tk.Button(master, text="Export Maze", command=self.export_maze)
        self.export_button.pack(side=tk.BOTTOM)

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
        self.axis.grid(True, linestyle='--', linewidth=0.5, color='grey')

        for spine in self.axis.spines.values():
            spine.set_linestyle('--')
            spine.set_linewidth(0.5)
            spine.set_color('grey')

        for row in range(self.rows):
            for column in range(self.columns):
                cell_walls = self.walls[row][column]
                if cell_walls['R']:
                    linewidth = 2 if column < self.columns - 1 else 4
                    self.axis.plot([column + 1, column + 1], [row, row + 1], color='black', linewidth=linewidth)
                if cell_walls['T']:
                    linewidth = 2 if row > 0 else 4
                    self.axis.plot([column, column + 1], [row, row], color='black', linewidth=linewidth)
                if cell_walls['L']:
                    linewidth = 2 if column > 0 else 4
                    self.axis.plot([column, column], [row, row + 1], color='black', linewidth=linewidth)
                if cell_walls['B']:
                    linewidth = 2 if row < self.rows - 1 else 4
                    self.axis.plot([column, column + 1], [row + 1, row + 1], color='black', linewidth=linewidth)

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
        click_threshold = 0.1
        if event.inaxes is not None:
            col, row = int(event.xdata), int(event.ydata)
            x, y = event.xdata - col, event.ydata - row
            if col == self.columns:
                col -= 1
                x = 1
            if row == self.rows:
                row -= 1
                y = 1
            if x < click_threshold:
                self.toggle_wall(row, col, 'L')
            elif x > 1 - click_threshold:
                self.toggle_wall(row, col, 'R')
            elif y < click_threshold:
                self.toggle_wall(row, col, 'T')
            elif y > 1 - click_threshold:
                self.toggle_wall(row, col, 'B')

            self.draw_maze()
        else:
            cell_x_size = (self.axis.bbox.xmax - self.axis.bbox.xmin) / self.columns
            cell_x_threshold = cell_x_size * click_threshold
            cell_y_size = (self.axis.bbox.ymax - self.axis.bbox.ymin) / self.rows
            cell_y_threshold = cell_y_size * click_threshold
            if self.axis.bbox.xmin - cell_x_threshold < event.x < self.axis.bbox.xmin and self.axis.bbox.ymin < event.y < self.axis.bbox.ymax:
                row = int((self.axis.bbox.ymax - event.y) / (self.axis.bbox.ymax - self.axis.bbox.ymin) * self.rows)
                self.toggle_wall(row, 0, 'L')
            elif self.axis.bbox.xmax < event.x < self.axis.bbox.xmax + cell_x_threshold and self.axis.bbox.ymin < event.y < self.axis.bbox.ymax:
                row = int((self.axis.bbox.ymax - event.y) / (self.axis.bbox.ymax - self.axis.bbox.ymin) * self.rows)
                self.toggle_wall(row, self.columns - 1, 'R')
            elif self.axis.bbox.ymin - cell_y_threshold < event.y < self.axis.bbox.ymin and self.axis.bbox.xmin < event.x < self.axis.bbox.xmax:
                col = int((event.x - self.axis.bbox.xmin) / (self.axis.bbox.xmax - self.axis.bbox.xmin) * self.columns)
                self.toggle_wall(self.rows - 1, col, 'B')
            elif self.axis.bbox.ymax < event.y < self.axis.bbox.ymax + cell_y_threshold and self.axis.bbox.xmin < event.x < self.axis.bbox.xmax:
                col = int((event.x - self.axis.bbox.xmin) / (self.axis.bbox.xmax - self.axis.bbox.xmin) * self.columns)
                self.toggle_wall(0, col, 'T')

            self.draw_maze()

    def export_maze(self):
        filename = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filename:
            init_cell_bracket_walls = [wall for wall, present in self.walls[0][0].items() if present]
            init_cell_bracket_str = "[" + ", ".join(init_cell_bracket_walls) + "]"
            if self.columns > 1:
                init_cell_bracket_str += ", "
            init_cell_bracket_len = len(init_cell_bracket_str) + 1 #+1 to account for the opening bracket of the grid

            max_width = 0
            for row in range(self.rows):
                for column in range(self.columns):
                    walls = [wall for wall, present in self.walls[row][column].items() if present]
                    cell_str = "[" + ", ".join(walls) + "]"
                    if column < self.columns - 1:
                            cell_str += ", "
                    max_width = max(max_width, len(cell_str))

            with open(filename, 'w') as file:
                file.write("[")
                for row in range(self.rows):
                    row_text = "["
                    for column in range(self.columns):
                        str_len = init_cell_bracket_len if (row != 0 or column != 0) and init_cell_bracket_len > max_width else max_width
                        walls = [wall for wall, present in self.walls[row][column].items() if present]
                        cell_str = "[" + ", ".join(walls) + "]"
                        if column < self.columns - 1:
                            cell_str += ", "
                        row_text += f"{cell_str:<{str_len}}" if column < self.columns - 1 else cell_str
                    row_text += "]"
                    if row < self.rows - 1:
                        row_text += ",\n"
                    file.write(row_text)
                file.write("]")

def main():
    root = tk.Tk()
    maze_generator = MazeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()