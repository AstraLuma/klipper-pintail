from ppb import Vector as V

from . import ui


class IconButton(ui.Sprite):
    icon: int
    text: str

    def _offset(self, font):
        return (110 - len(self.text) * font.x) / 2

    def redraw(self, screen):
        screen.draw_icon(self.top_left, 9, self.icon)
        if self.text:
            font = screen.Font.EIGHT_X_SIXTEEN
            screen.draw_text(
                (self.left+self._offset(font), self.top+55), font, self.text, 
                fg_color=screen.RGB(0xFFFFFF),
                bg_color=None,
                monospace=True,
            )

class MainMenuScene(ui.Scene):
    def on_scene_started(self, event, signal):
        self.children.add(IconButton(position=V(20, 100), icon=1, text="Print"))
        self.children.add(IconButton(position=V(150, 100), icon=5, text="Settings"))

    def redraw(self, screen):
        screen.clear_screen(screen.RGB(0x000000))