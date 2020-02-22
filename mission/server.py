import logging
import socket
from simplejson.errors import JSONDecodeError
from json import loads, dumps
from mission.errors import SimpleConnectorError
from mission.config import load_config
from socketserver import TCPServer, BaseRequestHandler


def get_local_ip():
    """
    Gets local ip based on socket
    Source: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib"""
    IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
     if not ip.startswith("127.")][:1], [[(s.connect(("8.8.8.8", 53)),
                                                        s.getsockname()[0],
                                                        s.close())
     for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return IP


class CoordinateRequestHandler(BaseRequestHandler):
    def handle(self):
        return


class CoordinateHandler:
    def __init__(self, address: tuple):
        """
        Handler for bidirectional coordinate communication with socketserver
        address: (ip, port)
        """
        self.server = TCPServer((get_local_ip(), 65534),
                                CoordinateRequestHandler)
        return

    def send(x, y):
        """Broadcasts x and y to all connected clients"""
        return


class SimpleConnector:
    def __init__(self, address=(), mode="server"):
        self.address = address
        self.mode = mode
        self.host = get_local_ip()
        self.setup(mode)
        return

    def setup(self):
        """Setups socket instance and creates socket
           for listining/ or connects to address depending on mode"""
        self.config = load_config(instance="SimpleConnector")
        self.socket = socket.socket()  # get instance

        if self.mode == "server":
            self.socket.bind((self.host, self.config["port"]))
            self.socket.listen(1)
        elif self.mode == "client":
            self.socket.connect(self.address)
            self.connected = True

    def accept(self):
        """Accepts connections in server mode"""
        if self.mode == "server":
            logging.info("Accepting Connections ...")
            self.conn, self.address = self.socket.accept()
            logging.info(f"{self.address} connected")
            self.connected = True
        else:
            raise SimpleConnectorError("Accept is not allowed for client mode")

    def recv(self, parse=True):
        if parse:
            return self.parse(self.conn.recv(1024).decode())
        else:
            return self.conn.recv(1024).decode()

    def is_connected(self):
        """Bind for convenience to connected attribute"""
        return self.connected

    def send(self, x, y):
        """Send x and y to client as json"""
        self._send(dumps({"x": x, "y": y}))

    def _send(self, data):
        """Sends raw data"""
        if self.mode == "server":
            self.conn.send(data.encode())
        elif self.mode == "client":
            self.socket.sendall(data.encode())

    def parse(self, data):
        """parses data to json"""
        if data is None:
            return None
        try:
            return loads(data)
        except JSONDecodeError:
            raise SimpleConnectorError("JSON Data was not porperly transported")

    def close(self):
        """Closes connection in both modes"""
        self.conn.close()
        self.connected = False
