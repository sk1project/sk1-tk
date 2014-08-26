# -------------------------------------Scrollbars----------------------------------------------------- 
        style layout Vertical.TScrollbar {
            Scrollbar.vscrollbg -children {
				Scrollbar.uparrow -side top -unit 1 -children {
						Scrollbar.uparrowface -side top
				}
                Scrollbar.downarrow -side bottom -unit 1 -children {
						Scrollbar.downarrowface -side bottom
				}
                Scrollbar.uparrow -side bottom -unit 1 -children {
						Scrollbar.uparrowface -side top
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
                Scrollbar.leftarrow -side right -unit 1 -children {
						Scrollbar.leftarrowface -side left
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
        style element create Vertical.Scrollbar.thumb image "sb_bg_mask" \
				-border {1 1 1 1} -padding {0 0 0 0} -width 16 -height 22 -sticky news
	
        style element create Vertical.Scrollbar.thumbface image [list "vscroll_thumb"  \
				{pressed !disabled} "vscroll_thumb_pressed"] \
				-border {3 6 3 6} -width 16 -height 22 -sticky news
				
        style element create vscrollbg image "vscroll_bg" 
		#"bg_mask"	
		style element create Vertical.Scrollbar.label  image "vscroll_grave" 
	
        style element create uparrowface image [list "vscroll_up_arrow"  {pressed !disabled} "vscroll_up_arrow_pressed"]
		style element create uparrow image "vscroll_up_arrow_mask"
		
        style element create downarrowface image [list "vscroll_down_arrow" {pressed !disabled} "vscroll_down_arrow_pressed"]
		style element create downarrow image "vscroll_down_arrow_mask"

# -----------------------------------------------Horizontal.Scrollbar Definition--------------------------------------
        style element create hscrollbg image "hscroll_bg"  

		style element create Horizontal.Scrollbar.thumb image "sb_bg_mask" \
				-border {1 1 1 1} -padding {0 0 0 0} -width 22 -height 16 -sticky news

		style element create Horizontal.Scrollbar.thumbface image [list "hscroll_thumb" \
				{pressed !disabled} "hscroll_thumb_pressed"] \
				-border {6 3 6 3} -width 22 -height 16 -sticky news
	    
		style element create Horizontal.Scrollbar.label  image "hscroll_grave" 

        style element create rightarrowface image [list "hscroll_right_arrow" {pressed !disabled} "hscroll_right_arrow_pressed"]
		style element create rightarrow image "hscroll_right_arrow_mask"

        style element create leftarrowface image [list "hscroll_left_arrow" {pressed !disabled} "hscroll_left_arrow_pressed"]
		style element create leftarrow image "hscroll_left_arrow_mask" 
