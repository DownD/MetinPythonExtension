import net_packet,app,m2k_lib,chat,sys,background,chr,player,m2k_lib,Levelbot,time
import Movement

        

#_str = net_packet.Get("Index")
#lst = app.GetFileList("locale")

#Handle = m2k_lib.EterPackOperator("d:\ymir work\pc\warrior\warrior_novice_lod_03.gr2")
#_str = Handle.read()
#Handle = app.OpenTextFile("settings.txt")

#with open("test.jpg", "wb") as myfile:
    #myfile.write(_str)
#chat.AppendChat(3,str(len(lst))) #might be IsFileExist 
#chat.AppendChat(3,str(len(net_packet.InstancesList)))


#val = net_packet.IsPositionBlocked(678,690)
#val = net_packet.FindPath(358,471,760,697)
#x,y = val[0]
#chr.SelectInstance(player.GetMainCharacterIndex())
#m2k_lib = reload(m2k_lib)
#x,y,my_z = player.GetMainCharacterPosition()
#chat.AppendChat(3,str(x))
#Movement = reload(Movement)
#Movement.GoToPositionAvoidingObjects(72400,16600)

#strr = "TEST"
#b = bytearray()
#b.append(3)
#b.extend(strr)

#Movement = reload(Movement)
#player.GetTargetVID()
#net_packet.SendAttackPacket(player.GetTargetVID(),0)
x,y,z = chr.GetPixelPosition(player.GetTargetVID())

net_packet.SendStatePacket(x,y,0,1,0)
net_packet.SendStatePacket(x,y,0,0,0)
net_packet.SendStatePacket(x,y,0,3,14)
net_packet.SendAttackPacket(player.GetTargetVID(),0)
chat.AppendChat(3,str(player.GetTargetVID()))
#net_packet.SendPacket(len(b),b)
#Movement = reload(Movement)
#Levelbot = reload(Levelbot)
#chat.AppendChat(3,str(player.GetMainCharacterPosition()))
#m2k_lib.RotateMainCharacter(36700,61700)
#chr.SetRotation(180)
