import net_packet,ui,net,chr,player,chat
import m2k_lib

ATTACK_MAX_DIST_NO_TELEPORT = 290


class DmgHacks(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()

	def __del__(self):
		chat.AppendChat(3,"TEST1")
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(300, 260)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName('WaitHack')
		self.Board.SetCloseEvent(self.Close)
		self.Board.Hide()
		self.comp = m2k_lib.Component()

		self.enableButton = self.comp.OnOffButton(self.Board, '', '', 130, 200, OffUpVisual='m2kmod/Images/start_0.tga', OffOverVisual='m2kmod/Images/start_1.tga', OffDownVisual='m2kmod/Images/start_2.tga',OnUpVisual='m2kmod/Images/stop_0.tga', OnOverVisual='m2kmod/Images/stop_1.tga', OnDownVisual='m2kmod/Images/stop_2.tga' )
		self.MetinButton = self.comp.OnOffButton(self.Board, '', 'Only attack metins', 220, 40,image="m2kmod/Images/General/metin.png")
  		self.playerClose = self.comp.OnOffButton(self.Board, '', '', 130, 50)
		self.RangeLabel = self.comp.TextLine(self.Board, 'Range', 13, 92, self.comp.RGB(255, 255, 255))
		self.SpeedLabel = self.comp.TextLine(self.Board, 'Speed', 13, 126, self.comp.RGB(255, 255, 255))
		self.MonsterLabel = self.comp.TextLine(self.Board, 'Monsters', 13, 160, self.comp.RGB(255, 255, 255))
		self.PlayerLabel = self.comp.TextLine(self.Board, 'Stop when player close', 12, 51, self.comp.RGB(255, 255, 255))
  		self.rangeNum = self.comp.TextLine(self.Board, '100', 254, 92, self.comp.RGB(255, 255, 255))
		self.speedNum = self.comp.TextLine(self.Board, '100 ms', 254, 125, self.comp.RGB(255, 255, 255))
		self.monsterNum = self.comp.TextLine(self.Board, '100', 254, 160, self.comp.RGB(255, 255, 255))
		self.RangeSlider = self.comp.SliderBar(self.Board, 0.0, self.Range_func, 73, 94)
		self.SpeedSlider = self.comp.SliderBar(self.Board, 0.0, self.Speed_func, 73, 127)
		self.MonsterSlider = self.comp.SliderBar(self.Board, 0.0, self.Monster_func, 73, 161)
		self.enableButton.SetOff()

		self.loadSettings()

		self.range = 0
		self.speed = 0
		self.lastTime = 0
		self.maxMonster = 0
		self.Speed_func()
		self.Range_func()
		self.Monster_func()

	def loadSettings(self):
		self.MonsterSlider.SetSliderPos(float(m2k_lib.ReadConfig("WaitHack_MaxMonsters")))
		self.SpeedSlider.SetSliderPos(float(m2k_lib.ReadConfig("WaitHack_Speed")))
		self.RangeSlider.SetSliderPos(float(m2k_lib.ReadConfig("WaitHack_Range")))
		self.MetinButton.SetValue(int(m2k_lib.ReadConfig("WaitHack_MetinAttack")))
		self.playerClose.SetValue(int(m2k_lib.ReadConfig("WaitHack_PlayerClose")))
	def saveSettings(self):
		m2k_lib.SaveConfig("WaitHack_MaxMonsters", str(self.MonsterSlider.GetSliderPos()))
		m2k_lib.SaveConfig("WaitHack_Speed", str(self.SpeedSlider.GetSliderPos()))
		m2k_lib.SaveConfig("WaitHack_Range", str(self.RangeSlider.GetSliderPos()))
		m2k_lib.SaveConfig("WaitHack_MetinAttack", str(self.MetinButton.isOn))
		m2k_lib.SaveConfig("WaitHack_PlayerClose", str(self.playerClose.isOn))
	
	
	def Monster_func(self):
		self.maxMonster = int(self.MonsterSlider.GetSliderPos()*1000)
		self.monsterNum.SetText(str(self.maxMonster))
  
	def Range_func(self):
		self.range = int(self.RangeSlider.GetSliderPos()*10000)
		self.rangeNum.SetText(str(self.range))
	
	def Speed_func(self):
		self.speed= float(self.SpeedSlider.GetSliderPos())
		self.speedNum.SetText(str(int(self.speed*1000)) + ' ms')
	
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
   
	def TeleportAttack(self,lst,x,y,attack_type):
		#net_packet.SendStatePacket(x,y,0,1,0)
		#net_packet.SendStatePacket(x,y,0,0,0)
		net_packet.SendStatePacket(x,y,0,3,attack_type)
		#chat.AppendChat(3,"Before: " + str(len(lst))) 
		vid_hits = 0
		for vid in lst:
			mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
			if m2k_lib.dist(x,y,mob_x,mob_y) < ATTACK_MAX_DIST_NO_TELEPORT:
				#chat.AppendChat(3,"Sent Attack")
				net_packet.SendAttackPacket(vid,0)
				lst.remove(vid)
				vid_hits+=1
		
		return vid_hits
		#chat.AppendChat(3,"After: " + str(len(lst))) 
    
				
	def OnUpdate(self):
		val, self.lastTime = m2k_lib.timeSleep(self.lastTime,self.speed)
		#chat.AppendChat(3,str(self.speed))
		if(val and self.enableButton.isOn):
			#chat.AppendChat(3,"Loop")
			x,y,z = chr.GetPixelPosition(net.GetMainActorVID())
			lst = list()
   			for vid in net_packet.InstancesList:
				if not chr.HasInstance(vid):
					continue
				if self.playerClose.isOn and chr.GetInstanceType(vid) == m2k_lib.PLAYER_TYPE and vid != net.GetMainActorVID():
					return
				if self.MetinButton.isOn and chr.GetInstanceType(vid) != m2k_lib.METIN_TYPE:
					continue
				if player.GetCharacterDistance(vid) < self.range:	
					lst.append(vid)
			hit_counter = 0
			i = 0
			while len(lst) > 0 and hit_counter < self.maxMonster:
				vid = lst[0]
				mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
				if net_packet.IsPositionBlocked(mob_x,mob_y):
					lst.remove(vid)
					continue
				hit_counter+=self.TeleportAttack(lst,mob_x, mob_y, 15 + (i %2))
				#net_packet.SendStatePacket(x,y,0,1,0)
				i+=1
	
	def Close(self):
		self.Board.Hide()
		self.saveSettings()

Dmg = DmgHacks()
Dmg.Show()