"""
A python game framework.

PursuedPyBear is object oriented and event driven. Practically, this means that
most of your code will be organized into classes. Game objects in
:mod:`ppb` are :class:`Sprite` instances, which get contained in
:class:`Scenes <Scene>`. In turn, the :class:`GameEngine`
contains the scenes and :class:`Systems <System>`.
:mod:`Events <events>` are defined as simple classes and event handlers
are based on their names.

The classes, modules, and methods exported directly are the most used parts of
the library and intended to be used by users at all levels (barring
make_engine). Advanced features tend to be in their own modules and subpackages.

Exports:

* :class:`Scene`
* :class:`Sprite`
* :class:`RectangleSprite`
* :class:`~ppb_vector.Vector`
* :mod:`events`
* :mod:`buttons`
* :mod:`keycodes`
* :mod:`flags`
* :mod:`directions`
* :class:`Signal`
"""

from ppb_vector import Vector
from ppb.engine import GameEngine
from ppb.engine import Signal
from ppb.scenes import Scene
from ppb.sprites import RectangleSprite
from ppb.sprites import Sprite
from ppb.utils import get_time

__all__ = (
    # Shortcuts
    'Scene', 'Sprite', 'RectangleSprite', 'Vector',
    'events', 'buttons', 'keycodes', 'flags', 'directions', 'Signal'
)
