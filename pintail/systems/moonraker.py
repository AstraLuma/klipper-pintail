"""
PPB system for calling moonraker
"""
import logging
import queue

import ppb

from .moonraker_rpc import MoonrakerUDS
from ..events import MoonrakerNotification, DisplayOn, DisplayOff

LOG = logging.getLogger(__name__)


class Moonraker(ppb.systemslib.System):
    rpc: MoonrakerUDS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine.register(..., self._add_rpc)

    def _add_rpc(self, event):
        if hasattr(self, 'rpc'):
            event.moonraker = self.rpc

    def __enter__(self):
        self.rpc = MoonrakerUDS(
            "/home/astraluma/printer_data/comms/moonraker.sock",
            on_notification=self._moonraker_notification,
        )
        LOG.info("Connected to moonraker")
        self.rpc(
            "server.connection.identify",
            client_name="pintail",
            version="0",
            type="display",
            url="https://github.com/AstraLuma/klipper-pintail/",
        )

    def __exit__(self, *exc):
        self.rpc.close()

    def _moonraker_notification(self, msg):
        self.engine.signal(MoonrakerNotification(name=msg.name, params=msg.params))



# Power off sequence:
# MoonrakerNotification(name='notify_power_changed', params=[{'device': 'printer', 'status': 'off', 'locked_while_printing': True, 'type': 'gpio'}])
# MoonrakerNotification(name='notify_gcode_response', params=['// Klipper state: Shutdown'])
# MoonrakerNotification(name='notify_klippy_shutdown', params=[])

# Power on sequence:
# MoonrakerNotification(name='notify_power_changed', params=[{'device': 'printer', 'status': 'on', 'locked_while_printing': True, 'type': 'gpio'}])
# MoonrakerNotification(name='notify_gcode_response', params=['// Klipper state: Disconnect'])
# MoonrakerNotification(name='notify_klippy_disconnected', params=[])
# MoonrakerNotification(name='notify_klippy_ready', params=[])

class GlobalSceneChanges(ppb.systemslib.System):
    """
    Handles some global scenes:
    * Power off
    * [Printing]
    * [Calibrations]
    """
    has_done_init = False
    printer_device = "printer"
    off_scene: type[ppb.Scene]

    def on_scene_started(self, event, signal):
        if getattr(event, 'moonraker', None) and not self.has_done_init:
            status = event.moonraker("machine.device_power.get_device", device=self.printer_device)
            if status[self.printer_device] == "off":
                self._start_off_scene()
            self.has_done_init = True

    def on_moonraker_notification(self, event, signal):
        # if event.name != "notify_proc_stat_update": print(event)
        attr_name = f"_on_{event.name}"
        if handler := getattr(self, attr_name, None):
            handler(*event.params)

    def _on_notify_power_changed(self, what):
        if what['device'] == self.printer_device and what['status'] == "off":
            self._start_off_scene()

    def _start_off_scene(self):
        if not isinstance(self.engine.current_scene, self.off_scene):
            self.engine.signal(ppb.events.StartScene(self.off_scene(printer_device=self.printer_device)))
