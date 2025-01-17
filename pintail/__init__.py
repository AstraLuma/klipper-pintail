import logging

import ppb

from .systems.moonraker import Moonraker


class FillerScene(ppb.Scene):
	...


def run():
	logging.basicConfig(level=logging.INFO)

	with ppb.GameEngine(FillerScene, systems=[Moonraker]) as eng:
		eng.run()