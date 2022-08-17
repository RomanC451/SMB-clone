import socket
from _thread import start_new_thread

from .game import ServerGame

server = "192.168.1.11"
port = 5555

max_players = 2


class Server:
    def __init__(self) -> None:

        self.server_game = ServerGame()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_server()
        self.start_listening()

        # server_ip = socket.gethostbyname(server)

    def bind_server(self) -> None:
        try:
            self.socket.bind((server, port))

        except socket.error as e:
            print(str(e))

    def start_listening(self) -> None:
        self.socket.listen(max_players)
        print("Waiting for connections......")

        while True:
            conn, addr = self.socket.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))

    def threaded_client(self, conn: socket.socket) -> None:

        player_id = self.server_game.create_player()

        conn.send(str.encode(player_id))

        while True:
            # try:
            data = conn.recv(2048).decode("utf-8")

            if not data:
                conn.send(str.encode("Goodbye"))
                break

            inputs = data_to_info(data)
            print(f"Recieved from id {id}: " + str(inputs))

            self.server_game.run(id, inputs)
            self.server_game.send_back_all_data(conn)

        # except:
        #     break

        print("Connection Closed")
        conn.close()


def data_to_info(data: str) -> list:

    return data.split(":")[1].split(",")
