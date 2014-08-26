# ------------------------------------Entry----------------------------------------------------
	style layout TEntry {
		TEntry.border -children {
			TEntry.focus_border -children {
				TEntry.textarea
			}
		}
	}		
	style element create TEntry.border image [list "entry_normal" \
				disabled "entry_disabled" \
				readonly "entry_disabled" ] \
				-border {2 2 2 2} -padding {0 0 0 0} -sticky news 
	
	style element create TEntry.focus_border image [list "entry_clear" \
			{focus !readonly} "entry_focusin" ] \
			-border {2 2 2 2} -padding {4 4 4 4} -sticky news 
				
	style configure TEntry -cursor xterm
	
	#focus "entry_focusin"
	
	# --------------------------
	style layout SpinEntry {
		SpinEntry.border -children {
			SpinEntry.focus_border -children {
				TEntry.textarea
			}
		}
	}		
	style element create SpinEntry.border image [list "spin_entry_normal" \
				disabled "spin_entry_disabled" \
				readonly "spin_entry_disabled" ] \
				-border {5 3 3 3} -padding {0 0 0 0} -sticky ew 
				
	style element create SpinEntry.focus_border image [list "spin_entry_clear" \
				focus "spin_entry_focusin" ] \
				-border {5 3 3 3} -padding {4 5 3 3} -sticky ew 
				
				
