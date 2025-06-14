import os
from typing import TypedDict, Literal, Any, Callable

from .lua_deps import load_deps, lua

load_deps()

class DrawRectangle(TypedDict):
    type: Literal["rectangle"]
    x: float
    y: float
    width: float
    height: float
    color: 'Color'

class DrawClipped(TypedDict):
    type: Literal["clip"]
    x: float
    y: float
    width: float
    height: float
    sub_commands: list['DrawCommand']

class DrawText(TypedDict):
    type: Literal["text"]
    x: float
    y: float
    text: str
    fontSize: float
    color: 'Color'

type DrawCommand = DrawRectangle | DrawClipped

def text_measure_line_height(f: Callable[[float], float]) -> Callable[[], float]:
    lua.globals().TextMeasurer.lineHeight = f
    return f

def text_measure_text_width(f: Callable[[str, float], float]) -> Callable[[str, float], float]:
    lua.globals().TextMeasurer.textWidth = f
    return f

class Color:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.lua_obj = lua.globals().color(r, g, b)

    def __repr__(self) -> str:
        return f'Color(r={self.r}, g={self.g}, b={self.b})'

    @property
    def r(self) -> int:
        return self.lua_obj.r

    @property
    def g(self) -> int:
        return self.lua_obj.g

    @property
    def b(self) -> int:
        return self.lua_obj.b

class UI:
    def __init__(self) -> None:
        self.lua_obj = lua.globals().Node.New()

    def __enter__(self) -> 'UI':
        self.lua_obj.enter(self.lua_obj)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.lua_obj.exit(self.lua_obj)

    def show(self) -> 'UI':
        with self: ...
        return self

    def background(self, color: Color | None) -> 'UI':
        if color is None:
            self.lua_obj.ui.color = None
        else:
            self.lua_obj.ui.color = color.lua_obj
        return self

    def no_background(self) -> 'UI':
        return self.background(None)

    def padding_left(self, padding: float) -> 'UI':
        self.lua_obj.ui.padding.left = padding
        return self

    def padding_right(self, padding: float) -> 'UI':
        self.lua_obj.ui.padding.right = padding
        return self

    def padding_top(self, padding: float) -> 'UI':
        self.lua_obj.ui.padding.top = padding
        return self

    def padding_bottom(self, padding: float) -> 'UI':
        self.lua_obj.ui.padding.bottom = padding
        return self

    def padding_hor(self, padding: float) -> 'UI':
        return self.padding_left(padding).padding_right(padding)

    def padding_ver(self, padding: float) -> 'UI':
        return self.padding_top(padding).padding_bottom(padding)

    def padding(self, padding: float) -> 'UI':
        return self.padding_hor(padding).padding_ver(padding)

    def child_gap(self, child_gap: float) -> 'UI':
        self.lua_obj.ui.childGap = child_gap
        return self

    def spacing(self, spacing: float) -> 'UI':
        return self.padding(spacing).child_gap(spacing)

    def width_fixed(self, width: float) -> 'UI':
        self.lua_obj.ui.sizing.width = 'fixed'
        self.lua_obj.ui.fixedSizing.width = width
        return self

    def height_fixed(self, height: float) -> 'UI':
        self.lua_obj.ui.sizing.height = 'fixed'
        self.lua_obj.ui.fixedSizing.height = height
        return self

    def sizing_fixed(self, width: float, height: float) -> 'UI':
        return self.width_fixed(width).height_fixed(height)

    def render(self, x: float = 0, y: float = 0) -> list[DrawCommand]:
        draw_commands = dict(self.lua_obj.calculateUI(self.lua_obj, x, y)).values()
        return list(map(transform_command, list(draw_commands)))

    def top_to_bottom(self) -> 'UI':
        self.lua_obj.ui.layoutDirection = 'ttb'
        return self

    def left_to_right(self) -> 'UI':
        self.lua_obj.ui.layoutDirection = 'ltr'
        return self

    def width_fit(self) -> 'UI':
        self.lua_obj.ui.sizing.width = 'fit'
        return self

    def height_fit(self) -> 'UI':
        self.lua_obj.ui.sizing.height = 'fit'
        return self

    def sizing_fit(self) -> 'UI':
        return self.width_fit().height_fit()

    def width_grow(self) -> 'UI':
        self.lua_obj.ui.sizing.width = 'grow'
        return self

    def height_grow(self) -> 'UI':
        self.lua_obj.ui.sizing.height = 'grow'
        return self

    def sizing_grow(self) -> 'UI':
        return self.width_grow().height_grow()



def transform_command(x: dict[str, Any]) -> DrawCommand:
    x = dict(x)
    if 'color' in x.keys():
        x['color'] = Color(x['color']['r'], x['color']['g'], x['color']['b'])
    if 'subCommands' in x.keys():
        x['sub_commands'] = map(transform_command, list(x['subCommands']))
        del x['subCommands']
    return x

class Text:
    def __init__(self, text: str):
        self.lua_obj = lua.globals().Text.New(text)

    def font_size(self, size: float) -> 'Text':
        self.lua_obj.ui.fontSize = size
        return self

    def color(self, color: Color) -> 'Text':
        self.lua_obj.ui.color = color.lua_obj
        return self

    def show(self) -> 'Text':
        with self: ...
        return self

    def __enter__(self) -> 'Text':
        self.lua_obj.enter(self.lua_obj)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lua_obj.exit(self.lua_obj)
