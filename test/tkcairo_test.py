import cairo
from sk1sdk import tkcairo
import Tkinter
from Tkinter import *

CAIRO_WHITE = (1.0, 1.0, 1.0)

root = Tk()
root.title('Button')

frame = Frame(root, width=700, height=500)
frame.pack(side=TOP)

def click():
	ctx = tkcairo.create_context(frame)
	ctx.set_source_rgb(*CAIRO_WHITE)
	ctx.paint()

Button(text='Button', command=click).pack(side=BOTTOM)
root.mainloop()
