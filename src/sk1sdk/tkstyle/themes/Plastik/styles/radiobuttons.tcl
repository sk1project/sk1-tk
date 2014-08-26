# -------------------------------------Radiobutton---------------------------------------------------

        style layout TRadiobutton {
                	TRadiobutton.indicator -side left -children {
                		TRadiobutton.focus_border
                	}
        		TRadiobutton.label -side left
        }

        style element create TRadiobutton.indicator image [list "radio_no_normal" \
				{!active  !disabled !selected} "radio_no_normal" \
				{!active  !disabled selected} "radio_yes_normal" \
				{active  !disabled selected} "radio_yes_normal" \
				{active  !disabled !selected} "radio_no_normal" \
				{disabled selected} "radio_yes_disabled" \
				{disabled !selected} "radio_no_disabled" ] \
				-width 18 -sticky w 

	style element create TRadiobutton.focus_border image [list "radio_clear" \
 		{active !disabled} "radio_active" ] -width 18 -sticky w

# ----------------------------------FineRadiobutton-------------------------------------------- 			
        style layout FineRadiobutton {
            FineRadiobutton.indicator -children {
	    	FineRadiobutton.focus -children {
                   FineRadiobutton.label -sticky ns
		}    
            }
        }			
        style element create FineRadiobutton.indicator image [list "fine_normal"\
				{!active  !disabled !selected} "fine_normal" \
				{!active  !disabled selected} "fine_selected" \
				{active  !disabled selected} "fine_selected" \
				{active  !disabled !selected} "fine_active" \
				{disabled selected} "fine_selected" \
				{disabled !selected} "fine_normal" ] \
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 33 -height 33  
				
# ----------------------------------ToolbarRadiobutton-------------------------------------------- 			
style layout ToolbarRadiobutton {
	ToolbarRadiobutton.indicator -children {
	ToolbarRadiobutton.focus -children {
		   ToolbarRadiobutton.label -sticky ns
}    
	}
}			
style element create ToolbarRadiobutton.indicator image [list "toolbutton_normal"\
		{!active  !disabled !selected} "toolbutton_normal" \
		{!active  !disabled selected} "toolbutton_selected" \
		{active  !disabled selected} "toolbutton_selected" \
		{active  !disabled !selected} "toolbutton_over" \
		{disabled selected} "toolbutton_selected" \
		{disabled !selected} "toolbutton_normal" ] \
		-border {2 2 2 2} \
		-padding {3 3 3 3} 