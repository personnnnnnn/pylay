Text = Class.create('Text', Element)

TextMeasurer = {
    lineHeight = function(fontSize) end,
    textWidth = function(text, fontSize) end,
}

function Text.MakeUIData()
    local ui = { }
    ui.color = color(0, 0, 0)
    ui.fontSize = 5
    return ui
end

function Text:create(text)
    Element.create(self)
    self.text = text
    self.ui = Text.MakeUIData()
end

function wrapText(text, fontSize, maxWidth)
    local toConsume = text
    local newString = ''
    local currentLine = ''
    local lineCount = 0

    toConsume = string.gsub(toConsume, '\r\n?', '\n')

    while #toConsume ~= 0 do
        local char
        char, toConsume = consume(toConsume)

        if char == '\n' then
            lineCount = lineCount + 1
            newString = newString .. '\n' .. currentLine
            currentLine = ''
        else
            local width = TextMeasurer.textWidth(currentLine .. char, fontSize)
            if width > maxWidth then
                lineCount = lineCount + 1
                newString = newString .. '\n' .. currentLine
                currentLine = char
            else
                currentLine = currentLine .. char
            end
        end
    end

    if currentLine ~= '' then
        lineCount = lineCount + 1
        newString = newString .. '\n' .. currentLine
    end

    local _
    _, newString = consume(newString)

    return newString, lineCount * TextMeasurer.lineHeight(fontSize)
end

function Text:wrapText()
    Element.wrapText(self)
    local height
    self.text, height = wrapText(self.text, self.ui.fontSize, self.dim.width)
    self.dim.height = height
    self.min.height = height
    self.max.height = height

    if self.parent ~= nil and self.parent.ui.sizing.height ~= 'fixed' then
        self.parent.dim.height = self.parent.dim.height + self.dim.height
        self.parent.min.height = self.parent.min.height + self.dim.height
    end
end

function Text:used()
    Element.used(self)

    self.dim.width = TextMeasurer.textWidth(self.text, self.ui.fontSize)
    self.max.width = TextMeasurer.textWidth(self.text, self.ui.fontSize)

    local words = split(self.text)

    if #words ~= 0 then
        local minWordLength = math.huge

        for _, word in ipairs(words) do
            local wordLength = TextMeasurer.textWidth(word, self.ui.fontSize)
            if wordLength < minWordLength then
                minWordLength = wordLength
            end
        end

        self.min.width = minWordLength
    end

    if self.parent ~= nil and self.parent.ui.sizing.width == 'fit' then
        if self.parent:xAxis() then
            self.parent.dim.width = self.parent.dim.width + self.dim.width
        else
            local innerWidth = self.parent.dim.width - self.parent:paddingSum(true)
            self.parent.dim.width = math.max(innerWidth, self.dim.width)
        end
    end
end

function Text:render(commands, x, y)
    Element.render(commands, x, y)

    text {
        commands = commands,
        text = self.text,
        x = x,
        y = y,
        fontSize = self.ui.fontSize,
        color = self.ui.color,
    }
    commands[#commands].width = self.dim.width
    commands[#commands].height = self.dim.height

end
