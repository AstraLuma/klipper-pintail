import ppb
from ppb import Vector as V

from . import ui, uibits, imdata


class PrepareMenu(ui.Scene):
    def on_scene_started(self, event, signal):
        self.children.add(uibits.IconedText(text="Prepare", icon=9, icon_size=18, position=V(136, 240), bg_color=imdata.ICON_BG))

    def on_knob_press(self, event, signal):
        signal(ppb.events.StopScene())

    def redraw(self, screen):
        screen.clear_screen(screen.RGB(0x000000))
