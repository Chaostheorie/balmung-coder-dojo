__all__ = ["game", "server", "errors"]
__doc__ = "Python Space Mission libary"


def main():
    import pygame
    import logging
    import sys
    from mission.config import load_config
    from mission.helpers import AssetHelper
    from mission.server import SimpleConnector

    # Load config
    config = load_config(instance="pygame")

    # Asks which mode should be used
    modes = {1: "server", 2: "client"}
    number = None
    while number not in modes.keys():
        print("".join([f"{modes[i+1]} [{i+1}] " for i in range(len(modes))]))
        number = int(input("Mode: "))

    mode = modes[number]

    # Initilize SimpleConnector
    if mode == "client":
        address = input("IP: ")
        conn = SimpleConnector(mode=mode, address=(address, config["port"]))
    else:
        conn = SimpleConnector(mode=mode)
        print(f"Waiting for connection ... (IP:{conn.host})")
        conn.accept()

    # Initilaze pygame and helper
    pygame.init()
    fpsClock = pygame.time.Clock()
    asset_helper = AssetHelper()
    _ = asset_helper.get_asset  # convenience bind as memory pointer
    surface = pygame.display.set_mode((config["display-width"],
                                       config["display-height"]))
    pygame.font.init()

    # Load background Music
    pygame.mixer.music.load(_("background.mp3"))
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play(-1)

    # server = CoordinateHandler((ip, port)) ip and port of target
    # Load graphics from /assets
    distance_wall = config["distance_wall"]
    distance_width = config["display-width"] - distance_wall
    distance_height = config["display-height"] - distance_wall
    image = pygame.image.load(_("canvas.png"))
    meeple1 = pygame.image.load(_("eyelander.png"))
    meeple2 = pygame.image.load(_("Snake.png"))
    player2_x = distance_width
    player2_y = distance_height
    background = pygame.Color(100, 149, 237)
    myfont = pygame.font.SysFont(config["font"], config["font-size"])

    steps_player1 = 0
    steps_player2 = 0
    player1_x = 100
    player1_y = 100

    while True:
        surface.fill(background)
        surface.blit(image, (0, 0))
        surface.blit(meeple1, (player1_x, player1_y))
        textsurface_1 = myfont.render(f"Highscore 1: {steps_player1}",
                                      False, (0, 0, 0))
        textsurface_2 = myfont.render(f"Highscore 2: {steps_player2}",
                                      False, (0, 0, 0))
        surface.blit(textsurface_1, (0, 0))
        surface.blit(textsurface_2, (0, 20))
        conn.send(player1_x, player1_y)
        data = conn.recv(parse=True)
        player2_x = data["x"]
        player2_y = data["y"]
        surface.blit(meeple2, (player2_x, player2_y))
        for event in pygame.event.get():
            logging.debug(player1_x, player1_y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1_x = 0
                    player1_y = 0
                elif event.key == pygame.K_RIGHT and player1_x < distance_width:
                    player1_x += 100
                    steps_player1 += 100
                elif event.key == pygame.K_LEFT and player1_x > distance_wall:
                    player1_x -= 100
                    steps_player1 += 100
                elif event.key == pygame.K_DOWN and player1_y < distance_height:
                    player1_y += 100
                    steps_player1 += 100
                elif event.key == pygame.K_UP and player1_y > distance_wall:
                    player1_y -= 100
                    steps_player1 += 100
                elif event.key == pygame.K_f:
                    # fire(player1_x, player1_y)
                    ammo = pygame.image.load(_("crystal_th.png"))
                    ammo_x = player1_x
                    ammo_y = player1_y
                    surface.blit(ammo, (ammo_x, ammo_y))
                    for y in range(ammo_y, 0, -10):
                        surface.blit(ammo, (ammo_x, ammo_y))
                        pygame.display.update()
                        pygame.time.delay(10)
                env_player1 = ((player1_x-100, player1_y-100), (player1_x, player1_y-100), (player1_x, player1_y+100), (player1_x-100, player1_y))
                env_player2 = ((player2_x-100, player2_y-100), (player2_x, player2_y-100), (player2_x, player2_y+100), (player2_x-100, player2_y))
                for touch in env_player1:
                    if touch in env_player2:
                        steps_player1 = 0
                        steps_player2 = 0

                logging.debug(f"Block Player 1: {env_player1}")
                logging.debug(f"Block Player 2: {env_player2}")
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(2)
                logging.info("Gracefull shutdown. Bye ;)")
                pygame.quit()
                sys.exit()
        pygame.display.update()
        fpsClock.tick(30)
