import ppb
from ppb import Vector as V

from . import ui

class PopupMsg(ui.Scene):
    text: str
    font: tuple[int,int] = (12, 24)
    border: int = 1
    padding: int = 1
    border_color: int = 0xFFFFFF
    bg_color: int = 0x000000
    text_color: int = 0xFFFFFF

    def redraw(self, screen):
        font = screen.Font.s(*self.font)
        text_size = V(len(self.text) * font.x, font.y)
        text_ul = (V(screen.width, screen.height) - text_size) / 2
        if text_ul.x < (self.border + self.padding):
            text_ul = text_ul.update(x=self.border + self.padding)

        padding_ul = text_ul - V(self.padding, self.padding)
        padding_lr = text_ul + text_size + V(self.padding, self.padding)

        border_ul = padding_ul - V(self.border, self.border)
        border_lr = padding_lr + V(self.border, self.border)

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.border_color), border_ul, border_lr)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), padding_ul, padding_lr)
        screen.draw_text(
            text_ul, font, self.text, 
            fg_color=screen.RGB(self.text_color),
            bg_color=None,
            monospace=True,
        )

    def on_knob_press(self, event, signal):
        signal(ppb.events.StopScene())