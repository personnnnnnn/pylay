from lupa import luajit21 as lupa
from contextlib import contextmanager
import os

lua = lupa.LuaRuntime()

location_stack = []

@contextmanager
def folder(name: str) -> None:
    try:
        location_stack.append(name)
        yield
    finally:
        location_stack.pop()

def load(name: str) -> None:
    path = os.path.dirname(__file__)
    for folder in location_stack:
        path = os.path.join(path, folder)
    path = os.path.join(path, f'{name}.lua')

    with open(path) as file:
        code = file.read()
    lua.execute(code, name=name)
