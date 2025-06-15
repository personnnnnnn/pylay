function Node:addPaddingToDimensionsAxis(xAxis)
    if self:getUILength(xAxis) == 'fixed' then
        return
    end

    self.dim:setLength(xAxis, self.dim:length(xAxis) + self:paddingSum(xAxis))

    if xAxis == self:xAxis() then
        local childGap = math.max(0, #self.children - 1) * self.ui.childGap
        self.dim:setLength(xAxis, self.dim:length(xAxis) + childGap)
    end
end

function Node:addPaddingToDimensions()
    self:addPaddingToDimensionsAxis(true)
    self:addPaddingToDimensionsAxis(false)
end

function Node:handleFitSizing(xAxis)
    for _, child in ipairs(self.children) do
        if Class.is(child, Node) then
            child:handleFitSizing(xAxis)
        elseif Class.is(child, Text) and xAxis then
            addDimensionsToParent(child, xAxis)
        end
    end
    addDimensionsToParent(self, xAxis)
end

-- self : Element
function addDimensionsToParent(self, xAxis)
    if self.parent == nil then
        return
    end

    if self.parent:getUILength(xAxis) ~= 'fit' then
        return
    end

    if xAxis == self.parent:xAxis() then
        self.parent.dim:setLength(
            xAxis,
            self.parent.dim:length(xAxis) + self.dim:length(xAxis)
        )
        self.parent.min:setLength(
            xAxis,
            self.parent.dim:length(xAxis) + self.dim:length(xAxis)
        )
    end

    if xAxis ~= self.parent:xAxis() then
        self.parent.dim:setLength(
            xAxis,
            math.max(self.parent.dim:length(xAxis), self.dim:length(xAxis) + self.parent:paddingSum(xAxis))
        )
        self.parent.min:setLength(
            xAxis,
            math.max(self.parent.min:length(xAxis), self.dim:length(xAxis) + self.parent:paddingSum(xAxis))
        )
    end
end

function Node:used()
    Element.used(self)

    if self.ui.sizing.width == 'fixed' then
        self.dim.width = self.dim.width + self.ui.fixedSizing.width
    end

    if self.ui.sizing.height == 'fixed' then
        self.dim.height = self.dim.height + self.ui.fixedSizing.height
    end

    self:addPaddingToDimensions()
end
