#from OpenBot.Modules import Levelbot, UIComponents
import net_packet,ui,net,chr,player,chat,shop,item,game,Levelbot,BotBase
import OpenLib,game,Hooks,ShopNPC,Movement,FishingBot,event,background,Hooks,ShopNPC,FileManager,Inventorymanager,MapManager,localeInfo,playerm2g2,app,uiRestart,uiScriptLocale
import itertools,Settings,DmgHacks,game,interfaceModule,uiPrivateShopBuilder,uiPrivateShopSearch
import MiningBot
#reload(DmgHacks)
#reload(MiningBot)
reload(MapManager)
#reload(FileManager)
#reload(MapManager)
##reload(Inventorymanager)
#reload(Movement)
#reload(ShopNPC)
##reload(FishingBot)
##reload(Hooks)
##reload(Ho)
#reload(FileManager)
#reload(BotBase)
#reload(Levelbot)
#reload(DmgHacks)
#reload(ShopNPC)

chat.AppendChat(3,str(background.GetCurrentMapName()))
#buffer_vid = 0
#sum = 0
#for vid in net_packet.InstancesList:
#	sum += vid
#	if vid > buffer_vid:
#		buffer_vid = vid
#chat.AppendChat(3,str(sum/len(net_packet.InstancesList)))
#chat.AppendChat(3,str(MapManager.maps))

for key in MapManager.maps.keys():
	chat.AppendChat(3,str(key))
#net.SendOnClickPacket(7952911)
#mining_glitch.clearInstances()
#for x in range(7900571,7901572):
#	net.SendOnClickPacket(x)
##chat.AppendChat(3,"TEST")
##net.SendPrivateShopSearchInfo()
#chat.AppendChat(3,str(mining_glitch.getFoundOres()))
##net.SendOnClickPacket(7625674)

#
#chat.AppendChat(3,str(uiPrivateShopBuilder.g_privateShopAdvertisementBoardDict.keys()))

#vid = player.GetTargetVID()
#
#
#mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
#net_packet.SendAddFlyTarget(vid,mob_x, mob_y)
#net_packet.SendShoot(net_packet.COMBO_SKILL_ARCH)

#OpenLib.extractFile('d:/ymir work/ui/metin2_map_privateshop_atlas.dds')
#links  = MapManager.GetMapPath(background.GetCurrentMapName(),'metin2_map_trent02')
#for link in links:
#def interceptAppear(*args,**kwargs):
#	global private_shop_func
#	chat.AppendChat(3,str(args)+str(kwargs))
#	return private_shop_func.CallOriginalFunction(*args,**kwargs)
#
#private_shop_func = Hooks.Hook(interfaceModule.Interface.AppearPrivateShop,interceptAppear)
#private_shop_func.HookFunction()
#chat.AppendChat(3,"Done")
#chat.AppendChat(3,str(localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR()))

#net.DirectEnter(1)

#chat.AppendChat(3,"Test")

#map = MapManager.GetMap()
#
#Hooks._debugHookFunctionArgs(net.SendCommandPacket)
#game.interface.RestartHere()
#chat.AppendChat(3,str(net.SendCommandPacket))
#

#for map_name,link in map.links.iteritems():
#    name = link.GetDestMapName()
#    chat.AppendChat(3,str(name))
#reload(OpenLib)
#reload(Movement)
#reload(FishingBot)
#Movement.GoToPositionAvoidingObjects(50000,50000,mapName="metin2_map_c1")
#Movement.StopMovement()
#Hooks._debugUnhookFunctionArgs()
#Hooks._debugHookFunctionArgs(net.SendPrivateShopSearchInfo)
#reload(OpenLib)
#Hooks._debugHookFunctionArgs(net.SetPhaseWindow)
#net.SendItemMovePacket(2,3,5)
#npcs = MapManager.GetMap().npcs
#for npc in npcs:
	#chat.AppendChat(3,str(npc) + ":" +str(npcs[npc]))
#maps,name = MapManager.GetClosestMapPathWithNPC(9009,map_name_start="metin2_map_milgyo")
#links = MapManager.GetMapPath('map_n_snowm_01')
#maps = MapManager.GetMap('map_n_snowm_01')
#Hooks.questHook.HookFunction()
#
#npc = ShopNPC.GetFishermanCarpa()
#npc.DoAction()
#chat.AppendChat(3,str(net_packet.GetCloseItemGround(0,0)))
#Hooks.questHook.UnhookFunction()

#x,y,z = player.GetMainCharacterPosition()
#vid,itemX,itemY = net_packet.GetCloseItemGround(x,y)
#dst = OpenLib.dist(x,y,itemX,itemY)
#net_packet.SendPickupItem(vid)
#
#name_file = str(net.GetServerInfo().split(',')[0]) + ".items"
#name_convert = "convertSend.py "
###Hooks.questHook.UnhookFunction()
#os.system('cd ' + net_packet.PATH + " && python " + name_convert+ " "+ name_file )
##os.system('python ' +  name_convert + name_file)
#chat.AppendChat(3,str('python ' +  name_convert + name_file))
##for link in maps:
#chat.AppendChat(3,str(dst))

#net.SendItemDropPacketNew(0,player.GetItemCount(0))
#OpenLib.StackItems()
#net.SendShopSellPacketNew(0,player.GetItemCount(0),1)

#from OpenBot.Modules import Hooks
#reload(FishingBot)
#reload(ShopNPC)
#Hooks._debugUnhookFunctionArgs()
#ShopNPC.RequestBusinessNPCClose([7,7,7,7],[],ShopNPC.FISHERMAN_SHOP)
#chat.AppendChat(3,str(net.GetEmpireID()))
#Hooks.questHook.UnhookFunction()
#net.SendShopBuyPacket(0)
#test()
#net.SendOnClickPacket(player.GetTargetVID())
#ShopNPC.test()
#event.SelectAnswer(0,1)
#reload(FishingBot)
#reload(ShopNPC)
#Hooks.questHook.UnhookFunction()
#net.SendGiveItemPacket(player.GetTargetVID(),player.SLOT_TYPE_INVENTORY,0,1)
#event.SelectAnswer(1,0)
#event.SelectAnswer(0,1)
#
#vid = player.GetTargetVID()
#chat.AppendChat(3,str(player.GetTargetVID()))
#chat.AppendChat(3,str(OpenLib.isPlayerCloseToInstance(vid)))
#chat.AppendChat(3,str(OpenLib.GetCurrentPhase()))

#net.DirectEnter(0,0)
#chat.AppendChat(3,str(net_packet.IsPositionBlocked(33600,22200)))

#for i in range(0,10):
#idx = player.GetItemIndex(2,item.EQUIPMENT_SHOES)
#item.SelectItem(idx)
#
#chat.AppendChat(3,str(item.GetItemSubType()))
#chat.AppendChat(3,str(item.GetItemType()))
#chat.AppendChat(3,str(item.ITEM_TYPE_WEAPON))
#chat.AppendChat(3,str(player.GetItemIndex(0)))

#name = background.GetCurrentMapName()
#OpenLib.extractFile(name+str())
#reload(FishingBot)
#reload(ShopNPC)

#net.SendShopSellPacketNew(0)
#net.SendGiveItemPacket(player.GetTargetVID(),player.SLOT_TYPE_INVENTORY,0,1)
#event.SelectAnswer(1,0)
#event.SelectAnswer(2,0)

#Hooks._debugHookFunctionArgs(net.DirectEnter)
#Hooks._debugUnhookFunctionArgs()
#net.SendGiveItemPacket(player.GetTargetVID(),player.SLOT_TYPE_INVENTORY,0,1)
#event.SelectAnswer(1,0)
#event.SelectAnswer(2,0)
#event.SelectAnswer(3,1)

#chat.AppendChat(3,str(net_packet.GetCurrentPhase()))
#chat.AppendChat(3,background.GetCurrentMapName())



#for i in range(0,player.METIN_SOCKET_MAX_NUM):
	#num = player.GetItemMetinSocket(player.SLOT_TYPE_INVENTORY,0,i)
	#chat.AppendChat(3,str(num))

#chat.AppendChat(3,str(num))
#for i in range(0,10):
#    num = player.GetItemIndex(player.EQUIPMENT,item.EQUIPMENT_WEAPON)
#    chat.AppendChat(3,str(num))
#Hooks.questHook.UnhookFunction()
#item.GetValue
#Gets some values of items


#SelectItem has index as argument


#ROD##
#To get rod current level use player.GetItemMetinSocket(slot,0)
#To get rod maxLevel level use item.GetValue(2) after select the item

#Possible Inventory type
#player module
#SLOT_TYPE_ACCE
#SLOT_TYPE_AURA
#SLOT_TYPE_AUTO
#SLOT_TYPE_BELT_INVENTORY
#SLOT_TYPE_CHANGE_LOOK
#SLOT_TYPE_DRAGON_SOUL_INVENTORY
#SLOT_TYPE_EMOTION
#SLOT_TYPE_EQUIPMENT
#SLOT_TYPE_EXCHANGE_OWNER
#SLOT_TYPE_EXCHANGE_TARGET
#SLOT_TYPE_FISH_EVENT
#SLOT_TYPE_GUILDBANK
#SLOT_TYPE_INVENTORY
#SLOT_TYPE_MALL
#SLOT_TYPE_NONE
#SLOT_TYPE_PET_FEED_WINDOW
#SLOT_TYPE_PREMIUM_PRIVATE_SHOP
#SLOT_TYPE_PRIVATE_SHOP
#SLOT_TYPE_QUICK_SLOT
#SLOT_TYPE_SAFEBOX
#SLOT_TYPE_SHOP
#SLOT_TYPE_SKILL

#If the above are not working, use this, some weird thing is going on in here
#RESERVED_WINDOW",	
#INVENTORY",			
#EQUIPMENT",			
#SAFEBOX",			
#MALL",				
#DRAGON_SOUL_INVENTORY",
#GROUND",				

#Possible inventory equipment values to be used with SLOT_TYPE_EQUIPMENT
#item module
#EQUIPMENT_ARROW
#EQUIPMENT_BELT
#EQUIPMENT_BODY
#EQUIPMENT_COUNT
#EQUIPMENT_EAR
#EQUIPMENT_GLOVE
#EQUIPMENT_HEAD
#EQUIPMENT_NECK
#EQUIPMENT_PENDANT
#EQUIPMENT_SHOES
#EQUIPMENT_UNIQUE1
#EQUIPMENT_UNIQUE2
#EQUIPMENT_WEAPON
#EQUIPMENT_WRIST



########################
#To be used with index using SelectItem(index)
########################
#Possible item Types
#item module
#GetItemType function
#ITEM_TYPE_NONE,					
#ITEM_TYPE_WEAPON,				
#ITEM_TYPE_ARMOR,				
#ITEM_TYPE_USE,					
#ITEM_TYPE_AUTOUSE,				
#ITEM_TYPE_MATERIAL,				
#ITEM_TYPE_SPECIAL,				
#ITEM_TYPE_TOOL,					
#ITEM_TYPE_LOTTERY,				
#ITEM_TYPE_ELK,					
#ITEM_TYPE_METIN,				
#ITEM_TYPE_CONTAINER,			
#ITEM_TYPE_FISH,					
#ITEM_TYPE_ROD,					
#ITEM_TYPE_RESOURCE,				
#ITEM_TYPE_CAMPFIRE,				
#ITEM_TYPE_UNIQUE,				
#ITEM_TYPE_SKILLBOOK,			
#ITEM_TYPE_QUEST,				
#ITEM_TYPE_POLYMORPH,			
#ITEM_TYPE_TREASURE_BOX,			
#ITEM_TYPE_TREASURE_KEY,			
#ITEM_TYPE_SKILLFORGET,			
#ITEM_TYPE_GIFTBOX,				
#ITEM_TYPE_PICK,					
#ITEM_TYPE_HAIR,					
#ITEM_TYPE_TOTEM,				
#ITEM_TYPE_BLEND,				
#ITEM_TYPE_COSTUME,				
#ITEM_TYPE_DS,					
#ITEM_TYPE_SPECIAL_DS,			
#ITEM_TYPE_EXTRACT,				
#ITEM_TYPE_SECONDARY_COIN,		
#ITEM_TYPE_RING,					
#ITEM_TYPE_BELT,					
#ITEM_TYPE_WON,					
#ITEM_TYPE_TRANSFER_SCROLL,
#ITEM_TYPE_GACHA,
#ITEM_TYPE_MAX_NUM,


#WEAPON subtypes
#item module
#GetItemSubType function
#WEAPON subtypes
#WEAPON_SWORD,
#WEAPON_DAGGER,
#WEAPON_BOW,
#WEAPON_TWO_HANDED,
#WEAPON_BELL,
#WEAPON_FAN,
#WEAPON_ARROW,
#WEAPON_UNLIMITED_ARROW,
#WEAPON_MOUNT_SPEAR,
#WEAPON_CLAW,
#WEAPON_NUM_TYPES,
