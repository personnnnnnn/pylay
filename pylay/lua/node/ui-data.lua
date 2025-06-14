function Node.MakeUIData()
    local ui = { }
    ui.sizing = {
        width = 'fit', -- 'fit', 'fixed' or 'grow'
        height = 'fit',
    }
    ui.fixedSizing = {
        width = 0,
        height = 0,
    }
    ui.layoutDirection = 'ltr' -- 'ltr' or 'ttb'
    ui.overflow = 'show' -- 'show' or 'hide'
    ui.color = nil -- nil or color
    ui.padding = {
        left = 0,
        right = 0,
        top = 0,
        bottom = 0,
    }
    ui.childGap = 0
    return ui
end
