import socket
from pygame import image
from ujson import loads, dumps
from mission.config import load_config
from mission.errors import TransportError


def fire(x, y, surface):
    """Fires crystal at x and y by next render"""
    ammo = image.load("assets/crystal.png")
    surface.blit(ammo, x, y)


class AssetHelper:
    def __init__(self):
        self.config = load_config(instance="helper")

    def get_asset(self, asset):
        """Gets path for asset as str"""
        return f"{self.config['path']}/{asset}"


def get_local_ip():
    """
    Gets local ip based on socket
    """
    try:
        IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
         if not ip.startswith("127.")][:1], [[(s.connect(("8.8.8.8", 53)),
                                              s.getsockname()[0],
                                              s.close())
         for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    except OSError:
        IP = "127.0.0.1"
    return IP


async def parse_json(reader):
    """convenience bind to ujson.loads with a StreamReader"""
    data = await reader.readline()
    try:
        return loads(data)
    except ValueError as e:
        raise TransportError(f"JSON was not parsable {e}")


async def dump_json(writer, data: dict):
    """convenience bind to ujson.dumps with a StreamWriter"""
    await writer.write(dumps(data))
    await writer.drain()
