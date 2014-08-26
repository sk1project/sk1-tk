# ------------------------------------Button----------------------------------------------------
        style layout TButton {
            TButton.background
            TButton.button -children {
		TButton.active_frame -children {
                TButton.focus -children {
                    TButton.space -children {
                        TButton.label -sticky ns
                    }
                }
		}
            }
        }
        style element create TButton.button image [list "button_normal" \
				{pressed !disabled} "button_pressed" \
				disabled "button_disabled" ] \
				-border {3 11} -padding {0 0 0 0} -sticky news
				
	style element create TButton.active_frame image [list "button_clear" \
				{active !disabled !pressed}  "button_active" ] \
				-border {3 11} -padding {3 3 3 3} -sticky news
				
	style element create TButton.space image "clear" \
				-border {1 1} -padding {12 1 12 1} -sticky news							
	
	#----------------------
        style layout Pal2TopButton {
            Pal2TopButton.background
            Pal2TopButton.button -children {
                Pal2TopButton.focus -children {
                    Pal2TopButton.label -sticky ns
                }
            }
        }
        style element create Pal2TopButton.button image [list "pal_top_dbl_normal" \
				{pressed !disabled} "pal_top_dbl_pressed" \
				{active !disabled}  "pal_top_dbl_normal" \
				disabled "pal_top_dbl_disabled"] \
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

        style element create PalTopButton.button image [list "pal_top_normal" \
				{pressed !disabled} "pal_top_pressed" \
				{active !disabled}  "pal_top_normal" \
				disabled "pal_top_disabled"] \
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

        style element create PalBottomButton.button image [list "pal_bot_normal" \
				{pressed !disabled} "pal_bot_pressed" \
				{active !disabled}  "pal_bot_normal" \
				disabled "pal_bot_disabled"] \
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

        style element create Pal2BottomButton.button image [list "pal_bot_dbl_normal" \
				{pressed !disabled} "pal_bot_dbl_pressed" \
				{active !disabled}  "pal_bot_dbl_normal" \
				disabled "pal_bot_dbl_disabled"] \
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

        style element create PalNoColorButton.button image "clear" \
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

        style element create SpinUpButton.button image [list "spin_upbut_normal" \
				{pressed !disabled} "spin_upbut_pressed" \
				disabled "spin_upbut_disabled"] \
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

        style element create SpinDownButton.button image [list "spin_downbut_normal" \
				{pressed !disabled} "spin_downbut_pressed" \
				disabled "spin_downbut_disabled"] \
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

        style element create CornerButton.button image [list "corner_normal" \
				{pressed !disabled} "corner_pressed" \
				{active !disabled}  "corner_active"] \
				-border {2 2 2 2} -padding {1 1 1 1} -sticky news 

# ---------------------------------------------------------------------------------------------------
	
        style layout Toolbutton {
            Toolbutton.button -children {
	    	Toolbutton.focus -children {
                    Toolbutton.label -sticky ns
		}    
            }
        }

        style element create Toolbutton.button image [list "toolbutton_normal" \
				{pressed !disabled} "toolbutton_pressed" \
				{active  !disabled}   "toolbutton_over" ] \
				-border {2 2 2 2} \
				-padding {3 3 3 3}  -sticky news

# ---------------------------------------------------------------------------------------------------
		style layout TSmallbutton {
			TSmallbutton.background
			TSmallbutton.button -expand true -sticky news -children {
				TSmallbutton.focus -children {
					TSmallbutton.label -sticky ns
				}
			}
		}
        style element create TSmallbutton.button image [list "clear" \
				{pressed !disabled} "button_pressed" \
				{active  !disabled}   "button_normal" ] \
				-border {2 2 2 2} \
				-padding {2 2 2 2} -sticky news

# ---------------------------------------------------------------------------------------------------
	
        style layout TextButton {
            TextButton.background
            TextButton.button -children {
                TextButton.focus -children {
                    TextButton.label
                }
            }
        }
        style element create TextButton.button image [list "button_clear" \
				{pressed !disabled} "button_pressed" \
				{active !disabled}  "button_normal" \
				disabled "button_clear"] \
				-border {3 11} -padding {5 3 5 3} -sticky news
			
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolCheckbutton {
            ToolCheckbutton.button -children {
	    	ToolCheckbutton.focus -children {
                    ToolCheckbutton.label -sticky ns
		}
            }
        }

        style element create ToolCheckbutton.button image "tools_pressed" \
            -border {2 2 2 2} -padding {3 3 3 3}
	    
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolbarCheckbutton {
            ToolbarCheckbutton.button -children {
	    	ToolbarCheckbutton.focus -children {
                    ToolbarCheckbutton.label -sticky ns
		}
            }
        }

        style element create ToolbarCheckbutton.button image "toolbutton_selected" \
            -border {2 2 2 2} -padding {3 3 3 3} 
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolsButton {
            ToolsButton.button -children {
	    	ToolsButton.focus -children {
                    ToolsButton.label -sticky ns
		}    
            }
        }

        style element create ToolsButton.button image [list "tools_normal" \
				{pressed !disabled} "tools_button_pressed" \
				{active  !disabled}   "tools_active"]\
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 33 -height 33
				
# ---------------------------------------------------------------------------------------------------
	
		style layout ColorButton {
			ColorButton.button -children {
			ColorButton.focus -children {
					ColorButton.label -sticky ns
		}    
			}
		}

		style element create ColorButton.button image [list "tools_active" \
				{pressed !disabled} "tools_button_pressed" \
				{active  !disabled}   "tools_active"]\
				-border {2 2 2 2} \
				-padding {2 2 2 2} \
				-width 47 -height 20
				
# ---------------------------------------------------------------------------------------------------
	
        style layout ToolBarCheckButton {
            ToolBarCheckButton.button -children {
	    	ToolBarCheckButton.focus -children {
                    ToolBarCheckButton.label -sticky ns
		}    
            }
        }

        style element create ToolBarCheckButton.button image [list "tools_normal" \
				{pressed !disabled} "tools_button_pressed" \
				{selected} "toolbutton_selected" \
				{active  !disabled}   "tools_active"]\
				-border {2 2 2 2} \
				-padding {3 3 3 3} \
				-width 28 -height 28	 

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
        style element create TComboSmall.button image [list "combo_normal"  \
				pressed "combo_active" \
				active "combo_active" \
				disabled "combo_disabled"] \
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
	
	style element create DocTabNormal.button image [list "doctabs_tab" \
					{pressed !disabled} "doctabs_tab_selected" \
					{active !disabled}  "doctabs_tab_selected"] \
		-border {1 5 2 4} -padding {5 5 5 4} -sticky ew	
		
	# ------DocTabActive-------
	style layout DocTabActive {
		DocTabActive.button -children {
			DocTabActive.label -side left
			DocTabActive.text -side left
			}
		}
	style configure DocTabActive  -relief flat 
	
	style element create DocTabActive.button image "doctabs_tab_active" \
		-border {2 3 3 2} -padding {5 3 5 2} -sticky ew	
				
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

	style element create PagerHome.button image [list "pager_normal_bg" \
			{pressed !disabled} "pager_pressed_bg" \
			{active !disabled}  "pager_active_bg"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerHome.label image [list "pager_home_arrow" \
			{pressed !disabled} "pager_home_arrow_pressed"] -sticky news 

	# ------END-------
	style layout PagerEnd {
		PagerEnd.background
		PagerEnd.button -children {
			PagerEnd.focus -children {
				PagerEnd.label -sticky ns
			}
		}
	}

	style element create PagerEnd.button image [list "pager_normal_bg" \
			{pressed !disabled} "pager_pressed_bg" \
			{active !disabled}  "pager_active_bg"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerEnd.label image [list "pager_end_arrow" \
			{pressed !disabled} "pager_end_arrow_pressed"] -sticky news 
	
	# ------PREVIOUS-------
	style layout PagerPrevious {
		PagerPrevious.background
		PagerPrevious.button -children {
			PagerPrevious.focus -children {
				PagerPrevious.label -sticky ns
			}
		}
	}

	style element create PagerPrevious.button image [list "pager_normal_bg" \
			{pressed !disabled} "pager_pressed_bg" \
			{active !disabled}  "pager_active_bg"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerPrevious.label image [list "pager_previous_arrow" \
			{pressed !disabled} "pager_previous_arrow_pressed"] -sticky news  
			
	# ------NEXT-------
	style layout PagerNext {
		PagerNext.background
		PagerNext.button -children {
			PagerNext.focus -children {
				PagerNext.label -sticky ns
			}
		}
	}

	style element create PagerNext.button image [list "pager_normal_bg" \
			{pressed !disabled} "pager_pressed_bg" \
			{active !disabled}  "pager_active_bg"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerNext.label image [list "pager_next_arrow" \
			{pressed !disabled} "pager_next_arrow_pressed"] -sticky news 
			
	# ------ADD-------
	style layout PagerAdd {
		PagerAdd.background
		PagerAdd.button -children {
			PagerAdd.focus -children {
				PagerAdd.label -sticky ns
			}
		}
	}

	style element create PagerAdd.button image [list "pager_normal_bg" \
			{pressed !disabled} "pager_pressed_bg" \
			{active !disabled}  "pager_active_bg"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news 
			
	style element create PagerAdd.label image [list "pager_plus" \
			{pressed !disabled} "pager_plus_pressed"] -sticky news 		
			
# ------Grip-------
	
	style layout VGrip {
		VGrip.background
		VGrip.button -children {
			VGrip.focus -children {
				VGrip.label
			}
		}
	}

	style element create VGrip.button image [list "gripbg" \
			{active !disabled}  "gripbg_active"] \
			-border {0 0 0 0} -padding {0 0 0 0} -sticky ns 
			
	style configure VGrip -image "vgrip"		
			
	style layout HGrip {
		HGrip.background
		HGrip.button -children {
			HGrip.focus -children {
				HGrip.label -sticky ns
			}
		}
	}

	style element create HGrip.button image [list "gripbg" \
			{active !disabled}  "gripbg_active"] \
			-border {0 0 0 0} -padding {0 0 0 0} -sticky ew 
			
	style configure HGrip -image "hgrip"	
	
# ------PM But-------
	
			style layout PWButton {
				PWButton.background
				PWButton.button -children {
						PWButton.label
				}
			}
			
	style element create PWButton.button image [list "pw_but_normal" \
			{pressed !disabled} "pw_but_pressed" \
			{active !disabled}  "pw_but_active" \
			disabled "pw_but_normal"] \
			-border {2 2 2 2} -padding {2 2 2 2} -sticky news

# ------Menu Button-------	
        style layout RootMenuButton {
            RootMenuButton.background
            RootMenuButton.button -children {
                    RootMenuButton.label -sticky ns
		}
        }
        style element create RootMenuButton.button image [list "menu_button_normal" \
				{pressed !disabled} "menu_button_pressed" \
				{active !disabled}  "menu_button_active" \
				disabled "menu_button_normal"] \
				-border {3 9 3 9} -padding {6 3 6 3} -sticky news

        style layout RootMenuButtonPressed {
            RootMenuButtonPressed.background
            RootMenuButtonPressed.button -children {
                    RootMenuButtonPressed.label -sticky ns
		}
        }
        style element create RootMenuButtonPressed.button image [list "menu_button_pressed" \
				{pressed !disabled} "menu_button_pressed" \
				{active !disabled}  "menu_button_pressed" \
				disabled "menu_button_normal"] \
				-border {3 9 3 9} -padding {6 3 6 3} -sticky news
			
			
			
			
			
			
			
			