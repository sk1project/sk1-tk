# ------------------------------------Checkbutton---------------------------------------------------

style layout TCheckbutton {
        	TCheckbutton.indicator -side left -children {
        		TCheckbutton.focus_border
        	}
		TCheckbutton.label -side left
}

style element create TCheckbutton.indicator image [list "check_no_normal" \
		{!active  !disabled !selected} "check_no_normal" \
		{!active  !disabled selected} "check_yes_normal" \
		{active  !disabled !selected} "check_no_normal" \
		{active  !disabled selected} "check_yes_normal" \
		{disabled selected} "check_yes_disabled" \
		{disabled !selected} "check_no_disabled" ] \
		-width 18 -sticky w
			
style element create TCheckbutton.focus_border image [list "check_clear" \
 		{active !disabled} "check_active" ] -width 18 -sticky w

# ------------------------------------------------------------------------------------------------------ 
