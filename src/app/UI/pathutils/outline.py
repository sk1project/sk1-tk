# Tamito KAJIYAMA <25 June 2002>

import base

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    objects = outline(objects)
    context.document.RemoveSelected()
    for object in objects:
        context.document.Insert(object)

from app import EmptyPattern, SolidPattern, StandardColors

def outline(objects):
    buffer = []
    new_paths, untouched_paths = base.intersect_objects(objects)
    for i, paths in new_paths:
        for cp1, path, cp2 in paths:
            new_object = objects[i].Duplicate()
            new_object.SetPaths([path])
            buffer.append(set_properties(new_object))
    for i, path in untouched_paths:
        new_object = objects[i].Duplicate()
        new_object.SetPaths([path])
        buffer.append(set_properties(new_object))
    return buffer

def set_properties(object):
    properties = object.Properties()
    if properties.fill_pattern.is_Solid:
        color = properties.fill_pattern.Color()
    else:
        color = StandardColors.black
    object.SetProperties(fill_pattern = EmptyPattern,
                         line_pattern = SolidPattern(color))
    if object.LineWidth() == 0:
        object.SetProperties(line_width = 1)
    return object

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Outline", "8. Outline", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
