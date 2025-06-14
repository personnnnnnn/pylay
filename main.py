from pprint import pprint
from pylay import *
import pygame as pg

scale = 1
SCALE_AMT = 1.25
def px(n: float) -> float:
    return n * scale

def rem(n: float = 1) -> float:
    return px(n) * 20


def Grow() -> 'UI':
    return UI().sizing_grow()


def render() -> UI:
    with UI().spacing(px(30)).sizing_fixed(pg.display.get_surface().get_width(), pg.display.get_surface().get_height()).background(Color(255, 255, 255)) as root_element:
        ...
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

pg.init()
pg.display.set_mode((400, 400), pg.RESIZABLE)
clock = pg.time.Clock()

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

    pg.display.get_surface().fill((255, 0, 255))

    draw_commands = get_draw_commands()
    render_draw_commands(draw_commands)

    pg.display.update()
    clock.tick()
