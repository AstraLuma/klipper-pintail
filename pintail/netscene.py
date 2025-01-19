import ppb
from ppb import Vector as V

from . import ui, uibits, netinfo


class NetScene(ui.Scene):
    __dirty_fields__ = 'mainaddr', 'hostname', 'alladdrs'
    mainaddr = None
    hostname = None
    alladdrs = None

    def on_scene_started(self, event, signal):
        self.mainaddr = netinfo.get_default_address()
        self.hostname = netinfo.hostname()
        self.alladdrs = frozenset(inter.ip for inter in netinfo.iter_all_interfaces() if inter.version == 4)

    def on_update(self, event, signal):
        self.mainaddr = netinfo.get_default_address()
        self.hostname = netinfo.hostname()
        self.alladdrs = frozenset(inter.ip for inter in netinfo.iter_all_interfaces() if inter.version == 4)

    def redraw(self, screen):
        additional_addrs = sorted(self.alladdrs - {self.mainaddr})
        all_urls = [
            f"http://{self.hostname}/",
            ip_url := f"http://{self.mainaddr}/",
            *(f"http://{ip!s}/" for ip in additional_addrs)
        ]

        font = screen.Font.TWELVE_X_TWENTYFOUR

        screen.clear_screen(screen.RGB(0x000000))

        qr_size = 4
        qr_pixels = qr_size * 46
        qr_left = (screen.width - qr_pixels) / 2
        qr_top = screen.height - qr_left

        ip_line_top = qr_top - qr_pixels
        name_line_top = ip_line_top - font.y

        screen.draw_qr(V(qr_left, qr_top), 4, ip_url.encode('utf-8'))

        text_y = qr_top - qr_pixels
        for text in all_urls:
            text_width = len(text) * font.x
            text_x = (screen.width - text_width) / 2
            screen.draw_text(
                V(text_x, text_y), font, text, 
                fg_color=screen.RGB(0xFFFF),
                bg_color=None,
                monospace=True,
            )
            text_y -= font.y
            if text_y <= 0:
                break


    def on_knob_press(self, event, signal):
        signal(ppb.events.StopScene())
