import ppb

from . import ui


class DisconnectedScene(ui.Scene):
    next: type[ppb.Scene]

    def redraw(self, screen):
        screen.draw_jpeg(0)
        screen.draw_text(
            (65, 220), screen.Font.TEN_X_TWENTY, "Connecting...",
            monospace=False,
            fg_color=screen.RGB(0xFFFFFF),
            bg_color=None,
        )

    # FIXME: Implement proper connection status handling.
    def on_idle(self, event, signal):
        if hasattr(event, "moonraker"):
            signal(ppb.events.ReplaceScene(self.next))