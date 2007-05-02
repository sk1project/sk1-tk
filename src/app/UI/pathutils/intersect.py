# Tamito KAJIYAMA <25 June 2002>

import base

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    object = objects[-1]
    for i in range(len(objects)-1):
        object = intersect([object, objects[i]])
        if object is None:
            break
    context.document.RemoveSelected()
    if object is not None:
        context.document.Insert(object)

def intersect(objects):
    assert len(objects) == 2
    buffer = []
    new_paths, untouched_paths = base.intersect_objects(objects)
    if not new_paths:
        return None
    for i, paths in new_paths:
        if i == 0:
            container = objects[1]
        else:
            container = objects[0]
        for cp1, path, cp2 in paths:
            if base.contained(path, container):
                buffer.append((cp1, path, cp2))
    object = objects[0].Duplicate()
    object.SetPaths(base.join(buffer))
    return object

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Intersect", "2. Intersect", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
