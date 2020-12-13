#import filter
#reload(filter)

#import filter#,chat
import player,chr,net_packet,chat,background,player
#vid = player.GetTargetVID()
x,y,z = net_packet.GetPixelPosition(player.GetMainCharacterIndex())
#chr.MoveToDestPosition(player.GetMainCharacterIndex(),x,y)
#chat.AppendChat(3,"Target VID = " + str(x))
#chat.AppendChat(3,"Target VID = " + str((len(net_packet.InstancesList))))

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

chat.AppendChat(3,str(x))