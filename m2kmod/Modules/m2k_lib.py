_chr = chr
from m2kmod.Modules.Hooks import Hook
import Hooks
import ui,chr,time,app, net, player,wndMgr,math,snd,net_packet,uiToolTip,item,FileManager,event,chat
from datetime import datetime
#import pack

CONFIG = net_packet.PATH + 'm2kmod/Saves/config.m2k'
CONFIG_PRICE = net_packet.PATH + 'm2kmod/Saves/priceconfig.m2k'
CONFIG_BOSSES_ID = net_packet.PATH + 'm2kmod/Saves/boss_ids.txt'
CONFIG_PSHOP_AUTO_BUY = net_packet.PATH + 'm2kmod/Saves/search_items_max_price.txt'
CONFIG_SHOP_CREATOR = net_packet.PATH + 'm2kmod/Saves/item_sell_prices.txt'
SHOP_CREATOR_LOG = net_packet.PATH + 'm2kmod/Saves/shop_log.txt'

ATTACK_RANGE = 270

#Types
METIN_TYPE = 2
MONSTER_TYPE = 0
PLAYER_TYPE = 6
BOSS_TYPE = -1

BOSS_IDS = dict()
#SEARCH_ITEMS_MAX_PRICE = dict()

MAX_INVENTORY_SIZE = 90
MAX_TELEPORT_DIST = 2400

MIN_RACE_SHOP = 30000
MAX_RACE_SHOP = 30008

PHASE_GAME = 5


#Minumum number of empty slots for the inventory to be considered full
INV_FULL_MIN_EMPTY = 10
MAX_ITEM_COUNT = 200

#Maximum distance to pickup before telport
MAX_PICKUP_DIST = 290



            
def isBoss(vnum):
    if chr.GetVirtualNumber(vnum) in BOSS_IDS:
        return True
    else:
        return False
        

#def Debug(self,*args):
		
def CreateLogininfo(id,pw,name,slot,ch,autologin):
	os.remove("logininfo.xml")
	f = file('logininfo.xml', 'w')
	f.write('<logininfo name="'+name+'" channel_idx="'+ch+'">\n')
	f.write('<id>'+id+'</id>\n')
	f.write('<pwd>'+pw+'</pwd>\n')
	f.write('<slot>'+slot+'</slot>\n')
	f.write('<auto_login>'+autologin+'</auto_login>\n')
	f.write('</logininfo>\n')
	f.close()


def DebugPrint(arg):
	with open("Log.txt","a") as f:
		f.write(str(datetime.now())+": "+arg+"\n")


def Revive():
	net.SendCommandPacket(5,1)

#Given the price in "kk" the function will return the price in wons and yang
#Example:
# "435kk" -> 4, 35000000 
def ConvertPrice(price_str,item_num=1):
	multiplier = price_str.count("k")	
	yang = float(price_str.replace("k",""))
	yang *= 1000**multiplier
	yang  *= item_num
	#yang = int(yang)
	#chat.AppendChat(3,str(yang))

	wons = int(yang/100000000)
	if(wons > 0):
		rest_yang = int(yang % (wons*100000000))
	else:
		rest_yang = int(yang)

	return (wons,rest_yang)


	
def GetClass():
	race = net.GetMainActorRace()
	group = net.GetMainActorSkillGroup()
	if race == 0 or race == 4:
		return "Warrior" + "/" + str(group)
	elif race == 1 or race == 5:
		return "Assassin" + "/" + str(group)
	elif race == 2 or race == 6:
		return "Sura" + "/" + str(group)
	elif race == 3 or race == 7:
		return "Shaman" + "/" + str(group)
		
def NewSkillsEnable():
	RaceGroupInfo = GetClass()
	Class = str(RaceGroupInfo).split("/")[0]
	if str(Class) == "Shaman" or str(Class) == "Sura":
		return 6
	else:
		return 5

#Skip python select answers
def skipAnswers(event_answers,hook=False):
	if hook:
		Hook.questHook.HookFunction()
	for index,answer in enumerate(event_answers,start=1):
		event.SelectAnswer(index,answer)

		
def GetCurrentText(self):
	return self.textLine.GetText()

def OnSelectItem(self, index, name):
	self.SetCurrentItem(name)
	self.CloseListBox()
	self.event()
	
def GetSelectedIndex(self):
	return self.listBox.GetSelectedItem()



#Checks if inventory is full by checking empty spaces
def isInventoryFull():
	numItems = MAX_INVENTORY_SIZE
	for i in range(0,MAX_INVENTORY_SIZE):
		curr_id = player.GetItemIndex(i)
		if curr_id != 0:
			numItems-=1
	
	if numItems < INV_FULL_MIN_EMPTY:
		return True
	else:
		return False
	
#return -1 on error
def GetItemByType(_id):
	for i in range(0,MAX_INVENTORY_SIZE):
		curr_id = player.GetItemIndex(i)
		if curr_id == 0:
			continue
		item.SelectItem(curr_id)
		if item.GetItemType() == _id:
			return i
	return -1

def UseAnyItemByID(id_list):
	for i in range(0,MAX_INVENTORY_SIZE):
		if player.GetItemIndex(i) in id_list:
			net.SendItemUsePacket(i)
	return -1


def GetItemByID(_id):
	for i in range(0,MAX_INVENTORY_SIZE):
		if player.GetItemIndex(i) == _id:
			return i
	return -1

def isItemTypeOnSlot(_type,invType = player.EQUIPMENT,slot=item.EQUIPMENT_WEAPON):
	idx = player.GetItemIndex(invType,slot)
	if idx != 0:
		item.SelectItem(idx)
		if item.GetItemType() == _type:
			return True
	return False

#returns a dicitionary containing the positions of each id in _id_list
def GetItemsSlotsByID(_id_list):
	result = {_id : [] for _id in _id_list}
	for i in range(0,MAX_INVENTORY_SIZE):
		id = player.GetItemIndex(i)
		if player.GetItemIndex(i) in _id_list:
			result[id].append(i)
	return result


#Return the angle needed to rotate from x0,y0 to x1,y1
def GetRotation(x0,y0,x1,y1):
    x1_relative = x1-x0
    y1_relative = y1-y0
    try:
        rada = 180 * (math.acos(y1_relative/math.sqrt((x1_relative)**2 + (y1_relative)**2))) / math.pi + 180
        if x0 >= x1:
            rada = 360 - rada
    except:
        rada = 0
    return rada

#Rotate Main Character to  x,y
def RotateMainCharacter(x,y):
    my_x,my_y,my_z = player.GetMainCharacterPosition()
    chr.SelectInstance(player.GetMainCharacterIndex())
    rot = GetRotation(my_x,my_y,x,y)
    chr.SetRotation(rot)
    
    
def GetCurrentPhase():
    return Hooks.GetCurrentPhase()

def IsInGamePhase():
	return GetCurrentPhase() == PHASE_GAME

def isPlayerCloseToInstance(vid_target):
	my_vid = net.GetMainActorVID()
	target_x,target_y,zz = chr.GetPixelPosition(vid_target) 
	for vid in net_packet.InstancesList:
		if not chr.HasInstance(vid):
			continue
		if chr.GetInstanceType(vid) == PLAYER_TYPE and vid != my_vid:
			curr_x,curr_y,z = chr.GetPixelPosition(vid)
			distance = dist(target_x,target_y,curr_x,curr_y)
			if(distance < 300):
				return True
	
	return False
		
def getClosestInstance(_type,is_unblocked=True):
	(closest_vid,_dist) = (-1,999999999)
	for vid in net_packet.InstancesList:
		if not chr.HasInstance(vid):
			continue
		if is_unblocked:
			mob_x,mob_y,mob_z = chr.GetPixelPosition(vid)
			if net_packet.IsPositionBlocked(mob_x,mob_y):
				continue
		this_distance = player.GetCharacterDistance(vid)
		if net_packet.IsDead(vid):
			continue

		type = chr.GetInstanceType(vid)
		if type in _type or (BOSS_TYPE in type and isBoss(vid)):
			if this_distance < _dist and not isPlayerCloseToInstance(vid):
				_dist = this_distance
				closest_vid = vid
	
	return closest_vid
    
MOVING_TO_TARGET = 1
ATTACKING_TARGET = 0
TARGET_IS_DEAD = -1

#Retuns -1 if is dead, 0 if attacking target or 1 if moving to target
def AttackTarget(vid):
    if net_packet.IsDead(vid):
        return TARGET_IS_DEAD
    mob_x,mob_y,mob_z = chr.GetPixelPosition(vid)
    if player.GetCharacterDistance(vid) < ATTACK_RANGE:
        Movement.StopMovement()
        RotateMainCharacter(mob_x,mob_y)
        player.SetAttackKeyState(True)
        return ATTACKING_TARGET
    else:
        player.SetAttackKeyState(False)
        Movement.GoToPositionAvoidingObjects(mob_x,mob_y)
        return MOVING_TO_TARGET
        

#Extracts an encrypted eter pakcet to Extractor folder inside the client
def extractFile(path):
    import os
    initial_folder = net_packet.PATH+"Extractor\\"
    file_location = initial_folder + path
    file_location = file_location.replace(":","")
    _str = net_packet.Get(path)
    
    if not os.path.exists(os.path.dirname(file_location)):
        os.makedirs(os.path.dirname(file_location))
        

    with open(file_location, "wb") as myfile:
        myfile.write(_str)


#Return point between 2 points at the specified distance from x1,y1
#If overflow=False and dist_ is bigger then the distance between the 2 points
#the function will return x2,y2, otherwise it will return a point beyond x2,y2
def getPointsDistance(x1,y1,x2,y2,dist_,allow_overflow=False):
	d = dist(x1,y1,x2,y2)
	if(d < 0.0001):
		return(x1,y1)
	if not allow_overflow:
		if (dist_>d):
			return (x2,y2)
	ux = (x2-x1)/d
	uy = (y2-y1)/d

	x = ux*dist_ + x1
	y = uy*dist_ + y1
	return (x,y)
	
ui.ComboBox.GetCurrentText = GetCurrentText
ui.ComboBox.GetSelectedIndex = GetSelectedIndex
ui.ComboBox.OnSelectItem = OnSelectItem


#func is a callback that give responsabilty to the caller for changing the state
#funcState is a callback that automatically changes the sate and pass it (the new state) as argument
class OnOffButton(ui.Button):
	def __init__(self,OffUpVisual, OffOverVisual, OffDownVisual,OnUpVisual, OnOverVisual, OnDownVisual, image=None,func=None,tooltip=None,funcState=None):
		ui.Button.__init__(self)
		self.OffUpVisual = OffUpVisual
		self.OffOverVisual = OffOverVisual 
		self.OffDownVisual = OffDownVisual
		self.OnUpVisual = OnUpVisual
		self.OnOverVisual = OnUpVisual
		self.OnDownVisual = OnDownVisual
		self.FuncState = funcState
		self.isOn = 1
		self.ExpandedImage = image 
		self.SetOn()
		if(func == None):
			self.SetEvent(self.OnChange)
		else:
			self.SetEvent(func)

	def OnChange(self):
		if self.isOn == 1:
			self.SetOff()
		else:
			self.SetOn()

		if self.FuncState != None:
			self.FuncState(self.isOn)

	def SetValue(self,val):
		if val == 1:
			self.SetOn()
		else:
			self.SetOff()

	def SetOn(self):
		self.SetUpVisual(self.OnUpVisual)
		self.SetOverVisual(self.OnOverVisual)
		self.SetDownVisual(self.OnDownVisual)
		self.isOn = 1

	def SetOff(self):
		self.SetUpVisual(self.OffUpVisual)
		self.SetOverVisual(self.OffOverVisual)
		self.SetDownVisual(self.OffDownVisual)
		self.isOn = 0
	def __del__(self):
		self.Hide()
		if self.image != None:
			self.image.Hide()
			self.image.__del__()
		ui.Button.__del__(self)
	
class SlotWithToolTip(ui.SlotWindow):
	def __init__(self,x,y,vnum,count,slotIndex,parent):
		slot = ui.SlotWindow.__init__(self)
		slot.SetParent(parent)
		slot.SetSize(32, 32)
		slot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		slot.AppendSlot(slotIndex, 0, 0, 32, 32)
		slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		slot.SetPosition(x, y)
		slot.SetItemSlot(slotIndex, vnum, count)
		slot.RefreshSlot()
		self.tooltipItem = uiToolTip.ItemToolTip()
		slot.Show()

	def OverInItem(self,slotIndex):
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.SetInventoryItem(slotIndex)
		self.tooltipItem.ShowToolTip()

	def OverOutItem(self):
		self.tooltipItem.HideToolTip()
		
class Component:

	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def OnOffButton(self,parent,buttonName, tooltipText,x,y,func=None,image=None,OffUpVisual='m2kmod/Images/off_0.tga', OffOverVisual='m2kmod/Images/off_1.tga', OffDownVisual='m2kmod/Images/off_2.tga',OnUpVisual='m2kmod/Images/on_0.tga', OnOverVisual='m2kmod/Images/on_1.tga', OnDownVisual='m2kmod/Images/on_2.tga',xImgOffset = 15,yImgOffset = 15,funcState=None):
		if image != None:
			image = self.ExpandedImage(parent,x,y,image)
			x += xImgOffset
			y += yImgOffset

		button = OnOffButton(OffUpVisual, OffOverVisual, OffDownVisual,OnUpVisual, OnOverVisual, OnDownVisual,image=image,func=func,funcState=funcState)
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetText("                "+ str(buttonName))
		button.SetToolTipText(tooltipText)
		#button.SetEvent(func)
		button.Show()
		return button	

		
	def HideButton(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.SetEvent(func)
		return button

	def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, UpVisual, OverVisual, DownVisual):
		button = ui.ToggleButton()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetToggleUpEvent(funcUp)
		button.SetToggleDownEvent(funcDown)
		return button

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(8, 2)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.SetIMEFlag(3)
		Value.Show()
		return SlotBar, Value
		
	def OnlyEditLine(self, parent, width, heigh, x, y, editlineText, max):
		Value = ui.EditLine()
		if parent != None:
			Value.SetParent(parent)
		Value.SetSize(width, heigh)
		Value.SetPosition(x, y)
		Value.SetMax(max)
		Value.SetText(editlineText)
		Value.SetNumberMode()
		Value.Show()
		return Value

	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.SetOutline()
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

	def SliderBar(self, parent, sliderPos, func, x, y):
		Slider = ui.SliderBar()
		if parent != None:
			Slider.SetParent(parent)
		Slider.SetPosition(x, y)
		Slider.SetSliderPos(sliderPos)
		Slider.Show()
		Slider.SetEvent(func)
		return Slider

	def ExpandedImage(self, parent, x, y, img, tooltip=None):
		image = ui.ExpandedImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
		#image.SetToolTipText(tooltip)
		return image
		
	def ComboBoxFunc(self, parent, text, x, y, width, func):
		combo = ui.ComboBox()
		if parent != None:
			combo.SetParent(parent)
		combo.SetPosition(x, y)
		combo.SetSize(width, 15)
		combo.SetCurrentItem(text)
		combo.SetEvent(func)
		combo.Show()
		return combo
		
	def ComboBox(self, parent, text, x, y, width):
		combo = ui.ComboBox()
		if parent != None:
			combo.SetParent(parent)
		combo.SetPosition(x, y)
		combo.SetSize(width, 15)
		combo.SetCurrentItem(text)
		combo.Show()
		return combo

	def ThinBoard(self, parent, moveable, x, y, width, heigh, center):
		thin = ui.ThinBoard()
		if parent != None:
			thin.SetParent(parent)
		if moveable == TRUE:
			thin.AddFlag('movable')
			thin.AddFlag('float')
		thin.SetSize(width, heigh)
		thin.SetPosition(x, y)
		if center == TRUE:
			thin.SetCenterPosition()
		thin.Show()
		return thin

	def Gauge(self, parent, width, color, x, y):
		gauge = ui.Gauge()
		if parent != None:
			gauge.SetParent(parent)
		gauge.SetPosition(x, y)
		gauge.MakeGauge(width, color)
		gauge.Show()
		return gauge
		
	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width + 20, heigh)
		bar.SetColor(1996488704)
		bar.Show()
		ListBox = ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetViewItemCount(11)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(bar)
		scroll.SetPosition(width + 5, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return (bar, ListBox, scroll)

	def ListBoxEx2(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width + 20, heigh)
		bar.SetColor(1996488704)
		bar.Show()
		ListBox = ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetViewItemCount(5)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(bar)
		scroll.SetPosition(width + 5, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return (bar, ListBox, scroll)	
		
	def FileListBox(self, parent, x, y, width, heigh, count):
		ListBox = ui.ListBoxEx()
		ListBox.SetParent(parent)
		ListBox.SetPosition(x, y)
		ListBox.SetViewItemCount(count)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width - 20, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return ListBox, scroll
		
	def ReadingListBox(self, parent, x, y, width, heigh, count):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width + 20, heigh)
		bar.Show()
		ListBox = ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(10, 13)
		ListBox.SetViewItemCount(count)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		return bar, ListBox



#Get current time in seconds
def GetTime():
    return time.clock()

#Return a tupple, the first value is true or false according if the timer has been reached, and the second value is the current timer
#if first value is true or the old timer if false
def timeSleep(last_time,sleepTime):
    timer = time.clock()
    if(last_time<timer-sleepTime):
        return(True,timer)
    return(False,last_time)

#Writes to a file located in Extractor folder inside client folder
def extractFile(path):
    import os
    initial_folder = "Extractor\\"
    file_location = initial_folder + path
    _str = net_packet.Get(path)
    
    if not os.path.exists(os.path.dirname(file_location)):
        os.makedirs(os.path.dirname(file_location))
        

    with open(file_location, "wb") as myfile:
        myfile.write(_str)


def dist(x1,y1,x2,y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def GetCurrentChannel():
	try:
		return int(net.GetServerInfo().split(',')[1][3:])
	except:
		return 0

#def ChangeChannel(val):
#    net.SendChatPacket('/ch ' + str(val))

class WaitingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime
		self.Show()		

	def Close(self):
		self.Hide()

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)
		
	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			return
		
	def OnPressExitKey(self):
		self.Close()
		return True
		
class Item(ui.ListBoxEx.Item):
	def __init__(self, fileName):
		ui.ListBoxEx.Item.__init__(self)
		self.canLoad=0
		self.text=fileName
		self.textLine=self.__CreateTextLine(fileName)          

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.text

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(0, 0)
		textLine.SetText(fileName)
		textLine.Show()
		return textLine	

class EterPackOperator(object):

	def __init__(self, filename):
		#if not pack.Exist(filename):
			#raise IOError, 'No file or directory'
		self.data = self.GetTextFile(filename)
		self.data=_chr(10).join(self.data.split(_chr(13)+_chr(10)))
 
	def read(self, len = None):
		if not self.data:
			return ''
		if len:
			tmp = self.data[:len]
			self.data = self.data[len:]
			return tmp
		else:
			tmp = self.data
			self.data = ''
			return tmp

	def readlines(self):
		Array = str(self.data).split("\n")
		return Array
		
	def getline(self, line):
		return self.readlines()[line - 1]
		
	def getlinecount(self):
		return len(self.readlines())

	def GetTextFile(self, file):
		tmp = []
		try:
			Handle = app.OpenTextFile(file)
			CountLines = app.GetTextFileLineCount(Handle)
		except:
			return ""
		for i in xrange(CountLines):
			line = app.GetTextFileLine(Handle, i)
			if line != "":
				tmp.append(line + "\n")
		app.CloseTextFile()
		return("".join(tmp))
		
class SkillButton(ui.Window):

	def __init__(self, layer = "UI"):
		ui.Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None

		self.ButtonText = None
		self.ToolTipText = None

	def __del__(self):
		ui.Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = ui.__mem_func__(func)
		self.eventArgs = args
		
	def SetEvent(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def SetTextColor(self, r, b, g):
		if not self.ButtonText:
			return
		self.ButtonText.SetFontColor(r, g, b)

	def SetButtonFontName(self, font):
		if not self.ButtonText:
			return
		BackUpText = self.ButtonText.GetText()	
		self.ButtonText.SetFontName(font)
		self.ButtonText.SetText("")
		self.ButtonText.SetText(str(BackUpText))		
		
	def SetText(self, text, height = 4):
		if not self.ButtonText:
			self.ButtonText = ui.TextLine()
			self.ButtonText.SetParent(self)
			self.ButtonText.SetPosition(self.GetWidth() / 2, self.GetHeight() / 2)
			self.ButtonText.SetVerticalAlignCenter()
			self.ButtonText.SetHorizontalAlignCenter()
			self.ButtonText.Show()

		self.ButtonText.SetText(text)

	def SetTextPosition(self, x, y):
		self.ButtonText.SetPosition(self.GetWidth() / 2 + int(x), self.GetHeight() / 2 + int(y))		
		
	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:		
			toolTip = ui.createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):		
		self.ToolTipText = toolTip		
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()
			
	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)

#LoadDictFile(CONFIG_PSHOP_AUTO_BUY,SEARCH_ITEMS_MAX_PRICE,float)



FileManager.LoadDictFile(CONFIG_BOSSES_ID,BOSS_IDS,int)
import Movement