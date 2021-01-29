import Movement
import ui,m2k_lib,ShopNPC,DmgHacks,player

class BotBase(ui.ScriptWindow):
	STATE_STOPPED = 0
	STATE_BOTTING = 1
	#STATE_GOING_SHOP = 2
	STATE_WATING = 3


	def __init__(self,time_wait=0.06):
		ui.ScriptWindow.__init__(self)
		self.Show()
		self.State = self.STATE_STOPPED
		self.time_wait = time_wait
		self.generalTimer = 0

		#Shop - Can be changed using callback by derived class
		self.onInvFullCallback = None #Will call this function before going to shop
		self.allowShopOnFullInv = False #Allow to go to shop when inventory full

		self.shopBuyItems = []
		self.shopSellItems = []


	def __SetStateBotting(self):
		self.State = self.STATE_BOTTING
		DmgHacks.Resume()
		self.Resume()

	def __SetStateStopped(self):
		self.State = self.STATE_STOPPED
		DmgHacks.Resume()
		self.Pause()

	def __SetStateShopping(self):
		self.State = self.STATE_WATING
		DmgHacks.Pause()
		self.Pause()

	
	#Setters
	#Enable to go shop on inventory full
	#Callback is a function called before going to shop
	def	SetShopOnInvFull(self,value,callback=None):
		self.allowShopOnFullInv = value
		if self.onInvFullCallback == None:
			self.onInvFullCallback = callback


	#Callbacks
	def _ResumeCallback(self):
		self.__SetStateBotting()



	#Functions for action
	def GoToShop(self):
		self.__SetStateShopping()
		if self.onInvFullCallback != None:
			self.onInvFullCallback()

		ShopNPC.RequestBusinessNPCAwayRestorePosition(self.shopBuyItems,self.shopSellItems,ShopNPC.GetGeneralShop(),callback=self._ResumeCallback)

		
	#Preform checks
	def DoChecks(self):
		if self.allowShopOnFullInv and m2k_lib.isInventoryFull() and self.CanPause():
			self.GoToShop()
			return True		
		
		return False

	#Abstract Function
	def Frame(self):
		pass

	def CanPause(self):
		pass

	def Resume(self):
		pass

	def Pause(self):
		pass

	def StartBot(self):
		return

	def StopBot(self):
		return


	def Start(self):
		self.StartBot()
		self.__SetStateBotting()

	def Stop(self):
		self.StopBot()
		self.__SetStateStopped()
		ShopNPC.StopAction()


	def OnUpdate(self):
		if self.STATE_STOPPED == self.State:
			return

		val, self.generalTimer = m2k_lib.timeSleep(self.generalTimer,self.time_wait)
		if not val:
			return

		if m2k_lib.GetCurrentPhase() != m2k_lib.PHASE_GAME:
			return

		if self.State == self.STATE_WATING:
			return

		if not self.DoChecks():		
			self.Frame()
