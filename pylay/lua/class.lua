Class = { }

function Class.anon(super)
    return Class.create('<anon>', super)
end

function Class.create(name, super)
    local class

    if super ~= nil then
        class = shallowCopy(super)
        class.ClassList = shallowCopy(class.ClassList)
    else
        class = { ClassList = { } }

        function class:__tostring()
            return "<" .. self.ClassName .. " object>"
        end

        local classMeta = { }

        function classMeta:__call(...)
            return self.New(...)
        end

        function classMeta:__tostring()
            return "<" .. self.ClassName .. " class>"
        end

        setmetatable(class, classMeta)
    end

    function class.New(...)
        local o = shallowCopy(class)
        setmetatable(o, class)
        o:create(...)
        return o
    end

    function class:create() end

    class.ClassList[#class.ClassList + 1] = class
    class.ClassName = name

    return class
end

function Class.isObject(object)
    return
        type(object.ClassName) == "string"
        and type(object.ClassList) == "table"
        and type(object.New) == "function"
end

function Class.extends(object, class)
    for _, c in ipairs(object.ClassList) do
        if c == class then return true end
    end
    return false
end

function Class.is(v, class)
    return Class.isObject(v) and Class.extends(v, class)
end
