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


class OffScene(PopupMsg):
    printer_device = None

    text = "Powering off..."
    padding = 20

    # Off: -> Printer off -> Klipper shutdown ->
    #     A               B                     C
    # On: -> Printer on -> klipper disconnected -> klipper ready ->
    #    D              E                       F                  G

    def on_scene_started(self, event, signal):
        # Recreate where we are in the above state machine
        status = event.moonraker("machine.device_power.get_device", device=self.printer_device)
        power = status[self.printer_device]
        klippy = event.moonraker("printer.info")
        self._on_notify_power_changed({"device": self.printer_device, "status": power}, signal=signal)

        if klippy["state"] == "shutdown":
            if power == "off":
                # Position C
                self._on_notify_klippy_shutdown(signal=signal)
            else:
                # Position E
                # Still powering on, ready is coming
                pass
        elif klippy["state"] == "disconnected":
            if power == "on":
                # Position F
                # powering on, ready is coming
                pass
            else:
                # This isn't on our chart, just get out of here
                raise RuntimeError(f"No idea how to handle power={power!r} klippy={klippy['state']!r}")
        elif klippy["state"]  == "ready":
            if power == "on":
                # Position G
                # fully powered on
                self._on_notify_klippy_ready(signal=signal)
            else:
                # Position B
                # Powered off, shutdown is coming
                pass

    def on_moonraker_notification(self, event, signal):
        attr_name = f"_on_{event.name}"
        if handler := getattr(self, attr_name, None):
            handler(*event.params, signal=signal)

    def _on_notify_klippy_shutdown(self, signal):
        signal(events.DisplayOff())
        self.text = "Klipper off"

    def _on_notify_klippy_ready(self, signal):
        signal(ppb.events.StopScene())

    def _on_notify_power_changed(self, what, signal):
        if what['device'] == self.printer_device:
            if what['status'] == "on":
                self.text = "Powering on..."
                signal(events.DisplayOn())
            elif what['status'] == "off":
                self.text = "Powering off..."
                signal(events.DisplayOff())

    def on_knob_press(self, event, signal):
        resp = event.moonraker("machine.device_power.post_device", device=self.printer_device, action="on")
        assert resp[self.printer_device] == "on"

    def on_scene_stopped(self, event, signal):
        signal(events.DisplayOn())
