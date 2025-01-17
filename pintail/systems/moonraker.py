"""
PPB system for calling moonraker
"""
import logging
import queue

import ppb

from .moonraker_rpc import MoonrakerUDS
from ..events import MoonrakerNotification

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
        self.rpc = MoonrakerUDS("/home/astraluma/printer_data/comms/moonraker.sock")
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

    def on_idle(self, event, signal):
        # Pump notifications
        while True:
            try:
                msg = self.rpc.events.get_nowait()
            except queue.Empty:
                break
            else:
                signal(MoonrakerNotification(name=msg.name, params=msg.params))