#----------------------Horizontal Progress bar-----------------children {fg}
style layout Horizontal.Progress {
	Horizontal.Progressbar.trough -children {
		Horizontal.Progress.pbar -children {fg} 
	}
}



style element create Horizontal.Progressbar.trough image "progress_bg" -border 2

style element create fg image "progress_bar"\
			-border {2 2}  -sticky news
style element create Horizontal.Progress.pbar image "progress_bar_mask"\
            -border {0 0}  -sticky news
			