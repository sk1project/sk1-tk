#
#	X specific stuff
#

from sk1 import x11const

ShiftMask = x11const.ShiftMask
LockMask = x11const.LockMask
ControlMask = x11const.ControlMask
Mod1Mask = x11const.Mod1Mask
Mod2Mask = x11const.Mod2Mask
Mod3Mask = x11const.Mod3Mask
Mod4Mask = x11const.Mod4Mask
Mod5Mask = x11const.Mod5Mask
MetaMask = Mod1Mask

Button1Mask = x11const.Button1Mask
Button2Mask = x11const.Button2Mask
Button3Mask = x11const.Button3Mask
Button4Mask = x11const.Button4Mask
Button5Mask = x11const.Button5Mask
AllButtonsMask = Button1Mask | Button2Mask | Button3Mask

Button1 = x11const.Button1
Button2 = x11const.Button2
Button3 = x11const.Button3
Button4 = x11const.Button4
Button5 = x11const.Button5

ContextButton	 = Button3
ContextButtonMask = Button3Mask

AllowedModifierMask = ShiftMask | ControlMask | MetaMask
ConstraintMask = ControlMask
AlternateMask = ShiftMask

AddSelectionMask = ShiftMask
SubtractSelectionMask = MetaMask

SubobjectSelectionMask = ControlMask

# cursors

CurStd		 = 'top_left_arrow'# is replaced by custom cursor in uimanager
CurHandle	 = 'crosshair'# is replaced by custom cursor in uimanager
CurPick		 = 'hand2'# is replaced by custom cursor in uimanager
CurMove		 = 'hand2'# is replaced by custom cursor in uimanager
#---------Tool cursors-------------
CurCreate	 = 'crosshair'# is replaced by custom cursor in uimanager
CurCreateRect	 = 'crosshair'# is replaced by custom cursor in uimanager
CurCreateEllipse = 'crosshair'# is replaced by custom cursor in uimanager
CurCreatePolyline = 'crosshair'# is replaced by custom cursor in uimanager
CurCreateBezier = 'crosshair'# is replaced by custom cursor in uimanager
#----------------------------------
CurPlace	 = 'crosshair'# is replaced by custom cursor in uimanager
CurHGuide = 'sb_v_double_arrow'# is replaced by custom cursor in uimanager
CurVGuide = 'sb_h_double_arrow'# is replaced by custom cursor in uimanager
CurZoom		 = 'plus'# is replaced by custom cursor in uimanager
CurCopy		 = 'plus'# is replaced by custom cursor in uimanager

CurEdit = 'left_ptr'# is replaced by custom cursor in uimanager
CurText = 'xterm'# is replaced by custom cursor in uimanager

#-----------Should be system defined-------------
CurHResize = 'sb_h_double_arrow'
CurVResize = 'sb_v_double_arrow'

#-----------Obsolete or unused-----------
CurUp = 'based_arrow_up'
CurUpDown = 'sb_v_double_arrow'
CurDown = 'based_arrow_down'
CurDragColor	 = 'spraycan'
CurTurn		 = 'exchange'
CurHelp		 = 'question_arrow'
CurWait		 = 'watch'