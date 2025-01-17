import ppb
from ppb.utils import get_time

from .dwin_screen import T5UIC1_LCD


class PostRender: pass


class DwinRender(ppb.systemslib.System):
    redraw: bool = False

    def __init__(self, **kwargs):
        self.last_draw = get_time()

    def __enter__(self):
        self.screen = T5UIC1_LCD("/dev/ttyAMA1")
        self.screen.set_brightness(0xFF)
        self.screen.draw_jpeg(0)
        self.screen.commit()

    def __exit__(self, *exc):
        del self.screen

    def on_quit(self, event, signal):
        if hasattr(self, 'screen'):
            self.screen.clear_screen(0)
            self.screen.set_brightness(0)
            self.screen.commit()

    def on_ui_dirtied(self, event, signal):
        self.redraw = True

    def on_screne_started(self, event, signal):
        self.redraw = True

    def on_scene_continued(self, event, signal):
        self.redraw = True

    def on_idle(self, event, signal):
        t = get_time()
        if self.redraw:
            # Do a render
            signal(ppb.events.PreRender(t - self.last_draw))
            signal(ppb.events.Render())
            signal(PostRender())
            self.last_draw = t

    def on_render(self, event, signal):
        # We are assuming that any dirty events beyond this point need to start
        # the render process all over
        self.redraw = False

    def on_post_render(self, event, signal):
        self.screen.commit()
