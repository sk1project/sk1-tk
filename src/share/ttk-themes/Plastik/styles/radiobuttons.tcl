# -------------------------------------Radiobutton---------------------------------------------------
        style element create Radiobutton.indicator image [list $K(radio_no_normal) \
				{!active  !disabled !selected} $K(radio_no_normal) \
				{!active  !disabled selected} $K(radio_yes_normal) \
				{active  !disabled selected} $K(radio_yes_active) \
				{active  !disabled !selected} $K(radio_no_active) \
				{disabled selected} $K(radio_yes_disabled) \
				{disabled !selected} $K(radio_no_disabled) ] \
				-width 20 -sticky w 
			

# ----------------------------------FineRadiobutton-------------------------------------------- 			
        style layout FineRadiobutton {
            FineRadiobutton.indicator -children {
	    	FineRadiobutton.focus -children {
                   FineRadiobutton.label
		}    
            }
        }			
        style element create FineRadiobutton.indicator image [list $K(fine_normal)\
				{!active  !disabled !selected} $K(fine_normal) \
				{!active  !disabled selected} $K(fine_selected) \
				{active  !disabled selected} $K(fine_selected) \
				{active  !disabled !selected} $K(fine_active) \
				{disabled selected} $K(fine_selected) \
				{disabled !selected} $K(fine_normal) ] \
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 33 -height 33  
				
# ----------------------------------ToolbarRadiobutton-------------------------------------------- 			
style layout ToolbarRadiobutton {
	ToolbarRadiobutton.indicator -children {
	ToolbarRadiobutton.focus -children {
		   ToolbarRadiobutton.label
}    
	}
}			
style element create ToolbarRadiobutton.indicator image [list $K(toolbutton_normal)\
		{!active  !disabled !selected} $K(toolbutton_normal) \
		{!active  !disabled selected} $K(toolbutton_selected) \
		{active  !disabled selected} $K(toolbutton_selected) \
		{active  !disabled !selected} $K(toolbutton_over) \
		{disabled selected} $K(toolbutton_selected) \
		{disabled !selected} $K(toolbutton_normal) ] \
		-border {2 2 2 2} \
		-padding {3 3 3 3} 