import ui
import dbg
import app
import OpenLib
import net_packet
import chat
import net



instances = dict()
last_n_recived = 0


def callback(arg,a,b):
	global last_n_recived
	instances[a] = (arg,b)
	last_n_recived = b
	#instances.append((arg,a,b))

def clearInstances():
	global instances
	instances = dict()

def getFoundOres():
	return [x for x in instances.keys()]


import Movement
import OpenLib,chr,player,net_packet,ui,chat,background
import FileManager,UIComponents
from BotBase import BotBase
from FileManager import boolean

class MiningBotDialog(BotBase):
	TIME_WAIT = 0.2
	STATE_MINING = 1
	STATE_SCANNING = 2
	STATE_START_MINING = 3
	TIME_FOR_SLASH = 2.1
	ACTION_WAIT_TIME = 3


	def __init__(self):
		BotBase.__init__(self,self.TIME_WAIT)
		self.miningState = self.STATE_SCANNING
		self.currVid = 0
		self.currOre = 0
		self.miningTimer = OpenLib.GetTime()
		self.delayWaitTime = 1
		self.scanningTimer = 0
		self.actionTimer = 0
		net_packet.RegisterDigMotionCallback(callback)
		self.BuildWindow()


	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar() 
		self.Board.SetPosition(52, 40)
		self.Board.SetSize(270, 210) 
		self.Board.SetTitleName("MiningBot")
		self.Board.AddFlag("movable")
		self.Board.SetCloseEvent(self.Close)
		self.Board.Hide()

		comp = UIComponents.Component()
		self.EnableButton = comp.OnOffButton(self.Board, '', '', 0,120,OffUpVisual='OpenBot/Images/start_0.tga', OffOverVisual='OpenBot/Images/start_1.tga', OffDownVisual='OpenBot/Images/start_2.tga',OnUpVisual='OpenBot/Images/stop_0.tga', OnOverVisual='OpenBot/Images/stop_1.tga', OnDownVisual='OpenBot/Images/stop_2.tga',funcState=self.OnStartStop)
		self.EnableButton.SetWindowHorizontalAlignCenter()

		self.minSlotEditLine, self.minEditLine = comp.EditLine(self.Board, '7699999', 55, 58, 50, 15, 7)
		self.minLabel = comp.TextLine(self.Board, "Min VID:", 15, 60, comp.RGB(255, 255, 255))
		self.maxSlotEditLine, self.maxEditLine = comp.EditLine(self.Board, '8999999', 195, 58, 50, 15, 7)
		self.maxLabel = comp.TextLine(self.Board, "Max VID:", 150, 60, comp.RGB(255, 255, 255))
		self.stepSizeSlotEditLine, self.stepSizeEditLine = comp.EditLine(self.Board, '1300', 113, 83, 40, 15, 7)
		self.stepLabel = comp.TextLine(self.Board, "Step:", 88, 85, comp.RGB(255, 255, 255))

		self.currVID = comp.TextLine(self.Board, "Current VID: 0", 98, 170, comp.RGB(255, 255, 255))

		self.delayLabel = comp.TextLine(self.Board, "Delay", 15, 35, comp.RGB(255, 255, 255))
		self.slideDelay = comp.SliderBar(self.Board, float(self.delayWaitTime/10), self.OnSlideDelay,self.delayLabel.GetLocalPosition()[0]+35,self.delayLabel.GetLocalPosition()[1]+3)
		self.delayNumLabel = comp.TextLine(self.Board, str(self.delayWaitTime),self.slideDelay.GetLocalPosition()[0] + 185, self.slideDelay.GetLocalPosition()[1]-2, comp.RGB(255, 255, 255))
		#self.delaySlotEditLine, self.delayEditLine = comp.EditLine(self.Board, '', 25, 80, 30, 15, 3)
		#self.maxEditLine, self.maxEditLine = comp.EditLine(self.Board, '', 182, 295, 30, 15, 3)

		self.LoadSettings()
		
		#Init

	def LoadSettings(self):
		pass
		#self.Range = int(FileManager.ReadConfig("LevelRange"))
		#self.goToCenter = boolean(FileManager.ReadConfig("LevelGoToCenter"))
		#self.ignoreBlockedPosition = boolean(FileManager.ReadConfig("LevelIgnoreBlockedPos"))
		#self.allowShopOnFullInv = boolean(FileManager.ReadConfig("LevelShopFullInv"))
		#self.allowLocChanger = boolean(FileManager.ReadConfig("LevelAllowLocation"))
		#locs = FileManager.LoadListFile(FileManager.CONFIG_LOCATION_CHANGER)
		#for loc in locs:
		#	this_loc = self.LocationCondition(0,0,0,0)
		#	try:
		#		this_loc.parseLocation(loc)
		#		self.locations.add(this_loc)
		#	except Exception:
		#		continue

	def SaveSettings(self):
		#chat.AppendChat(3,str(self.Range))
	#	FileManager.WriteConfig("LevelRange", str(self.Range))
	#	FileManager.WriteConfig("LevelGoToCenter", str(self.goToCenter))
	#	FileManager.WriteConfig("LevelIgnoreBlockedPos", str(self.ignoreBlockedPosition))
	#	FileManager.WriteConfig("LevelShopFullInv", str(self.allowShopOnFullInv))
	#	FileManager.WriteConfig("LevelAllowLocation", str(self.allowLocChanger))
	#	FileManager.SaveListFile(FileManager.CONFIG_LOCATION_CHANGER,self.locations)
	#	FileManager.Save()
		pass


	#UI
	def OnStartStop(self,val):
		if val:
			self.Start()
		else:
			self.Stop()

	def OnSlideDelay(self):
		self.delayWaitTime = float(self.slideDelay.GetSliderPos()*10)
		self.delayNumLabel.SetText(str('{:,.2f} s'.format(self.delayWaitTime)))

	
	#Logic
	def Close(self):
		self.SaveSettings()
		self.Board.Hide()

	def SetStateScanning(self):
		self.scanCurrVids()
		self.miningState = self.STATE_SCANNING
		self.currOre = 0
	
	def SetStateStartMining(self,ore):
		self.miningState = self.STATE_START_MINING
		self.currOre = ore
	
	def SetStateMining(self):
		self.miningState = self.STATE_MINING


	def scanCurrVids(self):
		max = int(self.maxEditLine.GetText())
		min = int(self.minEditLine.GetText())
		step = int(self.stepSizeEditLine.GetText())

		if self.currVid < min or self.currVid > max:
			self.currVid = min

		clearInstances()
		for vid in range(self.currVid,self.currVid+step):
			net.SendOnClickPacket(vid)
		
		self.currVID.SetText("Current VID: "+str(self.currVid))
	#Abstract Functions
	def CanPause(self):
		return True

	def Resume(self):
		self.SetStateScanning()

	def Pause(self):
		pass

	def StartBot(self):
		val = int(self.minEditLine.GetText())
		self.currVid = val
		self.Resume()

	def StopBot(self):
		self.Pause()

	def Frame(self):
		if self.miningState == self.STATE_MINING:
			if self.currOre in instances:
				n = instances[self.currOre][1]
			else:
				chat.AppendChat(3,"Ore not in instances")
				n = 20

			if OpenLib.GetTime() >= self.miningTimer+ self.TIME_FOR_SLASH*n:
				chat.AppendChat(3,"[Mining-Bot] Done, scanning new ores.")
				self.SetStateScanning()
				return
			return

		
		elif self.miningState == self.STATE_SCANNING:
			val,self.scanningTimer = OpenLib.timeSleep(self.scanningTimer,self.delayWaitTime)
			if not val:
				return
			ores = getFoundOres()
			if len(ores) > 0:
				ore = ores.pop()
				x,y,z = player.GetMainCharacterPosition()
				net_packet.SendStatePacket(x,y,0,net_packet.CHAR_STATE_WALK,0)
				self.SetStateStartMining(ore)
				return
			else:
				self.SetStateScanning()
				self.currVid += int(self.stepSizeEditLine.GetText())
			return
		
		elif self.miningState == self.STATE_START_MINING:
			val,self.actionTimer = OpenLib.timeSleep(self.actionTimer,self.ACTION_WAIT_TIME)
			if not val:
				return
			net.SendOnClickPacket(self.currOre)
			self.currVID.SetText("Current VID: "+str(self.currOre))
			self.miningTimer = OpenLib.GetTime()
			chat.AppendChat(3,"[Mining-Bot] Ore found with VID " + str(self.currOre))
			self.SetStateMining()


def switch_state():
	if not mining.Board.IsShow():
		mining.Board.Show()
	else:
		mining.Close()

mining = MiningBotDialog()
mining.Show()