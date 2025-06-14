function Node:render(commands, x, y)
    Element.render(self, commands, x, y)

    if self.ui.color ~= nil then
        rectangle {
            commands = commands,
            x = x,
            y = y,
            width = self.dim.width,
            height = self.dim.height,
            color = self.ui.color,
        }
    end

    local childCommands
    if self.ui.overflow == 'hide' then
        childCommands = { }
    else
        childCommands = commands
    end

    local xAxis = self:xAxis()

    local childX = x + self.ui.padding.left
    local childY = y + self.ui.padding.top

    for _, child in ipairs(self.children) do
        child:render(childCommands, childX, childY)
        local increment = self.ui.childGap + child.dim:length(xAxis)
        if xAxis then
            childX = childX + increment
        else
            childY = childY + increment
        end
    end

    if self.ui.overflow == 'hide' then
        clip {
            commands = commands,
            subCommands = childCommands,
            x = x + self.ui.padding.left,
            y = y + self.ui.padding.top,
            width = self.dim.width - self.ui.padding.right,
            height = self.dim.height - self.ui.padding.bottom,
        }
    end
end
