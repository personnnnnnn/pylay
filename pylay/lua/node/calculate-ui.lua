function Node:calculateUI(x, y)
    x = x or 0
    y = y or 0

    self:handleFitSizing(true)
    self:handleGrowingAndShrinking(true)
    self:wrapText()
    self:handleFitSizing(false)
    self:handleGrowingAndShrinking(false)

    return self:getDrawCommands(x, y)
end
