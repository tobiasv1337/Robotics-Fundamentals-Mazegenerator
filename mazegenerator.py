import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as tkagg
import ast

class MazeGenerator:
    def __init__(self, master):
        self.master = master
        self.rows = 6
        self.columns = 6
        self.init_cells()

        self.master.title("Maze Generator")

        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)
        self.figure, self.axis = self.create_figure()
        self.canvas = tkagg.FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.toolbar_frame = tk.Frame(self.canvas_frame)
        self.toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.toolbar = tkagg.NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

        button_frame = tk.Frame(master)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.import_button = tk.Button(button_frame, text="Import Maze", command=self.import_maze)
        self.import_button.grid(row=0, column=0, padx=5)
        self.import_gold_button = tk.Button(button_frame, text="Import Gold", command=lambda: self.import_feature('gold'))
        self.import_gold_button.grid(row=0, column=1, padx=5)
        self.import_helipad_button = tk.Button(button_frame, text="Import Helipad", command=lambda: self.import_feature('helipad'))
        self.import_helipad_button.grid(row=0, column=2, padx=5)
        self.export_maze_button = tk.Button(button_frame, text="Export Maze", command=self.export_maze)
        self.export_maze_button.grid(row=0, column=3, padx=5)
        self.export_gold_button = tk.Button(button_frame, text="Export Gold", command=lambda: self.export_feature('gold'))
        self.export_gold_button.grid(row=0, column=4, padx=5)
        self.export_helipad_button = tk.Button(button_frame, text="Export Helipad", command=lambda: self.export_feature('helipad'))
        self.export_helipad_button.grid(row=0, column=5, padx=5)

        tk.Label(button_frame, text="Rows:").grid(row=0, column=6, padx=5)
        self.rows_spinbox = tk.Spinbox(button_frame, from_=1, to=1000, width=5, command=self.update_maze_size)
        self.rows_spinbox.grid(row=0, column=7, padx=5)
        self.rows_spinbox.delete(0, tk.END)
        self.rows_spinbox.insert(0, self.rows)

        tk.Label(button_frame, text="Columns:").grid(row=0, column=8, padx=5)
        self.columns_spinbox = tk.Spinbox(button_frame, from_=1, to=1000, width=5, command=self.update_maze_size)
        self.columns_spinbox.grid(row=0, column=9, padx=5)
        self.columns_spinbox.delete(0, tk.END)
        self.columns_spinbox.insert(0, self.columns)

        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.draw_maze()

    def init_cells(self):
        self.cells = [[{'R': False, 'T': False, 'L': False, 'B': False, 'gold': False, 'helipad': False} for _ in range(self.columns)] for _ in range(self.rows)]

    def create_figure(self):
        figure = fig.Figure(figsize=(5, 5))
        axis = figure.add_subplot(111)
        axis.set_aspect('equal', adjustable='box')
        return figure, axis

    def draw_maze(self):
        self.axis.clear()
        self.axis.set_xlim(0, self.columns)
        self.axis.set_ylim(self.rows, 0)

        x_tick_positions = [i + 0.5 for i in range(self.columns)]
        y_tick_positions = [i + 0.5 for i in range(self.rows)]
        x_tick_labels = [str(i) for i in range(self.columns)]
        y_tick_labels = [str(i) for i in range(self.rows)]
        self.axis.set_xticks(x_tick_positions)
        self.axis.set_xticklabels(x_tick_labels)
        self.axis.set_yticks(y_tick_positions)
        self.axis.set_yticklabels(y_tick_labels)
        self.axis.tick_params(axis='x', which='both', top=True, bottom=True, labeltop=True, labelbottom=True)
        self.axis.tick_params(axis='y', which='both', left=True, right=True, labelleft=True, labelright=True)
        self.axis.set_xticks(range(self.columns + 1), minor=True)
        self.axis.set_yticks(range(self.rows + 1), minor=True)
        self.axis.grid(which='minor', linestyle='-', linewidth=0.5, color='grey')
        self.axis.grid(which='major', linestyle='None')

        for spine in self.axis.spines.values():
            spine.set_linestyle('--')
            spine.set_linewidth(0.5)
            spine.set_color('grey')

        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.cells[row][column]
                if cell['R']:
                    linewidth = 2 if column < self.columns - 1 else 4
                    self.axis.plot([column + 1, column + 1], [row, row + 1], color='black', linewidth=linewidth)
                if cell['T']:
                    linewidth = 2 if row > 0 else 4
                    self.axis.plot([column, column + 1], [row, row], color='black', linewidth=linewidth)
                if cell['L']:
                    linewidth = 2 if column > 0 else 4
                    self.axis.plot([column, column], [row, row + 1], color='black', linewidth=linewidth)
                if cell['B']:
                    linewidth = 2 if row < self.rows - 1 else 4
                    self.axis.plot([column, column + 1], [row + 1, row + 1], color='black', linewidth=linewidth)

                if cell['gold']:
                    self.axis.plot(column + 0.5, row + 0.5, marker='o', markersize=18, color='gold')
                if cell['helipad']:
                    self.axis.plot(column + 0.5, row + 0.5, marker='H', markersize=12, color='blue')

        self.canvas.draw()

    def update_maze_size(self):
        try:
            new_rows = int(self.rows_spinbox.get())
            new_columns = int(self.columns_spinbox.get())
            if new_rows != self.rows or new_columns != self.columns:
                self.rows = new_rows
                self.columns = new_columns
                self.init_cells()
                self.draw_maze()
        except ValueError:
            pass

    def toggle_wall(self, row, column, direction):
        self.cells[row][column][direction] = not self.cells[row][column][direction]
        if direction == 'R' and column < self.columns - 1:
            self.cells[row][column + 1]['L'] = self.cells[row][column][direction]
        elif direction == 'T' and row > 0:
            self.cells[row - 1][column]['B'] = self.cells[row][column][direction]
        elif direction == 'L' and column > 0:
            self.cells[row][column - 1]['R'] = self.cells[row][column][direction]
        elif direction == 'B' and row < self.rows - 1:
            self.cells[row + 1][column]['T'] = self.cells[row][column][direction]
        self.draw_maze()

    def toggle_cell_state(self, row, column):
        cell = self.cells[row][column]
        if not cell['gold'] and not cell['helipad']:
            cell['gold'] = True
        elif cell['gold'] and not cell['helipad']:
            cell['gold'] = False
            cell['helipad'] = True
        elif not cell['gold'] and cell['helipad']:
            cell['gold'] = True
        else:
            cell['gold'] = False
            cell['helipad'] = False

    def on_click(self, event):
        click_threshold = 0.2
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
            else:
                self.toggle_cell_state(row, col)

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
            init_cell_bracket_walls = [wall for wall, present in self.cells[0][0].items() if present and wall in ['R', 'T', 'L', 'B']]
            init_cell_bracket_str = "[" + ", ".join(init_cell_bracket_walls) + "]"
            if self.columns > 1:
                init_cell_bracket_str += ", "
            init_cell_bracket_len = len(init_cell_bracket_str) + 1 #+1 to account for the opening bracket of the grid

            max_width = 0
            for row in range(self.rows):
                for column in range(self.columns):
                    walls = [wall for wall, present in self.cells[row][column].items() if present and wall in ['R', 'T', 'L', 'B']]
                    cell_str = "[" + ", ".join(walls) + "]"
                    if column < self.columns - 1:
                            cell_str += ", "
                    max_width = max(max_width, len(cell_str))

            with open(filename, 'w') as file:
                file.write("[")
                for row in range(self.rows):
                    row_text = "["
                    for column in range(self.columns):
                        str_len = init_cell_bracket_len if (row != 0 or column != 0) and init_cell_bracket_len > max_width else max_width-1 if row == 0 and column == 0 else max_width
                        walls = [wall for wall, present in self.cells[row][column].items() if present and wall in ['R', 'T', 'L', 'B']]
                        cell_str = "[" + ", ".join(walls) + "]"
                        if column < self.columns - 1:
                            cell_str += ", "
                        row_text += f"{cell_str:<{str_len}}" if column < self.columns - 1 else cell_str
                    row_text += "]"
                    if row < self.rows - 1:
                        row_text += ",\n"
                    file.write(row_text)
                file.write("]")
    
    def export_feature(self, feature):
        filename = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filename:
            with open(filename, 'w') as file:
                feature_cells = []
                for row in range(self.rows):
                    for column in range(self.columns):
                        if self.cells[row][column][feature]:
                            feature_cells.append([row, column])
                feature_cells_str = '[' + ', '.join([f'[{row},{column}]' for row, column in feature_cells]) + ']'
                file.write(feature_cells_str)
    
    def import_maze(self):
        filename = fd.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filename:
            with open(filename, 'r') as file:
                maze_str = file.read()
            
            maze_str = maze_str.replace("R", "'R'").replace("T", "'T'").replace("L", "'L'").replace("B", "'B'")
            parsed_maze = ast.literal_eval(maze_str)

            new_cells = []

            for row in parsed_maze:
                new_row = []
                for cell in row:
                    new_cell = {wall: (wall in cell) for wall in ['R', 'T', 'L', 'B']}
                    new_cell['gold'] = False
                    new_cell['helipad'] = False
                    new_row.append(new_cell)
                new_cells.append(new_row)

            self.cells = new_cells
            self.rows = len(self.cells)
            self.columns = len(self.cells[0]) if self.rows > 0 else 0

            self.draw_maze()

    def import_feature(self, feature):
        filename = fd.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filename:
            with open(filename, 'r') as file:
                feature_positions = ast.literal_eval(file.read())
            
            for row, column in feature_positions:
                self.cells[row][column][feature] = True

            self.draw_maze()

def main():
    root = tk.Tk()
    maze_generator = MazeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()