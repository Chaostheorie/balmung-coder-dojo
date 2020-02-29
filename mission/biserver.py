import asyncio
import logging


class CoordinateHandler:
    clients = []
    players = []
    log = logging.getLogger("CoordinateHandler")

    def __init__(self, loop, address=None, port=None):
        self.address = (address, port)
        self.loop = asyncio.get_event_loop()

    async def init(self):
        # await self.load_config()
        await self.init_connection()
        return self

    async def init_connection(self):
        self.server_func = asyncio.start_server(self.accept_client, *self.address)

    async def accept_client(self, client_reader, client_writer):
        task = asyncio.Task(self.handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader, client_writer)

        def client_done(task):
            del self.clients[task]
            client_writer.close()
            self.log.info("End Connection")

        self.log.info(f"New Connection {task}")
        task.add_done_callback(client_done)

    async def run(self):
        self.server = self.loop.run_until_complete(self.server_func)
        try:
            pass
        except KeyboardInterrupt:
            self.server.close()
