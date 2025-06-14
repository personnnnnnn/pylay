from .dep_loader import folder, load, lua

def load_deps():
    with folder("lua"):
        # basics
        load("class")
        load("util")
        load("pylay")

        # helpers
        load("draw-commands")
        load("dimension")
        load("color")

        # actual logic
        load("element")

        load("text")

        with folder("node"):
            load("node")
            load("render")
            load("calculate-ui")
            load("ui")
            load("handle-growing-and-shrinking")
            load("ui-data")
