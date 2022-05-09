import pygame as pg
from utils import ID
from utils import Vec2, Color, Pixel, Message 
from utils import normalize_pos, vec2_to_idx
from utils import Static, Dispatcher_c
from utils import MsgType
from typing import Optional, Any, Final, Generator

SLIDER_GRIP_SIZE: Final[int] = 8
SLIDER_HEIGHT: Final[int] = 6

# TODO: organize and clean up code
# TODO: factor out or refactor brush class
class Brush_c:
    def __init__(self, color: Color) -> None:
        self.active_b: bool = False
        self.drawing_b: bool = False
        self.prev_pos: Vec2 = Vec2(0, 0)
        self.pos: Vec2 = Vec2(0, 0)
        self.color: Color = color

    def handle_events(self, event_list: list[Any]) -> None:
        mm_handled_b: bool

        mm_handled_b = False
        for event in event_list:
            if (event.type == pg.MOUSEBUTTONDOWN # TODO: make enum for mouse buttons
                and event.button == 1):
                self.drawing_b = True
                self.pos = event.pos
                self.prev_pos = event.pos
            elif (event.type == pg.MOUSEBUTTONUP
                and event.button == 1):
                self.drawing_b = False
                self.prev_pos = self.pos
                self.pos = event.pos
            elif event.type == pg.MOUSEMOTION:
                if mm_handled_b:
                    self.pos = event.pos
                else:
                    mm_handled_b = True
                    self.prev_pos = self.pos
                    self.pos = event.pos


class ColorBox_c(Static):

    def __init__(self, pos: Vec2, size: Vec2) -> None:
        super().__init__(pos, size)
        self.color: Color = Color(0,0,0)
        self.box: pg.rect.Rect = pg.Rect(pos, size)
    # 815
    #    # TODO: make better system for this V
    #    self.r: Optional[ID] = None
    #    self.g: Optional[ID] = None
    #    self.b: Optional[ID] = None

    #def set_id_slider(self, r: ID, g: ID, b: ID) -> None:
    #    self.r = r
    #    self.g = g
    #    self.b = b

    def update(self) -> None:
        pass

    def handle_events(self, events: list[pg.event.Event]) -> None:
        pass

    def draw(self, screen: pg.surface.Surface) -> None:
        HIT_BOX_BW: Final[int] = 5
        pg.draw.rect(screen, self.border_color, self.hit_box, HIT_BOX_BW)
        pg.draw.rect(screen, self.color, self.box)

    def handle_message(self, msg: Message) -> None:
        pass


class Slider_c(Static):
    global SLIDER_GRIP_SIZE, SLIDER_HEIGHT
    def __init__(self, pos: Vec2, size: Vec2,
                 val_min: int, val_max: int) -> None:
        super().__init__(pos, size)
        self.max_value: int = val_max
        self.min_value: int = val_min
        self.value: int = val_min
        self.slide_color: Color = Color(0,0,255)
        self.grip_color: Color = Color(255,0,0)
        self.dragging_b: bool = False
        self.slide: pg.rect.Rect = \
            pg.Rect(self.hit_box.x,
                    self.hit_box.y + self.hit_box.height // 2 - SLIDER_HEIGHT // 2,
                    self.hit_box.width,
                    SLIDER_HEIGHT)
        self.grip: pg.rect.Rect = \
            pg.Rect(
            # the posistion my be (0,0) because the grip will be clamped to the slider
            # in any case
                    0,
                    0,
                    SLIDER_GRIP_SIZE,
                    SLIDER_GRIP_SIZE) 
        self.grip.clamp_ip(self.slide)

    def draw(self, screen: pg.surface.Surface) -> None:
        HIT_BOX_BW: Final[int] = 5
        pg.draw.rect(screen, self.border_color, self.hit_box, HIT_BOX_BW)
        pg.draw.rect(screen, self.slide_color, self.slide)
        pg.draw.rect(screen, self.grip_color, self.grip)

    def handle_events(self, event_list: list[pg.event.Event]) -> None:
        for event in event_list:
            if (event.type == pg.MOUSEBUTTONDOWN
                and self.grip.collidepoint(event.pos)):

                self.dragging_b = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.dragging_b = False
            elif event.type == pg.MOUSEMOTION and self.dragging_b:
                x: int
                y: int
                x, y = event.pos
                self.grip.x = x
                self.grip.y = y
                self.grip.clamp_ip(self.slide)

    def update(self) -> None:
        min_grip_x: int
        max_grip_x: int
        min_grip_x = self.hit_box.x
        max_grip_x = self.hit_box.x + self.hit_box.width - SLIDER_GRIP_SIZE # TODO: fix grip size being magic const

        temp = self.value
        self.value = \
            round(
                    self.grip.x/((max_grip_x - min_grip_x)/(self.max_value - self.min_value))
                )

    def handle_message(self, msg: Message) -> None:
        pass
        

class ColorChanger_c(Static):
    SLIDE_H: Final[int] = 10
    SLIDE_W: Final[int] = 100

    def __init__(self, pos: Vec2, size: Vec2):
        super().__init__(pos, size)
        slider_builder: Generator = self.build_slider()
        self.slider_r: Slider_c = next(slider_builder)
        self.slider_g: Slider_c = next(slider_builder)
        self.slider_b: Slider_c = next(slider_builder)
        self.color_box: ColorBox_c = ColorBox_c(
                Vec2(
                    self.hit_box.x + self.SLIDE_W,
                    self.hit_box.y
                    ),
                Vec2(
                    self.SLIDE_H * 3,
                    self.SLIDE_H * 3
                    )
            )

    def build_slider(self) -> Generator:
        SLIDE_MAX: Final[int] = 255
        SLIDE_MIN: Final[int] = 0
        slider_count: int = 3
        for i in range(slider_count):
            yield Slider_c(
                Vec2(
                    self.hit_box.x,
                    self.hit_box.y + self.SLIDE_H * i
                ),
                Vec2(
                    self.SLIDE_W,
                    self.SLIDE_H
                ),
                SLIDE_MIN,
                SLIDE_MAX
            )
    
    def draw(self, screen: pg.surface.Surface) -> None:
        HIT_BOX_BW: Final[int] = 5
        pg.draw.rect(screen, self.border_color, self.hit_box, HIT_BOX_BW)

        self.slider_r.draw(screen)
        self.slider_g.draw(screen)
        self.slider_b.draw(screen)
        self.color_box.draw(screen)

    def handle_events(self, event_list: list[pg.event.Event]) -> None:
        self.slider_r.handle_events(event_list)
        self.slider_g.handle_events(event_list)
        self.slider_b.handle_events(event_list)
        self.color_box.handle_events(event_list)

    def handle_message(self, msg: Message) -> None:
        if msg.msg_type == MsgType.REQ_COLOR:
            new_msg: Message

            new_msg = Message(
                self.color_box.color,
                MsgType.SEND_COLOR,
                id(self),
                msg.sender_id
            )
            self.send_message(new_msg)

    def update(self) -> None:
        self.slider_r.update()
        self.slider_g.update()
        self.slider_b.update()
        self.color_box.update()

        self.color_box.color = \
                Color(
                        self.slider_r.value,
                        self.slider_g.value,
                        self.slider_b.value
                    )


class Canvas_c(Static):
    def __init__(self, pos: Vec2, res: Vec2,
                 px_size: int) -> None:
        super().__init__(pos, Vec2(res.x * px_size, res.y * px_size))
        self.pixel_size: int = px_size
        self.resolution: Vec2 = res
        self.pixel_array: list[Pixel] = []# TODO: make better pixel array
        self.active_brush: Brush_c = \
                Brush_c(
                        Color(255, 255, 255)
                    )
        self.bg_color: Color = Color(0,0,0)

        for row in range(self.resolution.x):
            for col in range(self.resolution.y):
                px_pos: Vec2
                px: Pixel

                px_pos = Vec2(row, col)
                # create Pixel
                px = Pixel(self.bg_color, px_pos)
                # append pixel
                self.pixel_array.append(px)


    def draw(self, screen: pg.surface.Surface) -> None:
        # TODO: change mothod of drawing canvas
        HIT_BOX_BW: Final[int] = 5
        pg.draw.rect(screen, self.border_color, self.hit_box, HIT_BOX_BW)
        for px in self.pixel_array:
            rect: pg.rect.Rect
            rect = pg.Rect(px.pos.x * self.pixel_size,
                           px.pos.y * self.pixel_size,
                           self.pixel_size,
                           self.pixel_size)
            pg.draw.rect(screen, px.color, rect)
            # px.draw(screen)

    def update(self) -> None:

        msg: Message
        msg = Message(None, MsgType.REQ_COLOR, id(self), None)
        self.send_message(msg)
        
        assert type(self.active_brush) == Brush_c
        if self.active_brush.drawing_b:
            vec_list: list[Vec2]
            vec_list = self.draw_line(
                self.active_brush.prev_pos,
                self.active_brush.pos
            )
            for vec in vec_list:
                idx: int
                idx = vec2_to_idx(vec, self.resolution)
                self.pixel_array[idx].color = self.active_brush.color



    def handle_message(self, msg: Message) -> None:
        if msg.recver_id == id(self):
            if msg.msg_type == MsgType.SEND_COLOR:
                assert type(msg.value) == Color
                assert self.active_brush
                self.active_brush.color = msg.value

    def draw_line(self, pnt1: Vec2, pnt2: Vec2) -> list[Vec2]:
        pos_x: int; pos_y: int; prev_pos_x: int; prev_pos_y: int
        delta_x: int; delta_y: int; rico: float
        range_x: range
        vec_list: list[Vec2] = []
        flipped: bool = False
        
        pos_x, pos_y = \
            normalize_pos(pnt2, self.pixel_size)
        prev_pos_x, prev_pos_y = \
            normalize_pos(pnt1, self.pixel_size)

        delta_x = pos_x - prev_pos_x
        delta_y = pos_y - prev_pos_y

        if delta_x == 0 and delta_y == 0: return [Vec2(prev_pos_x, prev_pos_y)]

        if abs(delta_x) < abs(delta_y):
            delta_x, delta_y = delta_y, delta_x
            prev_pos_x, prev_pos_y = prev_pos_y, prev_pos_x
            pos_x, pos_y = pos_y, pos_x
            flipped = True

        if delta_x > 0:
            range_x = range(delta_x)
        else:
            range_x  = range(0, delta_x, -1)
            

        rico = delta_y / delta_x

        for x in range_x:
            new_pos_x: int
            new_pos_y: int

            if flipped:
                new_pos_y = prev_pos_x + x
                new_pos_x = prev_pos_y + round(x*rico)
            else:
                new_pos_x = prev_pos_x + x
                new_pos_y = prev_pos_y + round(x*rico)

            vec_list.append(
                Vec2(new_pos_x, new_pos_y)
            )

        return vec_list

    # TODO: fix crash when mouse leaves canvas
    def handle_events(self, event_list: list[pg.event.Event]) -> None:
        mouse_pos: Vec2 = Vec2(*pg.mouse.get_pos())
        if not (mouse_pos.x >= self.hit_box.width or mouse_pos.y >= self.hit_box.height
                or mouse_pos.x <= 0 or  mouse_pos.y <= 0):
            self.active_brush.handle_events(event_list)
        else: #NOTEEEEE: not ideal solution to out of bounds issue
            assert type(self.active_brush) == Brush_c
            self.active_brush.drawing_b = False

class Core_c:
    def __init__(self, dimentions: Vec2) -> None:
        self.dispatcher = Dispatcher_c()
        self.screen = pg.display.set_mode(dimentions)
        self.static_elements: list[Static] = []
        self.clock = pg.time.Clock()
        self.running_b: bool = True

        self.construct()

    def construct(self) -> None:

        self.add_element(
            Canvas_c(
                Vec2(0, 0),
                Vec2(70, 70),
                5
            )
        )

        self.add_element(
            ColorChanger_c(
                Vec2(0, 350),
                Vec2(230, 30)
            )
        )
        

    def main_loop(self) -> None:

        while(self.running_b):
            self.clock.tick(60)

            self.screen.fill(Color(0,0,0))
            events = pg.event.get()
            for element in self.static_elements:
                element.draw(self.screen)
                element.handle_events(events)
                element.update() 
            pg.display.flip()
                
            for event in events:
                if event.type == pg.QUIT:
                    self.running_b = False

    def add_element(self, element: Static) -> None:
        element.set_dispatcher(self.dispatcher)

        assert issubclass(type(element), Static)
        if len(self.static_elements) > 0:
            self.static_elements[-1].set_next_static(element)
        else:
            self.dispatcher.set_start(element)
        self.static_elements.append(element)

def main() -> None:
    core = Core_c(Vec2(400, 400))
    core.main_loop()

if __name__ == "__main__":
    main()
