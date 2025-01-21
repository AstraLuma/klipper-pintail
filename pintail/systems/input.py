"""
Accept input from the display knob
"""
import logging
import selectors
import threading

import evdev
from evdev import ecodes
import ppb

from .. import events

LOG = logging.getLogger(__name__)

class Input(ppb.systemslib.System):
    input_devices = [
        "/dev/input/by-path/platform-button@c-event",
        "/dev/input/by-path/platform-rotary@13-event",
    ]

    _thread = None
    _selector = None

    def __enter__(self):
        self._thread = threading.Thread(None, self._read_thread, name=f"evdev-reader", daemon=True)
        self._thread.start()


    def __exit__(self, *exc):
        if self._selector is not None:
            self._selector.close()

    def _read_thread(self):
        self._selector = selectors.DefaultSelector()

        devices = [
            evdev.InputDevice(path)
            for path in self.input_devices
        ]

        for dev in devices:
            self._selector.register(dev, selectors.EVENT_READ)

        while True:
            for key, mask in self._selector.select():
                device = key.fileobj
                for event in device.read():
                    self._decode(event)


    def _decode(self, ev):
        if ev.type == ecodes.EV_KEY and ev.code == ecodes.BTN_0:
            if ev.value:
                self.engine.signal(events.KnobPress())
            else:
                self.engine.signal(events.KnobRelease())
        elif ev.type == ecodes.EV_REL and ev.code == ecodes.REL_X:
            self.engine.signal(events.KnobTurn(direction=events.Direction(ev.value)))
