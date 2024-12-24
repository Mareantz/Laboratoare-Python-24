import tkinter as tk

COLOR_1 = "#800020"  # burgundy
COLOR_2 = "#8B4513"  # maro
COLOR_3 = "#D8B98A"  # bej (fundal)


def get_board_state():
    triangles = [Triangle(i) for i in range(24)]

    triangles[0].pieces_black = 2
    triangles[5].pieces_white = 5
    triangles[7].pieces_white = 3
    triangles[11].pieces_black = 5
    triangles[12].pieces_white = 5
    triangles[16].pieces_black = 3
    triangles[18].pieces_black = 5
    triangles[23].pieces_white = 2

    return triangles


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


class Triangle:
    def __init__(self, index, pieces_white=0, pieces_black=0):
        self.index = index
        self.pieces_white = pieces_white
        self.pieces_black = pieces_black

    def add_piece(self, color):
        if color == 'white':
            self.pieces_white += 1
        elif color == 'black':
            self.pieces_black += 1

    def remove_piece(self, color):
        if color == 'white' and self.pieces_white > 0:
            self.pieces_white -= 1
        if color == 'black' and self.pieces_black > 0:
            self.pieces_black -= 1

    def can_move(self, color):
        opponent_count = self.pieces_black if color == 'white' else self.pieces_white
        return opponent_count < 2


class BackgammonBoard:
    def __init__(self, parent, is_white_home_right=True):
        self.parent = parent
        self.is_white_home_right = is_white_home_right
        self.triangles = get_board_state()
        self.dice = Dice()
        self.canvas = tk.Canvas(self.parent, bg=COLOR_3)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_triangle_click)
        self.segment_width = None

    def on_resize(self, event):
        self.segment_width = event.width / 13.0
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def on_triangle_click(self, event):

        if not self.segment_width:
            return

        segment_width = self.segment_width
        height = self.canvas.winfo_height()
        top_row = event.y < height / 2

        col = int(event.x // segment_width)
        if col == 6:
            print("Clicked on the bar")
            return
        col = col if col < 6 else col - 1

        if top_row:
            index = col + 12 if self.is_white_home_right else 23 - col
        else:
            index = 11 - col if self.is_white_home_right else col

        x_left = col * segment_width if col < 6 else (col + 1) * segment_width
        x_right = x_left + segment_width

        if top_row:
            triangle_height = height / 2
            x_center = (x_left + x_right) / 2
            if event.y > triangle_height * (1 - abs(event.x - x_center) / (segment_width / 2)):
                print("Clicked in the space between top triangles")
                return
        else:
            triangle_height = height / 2
            x_center = (x_left + x_right) / 2
            if event.y < height - triangle_height * (1 - abs(event.x - x_center) / (segment_width / 2)):
                print("Clicked in the space between bottom triangles")
                return

        print(f"Clicked triangle index: {index}")

    def roll_dice(self):
        """
        Rolls the dice and redraws the board.
        """
        self.dice.roll()
        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def draw_board(self, width, height):
        segment_width = width / 13.0
        bar_left = 6 * segment_width
        bar_right = 7 * segment_width

        self.canvas.create_rectangle(bar_left, 0, bar_right, height, fill="#444", outline="black")
        self.draw_triangles(width, height)
        self.draw_pieces(width, height)
        self.dice.draw(self.canvas, width, height)

    def draw_triangles(self, width, height):
        self.segment_width = width / 13.0

        for i in range(12):
            for top in [False, True]:
                coords = get_triangle_coords(i, self.segment_width, width, height, top)
                color = COLOR_1 if (i % 2 == 0) else COLOR_2
                self.canvas.create_polygon(*coords, fill=color, outline="black")

    def draw_pieces(self, width, height):
        segment_width = self.segment_width
        checker_radius = max(5, int(min(width, height) / 40))

        if self.is_white_home_right:
            bottom_idx = list(range(0, 12))
            top_idx = list(range(12, 24))
        else:
            bottom_idx = list(range(12, 24))
            top_idx = list(range(0, 12))

        # Bottom
        for i, triangle in enumerate(reversed([self.triangles[idx] for idx in bottom_idx])):
            w_count, b_count = triangle.pieces_white, triangle.pieces_black
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
        for i, triangle in enumerate([self.triangles[idx] for idx in top_idx]):
            w_count, b_count = triangle.pieces_white, triangle.pieces_black
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


def draw_dice_face(canvas, roll, x1, y1, x2, y2):
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    radius = (x2 - x1) / 12
    spacing = 0.5

    offsets = {
        1: [(0, 0)],
        2: [(-spacing, -spacing), (spacing, spacing)],
        3: [(-spacing, -spacing), (0, 0), (spacing, spacing)],
        4: [(-spacing, -spacing), (-spacing, spacing), (spacing, -spacing), (spacing, spacing)],
        5: [(-spacing, -spacing), (-spacing, spacing), (spacing, -spacing), (spacing, spacing), (0, 0)],
        6: [(-spacing, -spacing), (-spacing, 0), (-spacing, spacing), (spacing, -spacing), (spacing, 0),
            (spacing, spacing)],
    }

    for dx, dy in offsets[roll]:
        cx = center_x + dx * (x2 - x1) / 2
        cy = center_y + dy * (y2 - y1) / 2
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="black")


class Dice:
    def __init__(self):
        self.rolls = []

    def roll(self):
        import random
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        if d1 == d2:
            self.rolls = [d1, d1, d1, d1]
        else:
            self.rolls = [d1, d2]

    def draw(self, canvas, width, height):
        segment_width = width / 13.0
        bar_left = 6 * segment_width
        bar_right = 7 * segment_width
        bar_width = bar_right - bar_left
        dice_size = min(bar_width / 2.3, height / 12)
        dice_padding = dice_size / 4

        center_x = (bar_left + bar_right) / 2
        center_y = height / 2

        num_dice = len(self.rolls)
        rows = 2 if num_dice > 2 else 1
        cols = 2 if num_dice > 1 else 1

        total_width = cols * dice_size + (cols - 1) * dice_padding
        total_height = rows * dice_size + (rows - 1) * dice_padding

        start_x = center_x - total_width / 2
        start_y = center_y - total_height / 2

        for i, roll in enumerate(self.rolls):
            row = i // 2
            col = i % 2

            x1 = start_x + col * (dice_size + dice_padding)
            y1 = start_y + row * (dice_size + dice_padding)
            x2 = x1 + dice_size
            y2 = y1 + dice_size

            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", width=2)
            draw_dice_face(canvas, roll, x1, y1, x2, y2)


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

        roll_button = tk.Button(self.frame_board, text="Roll Dice", command=self.board_app.roll_dice,
                                font=("Helvetica", 14))
        roll_button.pack(pady=5, side=tk.BOTTOM)


def main():
    root = tk.Tk()
    root.geometry("800x600")
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
