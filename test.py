#import filter
#reload(filter)

#import filter#,chat
import player,chr,net_packet,chat,background
vid = player.GetTargetVID()
x,y,z = net_packet.GetPixelPosition(vid)
chat.AppendChat(3,"Target VID = " + str(x))

#vid = m2k_lib.getClosestInstance(m2k_lib.BOSS_TYPE,False)
#chat.AppendChat(3,str(vid))
#chat.AppendChat(3,str(net_packet.IsDead(vid)))
#net.SendItemDropPacket(0,0)
#chat.AppendChat(3,str(player.GetTargetVID()))
#for key in m2k_lib.BOSS_IDS:
    #chat.AppendChat(3,str(key))
#x,y,z = chr.GetPixelPosition(vid)
#Movement.GoToPositionAvoidingObjects(x,y)
#m2k_lib.AttackTarget(vid)
#x,y,z = chr.GetPixelPosition(player.GetMainCharacterIndex())
#chat.AppendChat(3,"X: " + str(x) + "Y: " + str(y) + " IsBlocked: " + str(net_packet.IsPositionBlocked(x,y)))