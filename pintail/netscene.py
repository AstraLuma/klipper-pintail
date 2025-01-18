import ppb
from ppb import Vector as V

from . import ui, uibits, netinfo


class NetScene(ui.Scene):
    __dirty_fields__ = 'ipaddr', 'hostname'
    ipaddr = None
    hostname = None

    def on_scene_started(self, event, signal):
        self.ipaddr = netinfo.get_default_address()
        self.hostname = netinfo.hostname()

    def on_update(self, event, signal):
        self.ipaddr = netinfo.get_default_address()
        self.hostname = netinfo.hostname()

    def redraw(self, screen):
        font = screen.Font.TWELVE_X_TWENTYFOUR
        ip_url = f"http://{self.ipaddr}/"
        name_url = f"http://{self.hostname}/"
        screen.clear_screen(screen.RGB(0x000000))

        qr_size = 4
        qr_pixels = qr_size * 46
        qr_left = (screen.width - qr_pixels) / 2
        qr_top = screen.height - qr_left

        ip_line_top = qr_top - qr_pixels
        name_line_top = ip_line_top - font.y

        screen.draw_qr(V(qr_left, qr_top), 4, ip_url.encode('utf-8'))

        text = str(ip_url)
        text_width = len(text) * font.x
        text_x = (screen.width - text_width) / 2
        screen.draw_text(
            V(text_x, ip_line_top), font, text, 
            fg_color=screen.RGB(0xFFFF),
            bg_color=None,
            monospace=True,
        )

        text = str(name_url)
        text_width = len(text) * font.x
        text_x = (screen.width - text_width) / 2
        screen.draw_text(
            V(text_x, name_line_top), font, text, 
            fg_color=screen.RGB(0xFFFF),
            bg_color=None,
            monospace=True,
        )

    def on_knob_press(self, event, signal):
        signal(ppb.events.StopScene)
