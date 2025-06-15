function Node:handleGrowingAndShrinking(xAxis)
    if #self.children == 0 then
        return
    end

    if xAxis ~= self:xAxis() then
        for _, child in ipairs(self.children) do
            if Class.is(child, Text) or (Class.is(child, Node) and child:getUILength(xAxis) == 'grow') then
                child.dim:setLength(xAxis, self.dim:length(xAxis) - self:paddingSum(xAxis))
            end
        end

        for _, child in ipairs(self.children) do
            if Class.is(child, Node) then
                child:handleGrowingAndShrinking(xAxis)
            end
        end

        return
    end

    local remainingLength = self.dim:length(xAxis) - self:paddingSum(xAxis)
    local changeable = { }

    for _, child in ipairs(self.children) do
        remainingLength = remainingLength - child.dim:length(xAxis)
        if (Class.is(child, Text) and xAxis) or (Class.is(child, Node) and child:getUILength(xAxis) == 'grow') then
            changeable[#changeable + 1] = child
        end
    end

    remainingLength = remainingLength - (#self.children - 1) * self.ui.childGap

    while self:getUILength(xAxis) ~= 'fit' and remainingLength > 0.1 and #changeable ~= 0 do -- grow
        local smallest = changeable[1].dim:length(xAxis)
        local secondSmallest = math.huge
        local lengthToAdd = remainingLength

        for _, child in ipairs(changeable) do
            if child.dim:length(xAxis) < smallest then
                secondSmallest = smallest
                smallest = child.dim:length(xAxis)
            end
            if child.dim:length(xAxis) > smallest then
                secondSmallest = math.min(secondSmallest, child.dim:length(xAxis))
                lengthToAdd = secondSmallest - smallest
            end
        end

        lengthToAdd = math.min(lengthToAdd, remainingLength / #changeable)

        for i, child in ipairs(changeable) do
            if child.dim:length(xAxis) == smallest then
                local previousLength = child.dim:length(xAxis)
                child.dim:setLength(xAxis, child.dim:length(xAxis) + lengthToAdd)
                if
                    child.dim:length(xAxis) >= child.max:length(xAxis)
                    and child.max:length(xAxis) ~= 0
                then
                    child.dim:setLength(xAxis, child.max:length(xAxis))
                    table.remove(changeable, i)
                end
                remainingLength = remainingLength - (child.dim:length(xAxis) - previousLength)
            end
        end
    end

    while remainingLength < -0.1 and #changeable ~= 0 do -- shrink
        local largest = changeable[1].dim:length(xAxis)
        local secondLargest = 0
        local lengthToAdd = remainingLength

        for _, child in ipairs(changeable) do
            if child.dim:length(xAxis) > largest then
                secondLargest = largest
                largest = child.dim:length(xAxis)
            end
            if child.dim:length(xAxis) < largest then
                secondLargest = math.max(secondLargest, child.dim:length(xAxis))
                lengthToAdd = secondLargest - largest
            end
        end

        lengthToAdd = math.max(lengthToAdd, remainingLength / #changeable)

        for i, child in ipairs(changeable) do
            if child.dim:length(xAxis) == largest then
                local previousLength = child.dim:length(xAxis)
                child.dim:setLength(xAxis, child.dim:length(xAxis) + lengthToAdd)
                if
                    child.dim:length(xAxis) <= child.min:length(xAxis)
                then
                    child.dim:setLength(xAxis, child.min:length(xAxis))
                    table.remove(changeable, i)
                end
                remainingLength = remainingLength + (child.dim:length(xAxis) - previousLength)
            end
        end
    end

    for _, child in ipairs(self.children) do
        if Class.is(child, Node) then
            child:handleGrowingAndShrinking(xAxis)
        end
    end
end
