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

Compile with gcc (may require python3-dev):
``
gcc main.c -O2 -Wall `pkg-config --cflags --libs python3` -o  space-mission
``

# Credits

All works of art belong to their respective creators.

Background Music: ["Space Ambience" by Alexander Nakarada](https://youtu.be/sB6jXSr7_wQ)
