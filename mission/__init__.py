__all__ = ["game", "server", "errors"]
__doc__ = "Python Space Mission libary"


def main(run=False):
    """
    Main functions for game running
    Doesn't need to run main loop
    """
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
    _ = asset_helper.get_asset  # convenience bind
    surface = pygame.display.set_mode((config["display-width"],
                                       config["display-height"]))

    # Set start coords and calculate borders
    distance_wall = config["distance_wall"]
    distance_width = config["display-width"] - distance_wall
    distance_height = config["display-height"] - distance_wall
    steps_player1 = 0
    steps_player2 = 0
    player2 = [0, 0]
    player1 = [0, 0]  # [x, y]

    # Load assets
    image = pygame.image.load(_("canvas.png"))
    meeple1 = pygame.image.load(_("eyelander.png"))
    meeple2 = pygame.image.load(_("Snake.png"))
    background = pygame.Color(100, 149, 237)
    pygame.font.init()
    myfont = pygame.font.SysFont(config["font"], config["font-size"])

    # Load background Music
    pygame.mixer.music.load(_("background.mp3"))
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play(-1)
    if not run:
        return  # returns if run == False
    while True:
        # Initilize Background and player1
        surface.fill(background)
        surface.blit(image, (0, 0))
        surface.blit(meeple1, (*player1))
        textsurface_1 = myfont.render(f"Highscore 1: {steps_player1}",
                                      False, (0, 0, 0))
        textsurface_2 = myfont.render(f"Highscore 2: {steps_player2}",
                                      False, (0, 0, 0))
        surface.blit(textsurface_1, (0, 0))
        surface.blit(textsurface_2, (0, 20))

        # Sends player1 data
        conn.send(*player1)

        # Gets player 2 data
        data = conn.recv(parse=True)
        player2 = [data["x"], data["y"]]
        surface.blit(meeple2, (*player2))

        # Checks for key actions
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1[0] = 0
                    player1[1] = 0
                elif event.key == pygame.K_RIGHT and player1[0] < distance_width:
                    player1[0] += 100
                    steps_player1 += 100
                elif event.key == pygame.K_LEFT and player1[0] > distance_wall:
                    player1[0] -= 100
                    steps_player1 += 100
                elif event.key == pygame.K_DOWN and player1[1] < distance_height:
                    player1[1] += 100
                    steps_player1 += 100
                elif event.key == pygame.K_UP and player1[1] > distance_wall:
                    player1[1] -= 100
                    steps_player1 += 100
                elif event.key == pygame.K_f:
                    # fire(*player1)
                    ammo = pygame.image.load(_("crystal_th.png"))
                    surface.blit(ammo, (*player1))
                    for y in range(player1[1], 0, -10):
                        surface.blit(ammo, (*player1))
                        pygame.display.update()
                        pygame.time.delay(10)

                # env player represents the space taken up by the player images
                env_player1 = ((player1[0]-100, player1[1]-100),
                               (player1[0], player1[1]-100),
                               (player1[0], player1[1]+100),
                               (player1[0]-100, player1[1]))
                env_player2 = ((player2[0]-100, player2[1]-100),
                               (player2[0], player2[1]-100),
                               (player2[0], player2[1]+100),
                               (player2[0]-100, player2[1]))

                # Positions saved for point calculation
                player1_last = player1
                player2_last = player2

                # Checks if players are leaving the window
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
