# Installation Instructions

Debian/ Ubuntu:
`sudo apt install python3 python-pygame`

Windows:
Working Python3 (at least 3.6) and pygame.

MacOS:
Working Python3 (at least 3.6) and pygame.


You can modify the `config.json` as long as you follow the JSON syntax


# Server Instructions

Port: 65534  (Maybe you need to open this port in iptables/ ufw)
The address of the other player needs to be provided at startup
If this port is taken on your system you can change the port in `config.json`. This system is a development build and should under no circumstances be used in a live deploy/ server.


# Cython Instructions

This is completely cython3 compatible.

Compile with cython3:
`cython3 --embed --cleanup 1 main.py`

Compile with gcc (may require `python3-dev` and `gcc`):
``
gcc main.c -O2 -Wall `pkg-config --cflags --libs python3` -o  space-mission
``

# Asnycio Server

`mission.server.CoordinateHandler` is a network server capable of low level network communication for handling of the coordinations and their distributions for multiple players. A basic asyncio network server is used. The communication will be in JSON (encoded) and handled by `ujson`.
Scenario 1:

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG5DbGllbnQgLT4-IFNlcnZlcjogVVVJRCArIENvb3Jkc1xuU2VydmVyIC0-PiBDbGllbnQ6IENvb3Jkc1x0XHRcdFx0IiwibWVybWFpZCI6eyJ0aGVtZSI6ImZvcmVzdCJ9fQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG5DbGllbnQgLT4-IFNlcnZlcjogVVVJRCArIENvb3Jkc1xuU2VydmVyIC0-PiBDbGllbnQ6IENvb3Jkc1x0XHRcdFx0IiwibWVybWFpZCI6eyJ0aGVtZSI6ImZvcmVzdCJ9fQ)

Scenario 2:

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG5TZXJ2ZXIgLT4-IENsaWVudDogVVVJRFxuQ2xpZW50IC0-PiBTZXJ2ZXI6IFVVSUQgKyBDb29yZHNcblNlcnZlciAtPj4gQ2xpZW50OiBDb29yZHNcblx0XHRcdFx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZm9yZXN0In19)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG5TZXJ2ZXIgLT4-IENsaWVudDogVVVJRFxuQ2xpZW50IC0-PiBTZXJ2ZXI6IFVVSUQgKyBDb29yZHNcblNlcnZlciAtPj4gQ2xpZW50OiBDb29yZHNcblx0XHRcdFx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZm9yZXN0In19)


# Credits

All works of art belong to their respective creators.

Background Music: ["Space Ambience" by Alexander Nakarada](https://youtu.be/sB6jXSr7_wQ)
