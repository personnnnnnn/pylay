Dimension = Class.create('Dimension')
function Dimension:create(width, height)
    self.width = width or 0
    self.height = height or 0
end

function Dimension:length(xAxis)
    if xAxis then
        return self.width
    else
        return self.height
    end
end

function Dimension:across(xAxis)
    return self:length(not xAxis)
end

function Dimension:setLength(xAxis, value)
    if xAxis then
        self.width = value
    else
        self.height = value
    end
end

function Dimension:setAcross(xAxis, value)
    self:setLength(not xAxis, value)
end
