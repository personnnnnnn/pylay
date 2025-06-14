from pprint import pprint
from pylay import *
import pygame as pg
from functools import lru_cache

scale = 1
SCALE_AMT = 1.25
def px(n: float) -> float:
    return n * scale

def rem(n: float = 1) -> float:
    return px(n) * 40


def Grow() -> 'UI':
    return UI().sizing_grow()

def VSpacing(amt: float) -> 'UI':
    return UI().height_fixed(amt)

def render() -> UI:
    with UI().padding(px(20)).child_gap(3).sizing_fixed(pg.display.get_surface().get_width(), pg.display.get_surface().get_height()).background(Color(255, 255, 255)) as root_element:
        with UI().background(Color(255, 255, 0)).top_to_bottom().width_grow():
            with Text('Other people\'s code:').font_size(rem(1.5)).color(Color(0, 0, 0)): ...
            with Text('print("Hello, World!")').font_size(rem(1)).color(Color(0, 0, 0)): ...
            with VSpacing(px(20)): ...
            with Text('My code (constantly sleep deprived):').font_size(rem(1.5)).color(Color(0, 0, 0)): ...
            with Text('"Hello, World!".print()').font_size(rem(1)).color(Color(0, 0, 0)): ...
    return root_element

def pylay_color_to_pg(color: Color) -> pg.Color:
    return pg.Color(color.r, color.g, color.b)

def get_draw_commands() -> list[DrawCommand]:
    root_element = render()
    draw_commands = root_element.render()
    return draw_commands

def render_draw_commands(draw_commands: list[DrawCommand]) -> None:
    for command in draw_commands:
        render_draw_command(command)

def render_draw_command(command: DrawCommand) -> None:
    if command['type'] == 'rectangle':
        pg.draw.rect(
            pg.display.get_surface(),
            pylay_color_to_pg(command['color']),
            (
                command['x'], command['y'],
                command['width'], command['height']
            )
        )
    elif command['type'] == 'text':
        # pg.draw.rect(
        #     pg.display.get_surface(),
        #     (255, 0, 0),
        #     (
        #         command['x'], command['y'],
        #         command['width'], command['height']
        #     )
        # )
        for i, line in enumerate(command['text'].split('\n')):
            text = font(command['fontSize']).render(line, True, pylay_color_to_pg(command['color']))
            pg.display.get_surface().blit(text, (command['x'], command['y'] + font(command['fontSize']).get_height() * i))

@lru_cache()
def font(font_size: float) -> pg.font.Font:
    return pg.font.Font(None, int(font_size))

def create_text_measurer() -> None:
    @text_measure_text_width
    @lru_cache()
    def text_width_fn(text: str, font_size: float) -> float:
        return font(font_size).size(text)[0]

    @text_measure_line_height
    @lru_cache()
    def line_height_fn(font_size: float) -> float:
        return font(font_size).get_height()


pg.init()
pg.display.set_mode((400, 400), pg.RESIZABLE)
clock = pg.time.Clock()

create_text_measurer()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if pg.key.get_mods() & pg.KMOD_CTRL:
                if event.key in (pg.K_EQUALS, pg.K_PLUS):
                    scale *= SCALE_AMT
                if event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                    scale /= SCALE_AMT
                if event.key == pg.K_0:
                    scale = 1

    pg.display.get_surface().fill((255, 0, 255))

    draw_commands = get_draw_commands()
    render_draw_commands(draw_commands)

    pg.display.update()
    clock.tick()
