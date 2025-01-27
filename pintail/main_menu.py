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


class PowerButton(ui.Sprite):
    padding_color: int = 0x00_00_00
    border_color: int = 0xFF_FF_FF

    bg_color: int = 0xFF_00_00
    text_color: int = 0x00_00_00

    focus_bg_color: int = 0xFF_7F_7F
    focus_text_color: int = 0x00_00_00

    border: int = 1
    padding: int = 0

    font = (10, 20)

    text: str = "Power Off"

    printer_device: str = "printer"  # FIXME: Get from engine kwargs

    def redraw(self, screen):
        font = screen.Font.s(*self.font)
        rect = uibits.BorderRect.from_sprite(self, border=self.border, padding=self.padding)
        text_tl, _ = rect.center_real_content((len(self.text) * font.x, font.y))

        border_color = self.border_color if self.has_focus else self.padding_color
        padding_color = self.padding_color
        content_color = self.focus_bg_color if self.has_focus else self.bg_color
        text_color = self.focus_text_color if self.has_focus else self.text_color

        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(border_color), rect.border_tl, rect.border_br)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(padding_color), rect.padding_tl, rect.padding_br)
        screen.draw_rect(screen.RectMode.FILLED, screen.RGB(content_color), rect.content_tl, rect.content_br)
        screen.draw_text(
            text_tl, font, self.text, 
            fg_color=screen.RGB(text_color),
            bg_color=None,
            monospace=True,
        )

    def on_knob_press(self, event, signal):
        if self.has_focus:
            resp = event.moonraker("machine.device_power.post_device", device=self.printer_device, action="off")
            assert resp[self.printer_device] == "off"


class MainMenuScene(ui.Scene):
    bg_color: int = 0x00_00_00
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

        self.children.add(PowerButton(
            position=V(136, 50), width=200, height=40,
            padding_color=self.bg_color, knobindex=4,
        ))

        self.children.add(NetworkBar(
            bg_color=imdata.BTN_NORMAL_BG, focus_color=imdata.BTN_FOCUS_BG,
            fg_color=0xFFFFFF, knobindex=5,
        ))

    def redraw(self, screen):
        screen.clear_screen(screen.RGB(self.bg_color))

    def on_print_clicked(self, event, signal):
        signal(ppb.events.StartScene(uibits.PopupMsg(text="Do a print")))

    def on_prepare_clicked(self, event, signal):
        signal(ppb.events.StartScene(prepare_menu.PrepareMenu()))
