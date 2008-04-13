# ------------------------------------Button----------------------------------------------------
        style layout TButton {
            Button.background
            Button.button -children {
                Button.focus -children {
                    Button.label
                }
            }
        }
        style element create button image [list $K(button) \
				{pressed !disabled} $K(button_pressed) \
				{active !disabled}  $K(button_active) \
				disabled $K(button_disabled)] \
				-border {3 3 3 3} -padding {15 3 15 3} -sticky news
			
        style configure TButton -padding {10 6}	
	
	#----------------------
        style layout Pal2TopButton {
            Pal2TopButton.background
            Pal2TopButton.button -children {
                Pal2TopButton.focus -children {
                    Pal2TopButton.label -sticky ns
                }
            }
        }
        style element create Pal2TopButton.button image [list $K(pal_top_dbl_normal) \
				{pressed !disabled} $K(pal_top_dbl_pressed) \
				{active !disabled}  $K(pal_top_dbl_normal) \
				disabled $K(pal_top_dbl_disabled)] \
				-border {3 3 3 3} -padding {3 3 3 3} -sticky news 

        style configure Pal2TopButton -padding {3 3}	
	
	#----------------------
        style layout PalTopButton {
            PalTopButton.background
            PalTopButton.button -children {
                PalTopButton.focus -children {
                    PalTopButton.label -sticky ns
                }
            }
        }

        style element create PalTopButton.button image [list $K(pal_top_normal) \
				{pressed !disabled} $K(pal_top_pressed) \
				{active !disabled}  $K(pal_top_normal) \
				disabled $K(pal_top_disabled)] \
				-border {3 3 3 3} -padding {3 3 3 3} -sticky news

        style configure PalTopButton -padding {3 3}	
	#----------------------
        style layout PalBottomButton {
            PalBottomButton.background
            PalBottomButton.button -children {
                PalBottomButton.focus -children {
                    PalBottomButton.label -sticky ns
                }
            }
        }

        style element create PalBottomButton.button image [list $K(pal_bot_normal) \
				{pressed !disabled} $K(pal_bot_pressed) \
				{active !disabled}  $K(pal_bot_normal) \
				disabled $K(pal_bot_disabled)] \
				-border {3 3 3 3} -padding {3 3 3 3} -sticky news 
		      
        style configure PalBottomButton -padding {3 3}
	#----------------------
        style layout Pal2BottomButton {
            Pal2BottomButton.background
            Pal2BottomButton.button -children {
                Pal2BottomButton.focus -children {
                    Pal2BottomButton.label -sticky ns
                }
            }
        }

        style element create Pal2BottomButton.button image [list $K(pal_bot_dbl_normal) \
				{pressed !disabled} $K(pal_bot_dbl_pressed) \
				{active !disabled}  $K(pal_bot_dbl_normal) \
				disabled $K(pal_bot_dbl_disabled)] \
				-border {3 3 3 3} -padding {3 3 3 3} -sticky news 
		      
        style configure Pal2BottomButton -padding {3 3}	
	
	#----------------------
        style layout PalNoColorButton {
            PalNoColorButton.background
            PalNoColorButton.button -children {
                PalNoColorButton.focus -children {
                    PalNoColorButton.label
                }
            }
        }

        style element create PalNoColorButton.button image $K(clear) \
            -border {0 0 0 0} -padding {0 0 0 0} -sticky news
		      
        style configure PalNoColorButton 

	#----------------------
        style layout SpinUpButton {
            SpinUpButton.background
            SpinUpButton.button -children {
                SpinUpButton.focus -children {
                    SpinUpButton.label -sticky ns
                }
            }
        }

        style element create SpinUpButton.button image [list $K(spin_upbut_normal) \
				{pressed !disabled} $K(spin_upbut_pressed) \
				{active !disabled}  $K(spin_upbut_active) \
				disabled $K(spin_upbut_disabled)] \
				-border {2 2 2 2} -padding {2 2 2 2} -sticky news

        style configure SpinUpButton -padding {2 2}	

	#----------------------
        style layout SpinDownButton {
            SpinDownButton.background
            SpinDownButton.button -children {
                SpinDownButton.focus -children {
                    SpinDownButton.label -sticky ns
                }
            }
        }

        style element create SpinDownButton.button image [list $K(spin_downbut_normal) \
				{pressed !disabled} $K(spin_downbut_pressed) \
				{active !disabled}  $K(spin_downbut_active) \
				disabled $K(spin_downbut_disabled)] \
				-border {2 2 2 2} -padding {2 2 2 2} -sticky news

        style configure SpinDownButton -padding {2 2}
			
# ------------------------------------Corner----------------------------------------------------
        style layout TCornerButton {
            Button.background
            CornerButton.button -children {
                Button.focus -children {
                    Button.label
                }
            }
        }

        style element create CornerButton.button image [list $K(corner_normal) \
				{pressed !disabled} $K(corner_pressed) \
				{active !disabled}  $K(corner_active)] \
				-border {2 2 2 2} -padding {1 1 1 1} -sticky news 

# ---------------------------------------------------------------------------------------------------
	
        style layout Toolbutton {
            Toolbutton.button -children {
	    	Toolbutton.focus -children {
                    Toolbutton.label
		}    
            }
        }

        style element create Toolbutton.button image [list $K(toolbutton_normal) \
				{pressed !disabled} $K(toolbutton_pressed) \
				{active  !disabled}   $K(toolbutton_over) ] \
				-border {2 2 2 2} \
				-padding {3 3 3 3}  -sticky news

# ---------------------------------------------------------------------------------------------------
	
        style layout TSmallbutton {
            TSmallbutton.button  -expand true  -sticky news -children {
	    	TSmallbutton.focus -children {
                    TSmallbutton.label
		}    
            }
        }

        style element create TSmallbutton.button image [list $K(clear) \
				{pressed !disabled} $K(smallbutton_pressed) \
				{active  !disabled}   $K(smallbutton_over) ] \
				-border {1 1 1 1} \
				-padding {1 1 1 1} -sticky ew

# ---------------------------------------------------------------------------------------------------
	
        style layout TextButton {
            TextButton.background
            TextButton.button -children {
                TextButton.focus -children {
                    TextButton.label
                }
            }
        }
        style element create TextButton.button image [list $K(clear15) \
				{pressed !disabled} $K(button_pressed) \
				{active !disabled}  $K(button_active) \
				disabled $K(clear15)] \
				-border {3 3 3 3} -padding {5 3 5 3} -sticky news
			
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolCheckbutton {
            ToolCheckbutton.button -children {
	    	ToolCheckbutton.focus -children {
                    ToolCheckbutton.label
		}
            }
        }

        style element create ToolCheckbutton.button image $K(tools_pressed) \
            -border {2 2 2 2} -padding {3 3 3 3}
	    
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolbarCheckbutton {
            ToolbarCheckbutton.button -children {
	    	ToolbarCheckbutton.focus -children {
                    ToolbarCheckbutton.label
		}
            }
        }

        style element create ToolbarCheckbutton.button image $K(toolbutton_selected) \
            -border {2 2 2 2} -padding {3 3 3 3} 
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolsButton {
            ToolsButton.button -children {
	    	ToolsButton.focus -children {
                    ToolsButton.label
		}    
            }
        }

        style element create ToolsButton.button image [list $K(tools_normal) \
				{pressed !disabled} $K(tools_button_pressed) \
				{active  !disabled}   $K(tools_active)]\
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 33 -height 33
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolBarCheckButton {
            ToolBarCheckButton.button -children {
	    	ToolBarCheckButton.focus -children {
                    ToolBarCheckButton.label
		}    
            }
        }

        style element create ToolBarCheckButton.button image [list $K(tools_normal) \
				{pressed !disabled} $K(tools_button_pressed) \
				{selected} $K(toolbutton_selected) \
				{active  !disabled}   $K(tools_active)]\
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 28 -height 28	 

# -------------------------------------RootMenubutton-----------------------------------------
        style layout TRootMenubutton {
	TRootMenubutton.background{
            TRootMenubutton.button -children {
                TRootMenubutton.focus -children {
                    TRootMenubutton.padding -children {
                        TRootMenubutton.label -side left 
                    }
                }
            }
        }
	}
	
		style configure TRootMenubutton -relief flat -sticky ew -side left
		style configure TRootMenubutton.background -relief flat -sticky ew -side left
		style element create TRootMenubutton.button image [list $K(menubutton_normal)  \
				pressed $K(menubutton_pressed) \
				active $K(menubutton_active) \
				disabled $K(menubutton_normal)] \
				-border {4 6 4 3} -sticky ew 
		

# -------------------------------------TComboSmall-----------------------------------------
        style layout TComboSmall {
	TComboSmall.background{
            TComboSmall.button -children {
                TComboSmall.focus -children {
                    TComboSmall.padding -children {
                        TComboSmall.label -side left 
                    }
                }
            }
        }
	}
	
		style configure TComboSmall -relief flat -sticky ew -side left
        style element create TComboSmall.button image [list $K(combo_normal)  \
				pressed $K(combo_active) \
				active $K(combo_active) \
				disabled $K(combo_disabled)] \
				-border {4 2 20 2} -padding {4 2 20 2} -sticky ew 
				
# ------------------------------------DocTabs--------------------------------------------------				
				
	# ------DocTabNormal-------
	style layout DocTabNormal {
		DocTabNormal.button -children {
			DocTabNormal.label -side left
			DocTabNormal.text -side left
			}
		}
	style configure DocTabNormal  -relief flat 
	
	style element create DocTabNormal.button image [list $K(doctabs_tab) \
					{pressed !disabled} $K(doctabs_tab_selected) \
					{active !disabled}  $K(doctabs_tab_selected)] \
		-border {1 5 2 4} -padding {5 5 5 4} -sticky ew	
		
	# ------DocTabActive-------
	style layout DocTabActive {
		DocTabActive.button -children {
			DocTabActive.label -side left
			DocTabActive.text -side left
			}
		}
	style configure DocTabActive  -relief flat 
	
	style element create DocTabActive.button image $K(doctabs_tab_active) \
		-border {2 3 3 2} -padding {5 3 5 2} -sticky ew	
				