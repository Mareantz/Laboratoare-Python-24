import pickle
import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class Triangle:
    """
    Represents a triangle (point) on the Backgammon board.

    Each triangle can hold a number of white and black pieces.
    """

    def __init__(self, index):
        """
        Initializes a Triangle instance.

        Sets up the triangle with no pieces initially.

        Parameters:
            index (int): The index of the triangle (0-23).
        """
        self.index = index
        self.pieces_white = 0
        self.pieces_black = 0


class GameServer:
    """
    Represents the Backgammon Game Server.

    Manages client connections, game state synchronization, and turn management.
    """

    def __init__(self, host='127.0.0.1', port=12345):
        """
        Initializes the GameServer instance.

        Sets up the server socket, binds to the specified host and port,
        and initializes the game state.

        Parameters:
            host (str, optional): The IP address to bind the server. Defaults to '127.0.0.1'.
            port (int, optional): The port number to bind the server. Defaults to 12345.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        self.clients = []
        self.colors = ["white", "black"]
        self.current_turn = 0
        self.triangles = [Triangle(i) for i in range(24)]
        self.bar_white = 0
        self.bar_black = 0
        self.white_boreoff = 0
        self.black_boreoff = 0
        print(f"Server started on {self.host}:{self.port}")

    def broadcast_game_state(self, exclude_client=None):
        """
        Broadcasts the current game state to all connected clients.

        Optionally excludes a specified client from the broadcast (typically the one who
        initiated the change).

        Parameters:
            exclude_client (socket.socket, optional): The client socket to exclude from the broadcast.
                                                     Defaults to None.
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
        for client in self.clients:
            if client != exclude_client:
                try:
                    client.send(pickle.dumps({"type": "game_state", "data": game_state}))
                    logging.debug(f"Sent game state to client {client.getpeername()}.")
                except Exception as e:
                    logging.error(f"Failed to send game state to client {client.getpeername()}: {e}")

    def notify_turn(self):
        """
        Notifies all clients about whose turn it is.

        Sends a message indicating whether each client is currently allowed to make a move.
        """
        for i, client in enumerate(self.clients):
            try:
                client.send(pickle.dumps({"type": "turn", "data": i == self.current_turn}))
                logging.debug(f"Notified client {client.getpeername()} of their turn status: {i == self.current_turn}.")
            except Exception as e:
                logging.error(f"Failed to notify client {client.getpeername()} of turn status: {e}")

    def client_handler(self, client_socket, addr):
        """
        Handles communication with a connected client.

        Receives messages from the client, processes them, and updates the game state accordingly.

        Parameters:
            client_socket (socket.socket): The socket connected to the client.
            addr (tuple): The address of the connected client.
        """
        color = self.colors[len(self.clients) % 2]
        self.clients.append(client_socket)
        response = {"color": color}
        try:
            client_socket.send(pickle.dumps(response))
            logging.info(f"Client connected: {addr} assigned color: {color}")
        except Exception as e:
            logging.error(f"Failed to send initial color to client {addr}: {e}")
            self.clients.remove(client_socket)
            client_socket.close()
            return

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    logging.info(f"No data received. Client {addr} may have disconnected.")
                    break

                request = pickle.loads(data)
                logging.info(f"Received request from {addr}: {request}")

                if request["type"] == "move":
                    self.broadcast_game_state(exclude_client=client_socket)
                    self.current_turn = (self.current_turn + 1) % len(self.clients)
                    self.notify_turn()

                elif request["type"] == "turn_end":
                    self.current_turn = (self.current_turn + 1) % len(self.clients)
                    self.notify_turn()

                elif request["type"] == "game_state":
                    game_state = request["data"]
                    for triangle in game_state["triangles"]:
                        triangle["index"] = 23 - triangle["index"]
                    self.triangles = [Triangle(t["index"]) for t in game_state["triangles"]]
                    for t in self.triangles:
                        t.pieces_white = next(
                            (tr["pieces_white"] for tr in game_state["triangles"] if tr["index"] == t.index), 0)
                        t.pieces_black = next(
                            (tr["pieces_black"] for tr in game_state["triangles"] if tr["index"] == t.index), 0)
                    self.bar_white = game_state.get("bar_white", 0)
                    self.bar_black = game_state.get("bar_black", 0)
                    self.white_boreoff = game_state.get("white_boreoff", 0)
                    self.black_boreoff = game_state.get("black_boreoff", 0)
                    self.broadcast_game_state(exclude_client=client_socket)

            except Exception as e:
                logging.error(f"Error with client {addr}: {e}")
                break

        logging.info(f"Client {addr} disconnected.")
        self.clients.remove(client_socket)
        client_socket.close()

    def start(self):
        """
        Starts the Game Server.

        Listens for incoming client connections and spawns a new thread to handle each client.
        """
        logging.info("Waiting for connections...")
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.client_handler, args=(client_socket, addr), daemon=True)
                thread.start()
                logging.info(f"Started thread for client {addr}.")
            except Exception as e:
                logging.error(f"Error accepting connections: {e}")
                break


if __name__ == "__main__":
    server = GameServer()
    server.start()
