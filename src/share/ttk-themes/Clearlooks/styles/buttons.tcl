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
				-border {4 4 4 4} -padding {15 3 15 3} -sticky news
			
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
				{active !disabled}  $K(pal_top_dbl_normal) ] \
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
				{active !disabled}  $K(pal_top_normal) ] \
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
				{active !disabled}  $K(pal_bot_normal) ] \
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
				{active !disabled}  $K(pal_bot_dbl_normal) ] \
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
                    Toolbutton.label -sticky ns
		}    
            }
        }

        style element create Toolbutton.button image [list $K(toolbutton_normal) \
				{pressed !disabled} $K(toolbutton_pressed) \
				{active  !disabled}   $K(toolbutton_over) ] \
				-sticky nwes \
				-border {3 3 3 3} \
				-padding {0 0 0 0}
#  -width 28 -height 28

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
				-border {4 4 4 4} -padding {5 3 5 3} -sticky news
			
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolCheckbutton {
            ToolCheckbutton.button -children {
	    	ToolCheckbutton.focus -children {
                    ToolCheckbutton.label -sticky ns
		}
            }
        }

        style element create ToolCheckbutton.button image $K(tools_pressed) \
		-sticky nwes \
            -border {3 3 3 3} -padding {0 0 0 0}
#  -width 28 -height 28
	    
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolbarCheckbutton {
            ToolbarCheckbutton.button -children {
	    	ToolbarCheckbutton.focus -children {
                    ToolbarCheckbutton.label -sticky ns
		}
            }
        }

        style element create ToolbarCheckbutton.button image $K(toolbutton_selected) \
		-sticky nwes \
            -border {3 3 3 3} -padding {0 0 0 0}
#  -width 28 -height 28
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolsButton {
            ToolsButton.button -children {
	    	ToolsButton.focus -children {
                    ToolsButton.label -sticky ns
		}    
            }
        }

        style element create ToolsButton.button image [list $K(tools_normal) \
				{pressed !disabled} $K(tools_button_pressed) \
				{active  !disabled}   $K(tools_active)]\
				-sticky nwes \
				-border {3 3 3 3} \
				-padding {0 0 0 0}
#				-width 28 -height 28
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolBarCheckButton {
            ToolBarCheckButton.button -children {
	    	ToolBarCheckButton.focus -children {
                    ToolBarCheckButton.label -sticky ns
		}    
            }
        }

        style element create ToolBarCheckButton.button image [list $K(tools_normal) \
				{pressed !disabled} $K(tools_button_pressed) \
				{selected} $K(toolbutton_selected) \
				{active  !disabled}   $K(tools_active)]\
				-sticky nwes \
				-border {3 3 3 3} \
				-padding {0 0 0 0}
#				-width 28 -height 28	 

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
	
	style element create DocTabNormal.button image $K(doctabs_tab) \
		-border {2 5 3 4} -padding {5 5 5 4} -sticky ew	
		
	# ------DocTabActive-------
	style layout DocTabActive {
		DocTabActive.button -children {
			DocTabActive.label -side left
			DocTabActive.text -side left
			}
		}
	style configure DocTabActive  -relief flat 
	
	style element create DocTabActive.button image $K(doctabs_tab_active) \
		-border {3 3 3 2} -padding {5 3 5 2} -sticky ew	
				
# ------------------------------------Pager----------------------------------------------------	
	# ------HOME-------
	style layout PagerHome {
		PagerHome.background
		PagerHome.button -children {
			PagerHome.focus -children {
				PagerHome.label -sticky ns
			}
		}
	}

	style element create PagerHome.button image [list $K(pager_normal_bg) \
			{pressed !disabled} $K(pager_pressed_bg) \
			{active !disabled}  $K(pager_active_bg)] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerHome.label image [list $K(pager_home_arrow) \
			{pressed !disabled} $K(pager_home_arrow_pressed)] -sticky news 

	# ------END-------
	style layout PagerEnd {
		PagerEnd.background
		PagerEnd.button -children {
			PagerEnd.focus -children {
				PagerEnd.label -sticky ns
			}
		}
	}

	style element create PagerEnd.button image [list $K(pager_normal_bg) \
			{pressed !disabled} $K(pager_pressed_bg) \
			{active !disabled}  $K(pager_active_bg)] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerEnd.label image [list $K(pager_end_arrow) \
			{pressed !disabled} $K(pager_end_arrow_pressed)] -sticky news 
	
	# ------PREVIOUS-------
	style layout PagerPrevious {
		PagerPrevious.background
		PagerPrevious.button -children {
			PagerPrevious.focus -children {
				PagerPrevious.label -sticky ns
			}
		}
	}

	style element create PagerPrevious.button image [list $K(pager_normal_bg) \
			{pressed !disabled} $K(pager_pressed_bg) \
			{active !disabled}  $K(pager_active_bg)] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerPrevious.label image [list $K(pager_previous_arrow) \
			{pressed !disabled} $K(pager_previous_arrow_pressed)] -sticky news  
			
	# ------NEXT-------
	style layout PagerNext {
		PagerNext.background
		PagerNext.button -children {
			PagerNext.focus -children {
				PagerNext.label -sticky ns
			}
		}
	}

	style element create PagerNext.button image [list $K(pager_normal_bg) \
			{pressed !disabled} $K(pager_pressed_bg) \
			{active !disabled}  $K(pager_active_bg)] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerNext.label image [list $K(pager_next_arrow) \
			{pressed !disabled} $K(pager_next_arrow_pressed)] -sticky news 
			
	# ------ADD-------
	style layout PagerAdd {
		PagerAdd.background
		PagerAdd.button -children {
			PagerAdd.focus -children {
				PagerAdd.label -sticky ns
			}
		}
	}

	style element create PagerAdd.button image [list $K(pager_normal_bg) \
			{pressed !disabled} $K(pager_pressed_bg) \
			{active !disabled}  $K(pager_active_bg)] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerAdd.label image [list $K(pager_plus) \
			{pressed !disabled} $K(pager_plus_pressed)] -sticky news 		
			
			
	# ------Grip-------
	
	style layout VGrip {
		VGrip.background
		VGrip.button -children {
			VGrip.focus -children {
				VGrip.label
			}
		}
	}

	style element create VGrip.button image [list $K(gripbg) \
			{active !disabled}  $K(gripbg_active)] \
			-border {0 0 0 0} -padding {0 0 0 0} -sticky ns 
			
	style configure VGrip -image $K(vgrip)		
			
	style layout HGrip {
		HGrip.background
		HGrip.button -children {
			HGrip.focus -children {
				HGrip.label
			}
		}
	}

	style element create HGrip.button image [list $K(gripbg) \
			{active !disabled}  $K(gripbg_active)] \
			-border {0 0 0 0} -padding {0 0 0 0} -sticky ew 
			
	style configure HGrip -image $K(hgrip)			
			
			
			
			
			
			
			
			
			
			
			
			
			