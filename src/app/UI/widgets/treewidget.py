# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import Frame, Entry, Label, ALL, NW, W, END

class TreeNode:

	def __init__(self, canvas, parent, item, colortheme, vspace=20):
		self.canvas = canvas
		self.parent = parent
		self.item = item
		self.state = 'collapsed'
		self.selected = False
		self.edited = False
		self.children = []
		self.colortheme =colortheme
		self.x = self.y = None
		self.vspace=vspace
		self.halfvspace=int(round(self.vspace/2))
		self.evenodd=0
		if not self.parent:
			self.canvas.bind('<Configure>',self.reconfig)

	def reconfig(self,*args):
		if len(self.canvas['scrollregion']) >0:
			w,n,e,s = self.canvas._getints(self.canvas['scrollregion'])	
			if e < self.canvas.winfo_width():
				e=self.canvas.winfo_width()	
			for item in self.canvas.windows:				
				win,x=item
				rightside=x+self.canvas._getints(self.canvas.itemcget(win,'width'))[0]
				if rightside<e:
					self.canvas.itemconfigure(win,width=e-x)			
		
	def destroy(self):
		for c in self.children[:]:
			self.children.remove(c)
			c.destroy()
		self.parent = None

	def geticonimage(self, name):
		return name

	def select(self, event=None):
		if self.selected:
			return
		self.deselectall()
		self.selected = True
#		self.canvas.delete(self.image_id)
		self.drawicon()
		self.drawtext()
		self.item.OnClick()

	def deselect(self, event=None):
		if not self.selected:
			return
		self.selected = False
#		self.canvas.delete(self.image_id)
		self.drawicon()
		self.drawtext()

	def deselectall(self):
		if self.parent:
			self.parent.deselectall()
		else:
			self.deselecttree()

	def deselecttree(self):
		if self.selected:
			self.deselect()
		for child in self.children:
			child.deselecttree()

	def flip(self, event=None):
		if self.state == 'expanded':
			self.collapse()
		else:
			self.expand()
		self.item.OnDoubleClick()
		return "break"

	def expand(self, event=None):
		if not self.item._IsExpandable():
			return
		if self.state != 'expanded':
			self.state = 'expanded'
			self.update()
			self.view()

	def collapse(self, event=None):
		self.deselecttree()
		if self.state != 'collapsed':
			self.state = 'collapsed'
			self.update()

	def view(self):
		top = self.y
		bottom = self.lastvisiblechild().y + self.vspace
		height = bottom - top
		visible_top = self.canvas.canvasy(0)
		visible_height = self.canvas.winfo_height()
		visible_bottom = self.canvas.canvasy(visible_height)
		if visible_top <= top and bottom <= visible_bottom:
			return
		x0, y0, x1, y1 = self.canvas._getints(self.canvas['scrollregion'])
		if top >= visible_top and height <= visible_height:
			fraction = top + height - visible_height
		else:
			fraction = top
		fraction = float(fraction) / y1
		self.canvas.yview_moveto(fraction)

	def lastvisiblechild(self):
		if self.children and self.state == 'expanded':
			return self.children[-1].lastvisiblechild()
		else:
			return self

	def update(self):
		if self.parent:
			self.parent.update()
		else:
			self.canvas.evenodd=1
			self.canvas.windows=[]
			oldcursor = self.canvas['cursor']
			self.canvas['cursor'] = "watch"
			self.canvas.update()
			self.canvas.delete(ALL)     
			self.draw(5, 3)
			x0, y0, x1, y1 = self.canvas.bbox(ALL)
			self.canvas.configure(scrollregion=(0, 0, x1, y1))
			self.canvas['cursor'] = oldcursor
			self.reconfig()

	def draw(self, x, y):
		if self.canvas.evenodd:
			self.evenodd=0
			self.canvas.evenodd=0
		else:
			self.evenodd=1
			self.canvas.evenodd=1
		self.x, self.y = x, y
		self.drawicon()
		self.drawtext()
		if self.state != 'expanded':
			return y+self.vspace
		# draw children
		if not self.children:
			sublist = self.item._GetSubList()
			if not sublist:
				# _IsExpandable() was mistaken; that's allowed
				return y+self.vspace
			for item in sublist:
				child = self.__class__(self.canvas, self, item, self.colortheme, self.vspace)
				self.children.append(child)
		cx = x+self.vspace
		cy = y+self.vspace
		cylast = 0
		for child in self.children:
			cylast = cy
			self.canvas.create_line(x+self.halfvspace, cy+self.halfvspace, cx, cy+self.halfvspace, 
								fill=self.colortheme.treelinescolor, stipple="gray50")
			cy = child.draw(cx, cy)
			if child.item._IsExpandable():
				if child.state == 'expanded':
					iconname = "tree_minus"
					callback = child.collapse
				else:
					iconname = "tree_plus"
					callback = child.expand
				image = self.geticonimage(iconname)
				id = self.canvas.create_image(x+self.halfvspace, cylast+self.halfvspace, image=image)
				self.canvas.tag_bind(id, "<1>", callback)
				self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
		id = self.canvas.create_line(x+self.halfvspace, y+self.halfvspace, x+self.halfvspace, 
									cylast+self.halfvspace, stipple="gray50", fill=self.colortheme.treelinescolor)
		self.canvas.tag_lower(id)
		return cy

	def drawicon(self):
	   	return

	def drawtext(self):
		textx = self.x
		texty = self.y
		labeltext = self.item.GetLabelText()
		if labeltext:
			id = self.canvas.create_text(textx, texty, anchor="nw", text=labeltext)
			self.canvas.tag_bind(id, "<1>", self.select)
			self.canvas.tag_bind(id, "<Double-1>", self.flip)
			x0, y0, x1, y1 = self.canvas.bbox(id)
			textx = max(x1, 200) + self.halfvspace
		text = self.item.GetText() or "<no text>"
		
		if self.selected:
			imagename = (self.item.GetSelectedIconName() or self.item.GetIconName() or "tree_node")
		else:
			imagename = self.item.GetIconName() or "tree_node"
		image = self.geticonimage(imagename)
		
		try:
			self.entry
		except AttributeError:
			pass
		else:
			self.edit_finish()
		try:
			label = self.label
		except AttributeError:

			self.frame = Frame(self.canvas, border=1, relief='flat')
			self.iconlabel = Label(self.frame, image=image, bd=0, padx=1, pady=1, anchor=W)
			self.label = Label(self.frame, text=text, bd=0, padx=3, pady=1, anchor=W)
			self.iconlabel.pack(side='left')
			self.label.pack(side='left', fill='y')

			
		widgets=[self.label,self.iconlabel, self.frame]
		
		if self.evenodd:
			bgcolor=self.colortheme.evencolor
		else:
			bgcolor=self.colortheme.editfieldbackground
			
		for widget in widgets:
			if self.selected:			
				widget['bg']=self.colortheme.selectbackground
			else:
				widget['bg']=bgcolor
				
		if self.selected:			
			self.label['fg']=self.colortheme.selectforeground
		else:
			self.label['fg']=self.colortheme.foreground
							
		width=self.frame.winfo_reqwidth()
		if width < self.canvas.winfo_width()-textx:
			width = self.canvas.winfo_width()-textx
			
		id = self.canvas.create_window(textx, texty, anchor=NW, window=self.frame, width=width)
		self.canvas.windows.append((id,textx))
		self.label.bind("<1>", self.select_or_edit)
		self.label.bind("<Double-1>", self.flip)
		self.iconlabel.bind("<1>", self.select_or_edit)
		self.iconlabel.bind("<Double-1>", self.flip)
		self.frame.bind("<1>", self.select_or_edit)
		self.frame.bind("<Double-1>", self.flip)
		self.label.bind("<Button-4>", self.unit_up)
		self.label.bind("<Button-5>", self.unit_down)
		self.iconlabel.bind("<Button-4>", self.unit_up)
		self.iconlabel.bind("<Button-5>", self.unit_down)
		self.frame.bind("<Button-4>", self.unit_up)
		self.frame.bind("<Button-5>", self.unit_down)		
		self.text_id = id
		
	def unit_up(self, event):
		first,last=self.canvas.yview()
		if first <= 0 and last >= 1:
			return "break"
		self.canvas.yview_scroll(-1, "unit")
		return "break"
	def unit_down(self, event):
		first,last=self.canvas.yview()
		if first <= 0 and last >= 1:
			return "break"
		self.canvas.yview_scroll(1, "unit")
		return "break"
	
	def select_or_edit(self, event=None):
		if self.selected and self.item.IsEditable():
			self.edit(event)
		else:
			self.select(event)

	def edit(self, event=None):
		if self.edited:
			return
		self.edited = True
		self.entry = Entry(self.label, bd=0, highlightthickness=1, width=0)
		self.entry.insert(0, self.label['text'])
		self.entry.selection_range(0, END)
		self.entry.pack(ipadx=5)
		self.entry.focus_set()
		self.entry.bind("<Return>", self.edit_finish)
		self.entry.bind("<Escape>", self.edit_cancel)

	def edit_finish(self, event=None):
		try:
			entry = self.entry
			del self.entry
			self.edited = False
		except AttributeError:
			return
		text = entry.get()
		entry.destroy()
		if text and text != self.item.GetText():
			self.item.SetText(text)
		text = self.item.GetText()
		self.label['text'] = text
		self.drawtext()
		self.canvas.focus_set()

	def edit_cancel(self, event=None):
		try:
			entry = self.entry
			del self.entry
			self.edited = False
		except AttributeError:
			return
		entry.destroy()
		self.drawtext()
		self.canvas.focus_set()


class TreeItem:

	"""Abstract class representing tree items.

	Methods should typically be overridden, otherwise a default action
	is used.

	"""

	def __init__(self):
		"""Constructor.  Do whatever you need to do."""

	def GetText(self):
		"""Return text string to display."""

	def GetLabelText(self):
		"""Return label text string to display in front of text (if any)."""

	expandable = None

	def _IsExpandable(self):
		"""Do not override!  Called by TreeNode."""
		if self.expandable is None:
			self.expandable = self.IsExpandable()
		return self.expandable

	def IsExpandable(self):
		"""Return whether there are subitems."""
		return 1

	def _GetSubList(self):
		"""Do not override!  Called by TreeNode."""
		if not self.IsExpandable():
			return []
		sublist = self.GetSubList()
		if not sublist:
			self.expandable = 0
		return sublist

	def IsEditable(self):
		"""Return whether the item's text may be edited."""

	def SetText(self, text):
		"""Change the item's text (if it is editable)."""

	def GetIconName(self):
		"""Return name of icon to be displayed normally."""

	def GetSelectedIconName(self):
		"""Return name of icon to be displayed when selected."""

	def GetSubList(self):
		"""Return list of items forming sublist."""

	def OnDoubleClick(self):
		"""Called on a double-click on the item."""
		pass
	
	def OnClick(self):
		"""Called on a double-click on the item."""
		pass
	
	def addComment(self):
		return ''