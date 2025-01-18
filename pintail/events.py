from dataclasses import dataclass
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

@dataclass
class KnobCw:
    pass

@dataclass
class KnobCcw:
    pass