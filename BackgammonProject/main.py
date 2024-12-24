import tkinter as tk

# Global variables
COLOR_1 = "#800020"  # burgundy
COLOR_2 = "#8B4513"  # maro
COLOR_3 = "#D8B98A"  # bej
CHECKER_RADIUS = 14


def create_initial_board_state():
    board = {i: (0, 0) for i in range(24)}
    board[23] = (2, 0)
    board[12] = (5, 0)
    board[7] = (3, 0)
    board[5] = (5, 0)
    board[0] = (0, 2)
    board[11] = (0, 5)
    board[16] = (0, 3)
    board[18] = (0, 5)
    return board


class BackgammonBoardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backgammon")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=COLOR_3)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_resize)
        self.board_state = create_initial_board_state()

    def on_resize(self, event):
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def draw_board(self, width, height):
        segment_width = width / 13.0
        x_left = 6 * segment_width
        x_right = 7 * segment_width
        self.canvas.create_rectangle(x_left, 0, x_right, height, fill="#444", outline="black")

        for idx in range(24):
            tri_idx = idx % 12
            top_side = idx >= 12
            coords = self.get_triangle_coords(tri_idx, top_side, segment_width, width, height)
            color = COLOR_1 if tri_idx % 2 == 0 else COLOR_2
            self.canvas.create_polygon(*coords, fill=color, outline="black")

        self.draw_checkers(width, height)

    def get_triangle_coords(self, tri_idx, top, segment_width, width, height):
        x_left = tri_idx * segment_width if tri_idx < 6 else (tri_idx + 1) * segment_width
        x_right = x_left + segment_width

        if top:
            return [x_left, 0, x_right, 0, (x_left + x_right) / 2, height / 2]
        else:
            return [x_left, height, x_right, height, (x_left + x_right) / 2, height / 2]

    def draw_checkers(self, width, height):
        segment_width = width / 13.0
        for idx in range(24):
            white_count, black_count = self.board_state[idx]
            if white_count == 0 and black_count == 0:
                continue

            tri_idx = idx % 12
            top_side = idx >= 12
            x_center = (tri_idx + 0.5) * segment_width if tri_idx < 6 else (tri_idx + 1.5) * segment_width

            if top_side:
                start_y = 20
                delta_y = 2 * CHECKER_RADIUS
                for i in range(white_count):
                    y = start_y + i * delta_y
                    self.draw_checker(x_center, y, "white")
                for i in range(black_count):
                    y = start_y + (white_count + i) * delta_y
                    self.draw_checker(x_center, y, "black")
            else:
                start_y = height - 20
                delta_y = 2 * CHECKER_RADIUS
                for i in range(white_count):
                    y = start_y - i * delta_y
                    self.draw_checker(x_center, y, "white")
                for i in range(black_count):
                    y = start_y - (white_count + i) * delta_y
                    self.draw_checker(x_center, y, "black")

    def draw_checker(self, x, y, color):
        r = CHECKER_RADIUS
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=2)


def main():
    root = tk.Tk()
    app = BackgammonBoardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
