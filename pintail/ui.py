"""
A basic UI framework.

Handles focus, dirty-prop rendering, and other stuff.
"""
import ppb

from . import events


class Drawable:
    is_dirty: bool = True
    __dirty_fields__ = None

    __dirty_hash = None

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

    def on_idle(self, event, signal):
        if self.__dirty_fields__ is None:
            return
        dirties = tuple(getattr(self, fname, None) for fname in self.__dirty_fields__)
        dhash = hash(dirties)
        if dhash != self.__dirty_hash:
            self.set_dirty(signal)
            self.__dirty_hash = dhash


class Scene(Drawable, ppb.Scene):
    current_focus = None
    def on_scene_continued(self, event, signal):
        self.set_dirty(signal)

    def set_dirty(self, signal):
        super().set_dirty(signal)
        for c in self.children:
            if hasattr(c, "set_dirty"):
                c.set_dirty(signal)
                # FIXME: We probably don't need a UIDirtied event for every element

    def on_knob_turn(self, event, signal):
        controls = sorted(
            (c for c in self.children.get(kind=Sprite) if hasattr(c, 'knobindex')),
            key=lambda o: o.knobindex,
        )
        old = self.current_focus
        if old is None:
            if controls:
                new = controls[0]
            else:
                new = None
        else:
            try:
                idx = controls.index(old)
            except ValueError:
                # Terrible, but better than nothing
                # FIXME: do better
                if controls:
                    new = controls[0]
                else:
                    new = None
            else:
                new = controls[(idx + int(event.direction)) % len(controls)]

        if old is not None:
            signal(events.Blur(), targets=[old])
        if new is not None:
            signal(events.Focus(), targets=[new])
        self.current_focus = new


class Sprite(Drawable, ppb.RectangleSprite):
    knobindex: int
    has_focus: bool = False

    def on_focus(self, event, signal):
        self.has_focus = True
        self.set_dirty(signal)

    def on_blur(self, event, signal):
        self.has_focus = False
        self.set_dirty(signal)