# ------------------------------------Checkbutton---------------------------------------------------
        style element create Checkbutton.indicator image [list $K(check_no_normal) \
				{!active  !disabled !selected} $K(check_no_normal) \
				{!active  !disabled selected} $K(check_yes_normal) \
				{active  !disabled selected} $K(check_yes_active) \
				{active  !disabled !selected} $K(check_no_active) \
				{disabled selected} $K(check_yes_disabled) \
				{disabled !selected} $K(check_no_disabled) ] \
				-width 20 -sticky w 
			
# ------------------------------------------------------------------------------------------------------ 
