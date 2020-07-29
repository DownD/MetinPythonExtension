import ui,app,chat,chr,net,player,item,skill,time,game,shop,chrmgr
import background,constInfo,miniMap,wndMgr,math,uiCommon,grp
import event,game,os
import net_packet
from m2kmod.Modules import m2k_lib, Movement
from m2k_lib import dist

class LevelbotDialog(ui.ScriptWindow): 				
	
	ActiveSkillList = []
	IsBuff = { "1": {"IsBuff": 0}, "2": {"IsBuff": 0}, "3": {"IsBuff": 0}, "4": {"IsBuff": 1}, "5": {"IsBuff": 1}, "6": {"IsBuff": 0}, "16": {"IsBuff": 0}, "17": {"IsBuff": 0}, "18": {"IsBuff": 0}, "19": {"IsBuff": 1}, "20": {"IsBuff": 0}, "21": {"IsBuff": 0}, "31": {"IsBuff": 0}, "32": {"IsBuff": 0}, "33": {"IsBuff": 0}, "34": {"IsBuff": 0}, "35": {"IsBuff": 0}, "36": {"IsBuff": 0}, "46": {"IsBuff": 0}, "47": {"IsBuff": 0}, "48": {"IsBuff": 0}, "49": {"IsBuff": 1}, "50": {"IsBuff": 0}, "51": {"IsBuff": 0}, "61": {"IsBuff": 0}, "62": {"IsBuff": 0}, "63": {"IsBuff": 1}, "64": {"IsBuff": 1}, "65": {"IsBuff": 1}, "66": {"IsBuff": 0}, "76": {"IsBuff": 0}, "77": {"IsBuff": 0}, "78": {"IsBuff": 0}, "79": {"IsBuff": 1}, "80": {"IsBuff": 1}, "81": {"IsBuff": 0}, "91": {"IsBuff": 0}, "92": {"IsBuff": 0}, "93": {"IsBuff": 0}, "94": {"IsBuff": 1}, "95": {"IsBuff": 1}, "96": {"IsBuff": 1}, "106": {"IsBuff": 0}, "107": {"IsBuff": 0}, "108": {"IsBuff": 0}, "109": {"IsBuff": 1}, "110": {"IsBuff": 1}, "111": {"IsBuff": 1}}
	Levelbot = 0
	State = 0
	IsReady = 0
	RestartPot = 0
	SkillCount = 0
	SkillIndex = 0
	DIST_TO_ATTACK = 280
	MIN_SPEED = 200
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Show()
		self.Board = ui.ThinBoard() 
		self.Board.SetPosition(52, 40)
		self.Board.SetSize(300, 420) 
	#	self.Board.AddFlag("float") 
		self.Board.AddFlag("movable")
		self.Board.Hide()
		
		self.comp = m2k_lib.Component()
		self.HeaderLabel = self.comp.TextLine(self.Board, 'Levelbot', 130, 8, self.comp.RGB(255, 255, 0))
		self.RedLabel = self.comp.TextLine(self.Board, '90 %', 250, 38, self.comp.RGB(255, 255, 255))
		self.BlueLabel = self.comp.TextLine(self.Board, '30 %', 250, 78, self.comp.RGB(255, 255, 255))
		self.TapfiLabel = self.comp.TextLine(self.Board, '20 Sec.', 250, 118, self.comp.RGB(255, 255, 255))

		self.CloseButton = self.comp.Button(self.Board, '', 'Close', 270, 8, self.Hide_UI, 'd:/ymir work/ui/public/close_button_01.sub', 'd:/ymir work/ui/public/close_button_02.sub', 'd:/ymir work/ui/public/close_button_03.sub')
		self.ImageRed = self.comp.ExpandedImage(self.Board, 19, 30, str("icon/item/27003.tga"))
		self.ImageBlue = self.comp.ExpandedImage(self.Board, 19, 70, str("icon/item/27006.tga"))
		#self.ImageTapfi = self.comp.ExpandedImage(self.Board, 19, 110, str("icon/item/70038.tga"))
		self.HorseImage = self.comp.ExpandedImage(self.Board, 35, 210, ("m2kmod/Images/General/horse.tga"))
		self.PickupImage = self.comp.ExpandedImage(self.Board, 85, 210, ("m2kmod/Images/General/pickup.tga"))
		self.RotationImage = self.comp.ExpandedImage(self.Board, 135, 214, ("m2kmod/Images/General/restart.tga"))
		self.EXPImage = self.comp.ExpandedImage(self.Board, 185, 217, ("m2kmod/Images/General/exp.tga"))
		self.PotImage = self.comp.ExpandedImage(self.Board, 232, 210, ("m2kmod/Images/General/pot.tga"))
		
		self.SlidbarRed = self.comp.SliderBar(self.Board, 0.9, self.SlideRed, 60, 40)
		self.SlidebarBlue = self.comp.SliderBar(self.Board, 0.3, self.SlideBlue, 60, 80)
		self.SlidebarTapfi = self.comp.SliderBar(self.Board, 0.2, self.SlideTapfi, 60, 120)
  
	
		self.BuffBotStartButton = self.comp.HideButton(self.Board, '', '', 130, 360, self.CheckLevelbot, 'm2kmod/Images/start_0.tga', 'm2kmod/Images/start_1.tga', 'm2kmod/Images/start_2.tga')
		self.BuffBotStopButton = self.comp.HideButton(self.Board, '', '', 130, 360, self.CheckLevelbot, 'm2kmod/Images/stop_0.tga', 'm2kmod/Images/stop_1.tga', 'm2kmod/Images/stop_2.tga')
		self.HorseOn = self.comp.HideButton(self.Board, '', 'Use horse for leveling', 57, 225, self.SetHorse, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		self.HorseOff = self.comp.HideButton(self.Board, '', 'Use horse for leveling', 57, 225, self.SetHorse, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.PickupOn = self.comp.HideButton(self.Board, '', 'Pickup', 98, 225, self.SetPickup, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		self.PickupOff = self.comp.HideButton(self.Board, '', 'Pickup', 98, 225, self.SetPickup, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.RotationOn = self.comp.HideButton(self.Board, '', 'Rotation Hits', 150, 225, self.SetRotation, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		self.RotationOff = self.comp.HideButton(self.Board, '', 'Rotation Hits', 150, 225, self.SetRotation, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.EXPOn = self.comp.HideButton(self.Board, '', 'EXP-Donator', 195, 225, self.SetExpDonator, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		self.EXPOff = self.comp.HideButton(self.Board, '', 'EXP-Donator', 195, 225, self.SetExpDonator, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.AutoPotOn = self.comp.HideButton(self.Board, '', 'Use AutoPotions', 255, 225, self.SetAutoPotion, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		self.AutoPotOff = self.comp.HideButton(self.Board, '', 'Use AutoPotions', 255, 225, self.SetAutoPotion, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		#self.PullOn = self.comp.HideButton(self.Board, '', 'Use Capes', 30, 120, self.SetPull, 'm2kmod/Images/on_0.tga', 'm2kmod/Images/on_1.tga', 'm2kmod/Images/on_2.tga')
		#self.PullOff = self.comp.HideButton(self.Board, '', 'Use Capes', 30, 120, self.SetPull, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.PullButton = self.comp.OnOffButton(self.Board, '', 'Use Capes', 19, 110, self.SetPull,image="icon/item/70038.tga")
		#self.PullOff = self.comp.HideButton(self.Board, '', 'Use Capes', 30, 120, self.SetPull, 'm2kmod/Images/off_0.tga', 'm2kmod/Images/off_1.tga', 'm2kmod/Images/off_2.tga')
		self.MetinButton = self.comp.OnOffButton(self.Board, '', 'Attack metins', 35, 280, self.SetMetinAttack,image="m2kmod/Images/General/metin.png")
		self.editTime ,self.TimeWaitMetinDead = self.comp.EditLine(self.Board, '1.2', 40, 320, 30, 14, 7)
		self.clockImage = self.comp.ExpandedImage(self.Board, 20, 320, "m2kmod/Images/General/clock.png")
  		self.BossButton = self.comp.OnOffButton(self.Board, '', 'Attack bosses', 85, 280,image="m2kmod/Images/General/boss.png")
		self.MonsterButton = self.comp.OnOffButton(self.Board, '', 'Attack monsters', 135, 280,image="m2kmod/Images/General/monster.png")

		self.LoadSettings()
		
		self.SlidbarRed.SetSliderPos(self.RedPercent*0.01)
		self.SlideRed()
		self.SlidebarBlue.SetSliderPos(self.BluePercent*0.01)
		self.SlideBlue()
		self.SlidebarTapfi.SetSliderPos(self.TapfiSec*0.01)
		self.SlideTapfi()
		
		if self.Horse:
			self.HorseOn.Show()
		else:	
			self.HorseOff.Show()
		if self.Pick:
			self.PickupOn.Show()
		else:	
			self.PickupOff.Show()
		if self.Rotation:
			self.RotationOn.Show()
		else:	
			self.RotationOff.Show()
		if self.ExpDonator:
			self.EXPOn.Show()
		else:	
			self.EXPOff.Show()
		if self.AutoPotion:
			self.AutoPotOn.Show()
		else:	
			self.AutoPotOff.Show()
		if self.Levelbot:
			self.BuffBotStopButton.Show()
		else:
			self.BuffBotStartButton.Show()
		
		#self.AddSkillIcons()
		#self.LoadSkill()
		self.LastAliveTime = 0
		#self.TimeWaitMetinDead = 1.2

		#Timers
		self.pullLastTime = 0
		self.pickupLastTime = 0
		self.restartLastTime = 0	
		self.restartPotsAndExp = 0
		self.attackLastTime = 0
		self.charStuckTrys = 0
		self.metinDeadLastTime = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def switch_state(self):
		if self.Board.IsShow():
			self.Hide_UI()
		else:
			self.Board.Show()
			self.AddSkillIcons()
			self.LoadSkill()
			self.LoadSettings()
	
	def LoadSettings(self):
		self.RedPercent = int(m2k_lib.ReadConfig("RedPercent"))
		self.BluePercent = int(m2k_lib.ReadConfig("BluePercent"))
		self.TapfiSec = int(m2k_lib.ReadConfig("TapfiSec"))
		self.Horse = int(m2k_lib.ReadConfig("Horse"))
		self.Pick = int(m2k_lib.ReadConfig("Pickup"))
		self.Rotation = int(m2k_lib.ReadConfig("Rotation"))
		self.ExpDonator = int(m2k_lib.ReadConfig("ExpDonator"))
		self.AutoPotion = int(m2k_lib.ReadConfig("AutoPotion"))
		self.RedPotID = int(m2k_lib.ReadConfig("Red-Pot"))
		self.BluePotID = int(m2k_lib.ReadConfig("Blue-Pot"))
		self.RedAutoPotID = int(m2k_lib.ReadConfig("AutoRed-Pot"))
		self.BlueAutoPotID = int(m2k_lib.ReadConfig("AutoBlue-Pot"))
		self.CapeId = int(m2k_lib.ReadConfig("Bravery-Cape"))
		self.PullButton.SetValue(int(m2k_lib.ReadConfig("Pull")))
		self.MetinButton.SetValue(int(m2k_lib.ReadConfig("Attack-Metin")))
		self.BossButton.SetValue(int(m2k_lib.ReadConfig("Attack-Boss")))
		self.MonsterButton.SetValue(int(m2k_lib.ReadConfig("Attack-Monster")))
		self.TimeWaitMetinDead.SetText(m2k_lib.ReadConfig("TimeMetinDead"))

	def Hide_UI(self):
		m2k_lib.SaveConfig("RedPercent", str(self.RedPercent))
		m2k_lib.SaveConfig("BluePercent", str(self.BluePercent))
		m2k_lib.SaveConfig("TapfiSec", str(self.TapfiSec))
		m2k_lib.SaveConfig("Horse", str(self.Horse))
		m2k_lib.SaveConfig("Pickup", str(self.Pick))
		m2k_lib.SaveConfig("Rotation", str(self.Rotation))
		m2k_lib.SaveConfig("ExpDonator", str(self.ExpDonator))
		m2k_lib.SaveConfig("AutoPotion", str(self.AutoPotion))
		m2k_lib.SaveConfig("Pull", str(self.PullButton.isOn))
		m2k_lib.SaveConfig("Attack-Metin", str(self.MetinButton.isOn))
		m2k_lib.SaveConfig("Attack-Boss", str(self.BossButton.isOn))
		m2k_lib.SaveConfig("Attack-Monster", str(self.MonsterButton.isOn))
		m2k_lib.SaveConfig("TimeMetinDead", str(self.TimeWaitMetinDead.GetText()))
	#	m2k_lib.SaveConfig("Red-Pot", str(self.RedPotID))
	#	m2k_lib.SaveConfig("Blue-Pot", str(self.BluePotID))
	#	m2k_lib.SaveConfig("AutoRed-Pot", str(self.RedAutoPotID))
	#	m2k_lib.SaveConfig("AutoBlue-Pot", str(self.BlueAutoPotID))
	#	m2k_lib.SaveConfig("Bravery-Cape", str(self.CapeId))
		self.Board.Hide()	
		
	def SetHorse(self):
		if self.Horse:
			self.Horse = 0
			self.HorseOff.Show()
			self.HorseOn.Hide()
		else: 
			self.Horse = 1
			self.HorseOn.Show()
			self.HorseOff.Hide()
			
	def SetPickup(self):
		if self.Pick:
			self.Pick = 0
			self.PickupOff.Show()
			self.PickupOn.Hide()
		else: 
			self.Pick = 1
			self.PickupOn.Show()
			self.PickupOff.Hide()

	def SetMetinAttack(self):
		if self.MetinButton.isOn:
			self.MetinButton.SetOff()
		else: 
			self.MetinButton.SetOn()

	def SetPull(self):
		if self.PullButton.isOn:
			self.PullButton.SetOff()
		else: 
			self.PullButton.SetOn()
			
	def SetRotation(self):
		if self.Rotation:
			self.Rotation = 0
			self.RotationOff.Show()
			self.RotationOn.Hide()
		else: 
			self.Rotation = 1
			self.RotationOn.Show()
			self.RotationOff.Hide()
			
	def SetExpDonator(self):
		if player.GetGuildID() != 0:
			if self.EXP:
				self.EXP = 0
				self.EXPOff.Show()
				self.EXPOn.Hide()
			else: 
				self.EXP = 1
				self.EXPOn.Show()
				self.EXPOff.Hide()
		else:
			chat.AppendChat(7,"[m2k-Mod] You need a Guild to donate EXP!")
	def SetAutoPotion(self):
		if self.AutoPotion:
			self.AutoPotion = 0
			self.AutoPotOff.Show()
			self.AutoPotOn.Hide()
		else: 
			self.AutoPotion = 1
			self.AutoPotOn.Show()
			self.AutoPotOff.Hide()
			
	def CheckLevelbot(self):
		if self.Levelbot:
			self.Levelbot = 0	
			self.State = 0
			self.BuffBotStopButton.Hide()	
			self.BuffBotStartButton.Show()
			Movement.StopMovement()	
			player.SetAttackKeyState(False)
		else:
			self.LastAliveTime = m2k_lib.GetTime()
			self.Levelbot = 1
			self.State = 1
			self.Target = -1
			self.BuffBotStopButton.Show()	
			self.BuffBotStartButton.Hide()
			self.myLastPosition_x,self.myLastPosition_y,_Z = player.GetMainCharacterPosition()
			self.myLastPositionTime = m2k_lib.GetTime()
			#player.SetAttackKeyState(TRUE)
			

	def SlideRed(self):
		self.RedPercent = int(self.SlidbarRed.GetSliderPos()*100)
		self.RedLabel.SetText(str(self.RedPercent) + ' %')
	def SlideBlue(self):
		self.BluePercent = int(self.SlidebarBlue.GetSliderPos()*100)
		self.BlueLabel.SetText(str(self.BluePercent) + ' %')
	def SlideTapfi(self):
		self.TapfiSec = int(self.SlidebarTapfi.GetSliderPos()*100)
		self.TapfiLabel.SetText(str(self.TapfiSec) + ' Sec.')

	def AddSkillIcons(self):
		self.SkillList = []
		try:
			handle = app.OpenTextFile(app.GetLocalePath() + "/skilldesc.txt")
			count = app.GetTextFileLineCount(handle)
		except IOError:
			chat.AppendChat(1, "Could not load " + app.GetLocalePath() + "/skilldesc.txt")

		for i in xrange(count):
			line = app.GetTextFileLine(handle, i)
			if str(line).count("\t") >= 21:
				SkillData = str(line).split("\t")
				SkillName = str(SkillData[2])
				SkillIconName = str(SkillData[12])
				SkillIndex = str(SkillData[0])
				SkillData = { 
					"NAME":SkillName,
					"ICON":SkillIconName,
					"INDEX":SkillIndex,
					}
				self.SkillList.append(SkillData)
		
		RaceGroupInfo = m2k_lib.GetClass()
		Class = str(RaceGroupInfo).split("/")[0]
		group = str(RaceGroupInfo).split("/")[1]
		if Class == "Warrior":
			SkillIndex = 1
			if int(group) == 2:
				SkillIndex = 16
		elif Class == "Assassin":
			SkillIndex = 31
			if int(group) == 2:
				SkillIndex = 46
		elif Class == "Sura":
			SkillIndex = 61
			if int(group) == 2:
				SkillIndex = 76
		elif Class == "Shaman":
			SkillIndex = 91
			if int(group) == 2:
				SkillIndex = 106
				
		self.SkillIconIndex = []
		Count = 0
		for SkillValue in xrange(m2k_lib.NewSkillsEnable()):
			try:
				Skillname = skill.GetSkillName(int(SkillIndex))
				SkillIndex += 1
				for Skills in self.SkillList:
					SkillNameList = Skills["NAME"]
					if str(Skillname) == str(SkillNameList):
						Count += 1
						SkillName = Skills["NAME"]
						SkillIcon = Skills["ICON"]
						SkillIndexAppend = SkillIndex - 1
						PrivateSkillData = { 
							"NAME":SkillName,
							"ICON":SkillIcon,
							"INDEX":SkillIndexAppend,
							"COUNT":Count,
							}
						self.SkillIconIndex.append(PrivateSkillData)
				self.SkillCount = Count
			except:
				pass
			
		self.GetSkillIcon()
		
	def GetSkillIcon(self):
		self.SkillIconList = []
		RaceGroupInfo = m2k_lib.GetClass()
		Class = str(RaceGroupInfo).split("/")[0]
		x = 15
		y = 150
		i = 0
		for Skills in self.SkillIconIndex:
			SkillIconButton = m2k_lib.SkillButton()
			SkillIconButton.SetParent(self.Board)
			SkillIconButton.SetPosition(x,y)
			SkillIconButton.SetUpVisual("d:/ymir work/ui/skill/" + str(Class).lower() + "/" + str(Skills["ICON"]) + "_0" + str(self.GetSkillLevel(str(Skills["NAME"]))) + ".sub")
			SkillIconButton.SetOverVisual("d:/ymir work/ui/skill/" + str(Class).lower() + "/" + str(Skills["ICON"]) + "_0" + str(self.GetSkillLevel(str(Skills["NAME"]))) + ".sub")
			SkillIconButton.SetDownVisual("d:/ymir work/ui/skill/" + str(Class).lower() + "/" + str(Skills["ICON"]) + "_0" + str(self.GetSkillLevel(str(Skills["NAME"]))) + ".sub")
			SkillIconButton.SetText("Off")
			SkillIconButton.SetTextColor(0.1, 0.7, 1.0)
			SkillIconButton.SetButtonFontName("MAGNETO:16")
			SkillIconButton.SetTextPosition(0, 22)
			SkillIconButton.Show()
			
			SkillActivated = m2k_lib.SkillButton()
			SkillActivated.SetParent(self.Board)
			SkillActivated.SetPosition(x,y)
			SkillActivated.SetUpVisual("d:/ymir work/ui/public/slot_cover_button_03.sub")
			SkillActivated.SetOverVisual("d:/ymir work/ui/public/slot_cover_button_03.sub")
			SkillActivated.SetDownVisual("d:/ymir work/ui/public/slot_cover_button_03.sub")
			SkillActivated.Hide()
			
			Mod = self.SkillIconIndex[i]			
			SkillIconButton.SetEvent(lambda arg = Mod: self.SelectSkill(arg))
			SkillActivated.SetEvent(lambda arg = Mod: self.SelectSkill(arg))
			self.SkillIconList.append(SkillIconButton)
			self.SkillIconList.append(SkillActivated)			
			if self.SkillCount == 5:
				x += 60
			else:
				x += 47
			i += 1
	
	def LoadSkill(self):
		for i in xrange(self.SkillCount):
			read = m2k_lib.ReadConfig("Skill"+str(i+1))
			split = read.split(",")
			ActiveSkillData = { 
				"COUNT":int(split[2]),
				"INDEX":int(split[1]),
				"NAME":skill.GetSkillName(int(split[1])),
			}
			if int(split[0]):
				self.ActiveSkillList.append(ActiveSkillData)
				self.SkillIconList[(int(split[2]) - 1)*2].SetText("On")
				self.SkillIconList[(int(split[2]) - 1)*2 + 1].Show()	
			else:
				try:
					self.ActiveSkillList.remove(ActiveSkillData)
				except:
					pass
				self.SkillIconList[(int(split[2]) - 1)*2].SetText("Off")
				self.SkillIconList[(int(split[2]) - 1)*2 + 1].Hide()
		
	def SelectSkill(self, skillindex):
		SkillEvent = skillindex["COUNT"]
		SkillIndex = skillindex["INDEX"]
		SkillName = skillindex["NAME"]
		Search = 0
		for test in self.ActiveSkillList:
			if test["INDEX"] == SkillIndex:
				Search = 1
		ActiveSkillData = { 
			"COUNT":SkillEvent,
			"INDEX":SkillIndex,
			"NAME":SkillName,
		}
		if Search == 0:
			m2k_lib.SaveConfig("Skill"+str(SkillEvent), "1," + str(SkillIndex) + "," + str(SkillEvent))
			self.ActiveSkillList.append(ActiveSkillData)
			chat.AppendChat(7, "[m2k-Mod] " + str(SkillName) + " has been activated")
			self.SkillIconList[(int(SkillEvent) - 1)*2].SetText("On")
			self.SkillIconList[(int(SkillEvent) - 1)*2 + 1].Show()	
		else:
			m2k_lib.SaveConfig("Skill"+str(SkillEvent), "0," + str(SkillIndex) + "," + str(SkillEvent))
			self.ActiveSkillList.remove(ActiveSkillData)
			chat.AppendChat(7,  "[m2k-Mod] " + str(SkillName) + " has been deactivated")
			self.SkillIconList[(int(SkillEvent) - 1)*2].SetText("Off")
			self.SkillIconList[(int(SkillEvent) - 1)*2 + 1].Hide()
		
	def GetSkillLevel(self, skillname):
		SkillIconLevel = []
		for Skill in self.SkillIconIndex:
			Skillgrade = player.GetSkillGrade(Skill["COUNT"])
			Skilllevel = player.GetSkillLevel(Skill["COUNT"])
			Skillname = Skill["NAME"]
			SkillLevelData = { 
				"GRADE":Skillgrade,
				"LEVEL":Skilllevel,
				"NAME":Skillname,
			}
			SkillIconLevel.append(SkillLevelData)
			
		for SkillData in SkillIconLevel:
			SkillLevel = int(SkillData["LEVEL"]) + int(SkillData["GRADE"])*10
			Skillname = str(SkillData["NAME"])
			if str(Skillname) == str(skillname):
				if int(SkillLevel) < 11:
					return 1
				elif int(SkillLevel) < 21:
					return 2
				else:
					return 3
 
	def OnUpdate(self):
		if self.State == 1:
			if not self.MetinButton.isOn:
				self.HandlePickup()
			self.HandleRestart()
			self.HandlePotsAndExp()
			self.HandlePull()
			self.HandleAutoAttack()
			#if self.Rotation:
				#chr.SetDirection(app.GetRandom(0,7))

	def HandleAutoAttack(self):
		val,self.attackLastTime = m2k_lib.timeSleep(self.attackLastTime,0.5)
		if(val):
			if self.MetinButton.isOn and self.metinDeadLastTime != 0 and self.metinDeadLastTime + float(self.TimeWaitMetinDead.GetText()) < m2k_lib.GetTime():
				return
			self.metinDeadLastTime = 0
			if(chr.HasInstance(self.Target)):
				if(net_packet.IsDead(self.Target)):
					self.metinDeadLastTime = m2k_lib.GetTime()
					self.Target = -1
					return
				self.AttackTarget()
			else:
				target = -1
				if(self.BossButton.isOn):
					target = m2k_lib.getClosestInstance(m2k_lib.BOSS_TYPE)
				if(self.MetinButton.isOn and target == -1):
					target = m2k_lib.getClosestInstance(m2k_lib.METIN_TYPE)
				if(self.MonsterButton.isOn and target == -1):
					target = m2k_lib.getClosestInstance(m2k_lib.MONSTER_TYPE)

				#chat.AppendChat(3,"Target = "+ str(chr.GetNameByVID(self.Target)))
				self.Target = target
				if self.Pick:
					player.PickCloseItem()

				if target == -1:
					player.SetAttackKeyState(True)
				
			
	def HandlePull(self):
		val,self.pullLastTime = m2k_lib.timeSleep(self.pullLastTime,self.TapfiSec)
		if(val):
			if self.PullButton.isOn == 1:
				UseItem(self.CapeId)
			
	def HandlePickup(self):
		val,self.pickupLastTime = m2k_lib.timeSleep(self.pickupLastTime,0.5)
		if not val:
			return
		if self.Pick:
			player.PickCloseItem()

	def HandleRestart(self):
		val,self.restartLastTime = m2k_lib.timeSleep(self.restartLastTime,1)
		if(val):
			if player.GetStatus(player.HP) < 1:
				self.LastAliveTime = self.restartLastTime
				net.SendChatPacket("/restart_here")
				return
			if self.Horse == 1:
				if not player.IsMountingHorse():
					net.SendChatPacket("/user_horse_ride")
					
     
	def HandlePotsAndExp(self):
		val,self.restartPotsAndExp = m2k_lib.timeSleep(self.restartPotsAndExp,0.2)
		if(val):
			self.RedPot()
			self.BluePot()
			if self.ExpDonator:
				cur_exp = player.GetStatus(player.EXP)
				next_exp = player.GetStatus(player.NEXT_EXP)
				cur_percent_value = cur_exp*100/next_exp
				if cur_percent_value >=(EXP):
					net.SendGuildOfferPacket(cur_exp)
			if self.AutoPotion:
				red_active = 0
				blue_active = 0
				for i in xrange(90,-1,-1):
					if player.GetItemIndex(i) == self.RedAutoPotID and player.GetItemMetinSocket(i, 0) == 1:
						red_active = 1
						continue
					if player.GetItemIndex(i) == self.BlueAutoPotID and player.GetItemMetinSocket(i, 0) == 1:
						blue_active = 1
						continue
				if red_active == 0:
					UseItem(self.RedAutoPotID)

				if blue_active == 0:
					UseItem(self.BlueAutoPotID)

	def AttackTarget(self):
		mobX, mobY, _ = chr.GetPixelPosition(self.Target)
		if player.GetCharacterDistance(self.Target) < self.DIST_TO_ATTACK:
			#Apply Rotation
			m2k_lib.RotateMainCharacter(mobX, mobY)
			#chr.MoveToDestPosition(player.GetMainCharacterIndex(),mobX, mobY)
			player.SetAttackKeyState(True)
		else:
			player.SetAttackKeyState(False)
			Movement.GoToPositionAvoidingObjects(mobX,mobY,self.DIST_TO_ATTACK)

	def RedPot(self):
		if (float(player.GetStatus(player.HP)) / (float(player.GetStatus(player.MAX_HP))) * 100) < self.RedPercent:
			for i in xrange(player.INVENTORY_PAGE_SIZE*3):
				RedPott = player.GetItemIndex(i)
				if RedPott == 27001 or RedPott == 27002 or RedPott == 27003 or RedPott == self.RedPotID:
					net.SendItemUsePacket(i)
					break
	def BluePot(self):
		if (float(player.GetStatus(player.SP)) / (float(player.GetStatus(player.MAX_SP))) * 100) < self.BluePercent:
			for i in xrange(player.INVENTORY_PAGE_SIZE*3):
				BluePott = player.GetItemIndex(i)
				if BluePott == 27004 or BluePott == 27005 or BluePott == 27006 or BluePott == self.BluePotID:
					net.SendItemUsePacket(i)
					break

	def Mount(self):
		player.ClickSkillSlot(self.SkillIndex)
		self.SkillIndex = 0
		net.SendChatPacket("/user_horse_ride")
	def MountOnly(self):
		net.SendChatPacket("/user_horse_ride")
	def SkillWait(self):
		player.ClickSkillSlot(self.SkillIndex)
		self.SkillIndex = 0
		self.WaitSkill = m2k_lib.WaitingDialog()			
		self.WaitSkill.Open(1.5)
		self.WaitSkill.SAFE_SetTimeOverEvent(self.MountOnly)
	
	def CheckMountAndGo(self):
		self.IsReady = 0		
		self.State = 1
		player.SetAttackKeyState(TRUE)	
		if self.Horse:
			net.SendChatPacket("/user_horse_ride")
			
		
	def InstallQuestWindowHook(self):
		self.OldRecv = game.GameWindow.OpenQuestWindow
		game.GameWindow.OpenQuestWindow = self.HookedQuestWindow
	def UnHookQuestWindow(self):
		game.GameWindow.OpenQuestWindow = self.OldRecv
	def HookedQuestWindow(self, skin, idx):
		pass
		
	
def CanUseSkill(index):
	cd = player.IsSkillCoolTime(int(index))
	if cd < 1:
		return 1
	else:
		return 0
		
def UseItem(id):
	for i in xrange(player.INVENTORY_PAGE_SIZE*3):
		index = player.GetItemIndex(i)
		if index == id:
			net.SendItemUsePacket(i)
			break


#LevelbotDialog().Show()