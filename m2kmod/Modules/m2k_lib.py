_chr = chr
import ui,chr,skill,time,game,shop,chrmgr
import app
import chat
import net
import player
import item
import background,constInfo,wndMgr,math,uiCommon,grp,dbg,snd
import net_packet,sys
#import pack
CONFIG = net_packet.PATH + 'm2kmod/Saves/config.m2k'
CONFIG_PRICE = net_packet.PATH + 'm2kmod/Saves/priceconfig.m2k'
ATTACK_RANGE = 250
METIN_TYPE = 2
MONSTER_TYPE = 0
PLAYER_TYPE = 6



def ReadConfig(Setting):
	f = open(CONFIG)
	#sys.stderr.write(CONFIG)
	
	
	with open(CONFIG,'a+') as search:
		for line in search:
			line = line.rstrip()  # remove '\n' at end of line
			if line.startswith(Setting):
				return line.split('=')[1]
		search.write(Setting + "=0\n")
		return 0



def SaveConfig(Setting, Value):
	sReader = open(CONFIG, 'r')
	sLines = file.readlines(sReader)
	sWriter = open(CONFIG, 'w')
	for Line in sLines:
		if Line.startswith(Setting + '='):
			Line = Setting + '=' + Value + '\n'
		sWriter.write(Line)
	sReader.close()
	sWriter.close()

def ReadAllElements(name,object):
    for attr in object.__dict__:
        if attr is int or attr is str:
            object.__dict__[attr] = ReadConfig(name + "." + str(attr))

def SaveAllElements(name,object):
    for attr in object.__dict__:
        if attr is int or attr is str:
            SaveConfig(name + "." + str(attr),object.__dict__[attr])
		
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
		
def imp_or_reload(name):
	import sys
	if name in sys.modules:
		return reload(sys.modules[name])
	return __import__(name)

		
def GetCurrentText(self):
	return self.textLine.GetText()
	
def OnSelectItem(self, index, name):
	self.SetCurrentItem(name)
	self.CloseListBox()
	self.event()
	
def GetSelectedIndex(self):
	return self.listBox.GetSelectedItem()
	
def GetItemByID(_id):
	for i in xrange(90,-1,-1):
		if player.GetItemIndex(i) == _id:
			return i
	return -1

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
    #angleInDegrees += math.pi
    
    #chat.AppendChat(3, "atan3:  "+str(angleInDegrees* (180 / math.pi)))
    #chat.AppendChat(3,str(angleInDegrees* (180 / math.pi)))
    #return (angle)

def RotateMainCharacter(x,y):
    my_x,my_y,my_z = player.GetMainCharacterPosition()
    chr.SelectInstance(player.GetMainCharacterIndex())
    rot = GetRotation(my_x,my_y,x,y)
    chr.SetRotation(rot)
    


#Extracts an encrypted eter pakcet to Extractor folder inside the client
def extractFile(path):
    import os
    initial_folder = "Extractor\\"
    file_location = initial_folder + path
    _str = net_packet.Get(path)
    
    if not os.path.exists(os.path.dirname(file_location)):
        os.makedirs(os.path.dirname(file_location))
        

    with open(file_location, "wb") as myfile:
        myfile.write(_str)
	
ui.ComboBox.GetCurrentText = GetCurrentText
ui.ComboBox.GetSelectedIndex = GetSelectedIndex
ui.ComboBox.OnSelectItem = OnSelectItem


class ByteMatrix:
    def __init__(self,max_x,max_y):
        self.buffer = bytearray(max_x*max_y)
        self.max_x = max_x
        self.max_y = max_y
        self.total_size = max_x*max_y
        
    def Get(self,x,y):
        if(x >= self.max_x):
            raise "Out of Bounds"
        
        return self.buffer[self.max_x*y + x]
    
    def Set(self,x,y,value):
        if(x >= self.max_x):
            raise "Out of Bounds"
        self.buffer[self.max_x*y + x] = value

class OnOffButton(ui.Button):
	def __init__(self,OffUpVisual, OffOverVisual, OffDownVisual,OnUpVisual, OnOverVisual, OnDownVisual, image=None,func=None):
		ui.Button.__init__(self)
		self.OffUpVisual = OffUpVisual
		self.OffOverVisual = OffOverVisual 
		self.OffDownVisual = OffDownVisual
		self.OnUpVisual = OnUpVisual
		self.OnOverVisual = OnUpVisual
		self.OnDownVisual = OnDownVisual
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

	def OnOffButton(self,parent,buttonName, tooltipText,x,y,func=None,image=None,OffUpVisual='m2kmod/Images/off_0.tga', OffOverVisual='m2kmod/Images/off_1.tga', OffDownVisual='m2kmod/Images/off_2.tga',OnUpVisual='m2kmod/Images/on_0.tga', OnOverVisual='m2kmod/Images/on_1.tga', OnDownVisual='m2kmod/Images/on_2.tga'):
		if image != None:
			image = self.ExpandedImage(parent,x,y,image)
			x += 15
			y += 15

		button = OnOffButton(OffUpVisual, OffOverVisual, OffDownVisual,OnUpVisual, OnOverVisual, OnDownVisual,image=image,func=func)
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetText(buttonName)
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

	def ExpandedImage(self, parent, x, y, img):
		image = ui.ExpandedImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
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
		return TRUE
		
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