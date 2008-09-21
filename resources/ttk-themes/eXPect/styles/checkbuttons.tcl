# ------------------------------------Checkbutton---------------------------------------------------
        style element create Checkbutton.indicator image [list $K(check_no_normal) \
				{!active  !disabled !selected !pressed} $K(check_no_normal) \
				{!active  !disabled  selected !pressed} $K(check_yes_normal) \
				{ active  !disabled  selected !pressed} $K(check_yes_active) \
				{ active  !disabled !selected !pressed} $K(check_no_active) \
				{!active  !disabled  selected  pressed} $K(check_yes_pressed) \
				{!active  !disabled !selected  pressed} $K(check_no_pressed) \
				{disabled  selected} $K(check_yes_disabled) \
				{disabled !selected} $K(check_no_disabled) ] \
				-width 20 -sticky w 
			
# ------------------------------------------------------------------------------------------------------ 
