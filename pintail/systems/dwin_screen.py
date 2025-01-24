"""
https://github.com/ihrapsa/T5UIC1-DWIN-toolset/
"""
import enum
import functools
import time
import logging
import math
import re
import serial
import struct
from typing import overload, Union

import ppb


LOG = logging.getLogger(__name__)


@overload
def RGB(hex: int) -> int: ...

@overload
def RGB(r: int, g: int, b: int) -> int: ...

@functools.cache
def RGB(*args):
    """
    Convert an RGB into the 16-bit format the screen likes.
    """
    if len(args) == 1:
        r, g, b = int(args[0]).to_bytes(length=3, byteorder='big', signed=False)
    else:
        r, g, b = args

    r = (r >> 3) & 0b11111
    g = (g >> 2) & 0b111111
    b = (b >> 3) & 0b11111
    return (r << 11) | (g << 5) | b


def _p(pos):
    if isinstance(pos, ppb.Vector):
        # Do axis conversion
        x, y = pos
        y = 480 - y
    else:
        x, y = pos
    return int(x), int(y)


class Commands(enum.IntEnum):
    #: ping/pong
    HANDSHAKE = 0x00
    BACKLIGHT_BRIGHTNESS_ADJUSTMENT = 0x30
    #: Added in 2.0
    WRITE_DATA_MEMORY = 0x31
    #: Added in 2.0
    READ_DATA_MEMORY = 0x32
    #: Added in 2.0
    WRITE_PICTURE_MEMORY = 0x33
    SET_ROTATION = 0x34

    EXPANSION_SERIAL_PORT_CONFIG = 0x38
    EXPANSION_SERIAL_PORT_SEND = 0x39
    EXPANSION_SERIAL_PORT_RECV= 0x3A

    CLEAR_SCREEN = 0x01
    DRAW_POINT = 0x02
    DRAW_LINE = 0x03
    DRAW_RECT = 0x05
    MOVE_REGION = 0x09
    DRAW_TEXT = 0x11
    DRAW_NUMBER = 0x14
    DRAW_QR_CODE = 0x21
    DRAW_JPEG = 0x22
    DRAW_ICON = 0x23
    DRAW_FROM_SRAM = 0x24
    DRAW_JPEG_BUFFER = 0x25
    DRAW_BUFFER = 0x26
    DRAW_BUFFER2 = 0x27
    DRAW_ICON_ANIM = 0x28
    SET_ANIM = 0x29



class RectMode(enum.IntEnum):
    OUTLINE = 0
    FILLED = 1
    XOR = 2

_font_dimensions = {
    0: (6,12),
    1: (8,16),
    2: (10,20),
    3: (12,24),
    4: (14,28),
    5: (16,32),
    6: (20,40),
    7: (24,48),
    8: (28,56),
    9: (32,64),
}

_font_lookup = {v:k for k,v in _font_dimensions.items()}

class Font(enum.IntEnum):
    # 6x12 doesn't seem to do anything
    SIX_X_TWELVE = 0
    EIGHT_X_SIXTEEN = 1
    TEN_X_TWENTY = 2
    TWELVE_X_TWENTYFOUR = 3
    FOURTEEN_X_TWENTYEIGHT = 4
    SIXTEEN_X_THIRTYTWO = 5
    # 20x40 and larger don't seem to do anything
    TWENTY_X_FOURTY = 6
    TWENTYFOUR_X_FOURTYEIGHT = 7
    TWENTYEIGHT_X_FIFTYSIX = 8
    THIRTYTWO_X_SIXTYFOUR = 9

    @property
    def x(self):
        x,y = _font_dimensions[int(self)]
        return x

    @property
    def y(self):
        x,y = _font_dimensions[int(self)]
        return y

    @classmethod
    def s(cls, x, y):
        """
        Get font by dimensions
        """
        if x is ...:
            raise NotImplementedError
        elif y is ...:
            raise NotImplementedError
        else:
            return cls(_font_lookup[x, y])

class T5UIC1_LCD:
    PACKET_HEAD = b"\xAA"
    PACKET_TAIL = b"\xCC\x33\xC3\x3C"

    width = 272
    height = 480

    RectMode = RectMode
    Font = Font
    RGB = staticmethod(RGB)

    def __init__(self, usart: str, exclusive=True):
        """
        Args:
            usart: serial port to connect to
        """
        self.port = serial.Serial(usart, 115200, timeout=1, exclusive=exclusive)
        LOG.debug("Port opened")
        while not self.handshake():
            pass
        LOG.info("Screen handshake completed")
        # self.JPG_ShowAndCache(0)
        self.set_direction(1)
        self.commit()

    def _send(self, cmd: int, fmt:str, *fields, flush: bool=True):
        """
        Send a command

        Args:
            cmd: the instruction byte
            fmt: the format for the rest of the data (in struct form)
            fields: arguments to pack into the data
        """
        buff = bytearray(self.PACKET_HEAD)
        try:
            buff += struct.pack('>B'+fmt, cmd, *fields)
        except struct.error as exc:
            print(f"{'>B'+fmt} {[cmd, *fields]!r}")
            raise
        # Optional CRC32 goes here, if firmware >=v2.3
        buff += self.PACKET_TAIL
        self.port.write(buff)
        if flush:
            self._flush()
        # This was in the original implementation; not sure why
        #time.sleep(0.001)

    def _flush(self):
        # Work around for https://github.com/pyserial/pyserial/issues/785
        import errno
        import termios
        while True:
            try:
                self.port.flush()
            except termios.error as exc:
                if exc.args[0] == errno.EINTR:
                    continue
                else:
                    raise
            else:
                return

    def _read_one(self) -> tuple[int, bytes]:
        """
        Read a single packet from the serial port
        """
        packet = self.port.read_until(self.PACKET_TAIL)
        assert packet.startswith(self.PACKET_HEAD)
        packet = packet.removeprefix(self.PACKET_HEAD).removesuffix(self.PACKET_TAIL)
        return packet[0], packet[1:]

    def handshake(self):
        """
        Send an noop and wait for an acknowledgement
        """
        self._send(Commands.HANDSHAKE, '')
        recv_cmd, recv_data = self._read_one()
        return recv_cmd == 0x00 and recv_data == b"OK"

    def set_brightness(self, value: int):
        """
        Set the brightness of the backlight

        Args:
            value: 0-0xFF, 0 is off, values <0x20 may cause flicker

        NOTE: No noticable difference in various brightnesses, but on/off works.
        """
        self._send(Commands.BACKLIGHT_BRIGHTNESS_ADJUSTMENT, "B", value)

    def set_direction(self, dir:int):
        """
        Set screen display direction

        Added in 2.0

        Args:
            dir: 0=0°, 1=90°, 2=180°, 3=270°
        """
        # TODO: What are these magic numbers?
        self._send(Commands.SET_ROTATION, 'BBBB', 0x34, 0x5A, 0xA5, dir)

    def commit(self):
        """
        Update display.

        Must be called after all draw operations and most config changes.
        """
        self._send(0x3D, '')

    def clear_screen(self, color: int):
        """
        Clear screen. Requires :meth:`commit`.

        Args:
            color: Use :func:`RGB`
        """
        self._send(Commands.CLEAR_SCREEN, 'H', color)

    def draw_points(self, color: int, *pos: tuple[int, int], size: tuple[int, int]=(0x01, 0x01)):
        """
        Draw points. Requires :meth:`commit`.

        FIXME: Not working.

        Args:
            color: Use :func:`RGB`
            pos: Position (x,y) of each point to draw
            size: width,height, each 0x01-0x0F
        """
        self._send(Commands.DRAW_POINT, 'H2B' + '2H'*len(pos), color, *size, *(c for p in pos for c in _p(p)))

    def draw_line(self, color: int, start: tuple[int, int], end: tuple[int, int]):
        """
        Draw a line. Requires :meth:`commit`.

        Args:
            color: Use :func:`RGB`
            start: x,y of starting point
            end: x,y of ending point
        """
        self._send(Commands.DRAW_LINE, 'H2H2H', color, *_p(start), *_p(end))

    def draw_rect(self, mode:RectMode, color: int, start: tuple[int, int], end: tuple[int, int]):
        """
        Draw a rectangle. Requires :meth:`commit`.
        
        FIXME: XOR mode doesn't work

        Args:
            mode: 0=outline, 1=filled, 2=XOR fill
            color: Use :func:`RGB`
            start: x,y of starting point
            end: x,y of ending point    
        """
        self._send(Commands.DRAW_RECT, 'BH2H2H', mode, color, *_p(start), *_p(end))        

    # Can't confirm
    def move_area(self, mode:int, dir:int, distance:int, color:int, start:tuple[int,int], end:tuple[int,int]):
        """
        Move a portion of the screen.

        FIXME: Not working.

        Args:
            mode: 0="cycle movement", 1=translate & fill
            dir: 0=left, 1=right, 2=up, 3=down
            distance: number of pixels to move in that direction
            color: filling color when mode=1
            start: x,y of one corner of rectangle
            end: x,y of the other corner
        """
        self._send(Commands.MOVE_REGION, 'BHH2H2H', (mode << 7) | dir, distance, color, *_p(start), *_p(end))

    def draw_text(self, pos:tuple[int,int], font:Font, text:str, *, fg_color:int, bg_color: Union[int,None], monospace:bool):
        """
        Draw text from a built-in font.

        Does not require :meth:`commit`.

        Args:
            pos: x,y of upper-left corner
            size: size, 0-9
            text: Text to render
            fg_color: Color of the text (see :func:`RGB`)
            bg_color: Color of the background, or None if transparent (see :func:`RGB`)
            monospace: True if monospace, False if proportional
        """
        btext = text.encode('utf-8')
        self._send(
            Commands.DRAW_TEXT, f'BHH2H{len(btext)}s', 
            (monospace << 7) | ((bg_color is not None) << 6) | (font & 0b1111),
            fg_color,
            bg_color or 0,
            *_p(pos),
            btext,
        )

    __number_format = re.compile(r"^(?P<prefix>[+])?(?P<fill>[ 0])?(?P<digits>\d+)(?:\.(?P<precision>\d+))?$")

    def draw_number(self, pos:tuple[int,int], font:Font, fmt:str, value:Union[int,float], *, fg_color:int, bg_color:Union[int,None]):
        """
        Draw a number.

        Does not require :meth:`commit`.

        Args:
            pos: x,y of upper-left
            font: size of text
            fmt: Format of number, in printf-ish ("+04.2", " 4.2", etc)
            value: Number to render
            fg_color: Color of the text (see :func:`RGB`)
            bg_color: Color of the background, or None if transparent (see :func:`RGB`)

        fmt is as follows:
        
        * ``+`` or omitted, to indicate if the sign should be included
        * `` `` or ``0`` or omitted, to indicate how to pad
        * a number, indicating the number of digits to the left of the decimal point to render
        * optionally, ``.`` and a number, indicating the number of fractional digits

        Note: ``+`` does not seem to do anything. `` `` seems to be treated as ``0``.
        """
        fmtmatch = self.__number_format.match(fmt)
        assert fmtmatch is not None
        fparams = fmtmatch.groupdict()

        if fparams['prefix'] == None:
            signed = False
        elif fparams['prefix'] == '+':
            signed = True
        else:
            raise ValueError

        if fparams['fill'] == None:
            dofill = False
            fillmode = 0
        elif fparams['fill'] == '0':
            dofill = True
            fillmode = 1
        elif fparams['fill'] == ' ':
            dofill = True
            fillmode = 0
        else:
            raise ValueError

        wholedigits, trailingdigits = int(fparams['digits'] or 1), int(fparams['precision'] or 0)

        inum = round(value * 10 ** trailingdigits)

        self._send(
            Commands.DRAW_NUMBER, "BHHBB2Hq",
            (bool(bg_color is not None) << 7) | (signed << 6) | (dofill << 5) | (fillmode << 4) | (int(font) & 0b1111),
            fg_color,
            bg_color or 0,
            wholedigits,
            trailingdigits,
            *_p(pos),
            inum
        )

    def draw_jpeg(self, id:int):
        """
        Display a fullscreen JPEG from "picture memory".
        
        IDs > 2 seem to start drawing icons.

        Requires :meth:`commit`.
        """
        self._send(Commands.DRAW_JPEG, 'BB', 0, id)

    def draw_icon(self, pos:tuple[int,int], lib_id:int, icon_id:int):
        """
        Draw an icon. Requires :meth:`commit`.
        
        Added in 2.0.

        Args: 
            lib_id: The libray to pull from
            icon_id: The icon from that library to draw
            pos: x,y

        TODO: Implement background modes

        NOTE: Only library 9 seems to be present 
        """
        self._send(Commands.DRAW_ICON, '2HBB', *_p(pos), 0x80 | lib_id, icon_id)

    def draw_qr(self, pos:tuple[int,int], size:int, data:bytes):
        """
        Draw a QR code. Requires :meth:`commit`.

        Args:
            pos: x,y of upper left
            size: pixels per cell, suggest no more than 6
            data: contents of QR code
        """
        assert 0x1 <= size <= 0xF
        assert len(data) <= 154
        self._send(Commands.DRAW_QR_CODE, f"2HB{len(data)}s", *_p(pos), size, data)


    # Astra: I don't feel like dealing with framebuffer stuff yet

    # # Unzip the JPG picture to a virtual display area
    # #  n: Cache index
    # #  id: Picture ID
    # def JPG_CacheToN(self, n, id):
    #     self.Byte(0x25)
    #     self.Byte(n)
    #     self.Byte(id)
    #     self.Send()

    # def JPG_CacheTo1(self, id):
    #     self.JPG_CacheToN(1, id)

    # #  Copy area from virtual display area to current screen
    # #   cacheID: virtual area number
    # #   xStart/yStart: Upper-left of virtual area
    # #   xEnd/yEnd: Lower-right of virtual area
    # #   x/y: Screen paste point
    # def Frame_AreaCopy(self, cacheID, xStart, yStart, xEnd, yEnd, x, y):
    #     self.Byte(0x27)
    #     self.Byte(0x80 | cacheID)
    #     self.Word(xStart)
    #     self.Word(yStart)
    #     self.Word(xEnd)
    #     self.Word(yEnd)
    #     self.Word(x)
    #     self.Word(y)
    #     self.Send()

    # def Frame_TitleCopy(self, id, x1, y1, x2, y2):
    #     self.Frame_AreaCopy(id, x1, y1, x2, y2, 14, 8)

    # #  Animate a series of icons
    # #   animID: Animation ID; 0x00-0x0F
    # #   animate: True on; False off;
    # #   libID: Icon library ID
    # #   picIDs: Icon starting ID
    # #   picIDe: Icon ending ID
    # #   x/y: Upper-left point
    # #   interval: Display time interval, unit 10mS
    # def ICON_Animation(self, animID, animate, libID, picIDs, picIDe, x, y, interval):
    #     if x > self.DWIN_WIDTH - 1:
    #         x = self.DWIN_WIDTH - 1
    #     if y > self.DWIN_HEIGHT - 1:
    #         y = self.DWIN_HEIGHT - 1
    #     self.Byte(0x28)
    #     self.Word(x)
    #     self.Word(y)
    #     # Bit 7: animation on or off
    #     # Bit 6: start from begin or end
    #     # Bit 5-4: unused (0)
    #     # Bit 3-0: animID
    #     self.Byte((animate * 0x80) | 0x40 | animID)
    #     self.Byte(libID)
    #     self.Byte(picIDs)
    #     self.Byte(picIDe)
    #     self.Byte(interval)
    #     self.Send()

    # #  Animation Control
    # #   state: 16 bits, each bit is the state of an animation id
    # def ICON_AnimationControl(self, state):
    #     self.Byte(0x28)
    #     self.Word(state)
    #     self.Send()

    # /*---------------------------------------- Memory functions ----------------------------------------*/
    #  The LCD has an additional 32KB SRAM and 16KB Flash

    #  Data can be written to the sram and save to one of the jpeg page files

    #  Write Data Memory
    #   command 0x31
    #   Type: Write memory selection; 0x5A=SRAM; 0xA5=Flash
    #   Address: Write data memory address; 0x000-0x7FFF for SRAM; 0x000-0x3FFF for Flash
    #   Data: data
    #
    #   Flash writing returns 0xA5 0x4F 0x4B

    #  Read Data Memory
    #   command 0x32
    #   Type: Read memory selection; 0x5A=SRAM; 0xA5=Flash
    #   Address: Read data memory address; 0x000-0x7FFF for SRAM; 0x000-0x3FFF for Flash
    #   Length: leangth of data to read; 0x01-0xF0
    #
    #   Response:
    #     Type, Address, Length, Data

    #  Write Picture Memory
    #   Write the contents of the 32KB SRAM data memory into the designated image memory space
    #   Issued: 0x5A, 0xA5, PIC_ID
    #   Response: 0xA5 0x4F 0x4B
    #
    #   command 0x33
    #   0x5A, 0xA5
    #   PicId: Picture Memory location, 0x00-0x0F
    #
    #   Flash writing returns 0xA5 0x4F 0x4B
    # def sendPicture(self, PicId, SRAM, Address, data):
    #   self.Byte(0x31)
    #   if SRAM:
    #       self.Byte(0x5A)
    #   else:
    #       self.Byte(0xA5)
    #   self.Word(Address)
    #   self.DWIN_SendBuf += data
    #   self.Send()
