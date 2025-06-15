from pprint import pprint
from pylay import *
import pygame as pg
from functools import lru_cache

scale = 1
SCALE_AMT = 1.25
def px(n: float) -> float:
    return n * scale

def rem(n: float = 1) -> float:
    return px(n) * 30


def Grow() -> UI:
    return UI().sizing_grow()

def VSpacing(amt: float) -> UI:
    return UI().height_fixed(amt)

def StyledText(text: str) -> Text:
    return Text(text).color(Color(100, 100, 100)).font_size(rem(1))

def Section() -> UI:
    return UI().background(Color(200, 200, 200)).spacing(px(10))

def render() -> UI:
    with UI().sizing_fixed(pg.display.get_surface().get_width(), pg.display.get_surface().get_height()) as root_element:
        with Grow().background(Color(255, 255, 255)).spacing(px(20)).top_to_bottom():
            with Section().width_grow():
                StyledText('Home').show()
                StyledText(f'Zoom: {int(scale * 100)}%').show()
                Grow().show()
                StyledText('File').show()
                StyledText('Exit').show()
            with Grow().child_gap(px(20)):
                with Section().height_grow().top_to_bottom():
                    StyledText('Document 1').show()
                    StyledText('Document 2').show()
                with Section().sizing_grow():
                    StyledText('Content').show()

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
