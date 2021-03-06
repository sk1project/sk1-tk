#
# combobox.tcl,v 1.28 2005/09/29 02:32:06 jenglish Exp
#
# ttk widget set: combobox bindings.
#
# Each combobox $cb has a child $cb.popdown, which contains
# a listbox $cb.popdown.l and a scrollbar.  The listbox -listvariable
# is set to a namespace variable, which is used to synchronize the
# combobox values with the listbox values.
#

namespace eval ttk::combobox {
    variable Values	;# Values($cb) is -listvariable of listbox widget

    variable State
    set State(entryPress) 0
}

### Combobox bindings.
#
# Duplicate the Entry bindings, override if needed:
#
## Clipboard events:
#
bind TCombobox <<Cut>> 			{ ttk::entry::Cut %W }
bind TCombobox <<Copy>> 			{ ttk::entry::Copy %W }
bind TCombobox <<Paste>> 			{ ttk::entry::Paste %W }
bind TCombobox <<Clear>> 			{ ttk::entry::Clear %W }

## Button1 bindings:
#	Used for selection and navigation.
#
bind TCombobox <ButtonPress-1> 		{%W state active; ttk::entry::Press %W %x }
bind TCombobox <Shift-ButtonPress-1>	{ ttk::entry::Shift-Press %W %x }
bind TCombobox <Double-ButtonPress-1> 	{ ttk::entry::Select %W %x word }
bind TCombobox <Triple-ButtonPress-1> 	{ ttk::entry::Select %W %x line }
bind TCombobox <B1-Motion>			{ ttk::entry::Drag %W %x }

bind TCombobox <B1-Leave> 		{ ttk::Repeatedly ttk::entry::AutoScroll %W }
bind TCombobox <B1-Enter>		{ ttk::CancelRepeat }
bind TCombobox <ButtonRelease-1>	{ ttk::CancelRepeat }

bind TCombobox <FocusIn>		{ %W state active}
#bind TCombobox <Leave>		{ %W state !active}
bind TCombobox <FocusOut>		{ %W state !active}

bind TCombobox <Control-ButtonPress-1> {
    %W instate {!readonly !disabled} { icursor @%x ;focus %W }
}

## Button2 bindings:
#	Used for scanning and primary transfer.
#	Note: ButtonRelease-2 is mapped to <<PasteSelection>> in tk.tcl.
#
bind TCombobox <ButtonPress-2> 		{ ttk::entry::ScanMark %W %x }
bind TCombobox <B2-Motion> 		{ ttk::entry::ScanDrag %W %x }
bind TCombobox <ButtonRelease-2>		{ ttk::entry::ScanRelease %W %x }
bind TCombobox <<PasteSelection>>		{ ttk::entry::ScanRelease %W %x }

## Keyboard navigation bindings:
#
bind TCombobox <Key-Left> 			{ ttk::entry::Move %W prevchar }
bind TCombobox <Key-Right> 		{ ttk::entry::Move %W nextchar }
bind TCombobox <Control-Key-Left>		{ ttk::entry::Move %W prevword }
bind TCombobox <Control-Key-Right>		{ ttk::entry::Move %W nextword }
bind TCombobox <Key-Home>			{ ttk::entry::Move %W home }
bind TCombobox <Key-End>			{ ttk::entry::Move %W end }

bind TCombobox <Shift-Key-Left> 		{ ttk::entry::Extend %W prevchar }
bind TCombobox <Shift-Key-Right>		{ ttk::entry::Extend %W nextchar }
bind TCombobox <Shift-Control-Key-Left>	{ ttk::entry::Extend %W prevword }
bind TCombobox <Shift-Control-Key-Right>	{ ttk::entry::Extend %W nextword }
bind TCombobox <Shift-Key-Home>		{ ttk::entry::Extend %W home }
bind TCombobox <Shift-Key-End>		{ ttk::entry::Extend %W end }

bind TCombobox <Control-Key-slash> 	{ %W selection range 0 end }
bind TCombobox <Control-Key-backslash> 	{ %W selection clear }

bind TCombobox <<TraverseIn>> 	{ %W selection range 0 end; %W icursor end }

## Edit bindings:
#
bind TCombobox <KeyPress> 			{ ttk::entry::Insert %W %A }
bind TCombobox <Key-Delete>		{ ttk::entry::Delete %W }
bind TCombobox <Key-BackSpace> 		{ ttk::entry::Backspace %W }

# Ignore all Alt, Meta, and Control keypresses unless explicitly bound.
# Otherwise, the <KeyPress> class binding will fire and insert the character.
# Ditto for Escape, Return, and Tab.
#
bind TCombobox <Alt-KeyPress>		{# nothing}
bind TCombobox <Meta-KeyPress>		{# nothing}
bind TCombobox <Control-KeyPress> 		{# nothing}
bind TCombobox <Key-Escape> 		{# nothing}

bind TCombobox <Key-Return> 		{ttk::combobox::Run %W}
bind TCombobox <Key-KP_Enter> 		{ttk::combobox::Run %W}

bind TCombobox <Key-Tab> 			{# nothing}

# Argh.  Apparently on Windows, the NumLock modifier is interpreted
# as a Command modifier.
if {[tk windowingsystem] eq "aqua"} {
    bind TCombobox <Command-KeyPress>	{# nothing}
}

## Additional emacs-like bindings:
#
bind TCombobox <Control-Key-a>		{ ttk::entry::Move %W home }
bind TCombobox <Control-Key-b>		{ ttk::entry::Move %W prevchar }
bind TCombobox <Control-Key-d> 		{ ttk::entry::Delete %W }
bind TCombobox <Control-Key-e> 		{ ttk::entry::Move %W end }
bind TCombobox <Control-Key-f> 		{ ttk::entry::Move %W nextchar }
bind TCombobox <Control-Key-h>		{ ttk::entry::Backspace %W }
bind TCombobox <Control-Key-k>		{ %W delete insert end }

#-------------------------------------------------------------------------------------------
#ttk::CopyBindings TEntry TCombobox

bind TCombobox <KeyPress-Down> 		{ ttk::combobox::Post %W }
bind TCombobox <KeyPress-Escape> 	{ ttk::combobox::Unpost %W }

bind TCombobox <ButtonPress-1> 		{ ttk::combobox::Press "" %W %x %y }
bind TCombobox <Shift-ButtonPress-1>	{ ttk::combobox::Press "s" %W %x %y }
bind TCombobox <Double-ButtonPress-1> 	{ ttk::combobox::Press "2" %W %x %y }
bind TCombobox <Triple-ButtonPress-1> 	{ ttk::combobox::Press "3" %W %x %y }
bind TCombobox <B1-Motion>		{ ttk::combobox::Drag %W %x }

bind TCombobox <MouseWheel> 	{ ttk::combobox::Scroll %W [expr {%D/-120}] }
if {[tk windowingsystem] eq "x11"} {
    bind TCombobox <ButtonPress-4>	{ ttk::combobox::Scroll %W -1 }
    bind TCombobox <ButtonPress-5>	{ ttk::combobox::Scroll %W  1 }
}

bind TCombobox <<TraverseIn>> 		{ ttk::combobox::TraverseIn %W }

### Combobox listbox bindings.
#
bind ComboboxListbox <ButtonPress-1> 	{ focus %W ; continue }
bind ComboboxListbox <ButtonRelease-1>	{ ttk::combobox::LBSelected %W }
bind ComboboxListbox <KeyPress-Return>	{ ttk::combobox::LBSelected %W }
bind ComboboxListbox <KeyPress-Escape>  { ttk::combobox::LBCancel %W }
bind ComboboxListbox <KeyPress-Tab>	{ ttk::combobox::LBTab %W next }
bind ComboboxListbox <<PrevWindow>>	{ ttk::combobox::LBTab %W prev }
bind ComboboxListbox <Destroy>		{ ttk::combobox::LBCleanup %W }
# Default behavior is to follow selection on mouseover
bind ComboboxListbox <Motion> {
    %W selection clear 0 end
    %W activate @%x,%y
    %W selection set @%x,%y
}

# The combobox has a global grab active when the listbox is posted,
# but on Windows that doesn't prevent the user from interacting
# with other applications. The listbox gets a <FocusOut> event
# when this happens.  Don't know how reliable this is:
#
bind ComboboxListbox <FocusOut>		{ ttk::combobox::LBCancel %W }

bind ComboboxListbox <Enter> {
    %W config -cursor top_left_arrow
}
### Option database settings.
#

if {[tk windowingsystem] eq "x11"} {
    option add *TCombobox*Listbox.background white
}

# The following ensures that the popdown listbox uses the same font 
# as the combobox entry field (at least for the standard ttk themes).
#
option add *TCombobox*Listbox.font TkTextFont

### Binding procedures.
#

## combobox::Press $mode $x $y --
#	ButtonPress binding for comboboxes.
#	Either post/unpost the listbox, or perform Entry widget binding,
#	depending on widget state and location of button press.
#
proc ttk::combobox::Press {mode w x y} {
    variable State
    set State(entryPress) [expr {
	   [$w instate {!readonly !disabled}]
	&& [string match *textarea [$w identify $x $y]]
    }]

    if {$State(entryPress)} {
	focus $w
	switch -- $mode {
	    s 	{ ttk::entry::Shift-Press $w $x 	; # Shift }
	    2	{ ttk::entry::Select $w $x word 	; # Double click}
	    3	{ ttk::entry::Select $w $x line 	; # Triple click }
	    ""	-
	    default { ttk::entry::Press $w $x }
	}
    } else {
	TogglePost $w
    }
}

## combobox::Drag --
#	B1-Motion binding for comboboxes.
#	If the initial ButtonPress event was handled by Entry binding,
#	perform Entry widget drag binding; otherwise nothing.
#
proc ttk::combobox::Drag {w x}  {
    variable State
    if {$State(entryPress)} {
	ttk::entry::Drag $w $x
    }
}

## TraverseIn -- receive focus due to keyboard navigation
#	For editable comboboxes, set the selection and insert cursor.
#
proc ttk::combobox::TraverseIn {w} {
    $w instate {!readonly !disabled} { 
	$w selection range 0 end
	$w icursor end
    }
}

## SelectEntry $cb $index -- 
#	Set the combobox selection in response to a user action.
#
proc ttk::combobox::SelectEntry {cb index} {
    $cb current $index
	$w instate {!readonly !disabled} {
    $cb selection range 0 end
    $cb icursor end
	}
	#uplevel #0 [$cb cget -postcommand]
    #event generate $cb <<ComboboxSelected>>
}

## Scroll -- Mousewheel binding
#
proc ttk::combobox::Scroll {cb dir} {
    $cb instate disabled { return }
    set max [llength [$cb cget -values]]
    set current [$cb current]
    incr current $dir
    if {$max != 0 && $current == $current % $max} {
	SelectEntry $cb $current
    }
}

## LBSelected $lb -- Activation binding for listbox
#	Set the combobox value to the currently-selected listbox value
#	and unpost the listbox.
#
proc ttk::combobox::LBSelected {lb} {
    set cb [LBMaster $lb]
    set selection [$lb curselection]
    Unpost $cb
    focus $cb
    if {[llength $selection] == 1} {
	SelectEntry $cb [lindex $selection 0]
    }
}

## LBCancel --
#	Unpost the listbox.
#
proc ttk::combobox::LBCancel {lb} {
    Unpost [LBMaster $lb]
}

## LBTab --
#	Tab key binding for combobox listbox:  
#	Set the selection, and navigate to next/prev widget.
#
proc ttk::combobox::LBTab {lb dir} {
    set cb [LBMaster $lb]
    switch -- $dir {
	next	{ set newFocus [tk_focusNext $cb] }
	prev	{ set newFocus [tk_focusPrev $cb] }
    }

    if {$newFocus ne ""} {
	LBSelected $lb
	# The [grab release] call in [Unpost] queues events that later 
	# re-set the focus.  [update] to make sure these get processed first:
	update
	keynav::traverseTo $newFocus
    }
}

## PopdownShell --
#	Returns the popdown shell widget associated with a combobox,
#	creating it if necessary.
#
proc ttk::combobox::PopdownShell {cb} {
    global sk1_disabledfg sk1_txtnormal
    if {![winfo exists $cb.popdown]} {
	set popdown [toplevel $cb.popdown -relief flat -bd 1 -bg $sk1_disabledfg]
	wm withdraw $popdown
	wm overrideredirect $popdown 1
	wm transient $popdown [winfo toplevel $cb]

	# XXX Until we have a proper native scrollbar on Aqua, use
	# XXX the regular Tk one
	if {[tk windowingsystem] eq "aqua"} {
	    scrollbar $popdown.sb -orient vertical \
		-command [list $popdown.l yview]
	} else {
	    ttk::scrollbar $popdown.sb -orient vertical \
		-command [list $popdown.l yview]
	}
	listbox $popdown.l \
	    -listvariable ttk::combobox::Values($cb) \
	    -yscrollcommand [list $popdown.sb set] \
	    -exportselection false \
	    -selectmode browse \
	    -borderwidth 1 -relief flat \
	    -highlightthickness 0 \
            -selectborderwidth 0 \
	    -activestyle none \
		-background #ffffff \
		-font $sk1_txtnormal
	    ;

	bindtags $popdown.l \
	    [list $popdown.l ComboboxListbox Listbox $popdown all]

	grid $popdown.l $popdown.sb -sticky news
	grid columnconfigure $popdown 0 -weight 1
	grid rowconfigure $popdown 0 -weight 1
    }
    return $cb.popdown
}
	
proc ttk::combobox::Run {cb} {
	uplevel #0 [$cb cget -postcommand]
}

## combobox::Post $cb --
#	Pop down the associated listbox.
#
proc ttk::combobox::Post {cb} {
    variable State
    variable Values

    # Don't do anything if disabled:
    #
    $cb instate disabled { return }

    # Run -postcommand callback:
    #
    #uplevel #0 [$cb cget -postcommand]

    # Combobox is in 'pressed' state while listbox posted:
    #
    $cb state pressed

    set popdown [PopdownShell $cb]
    set values [$cb cget -values]
    set current [$cb current]
    if {$current < 0} {
	set current 0 		;# no current entry, highlight first one
    }
    set Values($cb) $values
    $popdown.l selection clear 0 end
    $popdown.l selection set $current
    $popdown.l activate $current
    $popdown.l see $current
    # Should allow user to control listbox height
    set height [llength $values]
    if {$height > 10} {
	set height 10
    } else {
	grid forget $popdown.sb
    }
    $popdown.l configure -height $height
    update idletasks

    # Position listbox (@@@ factor with menubutton::PostPosition
    #
    set x [winfo rootx $cb]
    set y [winfo rooty $cb]
    set w [winfo width $cb]
    set h [winfo height $cb]
    if {[tk windowingsystem] eq "aqua"} {
	# Adjust for platform-specific bordering to ensure the box is
	# directly under actual 'entry square'
	set xoff 3
	set yoff 2
	incr x $xoff
	set w [expr {$w - $xoff*2}]
    } else {
	set yoff 3
    }

    set H [winfo reqheight $popdown]
    if {$y + $h + $H > [winfo screenheight $popdown]} {
	set Y [expr {$y - $H - $yoff}]
    } else {
	set Y [expr {$y + $h - $yoff}]
    }
    wm geometry $popdown ${w}x${H}+${x}+${Y}	

    # Post the listbox:
    #
    wm deiconify $popdown
    raise $popdown

    # @@@ Workaround for TrackElementState bug:
    event generate $cb <ButtonRelease-1>
    # /@@@
    ttk::globalGrab $cb
    focus $popdown.l
}

## combobox::Unpost $cb --
#	Unpost the listbox, restore focus to combobox widget.
#
proc ttk::combobox::Unpost {cb} {
    $cb state !pressed
    ttk::releaseGrab $cb
    if {[winfo exists $cb.popdown]} {
	wm withdraw $cb.popdown
    }
    focus $cb	
	uplevel #0 [$cb cget -postcommand]
}

## combobox::TogglePost $cb --
#	Post the listbox if unposted, unpost otherwise.
#
proc ttk::combobox::TogglePost {cb} {
    if {[$cb instate pressed]} { Unpost $cb } { Post $cb }
}

## LBMaster $lb --
#	Return the combobox main widget that owns the listbox.
#
proc ttk::combobox::LBMaster {lb} {
    winfo parent [winfo parent $lb]
}

## LBCleanup $lb --
#	<Destroy> binding for combobox listboxes.
#	Cleans up by unsetting the linked textvariable.
#
#	Note: we can't just use { unset [%W cget -listvariable] }
#	because the widget command is already gone when this binding fires).
#	[winfo parent] still works, fortunately.
#

proc ttk::combobox::LBCleanup {lb} {
    variable Values
    unset Values([LBMaster $lb])
}

#*EOF*
