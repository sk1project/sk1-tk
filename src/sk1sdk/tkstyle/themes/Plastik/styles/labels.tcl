# ------------------------------------Label------------------------------------------------------
	
	style layout FlatLabel {
		FlatLabel.label
		}
	style configure FlatLabel -borderwidth 4 -relief flat  

	style layout SmallFlatLabel {
		SmallFlatLabel.label
		}
	style configure SmallFlatLabel -borderwidth 4 -relief flat -font $sk1_txtsmall	
	
	# -------------ColorWatch total==14x40 px inside==12x38 px
	style layout ColorWatchNormal {
		ColorWatchNormal.background
		ColorWatchNormal.mask -children {
				ColorWatchNormal.label	
		}
		}
	style configure ColorWatchNormal -borderwidth 0 -relief flat -height 14 
	
	style element create ColorWatchNormal.mask image "color_watch" \
		-border {1 1 1 1} -padding {1 1 1 1} -sticky ew -height 12 
		
	# -------------	
	style layout ColorWatchDisabled {
		ColorWatchDisabled.background
		ColorWatchDisabled.label
		ColorWatchDisabled.mask
		}
	style configure ColorWatchDisabled -borderwidth 0 -relief flat -height 14 
	
	style element create ColorWatchDisabled.mask image "color_watch_disabled" \
		-border {1 1 1 1} -padding {1 1 1 1} -sticky ew -height 14
		
	# -------------	
	style layout ColorWatchTransp {
		ColorWatchTransp.background
		ColorWatchTransp.mask -children {
				ColorWatchTransp.label
				ColorWatchTransp.field		
		}
		}
	style configure ColorWatchTransp -borderwidth 0 -relief flat -height 14
	
	style element create ColorWatchTransp.field image "transp_sign" \
		-border {0 0 0 0} -padding {0 0 0 0} -height 12 
	
	style element create ColorWatchTransp.mask image "color_watch" \
		-border {1 1 1 1} -padding {1 1 1 1} -sticky ew -height 14
		
	# -------------
	style layout HLine {
		HLine.background -children {
			HLine.label
			}
		}
	style configure HLine  -relief flat 
	
	style element create HLine.background image "hline" \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ew
	
	# -------------
	style layout HLine2 {
		HLine2.background -children {
			HLine2.label
			}
		}
	style configure HLine2 -relief flat
	
	style element create HLine2.background image "hline2" \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ew
	
	# -------------
	style layout VLine2 {
		VLine2.background -children {
			VLine2.label
			}
		}
	style configure VLine2  -relief flat
	
	style element create VLine2.background image "vline2" \
		-border {1 1 1 1} -padding {0 0 0 0} -sticky ns
	
	# -------------
	style layout VLine3 {
		VLine3.background -children {
			VLine3.label
			}
		}
	style configure VLine3  -relief flat 
	
	style element create VLine3.background image "vline3" \
		-border {1 1 1 1} -padding {0 0 0 0} -sticky ns
	
	# -------------
	style layout DrawingAreaTop {
		DrawingAreaTop.background -children {
			DrawingAreaTop.label
			}
		}
	style configure DrawingAreaTop  -relief flat 
	
	style element create DrawingAreaTop.background image "draw_area_top" \
		-border {5 5 5 5} -padding {0 0 0 0} -sticky ew
	
	# -------------
	style layout DrawingAreaBottom {
		DrawingAreaBottom.background -children {
			DrawingAreaBottom.label
			}
		}
	style configure DrawingAreaBottom  -relief flat 
	
	style element create DrawingAreaBottom.background image "draw_area_bottom" \
		-border {5 5 5 5} -padding {0 0 0 0} -sticky ew
	
	# -------------
	style layout DrawingAreaLeft {
		DrawingAreaLeft.background -children {
			DrawingAreaLeft.label
			}
		}
	style configure DrawingAreaLeft  -relief flat 
	
	style element create DrawingAreaLeft.background image "draw_area_left" \
		-border {5 5 5 5} -padding {0 0 0 0} -sticky ns
	
	# -------------
	style layout DrawingAreaRight {
		DrawingAreaRight.background -children {
			DrawingAreaRight.label
			}
		}
	style configure DrawingAreaRight  -relief flat 
	
	style element create DrawingAreaRight.background image "draw_area_right" \
		-border {5 5 5 5} -padding {0 0 0 0} -sticky ns
	
	# -------------
	style layout PalLBorder {
		PalLBorder.background -children {
			PalLBorder.label
			}
		}
	style configure PalLBorder  -relief flat 
	
	style element create PalLBorder.background image "pal_left_border" \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ns
		
	style element create PalLBorder.label image "pal_left_border"
	
	# -------------
	style layout PalRBorder {
		PalRBorder.background -children {
			PalRBorder.label
			}
		}
	style configure PalRBorder  -relief flat 
	
	style element create PalRBorder.background image "pal_right_border" \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ns
		
	style element create PalRBorder.label image "pal_right_border"	
	
	# -------------
	style layout PWLabel {
		PWLabel.background -children {
			PWLabel.label
			}
		}
	style configure PWLabel -relief flat
	
	style element create PWLabel.background image "pw_but_normal" \
		-border {0 0 0 0} -padding {0 0 0 0} -sticky ew
# ------------------------------------Tooltips Label-------------------------------------------

	style layout Tooltips {
		Tooltips.background -children {
			Tooltips.label
			}
		}
	style element create Tooltips.background image "tooltips_bg" \
		-border {1 1 1 1} -padding {4 1 4 1} -sticky news
# ------------------------------------DocTabs--------------------------------------------------
		
	# ------DocTabsLeft-------
	style layout DocTabsLeft {
		DocTabsLeft.background -children {
			DocTabsLeft.label
			}
		}
	style configure DocTabsLeft  -relief flat 
	
	style element create DocTabsLeft.background image "doctabs_left" \
		-border {4 4 1 2} -padding {1 1 1 1} -sticky ew		
		
	# ------DocTabsLeftActive-------
	style layout DocTabsLeftActive {
		DocTabsLeftActive.background -children {
			DocTabsLeftActive.label
			}
		}
	style configure DocTabsLeftActive  -relief flat 
	
	style element create DocTabsLeftActive.background image "doctabs_left_active" \
		-border {4 4 1 2} -padding {1 1 1 1} -sticky ew	
		
	# ------DocTabsRight-------
	style layout DocTabsRight {
		DocTabsRight.background -children {
			DocTabsRight.label
			}
		}
	style configure DocTabsRight  -relief flat 
	
	style element create DocTabsRight.background image "doctabs_right" \
		-border {1 4 4 2} -padding {1 1 1 1} -sticky ew	
		
		
#########################################################################	
		

		