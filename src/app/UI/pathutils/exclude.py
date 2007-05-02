# Tamito KAJIYAMA <1 July 2002>

import base

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    object = exclude(objects)
    context.document.RemoveSelected()
    context.document.Insert(object)

def exclude(objects):
    buffer = []
    new_paths, untouched_paths = base.intersect_objects(objects)
    if new_paths:
        segments = []
        for i, paths in new_paths:
            segments.extend(paths)
        buffer.extend(base.join(segments))
        assert len(buffer) == 1
    for i, path in untouched_paths:
        buffer.append(path)
    object = objects[-1].Duplicate()
    object.SetPaths(buffer)
    return object

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Exclude", "3. Exclude", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
