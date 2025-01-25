import ppb
from ppb import Vector as V

from . import ui
from . import events


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
        text_extent = V(len(self.text) * font.x, -font.y)
        text_ul = (V(screen.width, screen.height) - text_extent) / 2
        if text_ul.x < (self.border + self.padding):
            text_ul = text_ul.update(x=self.border + self.padding)

        padding_ul = text_ul + V(-self.padding, self.padding)
        padding_lr = text_ul + text_extent + V(self.padding, -self.padding)

        border_ul = padding_ul + V(-self.border, self.border)
        border_lr = padding_lr + V(self.border, -self.border)

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.border_color), border_ul, border_lr)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), padding_ul, padding_lr)
        screen.draw_text(
            text_ul, font, self.text, 
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

        border_ul = self.top_left
        border_lr = self.bottom_right

        padding_ul = border_ul + V(self.border, -self.border)
        padding_lr = border_lr + V(-self.border, self.border)

        icon_ul = padding_ul + V(self.padding, -self.padding)
        text_ul = icon_ul + V(self.icon_size + self.icon_padding, 0)

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.border_color), border_ul, border_lr)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), padding_ul, padding_lr)
        screen.draw_icon(icon_ul, 9, self.icon)
        screen.draw_text(
            text_ul, font, self.text, 
            fg_color=screen.RGB(self.text_color),
            bg_color=screen.RGB(self.bg_color),
            monospace=True,
        )


