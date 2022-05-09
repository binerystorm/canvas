# programming challenge to emulate a drawing canvis or white board
import pygame as pg
import math
import sys
from typing import NamedTuple, Literal
from enum import Enum, auto
from abc import ABC, abstractmethod

class Color_c(NamedTuple):
    r: int
    g: int
    b: int


class Vec2_c(NamedTuple):
    x: int
    y: int

class Canvas_c:
    def __init__(self, size: Vec2_c, px_size: Vec2_c):
        self.size: Vec2_c = size
        self.px_size: Vec2_c = px_size
        self.fps = 60
        self.clock: pg.time.Clock = pg.time.Clock()
        self.brush_list: list[Brush_c] = [
            Brush_c(
                10,
                Color_c(0,0,255)
            )
        ]
        self.active_brush: Brush_c = self.brush_list[0]
        self.running: bool = True
        self.screen = pg.display.set_mode(tuple(self.size))

        self.clock.tick(self.fps)
        self.main_loop()

    def main_loop(self):
        while(self.running):
            events = pg.event.get()
            self.tick(events)

    def tick(self, event_list: list):
        self.active_brush.handle_events(event_list)
        if self.active_brush.drawing_b:
            pg.draw.line(
                self.screen,
                self.active_brush.color,
                self.active_brush.pos,
                self.active_brush.prev_pos,
                self.active_brush.width_n
            )
            # pg.draw.rect(
            #     self.screen,
            #     self.active_brush.color,
            #     pg.Rect(
            #         self.active_brush.pos,
            #         self.px_size
            #     )
            # )

        for event in event_list:
            if event.type == pg.QUIT:
                self.running = False

        pg.display.update()


class Dynamic_c(ABC):
    @abstractmethod
    def handle_events(self, event_list: list):
        pass

class Brush_c(Dynamic_c):
    def __init__(self, width_n: int, color: Color_c):
        self.width_n: int = width_n
        self.pos: Vec2_c = Vec2_c(0, 0)
        self.prev_pos: Vec2_c = Vec2_c(0, 0)
        self.color: Color_c = color
        self.drawing_b = False

    def handle_events(self, event_list: list):
        self.prev_pos = self.pos
        self.pos = pg.mouse.get_pos()

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.drawing_b = True
                self.prev_pos = pg.mouse.get_pos()
                self.pos = pg.mouse.get_pos()
                print(event.type)
            elif event.type == pg.MOUSEBUTTONUP:
                self.drawing_b = False
                self.pos = pg.mouse.get_pos()
                print(event.type)

def main():
    c = Canvas_c(Vec2_c(400, 400), Vec2_c(10,10))

def resolve_mouse(pixel_size, pix):
    mouse_x, mouse_y = pg.mouse.get_pos()
    pix_x, pix_y = pix
    return (math.floor(mouse_x/pixel_size) * pixel_size, math.floor(mouse_y/pixel_size) * pixel_size, pixel_size, pixel_size)


if __name__ == "__main__":
    main()
