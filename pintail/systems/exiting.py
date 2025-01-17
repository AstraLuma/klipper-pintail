"""
Handles signals, converting them into PPB events
"""
import signal

import ppb


class Signals(ppb.systemslib.System):
    def __enter__(self):
        signal.signal(signal.SIGINT, self._do_quit)
        signal.signal(signal.SIGHUP, self._do_quit)
        signal.signal(signal.SIGTERM, self._do_quit)
        # Skipping SIGABRT

    def __exit__(self, *exc):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

    def _do_quit(self, signum, frame):
        self.engine.signal(ppb.events.Quit())