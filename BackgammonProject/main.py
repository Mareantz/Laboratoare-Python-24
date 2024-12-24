import tkinter as tk

COLOR_1 = "#800020"  # burgundy
COLOR_2 = "#8B4513"  # maro
COLOR_3 = "#D8B98A"  # bej (fundal)


def get_board_state():
    board = {i: (0, 0) for i in range(24)}
    board[0] = (0, 2)
    board[5] = (5, 0)
    board[7] = (3, 0)
    board[11] = (0, 5)
    board[12] = (5, 0)
    board[16] = (0, 3)
    board[18] = (0, 5)
    board[23] = (2, 0)
    return board


def get_triangle_coords(i, segment_width, W, H, top):
    actual_col = i if i < 6 else (i + 1)
    if top:
        x_left = W - actual_col * segment_width
        x_right = x_left - segment_width
        return [x_left, 0, x_right, 0, (x_left + x_right) / 2, H / 2]
    else:
        x_left = actual_col * segment_width
        x_right = x_left + segment_width
        return [x_left, H, x_right, H, (x_left + x_right) / 2, H / 2]


class BackgammonBoard:
    def __init__(self, parent, is_white_home_right=True):
        self.parent = parent
        self.is_white_home_right = is_white_home_right
        self.board_state = get_board_state()
        self.canvas = tk.Canvas(self.parent, bg=COLOR_3)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def draw_board(self, width, height):
        segment_width = width / 13.0
        bar_left = 6 * segment_width
        bar_right = 7 * segment_width

        self.canvas.create_rectangle(bar_left, 0, bar_right, height, fill="#444", outline="black")
        self.draw_triangles(width, height)
        self.draw_pieces(width, height)

    def draw_triangles(self, width, height):
        segment_width = width / 13.0

        for i in range(12):
            for top in [False, True]:
                coords = get_triangle_coords(i, segment_width, width, height, top)
                color = COLOR_1 if (i % 2 == 0) else COLOR_2
                self.canvas.create_polygon(*coords, fill=color, outline="black")

    def draw_pieces(self, width, height):
        segment_width = width / 13.0
        checker_radius = max(5, int(min(width, height) / 40))

        if self.is_white_home_right:
            bottom_idx = list(range(0, 12))
            top_idx = list(range(12, 24))
        else:
            bottom_idx = list(range(12, 24))
            top_idx = list(range(0, 12))

        # Bottom
        for i, idx in enumerate(reversed(bottom_idx)):
            w_count, b_count = self.board_state[idx]
            if w_count == 0 and b_count == 0:
                continue

            actual_col = i if i < 6 else (i + 1)
            x_center = (actual_col + 0.5) * segment_width
            start_y = height - 20
            delta_y = 2 * checker_radius

            for n in range(w_count):
                y = start_y - n * delta_y
                self.draw_one_piece(x_center, y, "white", checker_radius)
            for n in range(b_count):
                y = start_y - (w_count + n) * delta_y
                self.draw_one_piece(x_center, y, "black", checker_radius)

        # Upper
        for i, idx in enumerate(top_idx):
            w_count, b_count = self.board_state[idx]
            if w_count == 0 and b_count == 0:
                continue

            actual_col = i if i < 6 else (i + 1)
            x_center = (actual_col + 0.5) * segment_width
            start_y = 20
            delta_y = 2 * checker_radius

            for n in range(w_count):
                y = start_y + n * delta_y
                self.draw_one_piece(x_center, y, "white", checker_radius)
            for n in range(b_count):
                y = start_y + (w_count + n) * delta_y
                self.draw_one_piece(x_center, y, "black", checker_radius)

    def draw_one_piece(self, x, y, color, r):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=2)


class MainMenu:
    def __init__(self, root):
        self.sub_frame = None
        self.frame_board = None
        self.board_app = None
        self.root = root
        self.root.title("Backgammon")
        self.menu_frame = tk.Frame(root, padx=20, pady=20)
        self.menu_frame.pack()

        btn_comp = tk.Button(self.menu_frame, text="Play vs Computer", font=("Helvetica", 14),
                             command=self.menu_vs_comp)
        btn_comp.pack(pady=5)

        btn_human = tk.Button(self.menu_frame, text="Play vs Human", font=("Helvetica", 14),
                              command=self.menu_vs_human)
        btn_human.pack(pady=5)

    def menu_vs_comp(self):
        self.menu_frame.destroy()
        self.sub_frame = tk.Frame(self.root, padx=20, pady=20)
        self.sub_frame.pack()

        lbl = tk.Label(self.sub_frame, text="Choose your color:", font=("Helvetica", 14))
        lbl.pack(pady=5)

        btn_white = tk.Button(self.sub_frame, text="White", font=("Helvetica", 14),
                              command=lambda: self.start_board(is_white=True))
        btn_white.pack(pady=5)

        btn_black = tk.Button(self.sub_frame, text="Black", font=("Helvetica", 14),
                              command=lambda: self.start_board(is_white=False))
        btn_black.pack(pady=5)

    def menu_vs_human(self):
        self.menu_frame.destroy()
        temp = tk.Frame(self.root, padx=20, pady=20)
        temp.pack()
        tk.Label(temp, text="Play vs Human: Not implemented", font=("Helvetica", 14)).pack()

    def start_board(self, is_white):
        self.sub_frame.destroy()
        self.frame_board = tk.Frame(self.root)
        self.frame_board.pack(fill=tk.BOTH, expand=True)

        if is_white:
            self.board_app = BackgammonBoard(self.frame_board, is_white_home_right=True)
        else:
            self.board_app = BackgammonBoard(self.frame_board, is_white_home_right=False)


def main():
    root = tk.Tk()
    root.geometry("800x600")
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
