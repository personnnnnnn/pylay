Node = Class.create('Node', Element)

function Node:create()
    Element.create(self)
    self.ui = Node.MakeUIData()
    self.children = { }
end

function Node:show()
    self:enter()
    self:exit()
end

function Node:xAxis()
    return self.ui.layoutDirection == 'ltr'
end

function Node:paddingSum(xAxis)
    if xAxis then
        return self.ui.padding.left + self.ui.padding.right
    else
        return self.ui.padding.top + self.ui.padding.bottom
    end
end

function Node:wrapText()
    Element.wrapText(self)
    for _, child in ipairs(self.children) do
        child:wrapText()
    end
end

function Node:getUILength(xAxis)
    if xAxis then
        return self.ui.sizing.width
    else
        return self.ui.sizing.height
    end
end
