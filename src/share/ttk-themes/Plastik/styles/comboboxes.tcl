# ------------------------------------ComboBox---------------------------------------------------- 


	style layout ComboNormal {
		ComboNormal.field -sticky ew -children {
		ComboNormal.downarrow -side right
		ComboNormal.padding -expand true -children {
			ComboNormal.textarea -sticky ew
		}
		}
	}		

	style element create ComboNormal.padding image [list $K(spin_entry_normal) \
				disabled $K(spin_entry_disabled) \
				readonly $K(combo_entry_readonly) \
				{focus !readonly} $K(spin_entry_focusin) \
				{active readonly} $K(combo_entry_readonly_active)] \
				-border {2 1 1 1} -padding {8 1 1 1} -sticky ew 
				
		style element create ComboNormal.field image $K(clear)  -padding {0 3 0 3}

        style element create ComboNormal.downarrow image [list $K(combo_button_normal) \
				{pressed !disabled} $K(combo_button_normal) \
				{focus !disabled !readonly}  $K(combo_button_active) \
				{active !disabled readonly}  $K(combo_button_normal) \
				disabled $K(combo_button_disabled)] \
				-border {1 1 1 1} -padding {1 1 1 1} -sticky e 

	style configure ComboNormal -borderwidth 0 -insertwidth 0 -ipady 0
	
	
# -------------------------PseudoActive----------------
	
		style layout PseudoActive {
			PseudoActive.field -sticky ew -children {
			PseudoActive.downarrow -side right
			PseudoActive.padding -expand true -children {
				PseudoActive.textarea -sticky ew
			}
			}
		}		
	
		style element create PseudoActive.padding image [list $K(spin_entry_normal) \
					disabled $K(spin_entry_disabled) \
					readonly $K(spin_entry_normal) \
					{focus !readonly} $K(spin_entry_focusin) \
					{active readonly} $K(combo_entry_readonly_active)] \
					-border {2 1 1 1} -padding {8 1 1 1} -sticky ew 
					
			style element create PseudoActive.field image $K(clear)  -padding {0 3 0 3}
	
			style element create PseudoActive.downarrow image [list $K(combo_button_normal) \
					{pressed !disabled} $K(combo_button_normal) \
					{active !disabled !readonly}  $K(combo_button_active) \
					{active !disabled readonly}  $K(combo_button_normal) \
					disabled $K(combo_button_disabled)] \
					-border {1 1 1 1} -padding {1 1 1 1} -sticky e 
	
		style configure PseudoActive -borderwidth 0 -insertwidth 0 -ipady 0
