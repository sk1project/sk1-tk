namespace eval ::desktop_integration {

	proc launch_dialog {} {
		global execline
		global fileId
		global answer		

		set fileId [open "|${execline} 2>/dev/null" r] 
		
		fileevent $fileId readable {
			if { [gets $fileId line] < 0 } {
				if [catch {close $fileId}] {
					#If the user pressed Cancel we get here
					set answer ""
					unset -nocomplain fileId 
				} else {
					set answer $temp
					unset -nocomplain fileId temp
				}
			} else {
				append temp $line
			}
		} 
		
		tkwait variable answer
		return $answer
	}
}