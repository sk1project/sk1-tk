# Tamito KAJIYAMA <25 June 2002>

import base

from minus import minus

def run_script(context):
    objects = base.get_selection(context)
    if not objects:
        return
    for i in range(len(objects)-1):
        for j in range(i+1, len(objects)):
            objects[i] = minus([objects[i], objects[j]])
    context.document.RemoveSelected()
    for i in range(len(objects)):
        context.document.Insert(objects[i])

###   REGISTRY   ###

import app.Scripting

app.Scripting.AddFunction("Trim", "7. Trim", run_script,
                             menu="PathUtils",
                             script_type=app.Scripting.AdvancedScript)
