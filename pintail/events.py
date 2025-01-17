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
    """
    The :class:`~ppb.systems.Renderer` is rendering.

    .. warning::
       In general, responses to :class:`Render` will not be reflected until the next
       render pass. If you want changes to effect this frame, see
       :class:`PreRender`
    """
    screen: typing.Any
