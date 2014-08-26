# Plastik.tcl - Pixmap & icon theme for sK1.
#
#  This theme is specialized and not recommended for general 
#  use with Ttk
#
#  Copyright (c) 2004 Googie
#  Copyright (c) 2004 Pat Thoyts <patthoyts@users.sourceforge.net>
#  Copyright (c) 2006 Igor E. Novikov  <igor.e.novikov@gmail.com>


package require Tk 8.5;                 # minimum version for Ttk

namespace eval ttk {
    namespace eval theme {
        namespace eval Plastik {
            variable version 0.4.0
        }
    }
}

namespace eval ttk::theme::Plastik {	
	
	global sk1_bg sk1_fg sk1_highlightbg sk1_highlightcolor
	global sk1_disabledfg sk1_selectbg sk1_selectfg
	global sk1_txtsmall sk1_txtnormal sk1_txtlarge

	set imgdir [file join [file dirname [info script]] widgets]

	foreach file [glob -directory $imgdir *.png] {
	    set img [file tail [file rootname $file]]
	    if {![info exists K($img)]} {
		set K($img) [image create photo -format "png" -file $file]
	    }
	}
	
	set maskdir [file join [file dirname [info script]] masks]
   
	foreach file [glob -directory $maskdir *.xbm] {	    
	    set img [file tail [file rootname $file]]
	    if {![info exists B($img)]} {
		image create bitmap $img -file $file -foreground $sk1_bg
	    }
		if {$img=="progress_bar_mask"} {
		image create bitmap $img -file $file -foreground $sk1_selectbg	
		}
	}
	
	
    namespace import -force ::ttk::style
	style theme create Plastik -parent alt -settings {
    
    	variable colors
	array set colors {
		-frame 	$sk1_selectbg
		-lighter      #cccccc
		-disabledfg	$sk1_disabledfg
		-selectbg	$sk1_selectbg
		-selectfg	$sk1_selectfg
	}

        style configure "." \
				-borderwidth 0 \
				-lighter #cccccc \
				-background $sk1_bg \
				-foreground $sk1_fg \
				-troughcolor $sk1_highlightbg \
				-selectbackground $sk1_selectbg \
				-selectforeground $sk1_selectfg \
				-font $sk1_txtnormal \
            ;

        style map . -foreground [list !disabled $sk1_fg disabled $sk1_disabledfg]
	
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

package provide ttk::theme::Plastik $::ttk::theme::Plastik::version

