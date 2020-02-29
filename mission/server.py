import logging
import socket
import asyncio
from ujson import loads, dumps
from uuid import uuid4
from mission.errors import SimpleConnectorError
from mission.config import load_config, aioload_config
from mission.helpers import get_local_ip, dump_json, parse_json


class SimpleConnector:
    """Designed for one server and one client"""
    def __init__(self, address=(), mode="server", listen=1,
                 log_level=logging.INFO):
        self.address = address
        self.mode = mode
        self.listen = listen
        self.log = logging.getLogger()
        logging.basicConfig(level=log_level, filename="space-mission.log")
        self.host = get_local_ip()
        self.setup()
        self.customize()
        return

    def setup(self):
        """Setups socket instance and creates socket
           for listining/ or connects to address depending on mode"""
        self.config = load_config(instance="SimpleConnector")
        self.socket = socket.socket()  # get instance

        if self.mode == "server":
            self.socket.bind((self.host, self.config["port"]))
            self.socket.listen(self.listen)
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

    def auto(self):
        """Operation mode for background operation with to independend clients"""
        for i in range(2):
            self.accept()

    def recv(self, parse=True):
        if self.mode == "client":
            data = self.socket.recv(1024).decode()
        elif self.mode == "server":
            data = self.conn.recv(1024).decode()
        if parse:
            return self.parse(data)
        else:
            return data

    def is_connected(self):
        """Bind for convenience to connected attribute"""
        return self.connected

    def send(self, x, y):
        """Send x and y to client as json"""
        self._send(dumps({"x": x, "y": y}))

    def _send(self, data):
        """Sends raw data"""
        if self.mode == "server":
            self.conn.sendall(data.encode())
        elif self.mode == "client":
            self.socket.send(data.encode())

    def parse(self, data):
        """parses data to json"""
        if data is None:
            return None
        try:
            return loads(data)
        except ValueError:
            raise SimpleConnectorError("JSON was not porperly recieved")

    def close(self):
        """Closes connection in both modes"""
        self.conn.close()
        self.connected = False

    def customize(self):
        """Function executed at the end of __init__ for custom stuff"""
        return


class CoordinateHandler:
    clients = {}
    players = {}
    log = logging.getLogger("CoordinateHandler")

    def __init__(self, loop, address=None, port=None):
        """
        Asnychronus game server with basic uuid idnetification
        """
        self.address = (address, port)
        self.loop = asyncio.get_event_loop()

    async def init(self):
        """Initilize the CoordinateHandler"""
        await self.load_config()
        await self.init_connection()
        return self

    async def load_config(self):
        """Loads config from config.json (CoordinateHandler)"""
        self.config = await aioload_config("CoordinateHandler")

    async def init_connection(self):
        """Startes asyncio network server"""
        self.factory = asyncio.start_server(self.accept_client, *self.address)

    def client_done(self, task):
        """Ends connection with the client and removes the task"""
        client_writer = self.clients[task][1]
        del self.clients[task]
        client_writer.close()
        self.log.info("End Connection")

    async def handle_client(self, reader, writer):
        """Handles communication with the client"""
        try:
            data = await asyncio.wait_for(parse_json(reader), timeout=5)
        except asyncio.TimeoutError:
            player = parse_json(reader)
        uuid = uuid4()
        dump_json(writer, {"uuid": new_player["uuid"]})
        self.players[uuid] = player
        """
        Idea:
        Scenario 1:
        Client -> UUID + Coords
        Client <- Coords
        Scenarion 2:
        Client <- UUID
        Client -> UUID + Coords
        Client <- Coords
        """


    async def handle_client_uuid(self, reader, writer):
        """Handles communication with the client"""
        # Needs to be implemented

    async def accept_client(self, client_reader, client_writer):
        """Handles client connection and task managing"""
        task = asyncio.Task(self.handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader, client_writer)
        self.log.info(f"New Connection {task}")
        task.add_done_callback(self.client_done)

    def run(self):
        """Runs server factory and loop.run_forever() until KeyboardInterrupt"""
        self.server = self.loop.run_until_complete(self.factory)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.close()

    async def close(self):
        [self.client_done(task) for task in self.tasks]
        return


class CoordinateHandlerClient:
    def __init__(self, host=None, port=None)
