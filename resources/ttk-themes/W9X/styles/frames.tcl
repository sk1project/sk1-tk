# ------------------------------------Frame-----------------------------------------------------
		style layout ToolBarFrame {
			ToolBarFrame.panel
			}  
		style configure ToolBarFrame -borderwidth 2 -relief flat
        style element create ToolBarFrame.panel image $K(menu_bg) -border {3 3 3 3} -sticky news

	# -------------	
	style layout MenuBarFrame {
			MenuBarFrame.panel -expand true
		} 
	style configure MenuBarFrame -relief flat   
        style element create MenuBarFrame.panel image $K(menu_bg) \
		 -border {3 3 3 4} -padding {3 3 3 4}
	
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
	
	style configure FlatFrame -borderwidth 2 -relief flat	
	
	# -------------
	style layout RoundedFrame {
		RoundedFrame.panel -expand true
		}
	
	style element create RoundedFrame.panel image $K(rounded_area) \
	-border {4 4 4 4} -padding {4 4 4 4} -sticky news
	
	style configure RoundedFrame -borderwidth 2 -relief flat	
	
	# -------------
	style configure TLabelframe -borderwidth 2 -relief groove -padding 5
	
	# -------------
	
	style layout PWinHead {
		PWinHead.panel
		}  
	style configure PWinHead -borderwidth 2 -relief flat
	style element create PWinHead.panel image $K(pluginwinheader) -border {4 2 4 2} -sticky news

	# -------------

	style layout PWinBody {
		PWinBody.panel
		}  
	style configure PWinBody -borderwidth 2 -relief flat
	style element create PWinBody.panel image $K(pluginwinbody) -border {2 2 2 2} -sticky news
	
	# -------------	
	
	style layout RoundedSBFrame {
		RoundedSBFrame.panel -expand true
		}
	
	style element create RoundedSBFrame.panel image $K(corner_normal) \
	-border {4 4 4 4} -padding {4 4 4 4} -sticky news
	
	style configure RoundedSBFrame -borderwidth 2 -relief flat		 
