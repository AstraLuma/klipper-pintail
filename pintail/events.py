from dataclasses import dataclass
import enum
import typing


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

@dataclass
class Render:
    screen: typing.Any

@dataclass
class KnobPress:
    pass

@dataclass
class KnobRelease:
    pass

class Direction(enum.IntEnum):
    CW = +1
    CCW = -1

@dataclass
class KnobTurn:
    direction: Direction

@dataclass
class Focus:
    pass

@dataclass
class Blur:
    pass


@dataclass
class DisplayOff:
    pass


@dataclass
class DisplayOn:
    pass