"""
Data about the baked assets
"""
from dataclasses import dataclass

@dataclass
class Icon:
    width: int
    height: int


#: The background of the little 24x24 icons
ICON_BG = 0x0B_0B_0B
#: Background of the ~100x100 buttons when in the default state
BTN_NORMAL_BG = 0x15_1F_21
#: Background of large buttons when focused
BTN_FOCUS_BG = 0x2D_35_37
#: Background of the status icons (78-81)
STATUS_BG = ...

ICONS = {
    0: Icon(width=130, height=17),
    1: Icon(width=110, height=100),
    2: Icon(width=110, height=100),
    3: Icon(width=110, height=100),
    4: Icon(width=110, height=100),
    5: Icon(width=110, height=100),
    6: Icon(width=110, height=100),
    7: Icon(width=110, height=100),
    8: Icon(width=110, height=100),
    9: Icon(width=18, height=18),
    10: Icon(width=18, height=18),
    11: Icon(width=18, height=18),
    12: Icon(width=18, height=18),
    13: Icon(width=20, height=20),
    14: Icon(width=20, height=20),
    15: Icon(width=24, height=24),
    16: Icon(width=24, height=24),
    17: Icon(width=80, height=100),
    18: Icon(width=80, height=100),
    19: Icon(width=80, height=100),
    20: Icon(width=80, height=100),
    21: Icon(width=80, height=100),
    22: Icon(width=80, height=100),
    23: Icon(width=80, height=100),
    24: Icon(width=80, height=100),
    25: Icon(width=242, height=20),
    26: Icon(width=20, height=20),
    27: Icon(width=20, height=20),
    28: Icon(width=20, height=20),
    29: Icon(width=20, height=20),
    30: Icon(width=20, height=20),
    31: Icon(width=20, height=20),
    32: Icon(width=20, height=20),
    33: Icon(width=20, height=20),
    34: Icon(width=20, height=20),
    35: Icon(width=20, height=20),
    36: Icon(width=20, height=20),
    37: Icon(width=20, height=20),
    38: Icon(width=20, height=20),
    40: Icon(width=20, height=20),
    41: Icon(width=20, height=20),
    42: Icon(width=20, height=20),
    43: Icon(width=20, height=20),
    44: Icon(width=20, height=20),
    45: Icon(width=20, height=20),
    46: Icon(width=20, height=20),
    47: Icon(width=20, height=20),
    48: Icon(width=20, height=20),
    49: Icon(width=20, height=20),
    50: Icon(width=20, height=20),
    51: Icon(width=20, height=20),
    52: Icon(width=20, height=20),
    53: Icon(width=20, height=20),
    54: Icon(width=20, height=20),
    55: Icon(width=20, height=20),
    56: Icon(width=20, height=20),
    57: Icon(width=20, height=20),
    58: Icon(width=20, height=20),
    59: Icon(width=20, height=20),
    60: Icon(width=20, height=20),
    61: Icon(width=20, height=20),
    62: Icon(width=20, height=20),
    63: Icon(width=20, height=20),
    64: Icon(width=20, height=20),
    65: Icon(width=20, height=20),
    66: Icon(width=20, height=20),
    67: Icon(width=20, height=20),
    68: Icon(width=20, height=20),
    69: Icon(width=20, height=20),
    70: Icon(width=20, height=20),
    71: Icon(width=20, height=20),
    72: Icon(width=20, height=20),
    73: Icon(width=20, height=20),
    74: Icon(width=20, height=20),
    75: Icon(width=20, height=20),
    76: Icon(width=20, height=20),
    77: Icon(width=14, height=52),
    78: Icon(width=73, height=66),
    79: Icon(width=73, height=66),
    80: Icon(width=73, height=66),
    81: Icon(width=73, height=66),
    82: Icon(width=100, height=38),
    83: Icon(width=100, height=38),
    84: Icon(width=100, height=38),
    85: Icon(width=100, height=38),
    86: Icon(width=100, height=38),
    87: Icon(width=100, height=38),
    88: Icon(width=100, height=38),
    89: Icon(width=100, height=38),
    90: Icon(width=110, height=100),
    91: Icon(width=110, height=100),
}
