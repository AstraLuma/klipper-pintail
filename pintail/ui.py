"""
A basic UI framework.

Handles focus, dirty-prop rendering, and other stuff.
"""
import ppb

from . import events


class Drawable:
    is_dirty: bool = True

    def on_render(self, event, signal):
        if self.is_dirty:
            self.redraw(event.screen)
            self.is_dirty = False

    def redraw(self, screen):
        pass

    def set_dirty(self, signal):
        """
        Request a redraw
        """
        self.is_dirty = True
        signal(events.UiDirtied())


class UIScene(Drawable, ppb.Scene):
    def on_scene_continued(self, event, signal):
        self.set_dirty(signal)

    def set_dirty(self, signal):
        super().set_dirty(signal)
        for c in self.children:
            if hasattr(c, "set_dirty"):
                c.set_dirty(signal)
                # FIXME: We probably don't need a UIDirtied event for every element


class UISprite(Drawable, ppb.Sprite):
    pass