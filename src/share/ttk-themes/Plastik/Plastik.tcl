# Plastik.tcl - Pixmap & icon theme for sK1.
#
#  This theme is specialized and not rcommended for general 
#  use with Tile & Tk
#
#  Copyright (c) 2004 Googie
#  Copyright (c) 2004 Pat Thoyts <patthoyts@users.sourceforge.net>
#  Copyright (c) 2006 Igor E. Novikov  <igor_n@users.sourceforge.net>


package require Tk 8.4;                 # minimum version for Tile
#package require tile 0.5;               # depends upon tile 0.5

namespace eval ttk {
    namespace eval theme {
        namespace eval Plastik {
            variable version 0.3.1
        }
    }
}

namespace eval ttk::theme::Plastik {

	set imgdir [file join [file dirname [info script]] widgets]

	foreach file [glob -directory $imgdir *.png] {
	    set img [file tail [file rootname $file]]
	    if {![info exists K($img)]} {
		set K($img) [image create photo -format "png" -file $file]
	    }
	}

	ttk::style theme create Plastik -parent alt -settings {
    
    	variable colors
	array set colors {
		-frame 	#EFEFEF
		-lighter      #cccccc
		-disabledfg	#AAAAAA
		-selectbg	#678DB2
		-selectfg	#FFFFFF
	}
	
#        array set colors {
#            -frame      "#EFEFEF"
#            -lighter    "#cccccc"
#            -window     "#EFEFEF"
#            -selectbg   "#eeeeee"
#            -selectfg   "#000000"
#            -disabledfg "#aaaaaa"
#        }

        # -----------------------------------------------------------------
        # Theme defaults  $colors(-frame)
        #
        style default . \
            -borderwidth 0 \
            -lighter #cccccc \
            -background [.testEntry cget -background] \
            -troughcolor [.testEntry cget -highlightbackground] \
	    -selectbackground [.testEntry cget -selectbackground] \
	    -selectforeground [.testEntry cget -selectforeground] \
            -font [.testNormalLabel cget -font] \
            ;

        style map . -foreground [list disabled [.testEntry cget -disabledforeground]]
	
# ------------------------------------Frame-----------------------------------------------------
	style layout ToolBarFrame {
		ToolBarFrame.panel
		}  
	style default ToolBarFrame -borderwidth 0 -relief flat
        style element create ToolBarFrame.panel image $K(menu_bg) -border {3 3 3 3} -sticky news

	# -------------	
	style layout MenuBarFrame {
		MenuBarFrame.border -children {
			TFrame
			}
		} 
	style default MenuBarFrame.frame -borderwidth 1 -relief raised   
        style element create MenuBarFrame.border image $K(menu_bg) \
		 -border {3 3 3 3} -padding {3 3 3 3} 
	
	# -------------	 
	style layout MFrame {
		MFrame.panel -expand true
		}
	
	style element create MFrame.panel image $K(menu_bg) \
	-border {3 3 3 3} -padding {3 3 3 3} -sticky news
	
	# -------------	 
		style layout FlatFrame {
		FlatFrame.panel -expand true
		}
	
	style default FlatFrame -borderwidth 2 -relief flat	
		
	# -------------
	style layout CanvasFrame {
		CanvasFrame.panel -expand true
		}
	
	style element create CanvasFrame.panel image $K(draw_area) \
	-border {5 5 5 5} -padding {3 3 3 3} -sticky news
	
	# -------------
	style layout RoundedFrame {
		RoundedFrame.panel -expand true
		}
	
	style element create RoundedFrame.panel image $K(rounded_area) \
	-border {4 4 4 4} -padding {4 4 4 4} -sticky news
	
	style default RoundedFrame -borderwidth 2 -relief flat	
	
	# -------------
	style default TLabelframe -borderwidth 2 -relief groove -padding 5
	
	# -------------
	style layout RoundedSBFrame {
		RoundedSBFrame.panel -expand true
		}
	
	style element create RoundedSBFrame.panel image $K(corner_normal) \
	-border {4 4 4 4} -padding {4 4 4 4} -sticky news
	
	style default RoundedSBFrame -borderwidth 2 -relief flat		
# ------------------------------------Label------------------------------------------------------
	
	style layout FlatLabel {
		FlatLabel.label
		}
	style default FlatLabel -borderwidth 4 -relief flat  

	style layout SmallFlatLabel {
		SmallFlatLabel.label
		}
	style default SmallFlatLabel -borderwidth 4 -relief flat -font [.testSmallLabel cget -font]	
	# -------------
	style layout ColorWatchNormal {
		ColorWatchNormal.background
		ColorWatchNormal.label
		ColorWatchNormal.mask
		}
	style default ColorWatchNormal -borderwidth 0 -relief flat 
	
	style element create ColorWatchNormal.mask image $K(color_watch) \
		-border {3 3 3 3} -padding {0 0 0 0} -sticky ew
		
	# -------------	
	style layout ColorWatchDisabled {
		ColorWatchDisabled.background
		ColorWatchDisabled.label
		ColorWatchDisabled.mask
		}
	style default ColorWatchDisabled -borderwidth 0 -relief flat 
	
	style element create ColorWatchDisabled.mask image $K(color_watch_disabled) \
		-border {3 3 3 3} -padding {0 0 0 0} -sticky ew
		
	# -------------	
	style layout ColorWatchTransp {
		ColorWatchTransp.background
		ColorWatchTransp.label
		ColorWatchTransp.field
		ColorWatchTransp.mask
		}
	style default ColorWatchTransp -borderwidth 0 -relief flat 
	
	style element create ColorWatchTransp.field image $K(transp_sign) \
		-border {0 0 0 0} -padding {0 0 0 0}
	
	style element create ColorWatchTransp.mask image $K(color_watch) \
		-border {3 3 3 3} -padding {0 0 0 0} -sticky ew
		
	# -------------
	style layout HLine {
		HLine.background -children {
			HLine.label
			}
		}
	style default HLine  -relief flat 
	
	style element create HLine.background image $K(hline) \
		-border {4 4 4 4} -padding {0 0 0 0} -sticky ew
		
	style element create HLine.label image $K(hline)
	
	# -------------
	style layout VLine2 {
		VLine2.background -children {
			VLine2.label
			}
		}
	style default VLine2  -relief flat 
	
	style element create VLine2.background image $K(vline2) \
		-border {2 2 2 2} -padding {0 0 0 0} -sticky ns
		
	style element create VLine2.label image $K(vline2)
	
	# -------------
	style layout PalLBorder {
		PalLBorder.background -children {
			PalLBorder.label
			}
		}
	style default PalLBorder  -relief flat 
	
	style element create PalLBorder.background image $K(pal_left_border) \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ns
		
	style element create PalLBorder.label image $K(pal_left_border)
	
	# -------------
	style layout PalRBorder {
		PalRBorder.background -children {
			PalRBorder.label
			}
		}
	style default PalRBorder  -relief flat 
	
	style element create PalRBorder.background image $K(pal_right_border) \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ns
		
	style element create PalRBorder.label image $K(pal_right_border)	
# ------------------------------------Tooltips Label-------------------------------------------

	style layout Tooltips {
		Tooltips.background -children {
			Tooltips.label
			}
		}
	style element create Tooltips.background image $K(tooltips_bg) \
		-border {1 1 1 1} -padding {4 4 4 4} -sticky news

# ------------------------------------Entry----------------------------------------------------
	style layout TEntry {
		TEntry.border -children {
			RegularEntry.textarea
		}
	}		
	style element create TEntry.border image $K(entry_normal) \
		-border {5 3 3 3} -padding {4 5 3 3} -sticky ew \
		-map [list disabled $K(entry_disabled) \
			readonly $K(entry_disabled) \
                        active $K(entry_focusin)]
			
	# --------------------------
	style layout SpinEntry {
		SpinEntry.border -children {
			RegularEntry.textarea
		}
	}		
	style element create SpinEntry.border image $K(spin_entry_normal) \
		-border {5 3 3 3} -padding {4 5 3 3} -sticky ew \
		-map [list disabled $K(spin_entry_disabled) \
			readonly $K(spin_entry_disabled) \
                        active $K(spin_entry_focusin)]

# ------------------------------------ComboBox---------------------------------------------------- 
# Group options -side, -sticky, -expand, -border, -unit, or -children

	style layout ComboNormal {
		ComboNormal.field -sticky ew
		ComboNormal.downarrow -side right
		ComboNormal.padding -children {
			ComboNormal.textarea -sticky ew
		}				
	}		

	style element create ComboNormal.padding image $K(spin_entry_normal) \
		-border {5 3 3 3} -padding {4 5 8 3} -sticky ew \
		-map [list disabled $K(spin_entry_disabled) \
			readonly $K(spin_entry_normal) \
                        active $K(spin_entry_focusin)]

        style element create ComboNormal.downarrow image $K(combo_button_normal) \
		-border {3 3 3 3} -padding {1 1 1 1} -sticky e \
		-map [list {pressed !disabled} $K(combo_button_normal) \
                      {active !disabled}  $K(combo_button_active) \
                      disabled $K(combo_button_disabled)]

	style default ComboNormal -borderwidth 0 -padding {3 3 3 3} -insertwidth 0 -cursor arrow -ipady 0
# ------------------------------------Button----------------------------------------------------
        style layout TButton {
            Button.background
            Button.button -children {
                Button.focus -children {
                    Button.label
                }
            }
        }
        style element create button image $K(button) \
            -border {3 3 3 3} -padding {15 3 15 3} -sticky news \
            -map [list {pressed !disabled} $K(button_pressed) \
                      {active !disabled}  $K(button_active) \
                      disabled $K(button_disabled)]		      
        style default TButton -padding {10 6}	
	
	#----------------------
        style layout Pal2TopButton {
            Pal2TopButton.background
            Pal2TopButton.button -children {
                Pal2TopButton.focus -children {
                    Pal2TopButton.label
                }
            }
        }
        style element create Pal2TopButton.button image $K(pal_top_dbl_normal) \
            -border {3 3 3 3} -padding {3 3 3 3} -sticky news \
            -map [list {pressed !disabled} $K(pal_top_dbl_pressed) \
                      {active !disabled}  $K(pal_top_dbl_normal) \
                      disabled $K(pal_top_dbl_disabled)]		      
        style default Pal2TopButton -padding {3 3}	
	
	#----------------------
        style layout PalTopButton {
            PalTopButton.background
            PalTopButton.button -children {
                PalTopButton.focus -children {
                    PalTopButton.label
                }
            }
        }

        style element create PalTopButton.button image $K(pal_top_normal) \
            -border {3 3 3 3} -padding {3 3 3 3} -sticky news \
            -map [list {pressed !disabled} $K(pal_top_pressed) \
                      {active !disabled}  $K(pal_top_normal) \
                      disabled $K(pal_top_disabled)]
		      
        style default PalTopButton -padding {3 3}	
	#----------------------
        style layout PalBottomButton {
            PalBottomButton.background
            PalBottomButton.button -children {
                PalBottomButton.focus -children {
                    PalBottomButton.label
                }
            }
        }

        style element create PalBottomButton.button image $K(pal_bot_normal) \
            -border {3 3 3 3} -padding {3 3 3 3} -sticky news \
            -map [list {pressed !disabled} $K(pal_bot_pressed) \
                      {active !disabled}  $K(pal_bot_normal) \
                      disabled $K(pal_bot_disabled)]
		      
        style default PalBottomButton -padding {3 3}
	#----------------------
        style layout Pal2BottomButton {
            Pal2BottomButton.background
            Pal2BottomButton.button -children {
                Pal2BottomButton.focus -children {
                    Pal2BottomButton.label
                }
            }
        }

        style element create Pal2BottomButton.button image $K(pal_bot_dbl_normal) \
            -border {3 3 3 3} -padding {3 3 3 3} -sticky news \
            -map [list {pressed !disabled} $K(pal_bot_dbl_pressed) \
                      {active !disabled}  $K(pal_bot_dbl_normal) \
                      disabled $K(pal_bot_dbl_disabled)]
		      
        style default Pal2BottomButton -padding {3 3}	
	
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
		      
        style default PalNoColorButton 

	#----------------------
        style layout SpinUpButton {
            SpinUpButton.background
            SpinUpButton.button -children {
                SpinUpButton.focus -children {
                    SpinUpButton.label
                }
            }
        }

        style element create SpinUpButton.button image $K(spin_upbut_normal) \
            -border {2 2 2 2} -padding {2 2 2 2} -sticky news \
            -map [list {pressed !disabled} $K(spin_upbut_pressed) \
                      {active !disabled}  $K(spin_upbut_active) \
                      disabled $K(spin_upbut_disabled)]		      
        style default SpinUpButton -padding {2 2}	

	#----------------------
        style layout SpinDownButton {
            SpinDownButton.background
            SpinDownButton.button -children {
                SpinDownButton.focus -children {
                    SpinDownButton.label
                }
            }
        }

        style element create SpinDownButton.button image $K(spin_downbut_normal) \
            -border {2 2 2 2} -padding {2 2 2 2} -sticky news \
            -map [list {pressed !disabled} $K(spin_downbut_pressed) \
                      {active !disabled}  $K(spin_downbut_active) \
                      disabled $K(spin_downbut_disabled)]      
        style default SpinDownButton -padding {2 2}
			
# ------------------------------------Corner----------------------------------------------------
        style layout TCornerButton {
            Button.background
            CornerButton.button -children {
                Button.focus -children {
                    Button.label
                }
            }
        }

        style element create CornerButton.button image $K(corner_normal) \
            -border {2 2 2 2} -padding {1 1 1 1} -sticky news \
            -map [list {pressed !disabled} $K(corner_pressed) \
                      {active !disabled}  $K(corner_active)]
# ---------------------------------------------------------------------------------------------------
	
        style layout Toolbutton {
            Toolbutton.button -children {
	    	Toolbutton.focus -children {
                    Toolbutton.label
		}    
            }
        }

        style element create Toolbutton.button image $K(toolbutton_normal) \
            -border {2 2 2 2} \
	    -padding {3 3 3 3} \
            -map [list {pressed !disabled} $K(toolbutton_pressed) \
                      {active  !disabled}   $K(toolbutton_over) ] 
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

        style element create ToolsButton.button image $K(tools_normal) \
            -border {2 2 2 2} \
	    -padding {3 3 3 3} \
	    -width 33 -height 33 \
            -map [list {pressed !disabled} $K(tools_button_pressed) \
                      {active  !disabled}   $K(tools_active)] 
		      
# ------------------------------------Checkbutton---------------------------------------------------
        style element create Checkbutton.indicator image $K(check_no_normal) \
            -width 20 -sticky w \
            -map [list   {!active  !disabled !selected} $K(check_no_normal) \
	    		{!active  !disabled selected} $K(check_yes_normal) \
			{active  !disabled selected} $K(check_yes_active) \
			{active  !disabled !selected} $K(check_no_active) \
			{disabled selected} $K(check_yes_disabled) \
			{disabled !selected} $K(check_no_disabled) ]
# ------------------------------------------------------------------------------------------------------ 
# -------------------------------------Radiobutton---------------------------------------------------
        style element create Radiobutton.indicator image $K(radio_no_normal) \
            -width 20 -sticky w \
            -map [list  {!active  !disabled !selected} $K(radio_no_normal) \
	    		{!active  !disabled selected} $K(radio_yes_normal) \
			{active  !disabled selected} $K(radio_yes_active) \
			{active  !disabled !selected} $K(radio_no_active) \
			{disabled selected} $K(radio_yes_disabled) \
			{disabled !selected} $K(radio_no_disabled) ]

# ----------------------------------FineRadiobutton-------------------------------------------- 			
        style layout FineRadiobutton {
            FineRadiobutton.indicator -children {
	    	FineRadiobutton.focus -children {
                   FineRadiobutton.label
		}    
            }
        }			
        style element create FineRadiobutton.indicator image $K(fine_normal) \
            -border {2 2 2 2} \
	    -padding {3 3 3 3} \
	    -width 33 -height 33 \
            -map [list  {!active  !disabled !selected} $K(fine_normal) \
	    		{!active  !disabled selected} $K(fine_selected) \
			{active  !disabled selected} $K(fine_selected) \
			{active  !disabled !selected} $K(fine_active) \
			{disabled selected} $K(fine_selected) \
			{disabled !selected} $K(fine_normal) ]			
# ------------------------------------------------------------------------------------------------------- 
        # The layout for the menubutton is modified to have a button element
        # drawn on top of the background. This means we can have transparent
        # pixels in the button element. Also, the pixmap has a special
        # region on the right for the arrow. So we draw the indicator as a
        # sibling element to the button, and draw it after (ie on top of) the
        # button image.
#        style layout TMenubutton {
#            Menubutton.background
#           Menubutton.button -children {
#                Menubutton.focus -children {
#                    Menubutton.padding -children {
#                        Menubutton.label -side left -expand true
#                    }
#                }
#            }
#            Menubutton.indicator -side right
#        }
#        style element create Menubutton.button image $I(mbut-n) \
#            -map [list {active !disabled} $I(mbut-a) \
#                      {pressed !disabled} $I(mbut-a) \
#                      {disabled}          $I(mbut-d)] \
#            -border {7 10 29 15} -padding {7 4 29 4} -sticky news
#        style element create Menubutton.indicator image $I(mbut-arrow-n) \
#            -width 11 -sticky w -padding {0 0 18 0}
	    
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
	
	style default TRootMenubutton -relief flat -sticky ew -side left
	style default TRootMenubutton.background -relief flat -sticky ew -side left
        style element create TRootMenubutton.button image $K(menubutton_normal) \
	    -border {4 6 4 3} -sticky ew \
            -map [list pressed $K(menubutton_pressed) \
	    active $K(menubutton_active) \
	    disabled $K(menubutton_normal)]

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
	
	style default TComboSmall -relief flat -sticky ew -side left
        style element create TComboSmall.button image $K(combo_normal) \
	    -border {4 2 20 2} -padding {4 2 20 2} -sticky ew \
            -map [list pressed $K(combo_active) \
	    active $K(combo_active) \
	    disabled $K(combo_disabled)]           

# -------------------------------------Scrollbars----------------------------------------------------- 
        style layout Vertical.TScrollbar {
            Scrollbar.vscrollbg -children {
		Scrollbar.uparrow -side top 
                Scrollbar.downarrow -side bottom
                Scrollbar.uparrow -side bottom
                Vertical.Scrollbar.thumb -side top -expand true -sticky ns  -children {
			Vertical.Scrollbar.label -expand true -sticky we
		}
            }
        }

        style layout Horizontal.TScrollbar { 
	    Scrollbar.hscrollbg -children {
                Scrollbar.leftarrow -side left
                Scrollbar.rightarrow -side right
                Scrollbar.leftarrow -side right
		Horizontal.Scrollbar.thumb -side left -expand true -sticky we -children {
			Horizontal.Scrollbar.label -expand true -sticky ns
		}
            }
        }

        style default TScrollbar -width 16 
# -------------------------------------Vertical.Scrollbar Definition-------------------------------------------------   
        style element create Vertical.Scrollbar.thumb image $K(vscroll_thumb) \
            -border {3 6 3 6} -width 16 -height 22 -sticky news \
            -map [list {pressed !disabled} $K(vscroll_thumb_pressed)]

        style element create vscrollbg image $K(clear)
	
	style element create Vertical.Scrollbar.label  image $K(vscroll_grave) 
	
        style element create uparrow image $K(vscroll_up_arrow) \
            -map [list {pressed !disabled} $K(vscroll_up_arrow_pressed)]     

        style element create downarrow image $K(vscroll_down_arrow) \
            -map [list {pressed !disabled} $K(vscroll_down_arrow_pressed)]

# -----------------------------------------------Horizontal.Scrollbar Definition--------------------------------------
        style element create hscrollbg image $K(clear)  

	style element create Horizontal.Scrollbar.thumb image $K(hscroll_thumb) \
            -border {6 3 6 3} -width 22 -height 16 -sticky news \
            -map [list {pressed !disabled} $K(hscroll_thumb_pressed)]
	    
	style element create Horizontal.Scrollbar.label  image $K(hscroll_grave) 

        style element create rightarrow image $K(hscroll_right_arrow) \
            -map [list {pressed !disabled} $K(hscroll_right_arrow_pressed)]	    

        style element create leftarrow image $K(hscroll_left_arrow) \
            -map [list {pressed !disabled} $K(hscroll_left_arrow_pressed)]
       
# ---------------------------------------------------------------------------------------------------------------------------------	    
	    
       
#        style element create Scale.slider image $I(hslider-n) -border 3
        
#        style element create Vertical.Scale.slider image $I(vslider-n) -border 3
        
#        style element create Horizontal.Progress.bar image $I(hsb-n) \
#            -border {6 4}  -sticky news
        
#        style element create Vertical.Progress.bar image $I(vsb-n) \
#            -border {4 6}
        
        
        # -----------------------------------------------------------------
        # Notebook elements
        #
#        style element create tab image $I(tab-n) \
#            -map [list selected $I(tab-p) active $I(tab-p)] \
#            -border {6 6 6 2} -height 12

    }
}

package provide ttk::theme::Plastik $::ttk::theme::Plastik::version

