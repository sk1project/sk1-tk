# Tamito KAJIYAMA <2 July 2002>

import base

def run_script(context, target):
    objects = base.get_selection(context)
    if not objects:
        return
    object = objects.pop(target)
    for i in range(len(objects)):
        object = minus([object, objects[i]])
    context.document.RemoveSelected()
    context.document.Insert(object)

def minus(objects):
    assert len(objects) == 2
    new_paths, untouched_paths = base.intersect_objects(objects)
    buffer = []
    for i, paths in new_paths:
        if i == 0:
            container = objects[1]
            condition = 0
        else:
            container = objects[0]
            condition = 1
        for cp1, path, cp2 in paths:
            if base.contained(path, container) == condition:
                buffer.append((cp1, path, cp2))
    paths = base.join(buffer)
    for i, path in untouched_paths:
        if i == 0:
            container = objects[1]
            condition = 0
        else:
            container = objects[0]
            condition = 1
        if base.contained(path, container) == condition:
            paths.append(path)
    object = objects[0].Duplicate()
    object.SetPaths(paths)
    return object

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Minus Front", "4. Minus Front", run_script,
                             menu="PathUtils", args=(0,),
                             script_type=app.Scripting.AdvancedScript)

app.Scripting.AddFunction("Minus Back", "5. Minus Back", run_script,
                             menu="PathUtils", args=(-1,),
                             script_type=app.Scripting.AdvancedScript)
