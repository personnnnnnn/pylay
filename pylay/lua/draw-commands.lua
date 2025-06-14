function rectangle(data)
    local commands = data.commands
    commands[#commands + 1] = {
        type = 'rectangle',
        x = data.x,
        y = data.y,
        width = data.width,
        height = data.height,
        color = data.color,
    }
end

function clip(data)
    local commands = data.commands
    commands[#commands + 1] = {
        type = 'clip',
        x = data.x,
        y = data.y,
        width = data.width,
        height = data.height,
        subCommands = data.subCommands,
    }
end
