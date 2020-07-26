import player, chat,chr,m2k_lib

m2k_lib.extractFile("ui.py")
chat.AppendChat(3,str(chr.GetInstanceType(player.GetTargetVID())))