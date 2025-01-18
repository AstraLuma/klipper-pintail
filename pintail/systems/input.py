"""
Accept input from the display knob
"""
import logging

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
    def __enter__(self):
        self.devices = [
            evdev.InputDevice(path)
            for path in self.input_devices
        ]

    def __exit__(self, *exc):
        for dev in self.devices:
            dev.close()

    def on_idle(self, event, signal):
        for dev in self.devices:
            for ev in iter(dev.read_one, None):
                print(ev)
                if ev.type == ecodes.EV_KEY and ev.code == ecodes.BTN_0:
                    if ev.value:
                        signal(events.KnobPress())
                    else:
                        signal(events.KnobRelease())
                elif ev.type == ecodes.EV_REL and ev.code == ecodes.REL_X:
                    if ev.value > 0:
                        signal(events.KnobCw())
                    elif ev.value < 0:
                        signal(events.KnobCcw())