# -------------------------------------Scrollbars----------------------------------------------------- 
        style layout Vertical.TScrollbar {
            Scrollbar.vscrollbg -children {
				Scrollbar.uparrow -side top -unit 1 -children {
						Scrollbar.uparrowface -side top
				}
                Scrollbar.downarrow -side bottom -unit 1 -children {
						Scrollbar.downarrowface -side bottom
				}
                Vertical.Scrollbar.thumb -side top -expand true -sticky wens -unit 1 -children {
						Vertical.Scrollbar.thumbface -side top -expand true -sticky ns -children {
								Vertical.Scrollbar.label -expand true -sticky we
					}
				}
            }
        }

        style layout Horizontal.TScrollbar { 
	    Scrollbar.hscrollbg -children {
                Scrollbar.leftarrow -side left -unit 1 -children {
						Scrollbar.leftarrowface -side left
				}
                Scrollbar.rightarrow -side right -unit 1 -children {
						Scrollbar.rightarrowface -side right
				}
				Horizontal.Scrollbar.thumb -side left -expand true -sticky wens -unit 1 -children {
						Horizontal.Scrollbar.thumbface -side left -expand true -sticky we -children {
								Horizontal.Scrollbar.label -expand true -sticky ns
					}
				}
            }
        }

        style configure TScrollbar -width 16 
# -------------------------------------Vertical.Scrollbar Definition-------------------------------------------------   
        style element create Vertical.Scrollbar.thumb image "scroll_mask" \
				-border {1 1 1 1} -padding {0 0 0 0} -width 16 -height 34 -sticky news
	
        style element create Vertical.Scrollbar.thumbface image [list $K(vscroll_thumb)  \
				{pressed !disabled} $K(vscroll_thumb_pressed) \
				{active !disabled} $K(vscroll_thumb_active)] \
				-border {3 7 3 7} -width 16 -height 34 -sticky news
				
        style element create vscrollbg image $K(vscroll_bg) 

		style element create Vertical.Scrollbar.label  image $K(vscroll_grave) 
	
        style element create uparrowface image [list $K(vscroll_up_arrow)  \
				{pressed !disabled} $K(vscroll_up_arrow_pressed) \
				{active !disabled}  $K(vscroll_up_arrow_active) ] 
		style element create uparrow image "scroll_mask"
		
        style element create downarrowface image [list $K(vscroll_down_arrow) \
				{pressed !disabled} $K(vscroll_down_arrow_pressed) \
				{active !disabled}  $K(vscroll_down_arrow_active) ] 
		style element create downarrow image "scroll_mask"

# -----------------------------------------------Horizontal.Scrollbar Definition--------------------------------------
        style element create hscrollbg image $K(hscroll_bg) 

		style element create Horizontal.Scrollbar.thumb image "scroll_mask" \
				-border {1 1 1 1} -padding {0 0 0 0} -width 34 -height 16 -sticky news

		style element create Horizontal.Scrollbar.thumbface image [list $K(hscroll_thumb) \
				{pressed !disabled} $K(hscroll_thumb_pressed) \
				{active !disabled} $K(hscroll_thumb_active)] \
				-border {7 3 7 3} -width 34 -height 16 -sticky news
	    
		style element create Horizontal.Scrollbar.label  image $K(hscroll_grave) 

        style element create rightarrowface image [list $K(hscroll_right_arrow) \
				{pressed !disabled} $K(hscroll_right_arrow_pressed) \
				{active !disabled}  $K(hscroll_right_arrow_active) ]
		style element create rightarrow image "scroll_mask"

        style element create leftarrowface image [list $K(hscroll_left_arrow) \
				{pressed !disabled} $K(hscroll_left_arrow_pressed) \
				{active !disabled}  $K(hscroll_left_arrow_active) ]
		style element create leftarrow image "scroll_mask" 
