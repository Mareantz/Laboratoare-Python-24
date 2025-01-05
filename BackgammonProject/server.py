import pickle
import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class GameServer:
    def __init__(self, host='127.0.0.1', port=12345):
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
        logging.info(f"Server started on {self.host}:{self.port}")

    def broadcast_game_state(self, exclude_client=None):
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
                client.send(pickle.dumps({"type": "game_state", "data": game_state}))

    def notify_turn(self):
        for i, client in enumerate(self.clients):
            client.send(pickle.dumps({"type": "turn", "data": i == self.current_turn}))

    def client_handler(self, client_socket, addr):
        color = self.colors[len(self.clients) % 2]
        self.clients.append(client_socket)
        response = {"color": color}
        client_socket.send(pickle.dumps(response))
        logging.info(f"Client {addr} connected as {color}")

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
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
                            tr["pieces_white"] for tr in game_state["triangles"] if tr["index"] == t.index)
                        t.pieces_black = next(
                            tr["pieces_black"] for tr in game_state["triangles"] if tr["index"] == t.index)
                    self.bar_white = game_state["bar_white"]
                    self.bar_black = game_state["bar_black"]
                    self.white_boreoff = game_state["white_boreoff"]
                    self.black_boreoff = game_state["black_boreoff"]
                    self.broadcast_game_state(exclude_client=client_socket)

            except Exception as e:
                logging.error(f"Error handling client {addr}: {e}")
                break

        logging.info(f"Client {addr} disconnected")
        client_socket.close()

    def start(self):
        logging.info("Waiting for clients to connect...")
        while True:
            client_socket, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.client_handler, args=(client_socket, addr))
            thread.start()


class Triangle:
    def __init__(self, index):
        self.index = index
        self.pieces_white = 0
        self.pieces_black = 0


if __name__ == "__main__":
    server = GameServer()
    server.start()
