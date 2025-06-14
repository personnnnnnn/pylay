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
