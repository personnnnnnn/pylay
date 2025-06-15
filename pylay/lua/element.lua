Element = Class.create('Element')

function Element:create()
    self.dim = Dimension.New()
    self.min = Dimension.New()
    self.max = Dimension.New()
    self.hasBeenOpened = false
    if #UIStack == 0 then
        self.parent = nil
    else
        self.parent = UIStack[#UIStack]
        self.parent.children[#self.parent.children + 1] = self
    end
end

function Element:used() end

function Element:enter()
    UIStack[#UIStack + 1] = self
end

function Element:exit()
    if not self.hasBeenOpened then
        self.hasBeenOpened = true
        self:used()
    end
    UIStack[#UIStack] = nil
end

--                      commands, x, y
function Element:render(_       , _, _) end

function Element:getDrawCommands(x, y)
    x = x or 0
    y = y or 0
    local commands = { }
    self:render(commands, x, y)
    return commands
end

function Element:wrapText() end
