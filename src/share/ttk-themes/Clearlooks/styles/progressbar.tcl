#----------------------Horizontal Progress bar-----------------children {fg}
style layout Horizontal.Progress {
	Horizontal.Progressbar.trough -children {
		Horizontal.Progress.pbar -children {fg} 
	}
}



style element create Horizontal.Progressbar.trough image $K(progress_bg) -border {1 1 2 1}

style element create fg image $K(progress_bar)\
			-border {0 0}  -sticky news
style element create Horizontal.Progress.pbar image "progress_bar_mask"\
            -border {0 0}  -sticky news
			