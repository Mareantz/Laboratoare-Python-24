import tkinter as tk
import random

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


def calculate_target_index(start_index, distance, moves_up):
    if moves_up:
        target = start_index + distance
    else:
        target = start_index - distance
    return target if 0 <= target < 24 else None


class Triangle:
    def __init__(self, index):
        self.index = index
        self.pieces_white = 0
        self.pieces_black = 0
        self.highlight_color = None

    def add_piece(self, color):
        if color == 'white':
            self.pieces_white += 1
        else:
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

        self.bar_white = 0
        self.bar_black = 0

        self.canvas = tk.Canvas(self.parent, bg=COLOR_3)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_triangle_click)

        self.segment_width = None
        self.selected_triangle = None

        self.current_player_color = "white" if is_white_home_right else "black"
        self.ai_color = "black" if self.current_player_color == "white" else "white"

    def switch_player(self):
        self.current_player_color = "black" if self.current_player_color == "white" else "white"
        if self.current_player_color == self.ai_color:
            self.ai_move()

    def ai_move(self):
        self.dice.roll()
        print(f"AI rolled: {self.dice.rolls}")

        while (self.ai_color == 'white' and self.bar_white > 0) or \
                (self.ai_color == 'black' and self.bar_black > 0):
            used_any = self.ai_reentry()
            if not used_any:
                # pass turn
                break

        if (self.ai_color == 'white' and self.bar_white == 0) or \
                (self.ai_color == 'black' and self.bar_black == 0):

            can_move_with_remaining = True
            while self.dice.rolls and can_move_with_remaining:
                can_move_with_remaining = False
                for roll in self.dice.rolls[:]:
                    start_index = self.find_ai_start_for_roll(roll)
                    if start_index is not None:
                        target_index = self.calculate_ai_target_index(start_index, roll)
                        self.move_piece(start_index, target_index)
                        self.reset_highlights()
                        can_move_with_remaining = True
                        break

        if self.dice.rolls:
            print("AI passing turn.")
            self.dice.reset_roll()

        self.switch_player()

    def find_ai_start_for_roll(self, roll):
        for idx, tr in enumerate(self.triangles):
            count = tr.pieces_white if self.ai_color == 'white' else tr.pieces_black
            if count > 0:
                target_index = self.calculate_ai_target_index(idx, roll)
                if target_index is not None and self.triangles[target_index].can_move(self.ai_color):
                    return idx
        return None

    def ai_reentry(self):
        color = self.ai_color
        used_any_die = False

        for roll in self.dice.rolls[:]:
            target_index = self.get_reentry_index(color, roll)
            if target_index is not None:
                self.reenter_piece(color, target_index)
                self.dice.use_distance(roll)
                used_any_die = True
                if (color == 'white' and self.bar_white == 0) or \
                        (color == 'black' and self.bar_black == 0):
                    break
            else:
                # pass turn
                pass

        return used_any_die

    def on_resize(self, event):
        self.segment_width = event.width / 13.0
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def on_triangle_click(self, event):
        if not self.segment_width:
            return

        if (self.current_player_color == 'white' and self.bar_white > 0) or \
                (self.current_player_color == 'black' and self.bar_black > 0):

            x, y = event.x, event.y
            clicked_index = self.get_triangle_index_by_click(x, y)
            if clicked_index is not None:
                if self.triangles[clicked_index].highlight_color == 'green':
                    self.reenter_piece(self.current_player_color, clicked_index)
                    distance_used = self.reentry_distance_for_index(clicked_index, self.current_player_color)
                    if distance_used is not None:
                        self.dice.use_distance(distance_used)

                self.highlight_bar_reentry_options()
                self.canvas.delete("all")
                self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())
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
            has_pieces = (triangle.pieces_white if self.current_player_color == "white"
                          else triangle.pieces_black)
            if has_pieces > 0:
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

    def get_triangle_index_by_click(self, x, y):
        if not self.segment_width:
            return None
        col = int(x // self.segment_width)
        if col == 6:
            return None
        col = col if col < 6 else col - 1

        height = self.canvas.winfo_height()
        top_row = y < height / 2

        if top_row:
            index = col + 12 if self.is_white_home_right else 23 - col
        else:
            index = 11 - col if self.is_white_home_right else col

        if 0 <= index < 24:
            return index
        return None

    def reentry_distance_for_index(self, target_index, color):
        if color == 'white':
            dist = 24 - target_index
            if dist in self.dice.rolls and 18 <= target_index <= 23:
                return dist
        else:
            dist = target_index + 1
            if dist in self.dice.rolls and 0 <= target_index <= 5:
                return dist
        return None

    def reenter_piece(self, color, target_index):
        tri = self.triangles[target_index]
        opponent_color = 'white' if color == 'black' else 'black'
        if opponent_color == 'white' and tri.pieces_white == 1:
            tri.remove_piece('white')
            self.bar_white += 1
        elif opponent_color == 'black' and tri.pieces_black == 1:
            tri.remove_piece('black')
            self.bar_black += 1

        tri.add_piece(color)

        if color == 'white':
            self.bar_white -= 1
        else:
            self.bar_black -= 1

        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def get_reentry_index(self, color, dice_value):
        if color == 'white':
            reentry_index = 24 - dice_value
            if 18 <= reentry_index <= 23:
                if self.triangles[reentry_index].can_move('white'):
                    return reentry_index
        else:
            reentry_index = dice_value - 1
            if 0 <= reentry_index <= 5:
                if self.triangles[reentry_index].can_move('black'):
                    return reentry_index
        return None

    def move_piece(self, start_index, target_index):
        start_triangle = self.triangles[start_index]
        target_triangle = self.triangles[target_index]
        distance_used = abs(start_index - target_index)

        if self.current_player_color == 'white':
            if target_triangle.pieces_black == 1:
                target_triangle.remove_piece('black')
                self.bar_black += 1
        else:
            if target_triangle.pieces_white == 1:
                target_triangle.remove_piece('white')
                self.bar_white += 1

        start_triangle.remove_piece(self.current_player_color)
        target_triangle.add_piece(self.current_player_color)

        self.dice.use_distance(distance_used)

        if not self.dice.rolls:
            self.dice.reset_roll()
            if self.current_player_color != self.ai_color:
                self.switch_player()

    def highlight_possible_moves(self, start_index):
        self.reset_highlights()

        if not self.dice.rolls:
            print("No dice left to use.")
            return

        dice_values = sorted(self.dice.rolls)
        possible_moves = list(dice_values)

        if len(dice_values) >= 2:
            combined_move = dice_values[0] + dice_values[1]
            if self.is_combined_move_partially_valid(start_index, dice_values[:2]):
                possible_moves.append(combined_move)

        if len(set(dice_values)) == 1:
            face = dice_values[0]
            for i in range(2, len(dice_values) + 1):
                combined = face * i
                if not self.is_partial_double_move_valid(start_index, face, i):
                    break
                possible_moves.append(combined)

        possible_moves = sorted(set(possible_moves))

        valid_moves_found = False
        for move_dist in possible_moves:
            target_index = self.calculate_user_target_index(start_index, move_dist)
            if target_index is not None and self.triangles[target_index].can_move(self.current_player_color):
                self.triangles[target_index].highlight_color = "green"
                valid_moves_found = True

        if not valid_moves_found:
            print("No valid moves available with the current dice.")
        else:
            green_list = [t.index for t in self.triangles if t.highlight_color == "green"]
            print("Highlighted possible moves:", green_list)

    def highlight_bar_reentry_options(self):
        self.reset_highlights()
        color = self.current_player_color
        for d in self.dice.rolls:
            possible_index = self.get_reentry_index(color, d)
            if possible_index is not None:
                self.triangles[possible_index].highlight_color = "green"

    def is_combined_move_partially_valid(self, start_index, dice_pair):
        first_move, second_move = dice_pair
        first_target = self.calculate_user_target_index(start_index, first_move)
        second_target = self.calculate_user_target_index(start_index, second_move)

        if (first_target is not None and self.triangles[first_target].can_move(self.current_player_color)) or \
                (second_target is not None and self.triangles[second_target].can_move(self.current_player_color)):
            return True
        return False

    def is_partial_double_move_valid(self, start_index, face, count):
        current_index = start_index
        moves_up = self.does_current_player_move_up()

        for _ in range(count):
            next_index = calculate_target_index(current_index, face, moves_up)
            if next_index is None or not self.triangles[next_index].can_move(self.current_player_color):
                return False
            current_index = next_index
        return True

    def does_current_player_move_up(self):
        return ((self.current_player_color == 'black' and self.is_white_home_right) or
                (self.current_player_color == 'white' and not self.is_white_home_right))

    def calculate_ai_target_index(self, start_index, distance):
        ai_moves_up = ((self.ai_color == 'black' and self.is_white_home_right) or
                       (self.ai_color == 'white' and not self.is_white_home_right))
        return calculate_target_index(start_index, distance, ai_moves_up)

    def calculate_user_target_index(self, start_index, distance):
        user_moves_up = self.does_current_player_move_up()
        return calculate_target_index(start_index, distance, user_moves_up)

    def reset_highlights(self):
        for t in self.triangles:
            t.highlight_color = None

    def roll_dice(self):
        if not self.dice.has_rolled:
            self.dice.roll()
            if (self.current_player_color == 'white' and self.bar_white > 0) or \
                    (self.current_player_color == 'black' and self.bar_black > 0):
                self.highlight_bar_reentry_options()

            self.canvas.delete("all")
            self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())
        else:
            print("Already rolled")

    def draw_board(self, width, height):
        bar_left = 6 * self.segment_width
        bar_right = 7 * self.segment_width
        self.canvas.create_rectangle(bar_left, 0, bar_right, height, fill="#444", outline="black")
        self.draw_triangles(width, height)
        self.draw_pieces(width, height)
        self.dice.draw(self.canvas, width, height)
        self.draw_bar_pieces()

    def draw_triangles(self, width, height):
        for idx in range(24):
            i, top = self.get_triangle_index_and_top(idx)
            coords = get_triangle_coords(i, self.segment_width, width, height, top)
            color = self.triangles[idx].highlight_color or (COLOR_1 if i % 2 == 0 else COLOR_2)
            self.canvas.create_polygon(*coords, fill=color, outline="black")

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
        self.canvas.create_oval(x - piece_radius, y - piece_radius,
                                x + piece_radius, y + piece_radius,
                                fill=color, outline="black", width=2)

    def draw_bar_pieces(self):
        bar_left = 6 * self.segment_width
        bar_right = 7 * self.segment_width
        bar_mid_x = (bar_left + bar_right) / 2

        piece_radius = max(5, int(min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 40))
        spacing = 2 * piece_radius

        for i in range(self.bar_black):
            x = bar_mid_x
            y = 50 + i * spacing
            self.canvas.create_oval(x - piece_radius, y - piece_radius,
                                    x + piece_radius, y + piece_radius,
                                    fill="black", outline="white", width=2)

        canvas_height = self.canvas.winfo_height()
        for i in range(self.bar_white):
            x = bar_mid_x
            y = canvas_height - 50 - i * spacing  # stack them upward
            self.canvas.create_oval(x - piece_radius, y - piece_radius,
                                    x + piece_radius, y + piece_radius,
                                    fill="white", outline="black", width=2)


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
        self.moves_used = 0

    def roll(self):
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
        self.moves_used = 0
        self.has_rolled = True
        print(f"Dice rolled: {self.rolls}")

    def reset_roll(self):
        self.has_rolled = False
        self.rolls = []
        self.used_rolls = []
        self.initial_roll_order = []
        self.moves_used = 0

    def use_distance(self, distance):
        if not self.rolls:
            return

        if distance in self.rolls:
            self.rolls.remove(distance)
            self.used_rolls.append(distance)
            self.moves_used += 1
            print(f"Used single die: {distance}")
            return

        if len(set(self.rolls)) == 1:
            face = self.rolls[0]
            available_count = len(self.rolls)
            if distance % face == 0:
                k = distance // face
                if k <= available_count:
                    for _ in range(k):
                        self.rolls.remove(face)
                        self.used_rolls.append(face)
                        self.moves_used += 1
                    print(f"Used double dice multiple: {distance} ({k}×{face})")
                    if not self.rolls:
                        print("Exhausted moves for doubles.")
                    return

        if self._remove_combination_that_sums(distance, [], 0):
            print(f"Used combined dice = {distance}")
        else:
            print(f"Could not use distance = {distance} with dice = {self.rolls}")

        if len(set(self.initial_roll_order)) == 1 and not self.rolls:
            print("Exhausted moves for doubles.")

    def _remove_combination_that_sums(self, target, chosen, start_index):
        if target == 0 and chosen:
            for val in chosen:
                self.rolls.remove(val)
                self.used_rolls.append(val)
                self.moves_used += 1
            return True
        if target < 0:
            return False

        for i in range(start_index, len(self.rolls)):
            val = self.rolls[i]
            chosen.append(val)
            if self._remove_combination_that_sums(target - val, chosen, i + 1):
                return True
            chosen.pop()

        return False

    def draw(self, canvas, width, height):
        if not self.initial_roll_order:
            return
        segment_width = width / 13
        bar_left = 6 * segment_width
        bar_right = 7 * segment_width
        bar_width = bar_right - bar_left
        dice_size = min(bar_width / 2.3, height / 12)
        dice_padding = dice_size / 4

        center_x = (bar_left + bar_right) / 2
        center_y = height / 2

        used_vals_count = {}
        for v in self.used_rolls:
            used_vals_count[v] = used_vals_count.get(v, 0) + 1

        all_dice = []
        for val in self.initial_roll_order:
            if used_vals_count.get(val, 0) > 0:
                all_dice.append({"value": val, "used": True})
                used_vals_count[val] -= 1
            else:
                all_dice.append({"value": val, "used": False})

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

            fill_color = "#CCCCCC" if die["used"] else "white"
            outline_color = "#666666" if die["used"] else "black"

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

        button_ai = tk.Button(self.menu_frame, text="Play vs AI", font=("Helvetica", 14), command=self.menu_vs_ai)
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
