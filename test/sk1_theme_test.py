
import Tkinter
from Tkinter import *
import ttk
from sk1sdk import tkstyle

CAIRO_WHITE = (1.0, 1.0, 1.0)

root = Tk()
root.title('Button')

root.withdraw()
style = tkstyle.get_system_style(root)
currentColorTheme = style.colors
tkstyle.set_style(root, style, 1)

def click():
	print 'click'

for a in range(20):
	ttk.Button(text='Button', command=click).pack(side=BOTTOM)

for a in range(20):
	ttk.Button(text='Button', command=click).pack(side=TOP)
root.deiconify()
root.update()
root.mainloop()
