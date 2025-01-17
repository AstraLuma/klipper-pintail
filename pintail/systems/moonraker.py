"""
PPB system for calling moonraker
"""
import ppb

from .moonraker_rpc import MoonrakerUDS

class Moonraker(ppb.systemslib.System):
	...