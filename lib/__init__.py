import ui
def importdump_functions():
	import dump_functions
	importbutton0.Hide()
importbutton0= ui.Button()
importbutton0.SetPosition(3, 120)
importbutton0.SetEvent(importdump_functions)
importbutton0.SetUpVisual('d:/ymir work/ui/public/large_button_01.sub')
importbutton0.SetOverVisual('d:/ymir work/ui/public/large_button_02.sub')
importbutton0.SetDownVisual('d:/ymir work/ui/public/large_button_03.sub')
importbutton0.SetText('>> dump_functions')
importbutton0.Show()
