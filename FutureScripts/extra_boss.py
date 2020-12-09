import net_packet,ui,net,chr,player,chat
import m2k_lib, uiToolTip

ATTACK_MAX_DIST_NO_TELEPORT = 290

MOVING_TO_TARGET = 1
ATTACKING_TARGET = 0
TARGET_IS_DEAD = -1


#Make a copy of an item in the inventory
class SlotWithToolTip(ui.SlotWindow):
	def __init__(self,parent,x,y,slotIndex,display_count=False):
		import uiToolTip,player
		ui.SlotWindow.__init__(self)
		self.SetParent(parent)
		self.SetSize(32, 32)
		#self.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.AppendSlot(slotIndex, 0, 0, 32, 32)
		self.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.SetPosition(x, y)
		if display_count:
			count = player.GetItemCount(slotIndex)
		else:
			count = 0
		self.SetItemSlot(slotIndex, player.GetItemIndex(slotIndex), count)
		self.RefreshSlot()
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.Show()

	def OverInItem(self,slotIndex):
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.SetInventoryItem(slotIndex)
		self.tooltipItem.ShowToolTip()

	def OverOutItem(self):
		self.tooltipItem.HideToolTip()

	def __del__(self):
		self.Hide()
		ui.SlotWindow.__del__(self)

class DmgHacks(ui.ScriptWindow):

	STATE_BOSS_KILLED = 0
	STATE_SEARCHING_BOSS = 1
	STATE_BOSS_FOUND = 2
	STATE_WAIT_LOADING = 3
 
	CH_CHANGE = 1
	SCROLL_CHANGE = 2

	def __init__(self):
		import m2k_lib
		ui.Window.__init__(self)
		self.x_size = 300
		self.State = self.STATE_SEARCHING_BOSS
		self.LastChange = self.SCROLL_CHANGE
		self.CurrScrollIndex = 0
		self.currIndexScroll = 0
		self.ScrollList = list()
		self.BuildWindow()
		self.TargetBoss = -1
		self.DelayAfterKill = 1.5
		self.wasLoading = 1
		self.timeChangeCH = 5

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(self.x_size, 220)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName('BossHunter')
		self.Board.SetCloseEvent(self.Close)
		self.Board.Show()
		self.comp = m2k_lib.Component()

		self.enableButton = self.comp.OnOffButton(self.Board, '', '', 130, 160, OffUpVisual='m2kmod/Images/start_0.tga', OffOverVisual='m2kmod/Images/start_1.tga', OffDownVisual='m2kmod/Images/start_2.tga',OnUpVisual='m2kmod/Images/stop_0.tga', OnOverVisual='m2kmod/Images/stop_1.tga', OnDownVisual='m2kmod/Images/stop_2.tga' )
		self.Refresh = self.comp.Button(self.Board, '', 'Refresh', self.x_size-50, 8, self.updateListScrolls, 'd:/ymir work/ui/game/guild/refresh_button_01.sub', 'd:/ymir work/ui/game/guild/refresh_button_02.sub', 'd:/ymir work/ui/game/guild/refresh_button_03.sub')
		self.warningMessage = self.monsterNum = self.comp.TextLine(self.Board, 'IMPORTANT: Deselect any unused scrolls', 50, 100, self.comp.RGB(255, 255, 255))
		self.ChLabel = self.comp.TextLine(self.Board, "Number of CH's", 85, 131, self.comp.RGB(255, 255, 255))
		self.editCh ,self.maxCH = self.comp.EditLine(self.Board, '6', 160, 131, 30, 14, 7)
		self.enableButton.SetOff()
		#self.tooltipItem = uiToolTip.ItemToolTip()
		#self.tooltipItem.Hide()

		#self.loadSettings()
		#self.Speed_func()
		#self.Range_func()
		#self.Monster_func()
		#chat.AppendChat(3,str(self.Board))
		self.updateListScrolls()

		self.timeOut = m2k_lib.GetTime()
		self.sleepTime = m2k_lib.GetTime()
		self.sleepAfterKillTime = m2k_lib.GetTime()

	def updateListScrolls(self):
		import m2k_lib,player
		global SlotWithToolTip
		self.enableButton.SetOff()
		scrollID = int(m2k_lib.ReadConfig("Scroll-Location"))
		if scrollID == 0:
			chat.AppendChat(3,"Scroll-Location id is not set, go to config.m2k and set the correct Scoll-Location ID")
			return

		Scrolls = list()
		for i in xrange(45):
			ItemIndex = player.GetItemIndex(i)
			if ItemIndex == scrollID:
				Scrolls.append(i)
    
		#Delete current scrolls
		for x in self.ScrollList:
			button, ui_scroll = x
			button.Hide()
			ui_scroll.Hide()
		
		del self.ScrollList

		self.ScrollList = list()
		if len(Scrolls)>self.x_size/32:
			var = len(Scrolls) - self.x_size/32
			Scrolls[:-var]

		step = (self.x_size - (len(Scrolls)*32))/(len(Scrolls)+1)
		x = step
		y = 50
		for item in Scrolls:
			ui_scroll = SlotWithToolTip(self.Board,x,y,item,True)
			button = self.comp.OnOffButton(self.Board,'','',x+10,y+30)
			button.item_slot = item
			self.ScrollList.append((button,ui_scroll))
			x+= step + 32
		self.currIndexScroll = 0
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()

	def ChangeNextLocation(self):
		import chat,net
		i = 0
		while i<len(self.ScrollList):
			self.currIndexScroll = (self.currIndexScroll + 1)%len(self.ScrollList)
			if(self.ScrollList[self.currIndexScroll][0].isOn):
				self.LastChange = self.SCROLL_CHANGE
				net.SendItemUsePacket(self.ScrollList[self.currIndexScroll][0].item_slot)	
				return True
			i+=1
		return False
  
	def ChangePlaceOrCh(self):
		import m2k_lib
		currCh = m2k_lib.GetCurrentChannel()
		self.State = self.STATE_WAIT_LOADING
		self.timeOut = m2k_lib.GetTime()
		if currCh == int(self.maxCH.GetText()):
			if self.LastChange == self.CH_CHANGE:
				if self.ChangeNextLocation():
					return
			m2k_lib.ChangeChannel(currCh%int(self.maxCH.GetText())+1)
			self.LastChange = self.CH_CHANGE
		else:
			m2k_lib.ChangeChannel(currCh%int(self.maxCH.GetText())+1)
			self.LastChange = self.CH_CHANGE
				
				
	def OnUpdate(self):
		import m2k_lib,net_packet,chat,player,net
		if not self.enableButton.isOn:
			return
  		val, self.sleepTime = m2k_lib.timeSleep(self.sleepTime,0.5)
		if(val):
			chat.AppendChat(3,str(self.State))
			
			if self.State == self.STATE_BOSS_FOUND:
				target_state = m2k_lib.AttackTarget(self.TargetBoss)
				if target_state == m2k_lib.TARGET_IS_DEAD:
					self.sleepAfterKillTime = m2k_lib.GetTime()
					self.State = self.STATE_BOSS_KILLED
			elif self.State == self.STATE_BOSS_KILLED:
				player.PickCloseItem()
				val1, self.sleepAfterKillTime = m2k_lib.timeSleep(self.sleepAfterKillTime,self.DelayAfterKill)
				if val1:
					self.ChangePlaceOrCh()
			elif self.State == self.STATE_SEARCHING_BOSS:
				self.TargetBoss = m2k_lib.getClosestInstance(m2k_lib.BOSS_TYPE,False)
				if self.TargetBoss !=-1:
					m2k_lib.AttackTarget(self.TargetBoss)
					self.State = self.STATE_BOSS_FOUND
				else:
					self.ChangePlaceOrCh()
			elif self.State == self.STATE_WAIT_LOADING:
				currTime = m2k_lib.GetTime()
				if self.timeOut + self.timeChangeCH < currTime:
					self.State = self.STATE_SEARCHING_BOSS
					if len(net_packet.InstancesList) > 0:
						self.State = self.STATE_SEARCHING_BOSS
			
    

	
	def Close(self):
		self.Board.Hide()
		self.__del__()

Dmg = DmgHacks()
Dmg.Show()

#currCh = 4
#chat.AppendChat(3,str((currCh%(int(6)))+1))
