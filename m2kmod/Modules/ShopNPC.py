import net_packet,ui,net,chr,player,chat,shop,event,background
import m2k_lib, Movement, Hooks, MapManager



STATE_NONE = 0
STATE_WAITING_OPEN_SHOP = 1
STATE_BUYING = 2
STATE_SELLING = 3
STATE_FINISH_SHOPPING = 4
STATE_GIVING_ITEMS = 5

#Tim after each loop
TIME_WAIT = 0.2

#Time Buy
TIME_BUY = 0.55

TIME_SELL = 0.55
TIME_GIVE_ITEM = .5


#NPC OPTIONS
#Creates an NPC action
#If map of the npc is unknown
#If the position is not specified it will find the closest NPC on that map
class NPCAction:
	def __init__(self,race,position=None,event_answer=[],_map=None):
		self.race = race
		self.event_answer = event_answer
		self.position = position
		self.mapName = _map

		if self.mapName == None:
			map_path,self.mapName = MapManager.GetClosestMapPathWithNPC(self.race)

		if self.position == None:
			self.position=MapManager.GetNpcFromMap(self.mapName,self.race)

		#m2k_lib.DebugPrint("[NPC-ACTION] - New NPC Action race "+str(self.race)+" on map " + str(self.mapName) + " at position "+ str(self.position))

	def GetNpcPosition(self):
		return self.position

	def DoAction(self):
		vid = self.SearchVIDClosest()
		if vid:
			m2k_lib.DebugPrint("[NPC-ACTION] - Doing NPC Action")
			net.SendOnClickPacket(vid)
			m2k_lib.skipAnswers(self.event_answer)
			return True
		return False

	def GoToPosition(self,callback=None):
		return Movement.GoToPositionAvoidingObjects(self.position[0],self.position[1],mapName=self.mapName,callback=callback)


#Gets the closest vid from the race
#if the race doesn't exist closeby returns None
	def SearchVIDClosest(self):
		npcs = dict()
		for vid in net_packet.InstancesList:
			chr.SelectInstance(vid)
			curr_race = chr.GetRace()
			if self.race == curr_race:
				dist = player.GetCharacterDistance(vid)
				npcs[vid] = dist
		if len(npcs) == 0:
			return None
		min_vid = min(npcs.keys(), key=(lambda k: npcs[k]))
		return min_vid

#This should be passed in the interface function to select the NPC
#First value is race, second value is the SelectAnswer arguments as a tupple, provide None if not needed


def GetFishermanShop():
	return NPCAction(9009,event_answer=[1])

def GetFishermanUpgrade():
	return NPCAction(9009,event_answer=[0,0])

def GetFishermanCarpa():
	return NPCAction(9009,event_answer=[5,0])

def GetGeneralShop():
	return NPCAction(9003,event_answer=[0,0])


#FISHERMAN_SHOP = NPCAction(9009,event_answer=[1])
#FISHERMAN_UPGRADE = NPCAction(9009,[77200,47200],event_answer=[0,0],_map='metin2_map_c1')
#GENERAL_SHOP = NPCAction(9003,[36400,31800],[0,0],_map='metin2_map_c1')



#Call SetOrder to set npc and order and call StartNPCBusiness aftwerwards to start business
class ShopNPCDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Show()
		self.lastTime = 0
		self.buyItems_list =list()
		self.sellItems_list =list()
		self.giveItems_list =list()
		self.ableToBuy = True
		self.State = STATE_NONE
		self.vid = 0
		self.lastTimeBuy = 0
		self.callback = None
		self.npcAction = 0
		self.lastTimeSell = 0
		self.lastTimeGive = 0
		


	def OpenShop(self):
		return self.npcAction.DoAction()

	def StartNPCBusiness(self,open_shop=True):
		Hooks.questHook.HookFunction()
		if open_shop:
			if not self.OpenShop():
				self.State = STATE_FINISH_SHOPPING
				chat.AppendChat(3,"[ShopNPC] NPC with Race:"+str(self.npcAction.race)+" is not close by")
				return False
		self.State = STATE_WAITING_OPEN_SHOP
		return True

	#Needs to be called before StartNPCBusiness
	def SetOrder(self,npc_action,buy_list,sell_list,callback=None):
		self.buyItems_list = list(buy_list)
		self.sellItems_list = list(sell_list)
		self.npcAction = npc_action
		self.callback = callback


	def EndNPCBusiness(self):
		if(self.callback != None):
			self.callback()
			self.callback = None
			#chat.AppendChat(3,"Calling callback")
		self.State = STATE_NONE
		net.SendShopEndPacket()
		Hooks.questHook.UnhookFunction()

	#Give Item Stuff
	def SetGiveItemsToNPC(self,npc_action,give_items_list,callback=None):
		self.giveItems_list = give_items_list
		self.npcAction = npc_action
		self.callback = callback

	def StartNPCGiveItem(self):
		Hooks.questHook.HookFunction()
		self.State = STATE_GIVING_ITEMS
		return True

	def EndNPCGiveItem(self):
		if(self.callback != None):
			self.callback()
			self.callback = None
		self.State = STATE_NONE
		Hooks.questHook.UnhookFunction()
		return True


	def OnUpdate(self):
		val, self.lastTime = m2k_lib.timeSleep(self.lastTime,TIME_WAIT)
		if not val or self.State == STATE_NONE or not m2k_lib.IsInGamePhase():
			return
		if self.State == STATE_WAITING_OPEN_SHOP:
			#chat.AppendChat(3,"Waiting for shop to be open.")
			if shop.IsOpen():
				self.State = STATE_SELLING
				return
			self.OpenShop()
			

		if self.State == STATE_SELLING:
			val, self.lastTimeSell = m2k_lib.timeSleep(self.lastTimeSell,TIME_SELL)
			if val:
				if len(self.sellItems_list) == 0:
					self.State = STATE_BUYING
					return
				slot = self.sellItems_list.pop(0)
				net.SendShopSellPacketNew(slot,player.GetItemCount(slot),1)
				chat.AppendChat(3,"[NPC-SHOPER] Sold item at slot " + str(slot))
			return

		if self.State == STATE_BUYING:
			val, self.lastTimeBuy = m2k_lib.timeSleep(self.lastTimeBuy,TIME_BUY)
			if(val):
				if len(self.buyItems_list) == 0:
					self.State = STATE_FINISH_SHOPPING
					return
				slot = self.buyItems_list.pop(0)
				net.SendShopBuyPacket(slot)
			else:
				return

		if self.State == STATE_FINISH_SHOPPING:
			self.EndNPCBusiness()
			return

		if self.State == STATE_GIVING_ITEMS:
			val, self.lastTimeGive = m2k_lib.timeSleep(self.lastTimeGive,TIME_GIVE_ITEM)
			if not val:
				return
			if len(self.giveItems_list) == 0:
				self.EndNPCGiveItem()
				return
			else:
				vid = self.npcAction.SearchVIDClosest()
				if vid== None:
					#chat.AppendChat(3,"[NPC-GIVER] No NPC with vid " +str(vid)+" is close.")
					self.EndNPCGiveItem()
					return
				else:
					slot = self.giveItems_list.pop()
					#chat.AppendChat(3,"[NPC-GIVER] Giving "+  str(player.GetItemCount(slot)) + " item(s) at slot " +str(slot)+" to VID " +str(vid))
					net.SendGiveItemPacket(vid,player.SLOT_TYPE_INVENTORY,slot,player.GetItemCount(slot))
					m2k_lib.skipAnswers(self.npcAction.event_answer)
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)


#Used to move back to original position
originalPosition = (0,0,0)
originalFunctionCallback = None

#Called by Movement module
def _StartBusinessProcessCallBack():
	instance.StartNPCBusiness(True)

#Called by Movement module
def _StartGiveItemProcessCallBack():
	instance.StartNPCGiveItem()

#Called by this module
def _ReturnToPositionCallBack():
	#global originalFunctionCallback
	chat.AppendChat(3,"Going Back")
	Movement.GoToPositionAvoidingObjects(originalPosition[0],originalPosition[1],callback=originalFunctionCallback)
	#originalFunctionCallback = None


###############################
##########INTERFACE############
###############################
#DO NOT CALL THIS MULTIPLE TIMES WITHOUT FINISHING THE PROCESS

#############SHOPER#############
#The answer bypass will be applied before the shop is opened

#This will buy the items specified in 
#The npc needs to be close by
#buy_items_list is a list containing the items(slots) to be bought
#callback       is a function that will be called when the buying process ends
#npc            is one of the option in npc options described above
#open_shop      is a optional argument, telling if it needs to open the shop
def RequestBusinessNPCClose(buy_items_list,sell_items_list,npc,callback=None,open_shop=True):
	instance.SetOrder(npc,buy_items_list,sell_items_list,callback)
	instance.StartNPCBusiness(open_shop)

#The same as the one before, but it moves to the npc position
def RequestBusinessNPCAway(buy_items_list,sell_items_list,npc,callback=None):
	instance.SetOrder(npc,buy_items_list,sell_items_list,callback)
	npc.GoToPosition(callback=_StartBusinessProcessCallBack)
	#Movement.GoToPositionAvoidingObjects(npc.position[0],npc.position[1],callback=_StartBusinessProcessCallBack)

#The same as the one before, but it moves to the npc position and comesback
def RequestBusinessNPCAwayRestorePosition(buy_items_list,sell_items_list,npc,callback=None,pos=player.GetMainCharacterPosition()):
	global originalPosition,originalFunctionCallback
	originalPosition = pos
	originalFunctionCallback = callback
	instance.SetOrder(npc,buy_items_list,sell_items_list,_ReturnToPositionCallBack)
	npc.GoToPosition(callback=_StartBusinessProcessCallBack)

#############ITEM_GIVER#############
#The answer bypass will be applied after the delivery of each item

#This will buy the items specified in 
#The npc needs to be close by
#give_item_list is a list containing the items(slots) to be given
#callback       is a function that will be called when the buying process ends
#npc            is one of the option in npc options described above
def RequestGiveItemNPCClose(give_items_list,npc,callback=None):
	instance.SetGiveItemsToNPC(npc,give_items_list,callback)
	instance.StartNPCGiveItem()

#The same as the one before, but it moves to the npc position
def RequestGiveItemNPCClose(give_items_list,npc,callback=None):
	instance.SetGiveItemsToNPC(npc,give_items_list,callback)
	npc.GoToPosition(callback=_StartBusinessProcessCallBack)

#The same as the one before, but it moves to the npc position and comesback
def RequestGiveItemNPCAwayRestorePosition(give_items_list,npc,callback=None,pos=player.GetMainCharacterPosition()):
	global originalPosition,originalFunctionCallback
	originalPosition = pos
	originalFunctionCallback = callback
	instance.SetGiveItemsToNPC(npc,give_items_list,_ReturnToPositionCallBack)
	npc.GoToPosition(callback=_StartGiveItemProcessCallBack)

def StopAction():
	instance.State = STATE_NONE
	Movement.StopMovement()
	Hooks.questHook.UnhookFunction()


instance = ShopNPCDialog()
		  
		
		

		