import dataclasses

import ppb
from ppb import Vector as V

from . import ui
from . import events


@dataclasses.dataclass
class BorderRect:
    """
    Utility to calculate the drawing elements of a box that has a sized border,
    a sized padding, and contents.
    """
    border_tl: ppb.Vector
    border_br: ppb.Vector

    padding_tl: ppb.Vector
    padding_br: ppb.Vector

    content_tl: ppb.Vector
    content_br: ppb.Vector

    def center_real_content(self, content_size: tuple[int, int]) -> tuple[ppb.Vector, ppb.Vector]:
        """
        In cases where the real content needs to be centered in a fixed rect,
        calculate the real top left and bottom right of that content
        """
        center = self.content_tl + (self.content_br - self.content_tl) / 2
        extent = V(content_size[0], -content_size[1])
        return (
            center - extent / 2,
            center + extent / 2,
        )

    @classmethod
    def from_content_tl(cls, top_left: ppb.Vector, content_size: tuple[int, int], border: int, padding: int):
        """
        Calculate, given the top left coordinate and size of the contents
        """
        border_tl = top_left
        padding_tl = border_tl + V(border, -border)
        content_tl = padding_tl + V(padding, -padding)

        content_br = content_tl + V(content_size[0], -content_size[1])
        padding_br = content_br + V(padding, -padding)
        border_br = padding_br + V(border, -border)

        # TODO: Limit to screen bounds
        return cls(
            border_tl=border_tl,
            border_br=border_br,
            padding_tl=padding_tl,
            padding_br=padding_br,
            content_tl=content_tl,
            content_br=content_br,
        )

    @classmethod
    def from_content_pos(cls, pos: ppb.Vector, content_size: tuple[int, int], border: int, padding: int):
        """
        Calculate, given the center coordinate and size of the contents
        """
        content_extent = V(content_size[0], -content_size[1])
        content_tl = pos - content_extent / 2
        content_br = pos + content_extent / 2

        padding_tl = content_tl + V(-padding, padding)
        padding_br = content_br + V(padding, -padding)

        border_tl = padding_tl + V(-border, border)
        border_br = padding_br + V(border, -border)

        # TODO: Limit to screen bounds
        return cls(
            border_tl=border_tl,
            border_br=border_br,
            padding_tl=padding_tl,
            padding_br=padding_br,
            content_tl=content_tl,
            content_br=content_br,
        )

    @classmethod
    def from_sprite(cls, sprite: ppb.Sprite, border: int, padding: int):
        """
        Calculate, given a sprite with position, width, and height describing
        the outer bounds
        """
        border_tl = sprite.top_left
        border_br = sprite.bottom_right

        padding_tl = border_tl + V(border, -border)
        padding_br = border_br + V(-border, border)

        content_tl = padding_tl + V(padding, -padding)
        content_br = padding_br + V(-padding, padding)

        # TODO: Limit to screen bounds
        return cls(
            border_tl=border_tl,
            border_br=border_br,
            padding_tl=padding_tl,
            padding_br=padding_br,
            content_tl=content_tl,
            content_br=content_br,
        )
    

class PopupMsg(ui.Scene):
    __dirty_fields__ = "text", "font", "border", "padding", "border_color", "bg_color", "text_color"

    text: str
    font: tuple[int,int] = (12, 24)
    border: int = 1
    padding: int = 1
    border_color: int = 0xFFFFFF
    bg_color: int = 0x000000
    text_color: int = 0xFFFFFF

    def redraw(self, screen):
        font = screen.Font.s(*self.font)
        rect = BorderRect.from_content_pos(
            pos=V(screen.width, screen.height)/2,
            content_size=(len(self.text) * font.x, font.y),
            border=self.border,
            padding=self.padding,
        )

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.border_color), rect.border_tl, rect.border_br)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), rect.padding_tl, rect.padding_br)
        screen.draw_text(
            rect.content_tl, font, self.text, 
            fg_color=screen.RGB(self.text_color),
            bg_color=screen.RGB(self.bg_color),
            monospace=True,
        )

    def on_knob_press(self, event, signal):
        signal(ppb.events.StopScene())


class IconedMenuItem(ui.Sprite):
    """
    An Icon, a label, a selection box, etc
    """

    __dirty_fields__ = "icon", "text", "font", "border", "padding", "border_color", "bg_color", "text_color"

    icon: int
    icon_padding: int = 1
    text: str
    font: tuple[int,int] = (10, 20)
    border: int = 1
    padding: int = 1
    border_color: int = 0xFFFFFF
    bg_color: int = 0x000000
    text_color: int = 0xFFFFFF

    selection_bar_width: int = 20

    @property
    def icon_size(self):
        return imdata.ICONS[self.icon].width

    @property
    def width(self):
        return 2 * self.border + 2 * self.padding + len(self.text) * self.font[0] + self.icon_size + self.icon_padding

    @property
    def height(self):
        return 2 * self.border + 2 * self.padding + self.font[1]

    def redraw(self, screen):
        font = screen.Font.s(*self.font)

        rect = BorderRect.from_sprite(self, border=self.border, padding=self.padding)

        icon_tl = rect.content_tl
        text_tl = icon_tl + V(self.icon_size + self.icon_padding, 0)

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.border_color), rect.border_tl, rect.border_br)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), rect.padding_tl, padding_br)
        screen.draw_icon(icon_tl, 9, self.icon)
        screen.draw_text(
            text_tl, font, self.text, 
            fg_color=screen.RGB(self.text_color),
            bg_color=screen.RGB(self.bg_color),
            monospace=True,
        )
