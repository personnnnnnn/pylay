function shallowCopy(t)
    local t2 = { }
    for k, v in pairs(t) do
        t2[k] = v
    end
    return t2
end

function printTable(t)
    print('{')
    for k, v in pairs(t) do
        print('\t'..tostring(k)..' = '..tostring(v)..',')
    end
    print('}')
end

function split(str, sep)
    if sep == nil then
        sep = '%s'
    end
    local t = { }
    for s in string.gmatch(str, '([^'..sep..']+)') do
        table.insert(t, s)
    end
    return t
end

-- returns the first character of a string, along with the rest of the string
function consume(str)
    return string.sub(str, 1, 1), string.sub(str, 2)
end
