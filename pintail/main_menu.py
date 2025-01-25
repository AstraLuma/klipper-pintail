import ppb
from ppb import Vector as V

from . import ui, uibits, netinfo, netscene, prepare_menu, imdata


class IconButton(ui.Sprite):
    __dirty_fields__ = 'icon', 'text'
    icon: int
    text: str

    border_color = 0xFF_FF_FF
    bg_color = 0x00_00_00

    @property
    def width(self):
        return imdata.ICONS[self.icon].width + 4

    @property
    def height(self):
        return imdata.ICONS[self.icon].height + 4

    def _offset(self, font):
        text_width = len(self.text) * font.x
        return (self.width - text_width) / 2

    def redraw(self, screen):
        screen.draw_rect(
            screen.RectMode.OUTLINE, 
            screen.RGB(self.border_color if self.has_focus else self.bg_color), 
            self.top_left, self.bottom_right,
        )
        screen.draw_icon(self.top_left + V(2, -2), 9, self.icon + int(self.has_focus))
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
    focus_color: int = 0x0000FF
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

        bg = self.focus_color if self.has_focus else self.bg_color

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(bg), self.top_left, self.bottom_right)
        screen.draw_text(
            V(self.left+text_x, self.top), font, text, 
            fg_color=screen.RGB(self.fg_color),
            bg_color=None,
            monospace=True,
        )

    def on_knob_press(self, event, signal):
        if self.has_focus:
            signal(ppb.events.StartScene(netscene.NetScene))


class MainMenuScene(ui.Scene):
    def on_scene_started(self, event, signal):
        self.children.add(IconButton(
            position=V(65, 325), icon=1, text="Print", knobindex=0,
            activate=self.on_print_clicked,
        ))
        self.children.add(IconButton(            
            position=V(195, 325), icon=7, text="Prepare", knobindex=1,
            activate=self.on_prepare_clicked,
        ))
        self.children.add(IconButton(            
            position=V(65, 175), icon=3, text="Calibrate", knobindex=2,
            # activate=self.on_settings_clicked,
        ))
        self.children.add(IconButton(            
            position=V(195, 175), icon=5, text="Admin", knobindex=3,
            # activate=self.on_settings_clicked,
        ))

        self.children.add(NetworkBar(
            bg_color=imdata.BTN_NORMAL_BG, focus_color=imdata.BTN_FOCUS_BG,
            fg_color=0xFFFFFF, knobindex=4,
        ))


    def redraw(self, screen):
        screen.clear_screen(screen.RGB(0x000000))

    def on_print_clicked(self, event, signal):
        signal(ppb.events.StartScene(uibits.PopupMsg(text="Do a print")))

    def on_prepare_clicked(self, event, signal):
        signal(ppb.events.StartScene(prepare_menu.PrepareMenu()))
