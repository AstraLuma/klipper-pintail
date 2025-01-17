from dataclasses import dataclass

@dataclass
class MoonrakerNotification:
	"""
	Moonraker sent us a notification
	"""
	name: str
	params: list

@dataclass
class UiDirtied:
	"""
	Something in the UI changed; rerender
	"""