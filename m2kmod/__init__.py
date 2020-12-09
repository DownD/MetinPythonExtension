#import Generel,Buffbot,Spambot,Energybot,Telehack,Inventorymanager,Itemcreator,InstantPickup,EQChanger,Info,Shopcreator,m2k_lib,m2k_hook,Global

#import m2kmod.Modules.Settings,m2kmod.Modules.Buffbot,m2kmod.Modules.Spambot,m2kmod.Modules.Fishbot,m2kmod.Modules.Energybot
#import m2kmod.Modules.Telehack,m2kmod.Modules.Inventorymanager,m2kmod.Modules.Itemcreator,m2kmod.Modules.InstantPickup,m2kmod.Modules.Generel
#import m2kmod.Modules.EQChanger,m2kmod.Modules.Info,m2kmod.Modules.Shopcreator,m2kmod.Modules.Mobscanner,m2kmod.Modules.CHChanger,m2kmod.Modules.Telehack

import sys
import chatm2g as _chat
import playerm2g2 as _player
import m2netm2g as _net
import chrmgrm2g as _chrmgr
import net_packet
#import yWp8YWaB4m5N2glpnses as _app
#import zsDuxBCwljHyuNKnD6Fh as _item
#import ui12zi as _uiminimap

sys.modules['player'] = _player
sys.modules['net'] = _net
#sys.modules['app'] = _app
#sys.modules['item'] = _item
#sys.modules['uiminimap'] = _uiminimap
sys.modules['chat'] = _chat
sys.modules['chrmgr'] = _chrmgr

setattr(_chrmgr, 'GetPixelPosition', net_packet.GetPixelPosition)
#setattr(_player, 'GetName', _player.GetChrName)
#setattr(_player, 'ClickSkillSlot', _player.UseSkillSlot)
#setattr(_net, 'GetServerInfo', _net.GetServerInfoGame)