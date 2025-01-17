"""
:class:`~ppb.systems.systemlib.System` is the core class for new subsystems. Systems add new features to 
the core ppb engine.
"""

import ppb.gomlib

class System(ppb.gomlib.GameObject):
    """ 
    Creates an object capable of modifying the engine itself. 

    All systems are context managers. For more see `Python context manager docs <https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`_
    Set-up and teardown with __enter__ and __exit__ methods.
    Subclass examples include :class:`~ppb.systems.renderer.Renderer` `~ppb.systems.clocks.Updater`
    """
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
