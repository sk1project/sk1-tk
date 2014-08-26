# ------------------------------------ComboBox---------------------------------------------------- 


	style layout ComboNormal {
		ComboNormal.field -sticky ew -children {
        		ComboNormal.downarrow -side right -children {
        			ComboNormal.arrowsign -sticky ns
				}
        		ComboNormal.padding -expand true -children {
					ComboNormal.padding_focus -expand true -children {
        				ComboNormal.textarea
					}
				}
		}
		ComboNormal.readonly_focus -sticky news
	}		

	style element create ComboNormal.padding image [list "combo_entry_normal" \
				disabled "combo_entry_disabled_readonly" \
				readonly "combo_entry_normal_readonly" ] \
				-border {2 10 2 10} -padding {0 0 0 0} -sticky news 
				
	style element create ComboNormal.padding_focus image [list "combo_entry_clear" \
					{focus !disabled !readonly} "combo_entry_focusin" ] \
					-border {2 2 2 2} -padding {8 4 1 4} -sticky news	
				
	style element create ComboNormal.field image "combo_entry_clear" -padding {0 0 0 0}
					
	style element create ComboNormal.readonly_focus image [list "combo_entry_clear" \
	 				{readonly active !disabled} "combo_entry_readonly_focusin" ] \
					-border {2 10 2 10} -padding {0 0 0 0}

        style element create ComboNormal.downarrow image [list "combo_button_normal" \
			disabled "combo_button_disabled"] \
			-border {2 10 2 10} -padding {1 1 1 1} -sticky nse
			
    style element create ComboNormal.arrowsign image [list "combo_arrow" \
			disabled "combo_arrow_disabled"] -sticky e

	style configure ComboNormal -insertwidth 0 -ipady 0
	
	
# -------------------------PseudoActive----------------
	
	style layout PseudoActive {
		PseudoActive.field -sticky ew -children {
    			PseudoActive.downarrow -side right -children {
        			ComboNormal.arrowsign -sticky ns
				}
    			PseudoActive.padding -expand true -children {
					ComboNormal.padding_focus -expand true -children {
    					PseudoActive.textarea -sticky ew
					}
			}
		}
	}		
	
	style element create PseudoActive.padding image [list "combo_entry_normal" \
				disabled "combo_entry_disabled" \
				readonly "combo_entry_normal" ] \
				-border {2 10 2 10} -padding {0 0 0 0} -sticky news 
					
	style element create PseudoActive.field image "combo_entry_clear" -padding {0 0 0 0}
	
	style element create PseudoActive.downarrow image [list "combo_button_normal" \
			disabled "combo_button_disabled"] \
			-border {2 10 2 10} -padding {1 1 1 1} -sticky ens
	
	style configure PseudoActive -insertwidth 0 -ipady 0
