from datetime import datetime
import net_packet

def DebugPrint(arg):
	"""
	Log's information to Log.txt file.

	Args:
		arg ([str]): Informatio to log.
	"""
	with open(net_packet.PATH+"\\Log.txt","a") as f:
		f.write(str(datetime.now())+": "+arg+"\n")
