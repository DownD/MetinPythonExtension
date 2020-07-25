import ui
import dbg
import app
import m2k_lib
import net_packet
import chat

class PythonManagerDialog(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.ThinBoard()
		self.Board.SetSize(448, 403)
		self.Board.SetPosition(52, 40)
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.Hide()
		self.__BuildKeyDict()
		self.comp = m2k_lib.Component()

		self.loadCMDButton = self.comp.Button(self.Board, 'Load', '', 179, 280, self.loadCMD, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.loadFileButton = self.comp.Button(self.Board, 'Load File', '', 341, 361, self.loadFile, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.slotbar_cmd, self.cmdEditBox = self.comp.EditLine(self.Board, 'import chat\nchat.AppendChat(3,"Execution Test")', 21, 38, 405, 225, 1200)
		self.slotbar_file, self.fileEditBox = self.comp.EditLine(self.Board, 'file.py', 24, 363, 310, 15, 60)
		self.text5 = self.comp.TextLine(self.Board, 'Python Command Line', 176, 11, self.comp.RGB(255, 255, 0))
		self.text8 = self.comp.TextLine(self.Board, 'Python File Loader', 179, 341, self.comp.RGB(255, 255, 0))
  		self.text9 = self.comp.TextLine(self.Board, 'Note: File has to be at the same location as the injector', 28, 381, self.comp.RGB(255, 255, 255))
	
		self.Close = self.comp.Button(self.Board, '', 'Close', 425, 10, self.Board.Hide, 'd:/ymir work/ui/public/close_button_01.sub', 'd:/ymir work/ui/public/close_button_02.sub', 'd:/ymir work/ui/public/close_button_03.sub')

	def loadCMD(self):
		exec(self.loadCMD.GetText())
	
	def loadFile(self):
		f = open(str(net_packet.PATH)+self.fileEditBox.GetText(),"r")
		exec(f.read())
		f.close()
	
	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_F5]	= lambda : self.OpenWindow()
		self.onPressKeyDict = onPressKeyDict

	def switch_state(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
	
	def OnKeyDown(self, key):
		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise
		return True
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
	
	def Close(self):
		self.Board.Hide()
