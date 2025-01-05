import tkinter as tk
import random
import socket
import pickle
import threading
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

SERVER_PORT = 12345
SERVER_HOST = '127.0.0.1'
COLOR_BURGUNDY = "#800020"
COLOR_RUSSET = "#8B4513"
COLOR_TAN = "#D8B98A"
BAR_COLOR = "#444"
USED_DICE_COLOR = "#CCCCCC"
UNUSED_DICE_COLOR = "white"

client_socket = None


def listen_from_server(board_app):
    """
    Listens for messages from the server and updates the game state accordingly.

    Continuously receives data from the server, deserializes it, and performs actions based on
    the message type, such as updating the game state or handling turn changes.

    Parameters:
        board_app (BackgammonBoard): The instance of the BackgammonBoard to update.
    """
    global client_socket
    if client_socket is None:
        logging.error("Socket is not connected.")
        return
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            response = pickle.loads(data)
            logging.debug(f"Server response: {response}")
            response_type = response.get("type")
            data = response.get("data")

            if response_type == "game_state":
                board_app.update_game_state(data)
            elif response_type == "turn":
                board_app.your_turn = data
                logging.info(f"Your turn: {board_app.your_turn}")
        except Exception as e:
            logging.error(f"Connection interrupted: {e}")
            break


def send_message_to_server(msg):
    """
    Sends a serialized message to the server.

    Serializes the provided message using pickle and sends it through the client socket.

    Parameters:
        msg (dict): The message to send, typically containing 'type' and 'data' keys.
    """
    global client_socket
    if client_socket is None:
        logging.error("Socket is not connected.")
        return

    try:
        client_socket.send(pickle.dumps(msg))
    except Exception as e:
        logging.error(f"Error sending message: {e}")


def get_board_state(player_color="white"):
    """
    Initializes the board state based on the player's color.

    Sets up the initial positions of the pieces on the board. If the player is black,
    it mirrors the standard white setup to maintain symmetry.

    Parameters:
        player_color (str, optional): The color of the player ("white" or "black").
                                       Defaults to "white".

    Returns:
        list of Triangle: A list containing 24 Triangle instances representing the board.
    """
    triangles = [Triangle(i) for i in range(24)]
    config = {
        0: {"black": 2}, 5: {"white": 5}, 7: {"white": 3}, 11: {"black": 5},
        12: {"white": 5}, 16: {"black": 3}, 18: {"black": 5}, 23: {"white": 2}
    }

    if player_color == "black":
        for piece_data in config.values():
            if "black" in piece_data:
                piece_data["white"] = piece_data.pop("black")
            elif "white" in piece_data:
                piece_data["black"] = piece_data.pop("white")

    for index, piece_data in config.items():
        triangles[index].pieces_white = piece_data.get("white", 0)
        triangles[index].pieces_black = piece_data.get("black", 0)

    return triangles


def get_triangle_coords(index, segment_width, width, height, is_top):
    """
    Calculates the coordinates of a triangle on the board.

    Determines the vertices of a triangular point based on its index and orientation.

    Parameters:
        index (int): The index of the triangle (0-23).
        segment_width (float): The width of one board segment.
        width (int): The total width of the canvas.
        height (int): The total height of the canvas.
        is_top (bool): True if the triangle is on the top row, False otherwise.

    Returns:
        list of float: A list containing the (x, y) coordinates of the triangle's vertices.
    """
    actual_col = index if index < 6 else (index + 1)
    if is_top:
        x_left = width - actual_col * segment_width
        x_right = x_left - segment_width
        return [x_left, 0, x_right, 0, (x_left + x_right) / 2, height / 2]
    else:
        x_left = actual_col * segment_width
        x_right = x_left + segment_width
        return [x_left, height, x_right, height, (x_left + x_right) / 2, height / 2]


def calculate_target_index(start_index, distance, for_ai):
    """
    Calculates the target index based on the start index and distance.

    Adjusts the target index calculation based on whether the move is for the AI.

    Parameters:
        start_index (int): The starting index of the move (0-23).
        distance (int): The distance to move.
        for_ai (bool): True if the move is for the AI, False otherwise.

    Returns:
        int or None: The target index after moving, or None if out of bounds.
    """
    if for_ai:
        start_index = 23 - start_index
    target = start_index - distance
    if 0 <= target < 24:
        return 23 - target if for_ai else target
    return None


def get_triangle_index_and_orientation(index):
    """
    Determines the triangle index and its orientation (top or bottom).

    Parameters:
        index (int): The index of the triangle (0-23).

    Returns:
        tuple: A tuple containing the adjusted index and a boolean indicating if it's on the top.
    """
    if index >= 12:
        return 23 - index, True
    return 11 - index, False


class Triangle:
    """
    Represents a triangle on the Backgammon board.

    Each triangle can hold a number of white and black pieces and can be highlighted for possible moves.
    """

    def __init__(self, index):
        """
        Initializes a Triangle instance.

        Sets up the initial state with no pieces and no highlight.

        Parameters:
            index (int): The index of the triangle (0-23).
        """
        self.index = index
        self.pieces_white = 0
        self.pieces_black = 0
        self.highlight_color = None

    def add_piece(self, color):
        """
        Adds a piece of the specified color to the triangle.

        Parameters:
            color (str): The color of the piece ("white" or "black").
        """
        if color == 'white':
            self.pieces_white += 1
        else:
            self.pieces_black += 1

    def remove_piece(self, color):
        """
        Removes a piece of the specified color from the triangle.

        Parameters:
            color (str): The color of the piece to remove ("white" or "black").
        """
        if color == 'white' and self.pieces_white > 0:
            self.pieces_white -= 1
        elif color == 'black' and self.pieces_black > 0:
            self.pieces_black -= 1

    def can_move(self, color):
        """
        Determines if a piece of the specified color can move from this triangle.

        A move is possible if the opponent has fewer than two pieces on this triangle.

        Parameters:
            color (str): The color of the player ("white" or "black").

        Returns:
            bool: True if a move is possible, False otherwise.
        """
        opponent_count = self.pieces_black if color == 'white' else self.pieces_white
        return opponent_count < 2


class Dice:
    """
    Manages the dice mechanics in the game.

    Handles rolling, tracking used rolls, and rendering dice on the game board.
    """

    def __init__(self):
        """
        Initializes a new instance of the Dice class.

        Sets up the initial state for rolls, used rolls, and tracking.
        """
        self.rolls = []
        self.used_rolls = []
        self.initial_roll_order = []
        self.has_rolled = False
        self.moves_used = 0

    def roll(self):
        """
        Rolls the dice for the current turn.

        Generates two random integers between 1 and 6. If both dice show the same number,
        it sets up four moves of that number (doubles). Otherwise, it sets up two distinct moves.

        Logs the result of the roll.

        Does nothing if the dice have already been rolled for the current turn.
        """
        if self.has_rolled:
            logging.info("Already rolled")
            return
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.rolls = [d1, d1, d1, d1] if d1 == d2 else [d1, d2]
        self.initial_roll_order = self.rolls.copy()
        self.used_rolls = []
        self.moves_used = 0
        self.has_rolled = True
        logging.info(f"Dice rolled: {self.rolls}")

    def reset_roll(self):
        """
        Resets the dice to their initial unrolled state.

        Clears all current rolls, used rolls, and resets the rolled flag.
        """
        self.has_rolled = False
        self.rolls = []
        self.used_rolls = []
        self.initial_roll_order = []
        self.moves_used = 0

    def use_distance(self, distance):
        """
        Marks a distance as used based on the current rolls.

        Attempts to use a single roll matching the distance. If not possible,
        it checks for multiple rolls that sum up to the distance.

        Logs the action taken or warns if the distance cannot be used.

        Parameters:
            distance (int): The distance to be used for moving a piece.
        """
        if not self.rolls:
            return

        if distance in self.rolls:
            self.rolls.remove(distance)
            self.used_rolls.append(distance)
            self.moves_used += 1
            logging.info(f"Used single die: {distance}")
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
                    logging.info(f"Used multiple dice: {distance} ({k}×{face})")
                    if not self.rolls:
                        logging.info("Exhausted moves for doubles.")
                    return

        if self.remove_combination_that_sums(distance, [], 0):
            logging.info(f"Used combined dice: {distance}")
        else:
            logging.warning(f"Could not use distance: {distance} with dice: {self.rolls}")

        if len(set(self.initial_roll_order)) == 1 and not self.rolls:
            logging.info("Exhausted moves for doubles.")

    def remove_combination_that_sums(self, target, chosen, start_index):
        """
        Recursively attempts to find a combination of rolls that sum to the target.

        Parameters:
            target (int): The target sum to achieve.
            chosen (list): The current combination of rolls being considered.
            start_index (int): The current index in the rolls list.

        Returns:
            bool: True if a valid combination is found and used; False otherwise.
        """
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
            if self.remove_combination_that_sums(target - val, chosen, i + 1):
                return True
            chosen.pop()

        return False

    def draw(self, canvas, width, height):
        """
        Draws the dice on the provided canvas.

        Represents used and unused dice with different colors and positions.

        Parameters:
            canvas (tk.Canvas): The canvas on which to draw the dice.
            width (int): The width of the canvas.
            height (int): The height of the canvas.
        """
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
        temp_count = dict(used_vals_count)
        for val in self.initial_roll_order:
            if temp_count.get(val, 0) > 0:
                all_dice.append({"value": val, "used": True})
                temp_count[val] -= 1
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
            fill_color = USED_DICE_COLOR if die["used"] else UNUSED_DICE_COLOR
            outline_color = "#666666" if die["used"] else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=2)
            draw_dice_face(canvas, die["value"], x1, y1, x2, y2)


def draw_dice_face(canvas, dice_value, x1, y1, x2, y2):
    """
    Draws the dots on a die face based on the dice value.

    Parameters:
        canvas (tk.Canvas): The canvas on which to draw the dice face.
        dice_value (int): The numerical value of the dice (1-6).
        x1 (int): The x-coordinate of the top-left corner of the dice.
        y1 (int): The y-coordinate of the top-left corner of the dice.
        x2 (int): The x-coordinate of the bottom-right corner of the dice.
        y2 (int): The y-coordinate of the bottom-right corner of the dice.
    """
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
        6: [(-spacing, -spacing), (-spacing, 0), (-spacing, spacing),
            (spacing, -spacing), (spacing, 0), (spacing, spacing)],
    }

    for dx, dy in offsets[dice_value]:
        px = center_x + dx * (x2 - x1) / 2
        py = center_y + dy * (y2 - y1) / 2
        canvas.create_oval(px - radius, py - radius, px + radius, py + radius, fill="black")


class BackgammonBoard:
    """
    Represents the Backgammon game board and manages game logic.

    Handles drawing the board, managing game state, player interactions, AI moves,
    and communication with the server for networked gameplay.
    """

    def __init__(self, parent, player_color="white", networked=False, client_sock=None):
        """
        Initializes a BackgammonBoard instance.

        Sets up the board state, canvas, UI elements, and network thread if applicable.

        Parameters:
            parent (tk.Frame): The parent Tkinter frame.
            player_color (str, optional): The color of the player ("white" or "black").
                                          Defaults to "white".
            networked (bool, optional): True if the game is networked (multiplayer),
                                        False for local play against AI. Defaults to False.
            client_sock (socket.socket, optional): The client socket for networked play.
                                                   Defaults to None.
        """
        self.parent = parent
        self.player_color = player_color
        self.networked = networked
        self.client_sock = client_sock
        self.triangles = get_board_state(player_color)
        self.dice = Dice()

        self.bar_white = 0
        self.bar_black = 0
        self.white_boreoff = 0
        self.black_boreoff = 0

        self.canvas = tk.Canvas(self.parent, bg=COLOR_TAN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_triangle_click)

        self.white_counter_label = tk.Label(
            self.parent, text=f"White: {self.white_boreoff}",
            font=("Helvetica", 14), bg=COLOR_TAN
        )
        self.white_counter_label.pack(side=tk.LEFT, padx=10)

        self.black_counter_label = tk.Label(
            self.parent, text=f"Black: {self.black_boreoff}",
            font=("Helvetica", 14), bg=COLOR_TAN
        )
        self.black_counter_label.pack(side=tk.RIGHT, padx=10)

        self.bore_off_button = tk.Button(
            self.parent, text="Bore Off", font=("Helvetica", 14),
            state=tk.DISABLED, command=self.perform_bore_off
        )
        self.bore_off_button.pack(side=tk.BOTTOM, pady=10)

        self.segment_width = None
        self.selected_triangle = None

        self.current_player_color = player_color
        self.ai_color = "black" if self.current_player_color == "white" else "white"

        self.your_turn = True if self.current_player_color == "white" else False
        self.network_thread = None

        if self.networked and self.client_sock:
            self.network_thread = threading.Thread(target=listen_from_server, args=(self,),
                                                   daemon=True)
            self.network_thread.start()

    def update_game_state(self, game_state):
        """
        Updates the game state based on data received from the server.

        Synchronizes the local game state with the server-provided state.

        Parameters:
            game_state (dict): A dictionary containing the updated game state,
                               including triangles, bar counts, and boreoff counts.
        """
        for triangle_data in game_state["triangles"]:
            index = triangle_data["index"]
            self.triangles[index].pieces_white = triangle_data["pieces_white"]
            self.triangles[index].pieces_black = triangle_data["pieces_black"]

        self.bar_white = game_state["bar_white"]
        self.bar_black = game_state["bar_black"]
        self.white_boreoff = game_state["white_boreoff"]
        self.black_boreoff = game_state["black_boreoff"]
        self.update_counters()

        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def update_counters(self):
        """
        Updates the bore-off counters on the UI.

        Reflects the current number of borne-off pieces for both players.
        """
        self.white_counter_label.config(text=f"White: {self.white_boreoff}")
        self.black_counter_label.config(text=f"Black: {self.black_boreoff}")

    def perform_bore_off(self):
        """
        Handles the bore-off action for the current player.

        Attempts to bear off pieces based on the current dice rolls. If successful,
        updates the game state and checks for the end of the turn or game.
        """
        color = self.current_player_color
        home_indices = range(0, 6)

        for roll in sorted(self.dice.rolls, reverse=True):
            for index in reversed(home_indices):
                triangle = self.triangles[index]
                if ((color == 'white' and triangle.pieces_white > 0) or
                    (color == 'black' and triangle.pieces_black > 0)) and index - roll <= -1:
                    self.bore_off(triangle, color, roll)
                    self.canvas.delete("all")
                    self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())
                    self.check_end_of_turn()
                    return
        logging.info("No valid pieces to bear off with the current dice.")

    def bore_off(self, triangle, color, dice_value):
        """
        Bores off a piece from the board.

        Removes a piece from the specified triangle, updates the bore-off count,
        uses the corresponding dice value, and checks for game end conditions.

        Parameters:
            triangle (Triangle): The triangle from which to bore off a piece.
            color (str): The color of the player performing the bore-off ("white" or "black").
            dice_value (int): The dice value used to perform the bore-off.
        """
        triangle.remove_piece(color)
        if color == 'white':
            self.white_boreoff += 1
        else:
            self.black_boreoff += 1

        self.update_counters()
        self.dice.use_distance(dice_value)
        self.send_game_state()
        self.bore_off_button.config(state=tk.DISABLED)
        self.check_game_end()

    def move_piece(self, start_index, target_index):
        """
        Moves a piece from start_index to target_index.

        Handles capturing opponent pieces if present and updates the game state accordingly.

        Parameters:
            start_index (int): The index of the triangle from which to move a piece.
            target_index (int): The index of the triangle to which to move the piece.
        """
        if not self.your_turn and self.networked is True:
            logging.warning("Not your turn!")
            return
        start_triangle = self.triangles[start_index]
        target_triangle = self.triangles[target_index]
        distance_used = abs(start_index - target_index)

        if self.current_player_color == 'white' and target_triangle.pieces_black == 1:
            target_triangle.remove_piece('black')
            self.bar_black += 1
        elif self.current_player_color == 'black' and target_triangle.pieces_white == 1:
            target_triangle.remove_piece('white')
            self.bar_white += 1

        start_triangle.remove_piece(self.current_player_color)
        target_triangle.add_piece(self.current_player_color)

        self.dice.use_distance(distance_used)
        self.send_game_state()

    def reenter_piece(self, color, target_index):
        """
        Reenters a piece from the bar onto the board.

        Handles capturing opponent pieces if necessary and updates the bar counts.

        Parameters:
            color (str): The color of the player reentering a piece ("white" or "black").
            target_index (int): The index of the triangle where the piece will reenter.
        """
        triangle = self.triangles[target_index]
        opponent_color = 'white' if color == 'black' else 'black'
        if opponent_color == 'white' and triangle.pieces_white == 1:
            triangle.remove_piece('white')
            self.bar_white += 1
        elif opponent_color == 'black' and triangle.pieces_black == 1:
            triangle.remove_piece('black')
            self.bar_black += 1

        triangle.add_piece(color)
        if color == 'white':
            self.bar_white -= 1
        else:
            self.bar_black -= 1

        self.send_game_state()

    def roll_dice(self):
        """
        Rolls the dice for the current player.

        Manages the rolling state, checks for valid moves, highlights reentry options
        if pieces are on the bar, and updates the game board accordingly.
        """
        if not self.your_turn and self.networked is True:
            logging.warning("Not your turn!")
            return
        if self.current_player_color == self.ai_color:
            logging.info("It's AI's turn; you can't roll.")
            return
        if not self.dice.has_rolled:
            self.dice.roll()
            if not self.has_valid_moves(self.current_player_color):
                logging.info(f"No valid moves for {self.current_player_color}. Passing turn.")
                self.dice.reset_roll()
                self.switch_player()
                return

            if ((self.current_player_color == 'white' and self.bar_white > 0) or
                    (self.current_player_color == 'black' and self.bar_black > 0)):
                logging.info("Player has pieces on the bar. Highlighting reentry options.")
                self.highlight_bar_reentry_options()

            self.canvas.delete("all")
            self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())
        else:
            logging.info("Already rolled")
        self.check_end_of_turn()

    def switch_player(self):
        """
        Switches the turn to the next player.

        Toggles the `your_turn` flag, updates the current player color,
        and initiates AI moves if applicable.
        """
        self.your_turn = not self.your_turn
        if self.networked is False:
            self.current_player_color = 'white' if self.current_player_color == 'black' else 'black'

        if self.networked is True and self.your_turn is False:
            send_message_to_server({"type": "turn_end"})

        if self.current_player_color == self.ai_color and self.networked is False:
            self.ai_move()

        self.bore_off_button.config(state=tk.DISABLED)
        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def has_valid_moves(self, color):
        """
        Checks if the current player has any valid moves.

        Evaluates all possible moves based on the current dice rolls and board state.

        Parameters:
            color (str): The color of the player to check ("white" or "black").

        Returns:
            bool: True if there are valid moves available, False otherwise.
        """
        if not self.dice.rolls:
            return False

        if (color == 'white' and self.bar_white > 0) or (color == 'black' and self.bar_black > 0):
            for roll in self.dice.rolls:
                reentry_index = self.get_reentry_index(is_ai=(color == self.ai_color), dice_value=roll)
                if reentry_index is not None:
                    logging.debug(f"Valid reentry move found for {color} with roll {roll}")
                    return True
            logging.debug(f"No valid reentry moves for {color}")
            return False

        for start_index, triangle in enumerate(self.triangles):
            piece_count = triangle.pieces_white if color == 'white' else triangle.pieces_black
            if piece_count > 0:
                for roll in self.dice.rolls:
                    for_ai = (color == self.ai_color)
                    target_index = calculate_target_index(start_index, roll, for_ai=for_ai)
                    if target_index is not None and self.triangles[target_index].can_move(color):
                        return True
                    if self.check_bearing_off(is_ai=for_ai):
                        return True
        return False

    def check_bearing_off(self, is_ai):
        """
        Checks if the player can bear off their pieces.

        Evaluates whether all pieces are in the home zone and no pieces are on the bar
        to determine if bearing off is possible.

        Parameters:
            is_ai (bool): True if checking for AI, False for human player.

        Returns:
            bool: True if bearing off is possible, False otherwise.
        """
        home_indices = range(0, 6) if not is_ai else range(18, 24)
        current_color = self.current_player_color if not is_ai else self.ai_color

        pieces_boredoff = self.white_boreoff if current_color == "white" else self.black_boreoff
        pieces_on_bar = self.bar_white if current_color == "white" else self.bar_black

        pieces_in_home_zone = sum(
            self.triangles[i].pieces_white if current_color == "white"
            else self.triangles[i].pieces_black
            for i in home_indices
        )

        pieces_outside_home_zone = sum(
            self.triangles[i].pieces_white if current_color == "white"
            else self.triangles[i].pieces_black
            for i in range(24) if i not in home_indices
        )

        total_pieces = pieces_boredoff + pieces_on_bar + pieces_in_home_zone + pieces_outside_home_zone

        if total_pieces != 15 or pieces_outside_home_zone > 0:
            return False

        return True

    def check_end_of_turn(self):
        """
        Checks if the current turn should end based on dice usage and valid moves.

        If there are no remaining dice or no valid moves, it resets the dice and switches the turn.
        """
        if not self.dice.rolls or not self.has_valid_moves(self.current_player_color):
            logging.info(f"{self.current_player_color.capitalize()} has no dice left. Switching turn.")
            self.dice.reset_roll()
            self.switch_player()

    def check_game_end(self):
        """
        Checks if the game has ended and declares the winner.

        Determines if either player has borne off all their pieces and ends the game if so.
        """
        if self.white_boreoff == 15:
            logging.info("White has won!")
            self.end_game()
        elif self.black_boreoff == 15:
            logging.info("Black has won!")
            self.end_game()

    def end_game(self):
        """
        Ends the game and closes the application.

        Clears the canvas and terminates the Tkinter main loop.
        """
        logging.info("Game over!")
        self.canvas.delete("all")
        self.parent.destroy()

    def ai_move(self):
        """
        Handles the AI's move logic.

        Automates the AI's decision-making process to perform valid moves based on dice rolls,
        including reentry from the bar and bearing off.
        """
        if self.current_player_color != self.ai_color:
            return

        if not self.dice.has_rolled:
            self.dice.roll()
            logging.info(f"AI rolled: {self.dice.rolls}")

            if not self.has_valid_moves(self.current_player_color):
                logging.info(f"No valid moves for {self.current_player_color}. Passing turn.")
                self.dice.reset_roll()
                self.switch_player()
                return

        move_made = False

        while (self.ai_color == 'white' and self.bar_white > 0) or \
                (self.ai_color == 'black' and self.bar_black > 0):
            used_any = self.ai_reentry()
            if used_any:
                move_made = True
            else:
                logging.info("AI passing turn.")
                break

        if (self.ai_color == 'white' and self.bar_white > 0) or \
                (self.ai_color == 'black' and self.bar_black > 0):
            logging.info("AI still has pieces on the bar but no reentry moves. Passing turn.")
            self.dice.reset_roll()
            self.switch_player()
            return

        self.ai_bear_off()

        if ((self.ai_color == 'white' and self.bar_white == 0) or
            (self.ai_color == 'black' and self.bar_black == 0)) and self.dice.rolls:

            while self.dice.rolls:
                for roll in self.dice.rolls[:]:
                    start_index = self.find_ai_start_for_roll(roll)
                    if start_index is not None:
                        target_index = calculate_target_index(start_index, roll, for_ai=True)
                        if target_index is not None and self.triangles[target_index].can_move(self.ai_color):
                            self.move_piece(start_index, target_index)
                            move_made = True
                            if not self.has_valid_moves(self.ai_color):
                                logging.info(f"No valid moves for {self.ai_color} after a move. Ending turn.")
                                self.dice.reset_roll()
                                self.switch_player()
                                return
                else:
                    break

        if not self.dice.rolls or not move_made:
            logging.info("AI has no valid moves or finished its dice. Passing turn.")
        self.check_end_of_turn()

    def ai_bear_off(self):
        """
        Handles the AI's bearing off logic.

        If the AI can bear off, it attempts to remove pieces from the home zone based on dice rolls.
        """
        color = self.ai_color
        if not self.check_bearing_off(is_ai=True):
            return

        home_indices = range(18, 24)
        while self.dice.rolls:
            used_any_die = False
            for roll in sorted(self.dice.rolls, reverse=True):
                piece_borne_off = False

                for index in home_indices:
                    piece_count = (self.triangles[index].pieces_white if color == 'white'
                                   else self.triangles[index].pieces_black)
                    if piece_count > 0:
                        target_index = index + roll
                        if target_index == 24:
                            self.bore_off(self.triangles[index], color, roll)
                            piece_borne_off = True
                            break
                        elif target_index > 24:
                            pieces_beyond = sum(
                                self.triangles[i].pieces_white if color == 'white'
                                else self.triangles[i].pieces_black
                                for i in home_indices if i < index
                            )
                            if pieces_beyond == 0:
                                self.bore_off(self.triangles[index], color, roll)
                                piece_borne_off = True
                                break

                if piece_borne_off:
                    used_any_die = True
                    break
            if not used_any_die:
                break

        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def find_ai_start_for_roll(self, roll):
        """
        Finds a starting index for the AI to make a move based on the roll.

        Searches for a valid starting triangle that can move based on the current roll.

        Parameters:
            roll (int): The dice value being considered for the move.

        Returns:
            int or None: The index of the triangle to move from, or None if no valid move found.
        """
        for index, triangle in enumerate(self.triangles):
            count = triangle.pieces_white if self.ai_color == 'white' else triangle.pieces_black
            if count > 0:
                target_index = calculate_target_index(index, roll, for_ai=True)
                if target_index is not None and self.triangles[target_index].can_move(self.ai_color):
                    return index
        return None

    def ai_reentry(self):
        """
        Handles the AI's reentry from the bar.

        Attempts to reenter pieces from the bar based on available dice rolls.

        Returns:
            bool: True if a reentry move was made, False otherwise.
        """
        used_any_die = False

        for roll in self.dice.rolls[:]:
            target_index = self.get_reentry_index(is_ai=True, dice_value=roll)
            if target_index is not None:
                self.reenter_piece(self.ai_color, target_index)
                self.dice.use_distance(roll)
                used_any_die = True
                if (self.ai_color == 'white' and self.bar_white == 0) or (
                        self.ai_color == 'black' and self.bar_black == 0):
                    break
        return used_any_die

    def on_resize(self, event):
        """
        Handles the resizing of the canvas.

        Recalculates segment width and redraws the board to fit the new dimensions.

        Parameters:
            event (tk.Event): The event object containing resize information.
        """
        self.segment_width = event.width / 13.0
        self.canvas.delete("all")
        self.draw_board(event.width, event.height)

    def on_triangle_click(self, event):
        """
        Handles the click event on the canvas to select and move pieces.

        Determines which triangle was clicked and processes selection or movement based on game state.

        Parameters:
            event (tk.Event): The event object containing click coordinates.
        """
        if not self.your_turn and self.networked is True:
            logging.warning("Not your turn!")
            return
        if not self.segment_width:
            return

        if self.current_player_color == self.ai_color:
            return

        if ((self.current_player_color == 'white' and self.bar_white > 0) or
                (self.current_player_color == 'black' and self.bar_black > 0)):

            clicked_index = self.get_triangle_index_by_click(event.x, event.y)
            if clicked_index is not None and self.triangles[clicked_index].highlight_color == 'green':
                self.reenter_piece(self.current_player_color, clicked_index)
                distance_used = self.reentry_distance_for_index(clicked_index)
                if distance_used is not None:
                    self.dice.use_distance(distance_used)
                if self.dice.rolls:
                    if not ((self.current_player_color == 'white' and self.bar_white > 0) or
                            (self.current_player_color == 'black' and self.bar_black > 0)):
                        self.reset_highlights()
                    else:
                        self.highlight_bar_reentry_options()
                else:
                    logging.info(f"{self.current_player_color.capitalize()} cannot make more moves. Passing turn.")
                    self.check_end_of_turn()
                self.canvas.delete("all")
                self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

            else:
                if not self.dice.rolls:
                    possible = any(
                        self.get_reentry_index(is_ai=False, dice_value=roll) is not None
                        for roll in self.dice.rolls
                    )
                    if not possible:
                        logging.info(f"{self.current_player_color.capitalize()} cannot reenter. Passing turn.")
                        self.check_end_of_turn()
            return

        segment_width = self.segment_width
        height = self.canvas.winfo_height()
        is_top_row = event.y < height / 2

        col = int(event.x // segment_width)
        if col == 6:
            logging.info("Clicked on the bar")
            return
        col = col if col < 6 else col - 1

        if is_top_row:
            index = col + 12
        else:
            index = 11 - col

        logging.info(f"Clicked on triangle {index}")

        if self.selected_triangle is None:
            triangle = self.triangles[index]
            has_pieces = (triangle.pieces_white if self.current_player_color == "white" else triangle.pieces_black)
            if has_pieces > 0:
                self.selected_triangle = index
                self.highlight_possible_moves(index)
            else:
                logging.info("No pieces to select here.")
        else:
            if 0 <= index < 24 and self.triangles[index].highlight_color == "green":
                self.move_piece(self.selected_triangle, index)
                self.reset_highlights()
                self.selected_triangle = None
                if not self.dice.rolls or not self.has_valid_moves(self.current_player_color):
                    logging.info(f"{self.current_player_color.capitalize()} has no dice left. Passing turn.")
                    self.check_end_of_turn()
            else:
                logging.info("Invalid move")
                self.reset_highlights()
                self.selected_triangle = None

        self.canvas.delete("all")
        self.draw_board(self.canvas.winfo_width(), self.canvas.winfo_height())

    def get_triangle_index_by_click(self, x, y):
        """
        Determines the triangle index based on the click coordinates.

        Calculates which triangle on the board was clicked based on the (x, y) coordinates.

        Parameters:
            x (int): The x-coordinate of the click event.
            y (int): The y-coordinate of the click event.

        Returns:
            int or None: The index of the clicked triangle (0-23), or None if click is invalid.
        """
        if not self.segment_width:
            return None
        col = int(x // self.segment_width)
        if col == 6:
            return None
        col = col if col < 6 else col - 1

        height = self.canvas.winfo_height()
        is_top_row = y < height / 2

        index = col + 12 if is_top_row else 11 - col

        return index if 0 <= index < 24 else None

    def reentry_distance_for_index(self, target_index):
        """
        Determines the distance used for reentry based on the target index.

        Calculates the corresponding dice value needed to reenter a piece at the specified index.

        Parameters:
            target_index (int): The index of the triangle where the piece will reenter.

        Returns:
            int or None: The distance (dice value) used for reentry, or None if invalid.
        """
        dist = 24 - target_index
        if 18 <= target_index <= 23 and dist in self.dice.rolls:
            return dist
        return None

    def get_reentry_index(self, is_ai, dice_value):
        """
        Gets the reentry index based on dice value and player type.

        Determines the appropriate triangle index for reentry based on the dice roll
        and whether the player is AI or human.

        Parameters:
            is_ai (bool): True if the player is AI, False otherwise.
            dice_value (int): The dice value being used for reentry.

        Returns:
            int or None: The target triangle index for reentry, or None if invalid.
        """
        if is_ai:
            reentry_index = dice_value - 1
            if 0 <= reentry_index <= 5 and self.triangles[reentry_index].can_move(self.ai_color):
                return reentry_index
        else:
            reentry_index = 24 - dice_value
            if 18 <= reentry_index <= 23 and self.triangles[reentry_index].can_move(self.current_player_color):
                return reentry_index
        return None

    def highlight_possible_moves(self, start_index):
        """
        Highlights possible moves from the selected triangle.

        Evaluates all potential moves based on current dice rolls and updates the UI
        to indicate valid target triangles.

        Parameters:
            start_index (int): The index of the selected triangle.
        """
        self.reset_highlights()

        if not self.dice.rolls:
            logging.info("No dice left to use.")
            return

        dice_values = sorted(self.dice.rolls)
        possible_moves = list(dice_values)

        if len(dice_values) >= 2:
            combined_move = dice_values[0] + dice_values[1]
            if self.is_combined_move_partially_valid(start_index, dice_values[:2]):
                possible_moves.append(combined_move)

        if len(set(dice_values)) == 1:
            face = dice_values[0]
            count = len(dice_values)
            for i in range(2, count + 1):
                combined = face * i
                if not self.is_partial_double_move_valid(start_index, face, i):
                    break
                possible_moves.append(combined)

        possible_moves = sorted(set(possible_moves))

        valid_moves_found = False
        color = self.current_player_color

        for move_dist in possible_moves:
            target_index = calculate_target_index(start_index, move_dist, for_ai=False)
            if target_index is not None and self.triangles[target_index].can_move(color):
                self.triangles[target_index].highlight_color = "green"
                valid_moves_found = True

        if self.check_bearing_off(is_ai=False):
            for index in (reversed(range(0, 6))):
                for roll in dice_values:
                    if index - roll == -1:
                        self.bore_off_button.config(state=tk.NORMAL)
                        valid_moves_found = True

        if not valid_moves_found:
            logging.info("No valid moves available with the current dice.")
        else:
            greens = [t.index for t in self.triangles if t.highlight_color == "green"]
            logging.debug(f"Highlighted possible moves: {greens}")

    def highlight_bar_reentry_options(self):
        """
        Highlights possible reentry options from the bar.

        Evaluates available dice rolls and updates the UI to indicate valid reentry triangles.
        """
        can_reenter = False
        self.reset_highlights()
        for d in self.dice.rolls:
            possible_index = self.get_reentry_index(is_ai=False, dice_value=d)
            if possible_index is not None:
                self.triangles[possible_index].highlight_color = "green"
                can_reenter = True

        if can_reenter is False:
            logging.info("No valid reentry options available.")
            self.dice.reset_roll()
            self.switch_player()

    def reset_highlights(self):
        """
        Resets all triangle highlights.

        Clears any previous move highlights to prepare for new move evaluations.
        """
        for t in self.triangles:
            t.highlight_color = None

    def is_combined_move_partially_valid(self, start_index, dice_pair):
        """
        Checks if a combined move is partially valid.

        Evaluates whether combining two dice rolls results in a valid move.

        Parameters:
            start_index (int): The index of the starting triangle.
            dice_pair (list of int): A list containing two dice values.

        Returns:
            bool: True if the combined move is valid, False otherwise.
        """
        first_move, second_move = dice_pair
        first_target = calculate_target_index(start_index, first_move, for_ai=False)
        second_target = calculate_target_index(start_index, second_move, for_ai=False)
        color = self.current_player_color

        if (first_target is not None and self.triangles[first_target].can_move(color)) \
                or (second_target is not None and self.triangles[second_target].can_move(color)):
            return True
        return False

    def is_partial_double_move_valid(self, start_index, face, count):
        """
        Checks if a partial double move is valid.

        Determines if multiple moves using the same dice face are possible.

        Parameters:
            start_index (int): The index of the starting triangle.
            face (int): The dice face value being used.
            count (int): The number of times the dice face is used.

        Returns:
            bool: True if all partial moves are valid, False otherwise.
        """
        current_index = start_index
        color = self.current_player_color

        for _ in range(count):
            next_index = calculate_target_index(current_index, face, for_ai=False)
            if next_index is None or not self.triangles[next_index].can_move(color):
                return False
            current_index = next_index
        return True

    def draw_board(self, width, height):
        """
        Draws the entire board.

        Renders the bar, triangles, pieces, and dice on the canvas.

        Parameters:
            width (int): The width of the canvas.
            height (int): The height of the canvas.
        """
        bar_left = 6 * self.segment_width
        bar_right = 7 * self.segment_width
        self.canvas.create_rectangle(bar_left, 0, bar_right, height, fill=BAR_COLOR, outline="black")

        self.draw_triangles(width, height)
        self.draw_pieces(width, height)
        self.dice.draw(self.canvas, width, height)
        self.draw_bar_pieces()

    def draw_triangles(self, width, height):
        """
        Draws all the triangles on the board.

        Iterates through each triangle and renders it on the canvas with appropriate colors.

        Parameters:
            width (int): The width of the canvas.
            height (int): The height of the canvas.
        """
        for index in range(24):
            i, is_top = get_triangle_index_and_orientation(index)
            coords = get_triangle_coords(i, self.segment_width, width, height, is_top)
            fill_color = self.triangles[index].highlight_color or (COLOR_BURGUNDY if i % 2 == 0 else COLOR_RUSSET)
            self.canvas.create_polygon(*coords, fill=fill_color, outline="black")

    def draw_pieces(self, width, height):
        """
        Draws all the pieces on the board.

        Renders white and black pieces on their respective triangles.

        Parameters:
            width (int): The width of the canvas.
            height (int): The height of the canvas.
        """
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

        bottom_indices = list(range(11, -1, -1))
        top_indices = list(range(12, 24))

        draw_pieces_on_column([self.triangles[x] for x in bottom_indices], height - 20, -1)
        draw_pieces_on_column([self.triangles[x] for x in top_indices], 20, 1)

    def draw_one_piece(self, x, y, color, radius):
        """
        Draws a single game piece.

        Renders an oval representing a piece at the specified coordinates.

        Parameters:
            x (float): The x-coordinate of the center of the piece.
            y (float): The y-coordinate of the center of the piece.
            color (str): The color of the piece ("white" or "black").
            radius (int): The radius of the piece.
        """
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="black", width=2)

    def draw_bar_pieces(self):
        """
        Draws the pieces on the bar.

        Renders white and black pieces that are currently on the bar.
        """
        bar_left = 6 * self.segment_width
        bar_right = 7 * self.segment_width
        bar_mid_x = (bar_left + bar_right) / 2

        piece_radius = max(5, int(min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 40))
        spacing = 2 * piece_radius

        for i in range(self.bar_black):
            x = bar_mid_x
            y = 50 + i * spacing
            self.canvas.create_oval(
                x - piece_radius, y - piece_radius,
                x + piece_radius, y + piece_radius,
                fill="black", outline="white", width=2
            )

        canvas_height = self.canvas.winfo_height()
        for i in range(self.bar_white):
            x = bar_mid_x
            y = canvas_height - 50 - i * spacing
            self.canvas.create_oval(
                x - piece_radius, y - piece_radius,
                x + piece_radius, y + piece_radius,
                fill="white", outline="black", width=2
            )

    def send_game_state(self):
        """
        Sends the current game state to the server.

        Serializes and transmits the game state, including triangles, bar counts,
        and boreoff counts, to synchronize with the server.
        """
        game_state = {
            "triangles": [
                {"index": t.index, "pieces_white": t.pieces_white, "pieces_black": t.pieces_black}
                for t in self.triangles
            ],
            "bar_white": self.bar_white,
            "bar_black": self.bar_black,
            "white_boreoff": self.white_boreoff,
            "black_boreoff": self.black_boreoff
        }
        send_message_to_server({"type": "game_state", "data": game_state})


class MainMenu:
    """
    Represents the main menu of the Backgammon game.

    Provides options to play against AI or another human player.
    """
    def __init__(self, root):
        """
        Initializes the MainMenu instance.

        Sets up the main menu UI with options to play against AI or another human.

        Parameters:
            root (tk.Tk): The root Tkinter window.
        """
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
        """
        Handles the selection of playing against AI.

        Destroys the main menu and presents options to choose the player's color.
        """
        self.menu_frame.destroy()
        self.sub_frame = tk.Frame(self.root, padx=20, pady=20)
        self.sub_frame.pack()
        label = tk.Label(self.sub_frame, text="Choose your color:", font=("Helvetica", 14))
        label.pack(pady=5)

        button_white = tk.Button(self.sub_frame, text="White", font=("Helvetica", 14),
                                 command=lambda: self.start_board(is_white=True))
        button_white.pack(pady=5)
        button_black = tk.Button(self.sub_frame, text="Black", font=("Helvetica", 14),
                                 command=lambda: self.start_board(is_white=False))
        button_black.pack(pady=5)

    def menu_vs_human(self):
        """
        Handles the selection of playing against a human via network.

        Destroys the main menu and initiates a connection to the server.
        """
        self.menu_frame.destroy()
        self.sub_frame = tk.Frame(self.root, padx=20, pady=20)
        self.sub_frame.pack()

        label = tk.Label(self.sub_frame, text="Connecting to server...", font=("Helvetica", 14))
        label.pack(pady=5)

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        """
        Connects to the game server for multiplayer gameplay.

        Attempts to establish a socket connection to the server and initializes the game board
        upon successful connection. Handles connection errors gracefully by providing feedback
        and retry options to the user.
        """
        global client_socket
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            logging.info(f"Connected to server: {SERVER_HOST}:{SERVER_PORT}")

            data = client_socket.recv(4096)
            response = pickle.loads(data)
            starting_color = response.get("color")
            is_white = starting_color == "white"

            self.start_board(networked=True, client_sock=client_socket, is_white=is_white)
            threading.Thread(target=listen_from_server, args=(self.board_app,), daemon=True).start()

        except Exception as e:
            logging.error(f"Error connecting to server: {e}")
            self.sub_frame.destroy()
            self.menu_frame = tk.Frame(self.root, padx=20, pady=20)
            self.menu_frame.pack()
            error_label = tk.Label(
                self.menu_frame, text="Failed to connect to server.", font=("Helvetica", 14), fg="red"
            )
            error_label.pack(pady=5)
            retry_button = tk.Button(
                self.menu_frame, text="Retry", font=("Helvetica", 14), command=self.menu_vs_human
            )
            retry_button.pack(pady=5)

    def start_board(self, is_white, networked=False, client_sock=None):
        """
        Initializes the game board.

        Destroys any existing sub-frames and sets up the BackgammonBoard instance along with the
        "Roll Dice" button.

        Parameters:
            is_white (bool): True if the player chooses white, False for black.
            networked (bool, optional): True if the game is networked (multiplayer),
                                        False for local play against AI. Defaults to False.
            client_sock (socket.socket, optional): The client socket for networked play.
                                                   Defaults to None.
        """
        if self.sub_frame is not None:
            self.sub_frame.destroy()
        self.frame_board = tk.Frame(self.root)
        self.frame_board.pack(fill=tk.BOTH, expand=True)

        color = "white" if is_white else "black"
        self.board_app = BackgammonBoard(self.frame_board, player_color=color, networked=networked,
                                         client_sock=client_sock)
        button_roll = tk.Button(self.frame_board, text="Roll Dice", font=("Helvetica", 14),
                                command=self.board_app.roll_dice)
        button_roll.pack(pady=5, side=tk.BOTTOM)


def main():
    """
    The main entry point for the Backgammon game.

    Initializes the Tkinter root window, sets its size, and launches the MainMenu.
    """
    root = tk.Tk()
    root.geometry("800x600")
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
