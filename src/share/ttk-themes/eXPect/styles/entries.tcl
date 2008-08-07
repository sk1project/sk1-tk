# ------------------------------------Entry----------------------------------------------------
	style layout TEntry {
		TEntry.border -children {
			TEntry.textarea
		}
	}		
	style element create TEntry.border image [list $K(entry_normal) \
				disabled $K(entry_disabled) \
				readonly $K(entry_disabled) \
				focus $K(entry_focusin)] \
				-border {5 3 3 3} -padding {4 5 3 3} -sticky ew 
				
	style configure TEntry -cursor xterm		
	# --------------------------
	style layout SpinEntry {
		SpinEntry.border -children {
			TEntry.textarea
		}
	}		
	style element create SpinEntry.border image [list $K(spin_entry_normal) \
				disabled $K(spin_entry_disabled) \
				readonly $K(spin_entry_disabled) ] \
				-border {5 3 3 3} -padding {4 5 3 3} -sticky ew 
