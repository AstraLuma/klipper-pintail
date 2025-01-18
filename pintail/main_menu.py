import ppb
from ppb import Vector as V

from . import ui, uibits, netinfo


class IconButton(ui.Sprite):
    __dirty_fields__ = 'icon', 'text'
    icon: int
    text: str

    def __init__(self, **props):
        super().__init__(width=110, height=100, **props)

    def _offset(self, font):
        text_width = len(self.text) * font.x
        return (self.width - text_width) / 2

    def redraw(self, screen):
        screen.draw_icon(self.top_left, 9, self.icon + int(self.has_focus))
        if self.text:
            font = screen.Font.EIGHT_X_SIXTEEN
            screen.draw_text(
                V(self.left+self._offset(font), self.top-55), font, self.text, 
                fg_color=screen.RGB(0xFFFFFF),
                bg_color=None,
                monospace=True,
            )

    def on_knob_press(self, event, signal):
        if self.has_focus:
            self.activate(event, signal)

    def activate(self, event, signal):
        pass


class NetworkBar(ui.Sprite):
    __dirty_fields__ = 'fg_color', 'bg_color', 'font', 'ipaddr'

    bg_color: int = 0x000000
    fg_color: int = 0xFFFFFF
    font = (10, 20)

    def __init__(self, **props):
        super().__init__(**props)
        self.ipaddr = netinfo.get_default_address()

    def on_update(self, event, signal):
        self.ipaddr = netinfo.get_default_address()

    def redraw(self, screen):
        font = screen.Font.s(*self.font)
        self.width = screen.width
        self.height = font.y
        self.top = self.height
        self.left = 0

        text = str(self.ipaddr)
        text_width = len(text) * font.x
        text_x = (self.width - text_width) / 2

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(self.bg_color), self.top_left, self.bottom_right)
        screen.draw_text(
            V(self.left+text_x, self.top), font, text, 
            fg_color=screen.RGB(self.fg_color),
            bg_color=None,
            monospace=True,
        )


class MainMenuScene(ui.Scene):
    def on_scene_started(self, event, signal):
        self.children.add(IconButton(
            position=V(65, 250), icon=1, text="Print", knobindex=0,
            activate=self.on_print_clicked,
        ))
        self.children.add(IconButton(            
            position=V(195, 250), icon=5, text="Settings", knobindex=1,
            activate=self.on_settings_clicked,
        ))

        self.children.add(NetworkBar(bg_color=0x6666FF, fg_color=0x000000))


    def redraw(self, screen):
        screen.clear_screen(screen.RGB(0x000000))

    def on_print_clicked(self, event, signal):
        signal(ppb.events.StartScene(uibits.PopupMsg(text="Do a print")))

    def on_settings_clicked(self, event, signal):
        signal(ppb.events.StartScene(uibits.PopupMsg(text="Change settings")))
