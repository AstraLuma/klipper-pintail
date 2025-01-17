import logging

import ppb

from .systems.moonraker import Moonraker


class FillerScene(ppb.Scene):
	...


def run():
	logging.basicConfig(level=logging.INFO)

	with ppb.GameEngine(FillerScene, systems=[Moonraker], time_step=1.0) as eng:
		eng.run()