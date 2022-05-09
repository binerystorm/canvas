import pygame as pg
from pygame.rect import Rect
from typing import NamedTuple, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum, auto

ID = int

class MsgType(Enum):
    REQ_VAL  = auto()
    SEND_VAL = auto()
    REQ_COLOR = auto()
    SEND_COLOR = auto()


class Message_c(NamedTuple):
    value: Optional[Any]
    msg_type: MsgType
    sender_id: ID
    recver_id: Optional[ID]


class Vec2_c(NamedTuple):
    x: int
    y: int
        

class Color_c(NamedTuple):
    r: int
    g: int
    b: int


@dataclass
class Pixel_c:
    color: Color_c
    pos: Vec2_c

class Dispatcher_c:
    def __init__(self) -> None:
        self.start: Optional['Static_Ac'] = None

    def set_start(self, start: 'Static_Ac') -> int:
        if not self.start:
            self.start = start
            return 0
        else:
            return -1
    

    def is_defined(self) -> bool:
        if self.start:
            return True
        else:
            return False

    def dispatch(self, msg: Message_c) -> int:
        if self.is_defined():
            assert isinstance(self.start, Static_Ac)
            self.start.resv_message(msg)
            return 0
        else:
            return -1


class Static_Ac(ABC):
    def __init__(self, pos: Vec2_c, size: Vec2_c):
        self.hit_box: Rect = Rect(pos, size)
        self.border_color: Color_c = Color(50,50,50)
        self.dispatcher: Optional[Dispatcher_c] = None 
        self.next_static: Optional['Static_Ac'] = None

    def send_message(self, msg: Message_c) -> None:
        assert not self.dispatcher is None
        assert isinstance(self.dispatcher, Dispatcher_c)
        self.dispatcher.dispatch(msg)

    def resv_message(self, msg: Message_c) -> None:
        if msg.sender_id != id(self):
            self.handle_message(msg)
        if self.is_next_static():
            assert isinstance(self.next_static, Static_Ac)
            self.next_static.resv_message(msg)

    def is_next_static(self) -> bool:
        if self.next_static:
            return True
        else:
            return False

    def set_next_static(self, element: 'Static_Ac') -> None:
        temp: Optional[Static_Ac]

        temp = self.next_static
        self.next_static = element
        self.next_static.next_static = temp

    def set_dispatcher(self, dispatcher: Dispatcher_c) -> int:
        if self.dispatcher:
            return -1
        else:
            self.dispatcher = dispatcher
            return 0

    @abstractmethod
    def handle_events(self, event_list: list[pg.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pg.surface.Surface) -> None:
        pass

    @abstractmethod
    def handle_message(self, msg: Message_c) -> None:
        pass

def normalize_pos(pos: Vec2_c, std: int) -> Vec2_c:
    x, y = pos
    x = x // std
    y = y // std
    return Vec2_c(x, y)
    
def vec2_to_idx(pos: Vec2_c, std: Vec2_c) -> int:
    if (pos.x >= std.x or pos.y >= std.y or
        pos.x <= 0     or pos.y <= 0):
        raise Exception("error: posistion out of bounds")

    return ((pos.x) * (std.y)) + (pos.y)

Vec2   = Vec2_c
Color  = Color_c
Static = Static_Ac
Pixel  = Pixel_c
Message = Message_c

