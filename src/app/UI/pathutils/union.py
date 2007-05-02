# Tamito KAJIYAMA <25 June 2002>

import base

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    object = objects[-1]
    for i in range(len(objects)-1):
        object = union([object, objects[i]])
    context.document.RemoveSelected()
    context.document.Insert(object)

def union(objects):
    assert len(objects) == 2
    buffer = []
    new_paths, untouched_paths = base.intersect_objects(objects)
    for i, paths in new_paths:
        if i == 0:
            container = objects[1]
        else:
            container = objects[0]
        for cp1, path, cp2 in paths:
            if not base.contained(path, container):
                buffer.append((cp1, path, cp2))
    paths = base.join(buffer)
    for i, path in untouched_paths:
        paths.append(path)
    object = objects[0].Duplicate()
    object.SetPaths(paths)
    return object

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Union", "1. Union", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
