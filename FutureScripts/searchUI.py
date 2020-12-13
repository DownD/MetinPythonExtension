import ui,app,chat,chr,m2netm2g,player,item,skill,time,game,shop,chrmgr,thread,chatm2g

class SearchDialog(ui.ScriptWindow):

	SLOT_COUNT = 45
	STATE_SEARCH_PLAYERS = 1
	STATE_OPEN_SHOP = 2
	STATE_WAIT_SHOP_OPEN = 3
	STATE_WAIT_SHOP_CLOSE = 4
	STATE_END = 5
	State = 1
	PlayersVids = []
	Items = []
	PlayerIndex = 0
	PlayerVID = 0
	ATTEMPTS_WAIT = 1
	numAttempts = 0
	TIME_WAIT = 1
	MAX_DIST = 4000
 
	lastTime = 0

	class Item :
		def __init__(self, itemName, shopVID, count, price, slot):
			self.name = itemName
			self.shop = shopVID
			self.count = count
			self.price = price
			self.slot = slot

		def getStringFormat(self):
			return "Slot: " + str(self.slot) + "  Name: " + str(self.name) + "  Price: " + str(self.price) + " yang  Count: " + str(self.count) + " Shop VID: " + str(self.shop)
	
	def __init__(self):
		ui.ScriptWindow.__init__(self) 
		
		self.Board = ui.ThinBoard()
		self.Board.SetSize(218, 250)
		self.Board.SetCenterPosition()
		self.Board.AddFlag("movable")
		self.Board.Show()

		self.comp = Component()
		self.Header = self.comp.TextLine(self.Board, 'Buy & Sell Bot', 65, 8, self.comp.RGB(255, 255, 0))
		self.BarItems, self.ListBoxItems, ScrollItems = self.comp.ListBoxEx(self.Board, 10, 50, 170, 140)
		self.SkillIdNameLabel = self.comp.TextLine(self.Board, 'ID:        Name:', 16, 37, self.comp.RGB(255, 255, 255))
		
		self.Close = self.comp.Button(self.Board, '', 'Close', 183, 8, self.CloseWindow, 'd:/ymir work/ui/public/close_button_01.sub', 'd:/ymir work/ui/public/close_button_02.sub', 'd:/ymir work/ui/public/close_button_03.sub')
		self.Refresh = self.comp.Button(self.Board, '', 'Refresh', 163, 6, self.UpdateItemList, 'd:/ymir work/ui/game/guild/refresh_button_01.sub', 'd:/ymir work/ui/game/guild/refresh_button_02.sub', 'd:/ymir work/ui/game/guild/refresh_button_03.sub')
		self.StartButton = self.comp.Button(self.Board, 'Start', '', 70, 205, self.SetStatus, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.UpdateItemList()

	def CloseWindow(self):
		self.Board.Hide()
		self.Board.Destroy()

	def UpdateItemList(self):
		if not shop.IsOpen():
			chat.AppendChat(7, "[M2-BOB] Please open a Shop first!")
			return
    
		self.ListBoxItems.RemoveAllItems()
		for i in xrange(shop.SHOP_SLOT_COUNT):
			ItemIndex = shop.GetItemID(i)
			if ItemIndex != 0:
				ItemName = item.GetItemName(item.SelectItem(int(ItemIndex)))
				self.ListBoxItems.AppendItem(Item(str(ItemIndex) + '    ' + ItemName))
    
	def ScanPlayers(self):
		import chat, chr, shop, item, playerm2g2
		for x in xrange(0,10000000):
			instanceType = chr.GetInstanceType(x)
			test = chr.HasInstance(x)
			if test != 0 and instanceType == chr.INSTANCE_TYPE_PLAYER:
				#chat.AppendChat(3,"Name: " + str(chr.GetNameByVID(x)) + " IsShop: " +  str(shop.IsNonNPCShop()))
				self.PlayersVids.append(x)
		return


	def OpenShop(self,vid):
		import m2netm2g, chr
		f = open("log.txt","a")
		f.write('Opening Shop  ||  ')
		f.close()
		if self.IsShopOpen() == False and chr.HasInstance(vid):
			m2netm2g.SendOnClickPacket(vid)

	def IsShopOpen(self):
		import shop
		return shop.IsOpen()
    
	def CloseShop(self):
		import m2netm2g
		f = open("log.txt","a")
		f.write('Closeing Shop  ||  ')
		f.close()
		if self.IsShopOpen() == True:
			m2netm2g.SendShopEndPacket()

	def ScanShop(self,vid):
		import chat, chr, shop, item, playerm2g2, thread, m2netm2g

		#time = shop.GetTabCount()
		max_slot = (self.SLOT_COUNT) -1
		for x in xrange(0,max_slot):
			id = shop.GetItemID(x)
			if id != 0:
				price = shop.GetItemPrice(x)
				name = item.GetItemNameByVnum(id)
				count = shop.GetItemCount(x)
				it = self.Item(name,vid,count,price,x)
				self.Items.append(self.Item(name,vid,count,price,x))
				#chat.AppendChat(3,it.getStringFormat())
				#chat.AppendChat(3,"Slot: " + str(x) + "  Name: " + str(name) + "  Price: " + str(price) + " yang  Count: " + str(count))
        
	def OnUpdate(self):
		import chat, chr, playerm2g2, app
  
		currTime = app.GetTime()
		if currTime-self.lastTime < self.TIME_WAIT:
			return

		self.lastTime = currTime
		if self.State == self.STATE_SEARCH_PLAYERS:
			self.ScanPlayers()
			chat.AppendChat(3,"Scanned -> "+ str(self.PlayersVids.__len__()) + " players")
			if self.PlayersVids.__len__() == 0:
				self.State = self.STATE_OPEN_END
				return
			self.PlayerVID = self.PlayersVids[0]
			self.State = self.STATE_OPEN_SHOP
			return
        
		elif self.State == self.STATE_OPEN_SHOP:
			chat.AppendChat(3,"Opening Index-> "+ str(self.PlayerIndex))
			f = open("log.txt","a")
			f.write('Index: ' + str(self.PlayerIndex) + ' VID: ' + str(self.PlayerVID) + ' Distance: ' + str(playerm2g2.GetCharacterDistance(self.PlayerVID)) + ' Name: ' + str(chr.GetNameByVID(self.PlayerVID)) + '\n')
			f.close()
			self.OpenShop(self.PlayerVID)
			self.State = self.STATE_WAIT_SHOP_OPEN
			return
        
		elif self.State == self.STATE_WAIT_SHOP_OPEN:
			chat.AppendChat(3,"State Wait Open Shop")
			if self.numAttempts > self.ATTEMPTS_WAIT:
				chat.AppendChat(3,"Skipping Wait Open")
				f = open("log.txt","a")
				f.write('Possible not shop\n')
				f.close()
				self.numAttempts = 0
				self.State = self.STATE_WAIT_SHOP_CLOSE
				return
			if self.IsShopOpen() == True:
				self.State = self.STATE_WAIT_SHOP_CLOSE
				self.ScanShop(self.PlayerVID)
				self.CloseShop()
				self.numAttempts = 0
			else:
				self.numAttempts += 1 
			return
        
		elif self.State == self.STATE_WAIT_SHOP_CLOSE:
			chat.AppendChat(3,"State Wait Close Shop")
			if self.IsShopOpen() == False:
				self.numAttempts = 0
				self.State = self.STATE_OPEN_SHOP
				self.PlayerIndex += 1
				if self.PlayerIndex >= self.PlayersVids.__len__():
					self.State = self.STATE_END
					return
				self.PlayerVID = self.PlayersVids[self.PlayerIndex]
				return
			else:
				return
		
		elif self.State == self.STATE_END:
			chat.AppendChat(3,"Done, Scanned " + str(self.Items.__len__()) + " items")
			f = open("items.txt","w")
			_items = self.Items
			for x in _items:
			    f.write(str(x.getStringFormat())+ '\n')    			
			f.close()
			self.State = 99
			self.Board.Hide()
			self.Board.Destroy()
        
				
	def SetStatus(self):
		ItemIndex = self.ListBoxItems.GetSelectedItem()
		if ItemIndex:
			pass
		else:
			chat.AppendChat(7, "[M2-BOB] No Item selected!")
			return
			
		if not shop.IsOpen():
			chat.AppendChat(7, "[M2-BOB] Please open a Shop first!")
			return
		
		if self.State:
			self.State = 0
			self.StartButton.SetText("Start")
			self.SellRestItems()
		else:
			self.ItemID = int(ItemIndex.GetText().split("    ")[0])
			self.State = 1
			thread.start_new_thread(self.BuyAndSellItems,())
			self.StartButton.SetText("Stop")
			
	
	
	def BuyAndSellItems(self):
		while self.State == 1 and shop.IsOpen(): 
			for EachShopSlot in xrange(shop.SHOP_SLOT_COUNT): 
				getShopItemID = shop.GetItemID(EachShopSlot) 
				if getShopItemID == self.ItemID: 
					price = shop.GetItemPrice(EachShopSlot)
					if price <= player.GetMoney():
						m2netm2g.SendShopBuyPacket(EachShopSlot) 
						break
					else:
						self.State = 1
						self.StartButton.SetText("Stop")
			time.sleep(0.01)	# 0.1 = 100ms, 0.01 = 10ms
			self.SellRestItems()
		self.SellRestItems()		
							
	def SellRestItems(self):
		for EachInventorySlot in xrange(90): 
			ItemIndex = player.GetItemIndex(EachInventorySlot) 
			if ItemIndex == self.ItemID: 
				m2netm2g.SendShopSellPacket(EachInventorySlot)

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
		ListBox.SetViewItemCount(7)
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
	
x = SearchDialog()
x.Show()
