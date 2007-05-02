# Tamito KAJIYAMA <25 June 2002>

import base

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    objects[0:2] = divide(objects[0], objects[1])
    context.document.RemoveSelected()
    for object in objects:
        context.document.Insert(object)

def divide(object1, object2):
    buffer = []
    new_paths, untouched_paths = base.intersect_objects([object1, object2])
    if new_paths:
        common = []
        parts = ([], [])
        for i, paths in new_paths:
            if i == 0:
                container = object2
                parts2, parts1 = parts
            else:
                container = object1
                parts1, parts2 = parts
            for cp1, path, cp2 in paths:
                if base.contained(path, container):
                    common.append((cp1, path, cp2))
                    parts2.append((cp1, path, cp2))
                else:                         
                    parts1.append((cp1, path, cp2))
        for path in base.join(parts1):
            object = object1.Duplicate()
            object.SetPaths([path])
            buffer.append(object)
        for path in base.join(parts2):
            object = object2.Duplicate()
            object.SetPaths([path])
            buffer.append(object)
        for path in base.join(common):
            object = object2.Duplicate()
            object.SetPaths([path])
            buffer.append(object)
        for i, path in untouched_paths:
            if i == 0:
                object = object1.Duplicate()
            else:
                object = object2.Duplicate()
            object.SetPaths([path])
            buffer.append(object)
    else:
        buffer.append(object1.Duplicate())
        buffer.append(object2.Duplicate())
    return buffer

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Divide", "6. Divide", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
