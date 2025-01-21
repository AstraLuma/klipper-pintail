"""
This module performs time keeping of subsystems 
"""
import signal

import ppb
import ppb.events as events
from ppb.systemslib import System


class Updater(System):
    time_step = 0.016
    last_tick = None

    def __enter__(self):
        self.last_tick = ppb.get_time()
        signal.siginterrupt(signal.SIGALRM, False)
        signal.signal(signal.SIGALRM, self._on_sigalrm)
        signal.setitimer(signal.ITIMER_REAL, self.time_step, self.time_step)

    def __exit__(self, *exc):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    def _on_sigalrm(self, signum, frame):
        # Let's just assume that ITIMER is accurate
        if self.last_tick is None:
            self.last_tick = ppb.get_time()
        this_tick = ppb.get_time()
        self.engine.signal(events.Update(this_tick - self.last_tick))
        self.last_tick = this_tick
