import logging

import ppb

from .systems.exiting import Signals
from .systems.moonraker import Moonraker
from .systems.render import DwinRender
from .wait_for_moonraker import DisconnectedScene
from .main_menu import MainMenuScene


def run():
    logging.basicConfig(level=logging.INFO)

    with ppb.GameEngine(DisconnectedScene(next=MainMenuScene), systems=[Signals, Moonraker, DwinRender], time_step=1.0) as eng:
        eng.run()