import tkinter as tk

COLOR_1 = "#800020"  # burgundy
COLOR_2 = "#8B4513"  # maro
COLOR_3 = "#D8B98A"  # bej (fundal)


def get_board_state(is_white_home_right=True):
    triangles = [Triangle(i) for i in range(24)]
    pieces = {
        "white_home_right": {
            0: {"black": 2}, 5: {"white": 5}, 7: {"white": 3}, 11: {"black": 5},
            12: {"white": 5}, 16: {"black": 3}, 18: {"black": 5}, 23: {"white": 2}
        },
        "black_home_left": {
            0: {"white": 2}, 5: {"black": 5}, 7: {"black": 3}, 11: {"white": 5},
            12: {"black": 5}, 16: {"white": 3}, 18: {"white": 5}, 23: {"black": 2}
        }
    }
    config = pieces["white_home_right"] if is_white_home_right else pieces["black_home_left"]
    for idx, piece_data in config.items():
        triangles[idx].pieces_white = piece_data.get("white", 0)
        triangles[idx].pieces_black = piece_data.get("black", 0)

    return triangles


def get_triangle_coords(i, segment_width, width, height, top):
    actual_col = i if i < 6 else (i + 1)
    if top:
        x_left = width - actual_col * segment_width
        x_right = x_left - segment_width
        result = [x_left, 0, x_right, 0, (x_left + x_right) / 2, height / 2]
    else:
        x_left = actual_col * segment_width
        x_right = x_left + segment_width
        result = [x_left, height, x_right, height, (x_left + x_right) / 2, height / 2]
    return result


def calculate_target_index(start_index, distance):
    target_index = start_index - distance
    if 0 <= target_index < 24:
        return target_index
    return None


class Triangle:
    def __init__(self, index):
        self.index = index
        self.pieces_white = 0
        self.pieces_black = 0
        self.highlight_color = None

    def add_piece(self, color):
        if color == 'white':
            self.pieces_white += 1
        elif color == 'black':
            self.pieces_black += 1

    def remove_piece(self, color):
        if color == 'white' and self.pieces_white > 0:
            self.pieces_white -= 1
        elif color == 'black' and self.pieces_black > 0:
            self.pieces_black -= 1

    def can_move(self, color):
        opponent_count = self.pieces_black if color == 'white' else self.pieces_white
        return opponent_count < 2


class BackgammonBoard:
    def __init__(self, parent, is_white_home_right=True):
        self.parent = parent
        self.is_white_home_right = is_white_home_right
        self.triangles = get_board_state(is_white_home_right)
        self.dice = Dice()

        self.canvas = tk.Canvas(self.parent, bg=COLOR_3)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_triangle_click)

        self.segment_width = None
        self.selected_triangle = None
        self.current_player_color = "white" if is_white_home_right else "black"

    def on_resize(self, event):
        self.segment_width = event.width / 13.0
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def on_triangle_click(self, event):
        """
        white:
          top => 12..23 left-> right => index=12+col
          bottom => 11..0 => index=11-col
        black:
          top => 23..12 right-> left => index=23-col
          bottom => 0..11 => index=col
        """
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

        if self.selected_triangle is None:
            triangle = self.triangles[index]
            has_pieces = (triangle.pieces_white > 0 if self.current_player_color == "white"
                          else triangle.pieces_black > 0)
            if has_pieces:
                self.selected_triangle = index
                self.highlight_possible_moves(index)
            else:
                print("No pieces to select here.")
        else:
            if self.triangles[index].highlight_color == "green":
                self.move_piece(self.selected_triangle, index)
                self.reset_highlights()
                self.selected_triangle = None

            else:
                print("Invalid move")
                self.reset_highlights()
                self.selected_triangle = None

        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def move_piece(self, start_index, target_index):
        start_triangle = self.triangles[start_index]
        target_triangle = self.triangles[target_index]

        start_triangle.remove_piece(self.current_player_color)
        target_triangle.add_piece(self.current_player_color)

        distance_used = abs(start_index - target_index)
        self.dice.use_distance(distance_used)

    def highlight_possible_moves(self, start_index):
        self.reset_highlights()
        dice_values = self.dice.rolls
        possible_moves = dice_values + [sum(dice_values[:2])] if len(dice_values) > 1 else dice_values

        for move in possible_moves:
            target_index = calculate_target_index(start_index, move)
            if target_index is not None and self.triangles[target_index].can_move(self.current_player_color):
                self.triangles[target_index].highlight_color = "green"

    def reset_highlights(self):
        for t in self.triangles:
            t.highlight_color = None

    def roll_dice(self):
        if not self.dice.has_rolled:
            self.dice.roll()
            self.canvas.delete("all")
            self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())
        else:
            print("Already rolled")

    def get_triangle_index_and_top(self, idx):
        if self.is_white_home_right:
            if idx >= 12:
                return 23 - idx, True
            else:
                return 11 - idx, False
        else:
            if idx >= 12:
                return idx - 12, True
            else:
                return idx, False

    def draw_board(self, width, height):
        bar_left = 6 * self.segment_width
        bar_right = 7 * self.segment_width
        self.canvas.create_rectangle(bar_left, 0, bar_right, height, fill="#444", outline="black")
        self.draw_triangles(width, height)
        self.draw_pieces(width, height)
        self.dice.draw(self.canvas, width, height)

    def draw_triangles(self, width, height):
        for idx in range(24):
            i, top = self.get_triangle_index_and_top(idx)
            coords = get_triangle_coords(i, self.segment_width, width, height, top)
            color = self.triangles[idx].highlight_color or (
                COLOR_1 if i % 2 == 0 else COLOR_2
            )
            self.canvas.create_polygon(*coords, fill=color, outline="black")

    def draw_pieces(self, width, height):
        piece_radius = max(5, int(min(width, height) / 40))
        distance_y = 2 * piece_radius

        def draw_pieces_on_column(triangles, start_y, direction):
            for i, triangle in enumerate(triangles):
                white_pieces = triangle.pieces_white
                black_pieces = triangle.pieces_black
                if white_pieces == 0 and black_pieces == 0:
                    continue
                col = i if i < 6 else i + 1
                x_center = (col + 0.5) * self.segment_width
                for n in range(white_pieces):
                    y = start_y + direction * n * distance_y
                    self.draw_one_piece(x_center, y, "white", piece_radius)
                for n in range(black_pieces):
                    y = start_y + direction * (white_pieces + n) * distance_y
                    self.draw_one_piece(x_center, y, "black", piece_radius)

        if self.is_white_home_right:
            bottom_index = list(range(11, -1, -1))
            top_index = list(range(12, 24))
        else:
            bottom_index = list(range(0, 12))
            top_index = list(range(23, 11, -1))

        draw_pieces_on_column([self.triangles[x] for x in bottom_index], height - 20, -1)
        draw_pieces_on_column([self.triangles[x] for x in top_index], 20, 1)

    def draw_one_piece(self, x, y, color, piece_radius):
        self.canvas.create_oval(x - piece_radius, y - piece_radius, x + piece_radius, y + piece_radius, fill=color,
                                outline="black", width=2)


def draw_dice_face(canvas, dice_value, x1, y1, x2, y2):
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
    for dx, dy in offsets[dice_value]:
        px = center_x + dx * (x2 - x1) / 2
        py = center_y + dy * (y2 - y1) / 2
        canvas.create_oval(px - radius, py - radius, px + radius, py + radius, fill="black")


class Dice:
    def __init__(self):
        self.rolls = []
        self.used_rolls = []
        self.initial_roll_order = []
        self.has_rolled = False

    def roll(self):
        import random
        if self.has_rolled:
            print("Already rolled")
            return
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        if d1 == d2:
            self.rolls = [d1, d1, d1, d1]
        else:
            self.rolls = [d1, d2]
        self.initial_roll_order = self.rolls.copy()
        self.used_rolls = []
        self.has_rolled = True

    def reset_roll(self):
        self.has_rolled = False
        self.rolls = []
        self.used_rolls = []
        self.initial_roll_order = []

    def use_distance(self, distance):
        if distance in self.rolls:
            self.rolls.remove(distance)
            self.used_rolls.append(distance)
            print(f"Used single die: {distance}")
        else:
            removed = False
            for i in range(len(self.rolls)):
                for j in range(i + 1, len(self.rolls)):
                    if self.rolls[i] + self.rolls[j] == distance:
                        val1 = self.rolls[i]
                        val2 = self.rolls[j]
                        self.used_rolls.append(val1)
                        self.used_rolls.append(val2)
                        if j > i:
                            self.rolls.pop(j)
                            self.rolls.pop(i)
                        else:
                            self.rolls.pop(i)
                            self.rolls.pop(j)
                        print(f"Used combined dice: {val1}+{val2} = {distance}")
                        removed = True
                        break
                if removed:
                    break

    def draw(self, canvas, width, height):
        segment_width = width / 13
        bar_left = 6 * segment_width
        bar_right = 7 * segment_width
        bar_width = bar_right - bar_left
        dice_size = min(bar_width / 2.3, height / 12)
        dice_padding = dice_size / 4

        center_x = (bar_left + bar_right) / 2
        center_y = height / 2

        all_dice = [
            {"value": val, "used": val in self.used_rolls}
            for val in self.initial_roll_order
        ]
        num_dice = len(all_dice)
        rows = 2 if num_dice > 2 else 1
        cols = 2 if num_dice > 1 else 1

        total_width = cols * dice_size + (cols - 1) * dice_padding
        total_height = rows * dice_size + (rows - 1) * dice_padding

        start_x = center_x - total_width / 2
        start_y = center_y - total_height / 2

        for i, die in enumerate(all_dice):
            row = i // 2
            col = i % 2

            x1 = start_x + col * (dice_size + dice_padding)
            y1 = start_y + row * (dice_size + dice_padding)

            x2 = x1 + dice_size
            y2 = y1 + dice_size

            if die["used"]:
                fill_color = "#CCCCCC"
                outline_color = "#666666"
            else:
                fill_color = "white"
                outline_color = "black"

            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=2)
            draw_dice_face(canvas, die["value"], x1, y1, x2, y2)


class MainMenu:
    def __init__(self, root):
        self.sub_frame = None
        self.frame_board = None
        self.board_app = None
        self.root = root
        self.root.title("Backgammon")
        self.menu_frame = tk.Frame(root, padx=20, pady=20)
        self.menu_frame.pack()

        button_ai = tk.Button(self.menu_frame, text="Play vs AI", font=("Helvetica", 14),
                              command=self.menu_vs_ai)
        button_ai.pack(pady=5)

        button_human = tk.Button(self.menu_frame, text="Play vs Human", font=("Helvetica", 14),
                                 command=self.menu_vs_human)
        button_human.pack(pady=5)

    def menu_vs_ai(self):
        self.menu_frame.destroy()
        self.sub_frame = tk.Frame(self.root, padx=20, pady=20)
        self.sub_frame.pack()
        label = tk.Label(self.sub_frame, text="Choose your color:", font=("Helvetica", 14))
        label.pack(pady=5)

        button_white = tk.Button(self.sub_frame, text="White", font=("Helvetica", 14),
                                 command=lambda: self.start_board(True))
        button_white.pack(pady=5)
        button_black = tk.Button(self.sub_frame, text="Black", font=("Helvetica", 14),
                                 command=lambda: self.start_board(False))
        button_black.pack(pady=5)

    def menu_vs_human(self):
        self.menu_frame.destroy()
        temp = tk.Frame(self.root, padx=20, pady=20)
        temp.pack()
        tk.Label(temp, text="Play vs Human: Not implemented", font=("Helvetica", 14)).pack()

    def start_board(self, is_white):
        self.sub_frame.destroy()
        self.frame_board = tk.Frame(self.root)
        self.frame_board.pack(fill=tk.BOTH, expand=True)

        self.board_app = BackgammonBoard(self.frame_board, is_white_home_right=is_white)
        button_roll = tk.Button(self.frame_board, text="Roll Dice", font=("Helvetica", 14),
                                command=self.board_app.roll_dice)
        button_roll.pack(pady=5, side=tk.BOTTOM)


def main():
    root = tk.Tk()
    root.geometry("800x600")
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
