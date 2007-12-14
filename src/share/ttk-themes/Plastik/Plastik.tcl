# Plastik.tcl - Pixmap & icon theme for sK1.
#
#  This theme is specialized and not recommended for general 
#  use with Tile & Tk
#
#  Copyright (c) 2004 Googie
#  Copyright (c) 2004 Pat Thoyts <patthoyts@users.sourceforge.net>
#  Copyright (c) 2006 Igor E. Novikov  <igor_n@users.sourceforge.net>


package require Tk 8.4;                 # minimum version for Tile

namespace eval ttk {
    namespace eval theme {
        namespace eval Plastik {
            variable version 0.4.0
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
   
	foreach file [glob -directory $imgdir *.xbm] {	    
	    set img [file tail [file rootname $file]]
	    if {![info exists B($img)]} {
		image create bitmap $img -file $file -foreground [.testEntry cget -background]
	    }
	}	
	
    namespace import -force ::ttk::style
	style theme create Plastik -parent alt -settings {
    
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
        style configure "." \
				-borderwidth 0 \
				-lighter #cccccc \
				-background [.testEntry cget -background] \
				-troughcolor [.testEntry cget -highlightbackground] \
				-selectbackground [.testEntry cget -selectbackground] \
				-selectforeground [.testEntry cget -selectforeground] \
				-font [.testNormalLabel cget -font] \
            ;

        style map . -foreground [list disabled [.testEntry cget -disabledforeground]]
	
	set styledir [file join [file dirname [info script]] styles]	

	source [file join $styledir frames.tcl]
	source [file join $styledir labels.tcl]
	source [file join $styledir entries.tcl]
	source [file join $styledir comboboxes.tcl]
	source [file join $styledir buttons.tcl]
	source [file join $styledir checkbuttons.tcl]
	source [file join $styledir radiobuttons.tcl]
	source [file join $styledir scrollbars.tcl]


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

