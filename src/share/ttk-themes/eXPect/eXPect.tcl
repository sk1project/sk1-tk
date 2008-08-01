# eXPect.tcl - Pixmap & icon theme for sK1.
#
#  This theme is specialized and not recommended for general 
#  use with Ttk
#
#  Copyright (c) 2008 Igor E. Novikov  <igor.e.novikov@gmail.com>


package require Tk 8.4;                 # minimum version for Ttk

namespace eval ttk {
    namespace eval theme {
        namespace eval eXPect {
            variable version 0.4.0
        }
    }
}

namespace eval ttk::theme::eXPect {

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
		if {$img=="progress_bar_mask"} {
		image create bitmap $img -file $file -foreground [.testEntry cget -selectbackground]	
		}
	}
	
	
    namespace import -force ::ttk::style
	style theme create eXPect -parent alt -settings {
    
    	variable colors
	array set colors {
		-frame 	#EFEFEF
		-lighter      #cccccc
		-disabledfg	#AAAAAA
		-selectbg	#678DB2
		-selectfg	#FFFFFF
	}

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
	source [file join $styledir progressbar.tcl]
	source [file join $styledir notebook.tcl]

    }
}

package provide ttk::theme::eXPect $::ttk::theme::eXPect::version

