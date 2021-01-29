import net_packet,chat



CONFIG_MAP_NPCS = net_packet.PATH + 'm2kmod/Saves/NpcMaps/'
CONFIG_MAP_LINKS = net_packet.PATH + 'm2kmod/Saves/map_linker.txt'


CONFIG = net_packet.PATH + 'm2kmod/Saves/config.m2k'
CONFIG_PRICE = net_packet.PATH + 'm2kmod/Saves/priceconfig.m2k'
CONFIG_BOSSES_ID = net_packet.PATH + 'm2kmod/Saves/boss_ids.txt'
CONFIG_PSHOP_AUTO_BUY = net_packet.PATH + 'm2kmod/Saves/search_items_max_price.txt'
CONFIG_PICKUP_FILTER = net_packet.PATH + 'm2kmod/Saves/pickup_filter.txt'
CONFIG_SHOP_CREATOR = net_packet.PATH + 'm2kmod/Saves/item_sell_prices.txt'
CONFIG_SELL_INVENTORY = net_packet.PATH + 'm2kmod/Saves/items_to_sell.txt'
CONFIG_LOCATION_CHANGER = net_packet.PATH + 'm2kmod/Saves/location_changer.txt'
SHOP_CREATOR_LOG = net_packet.PATH + 'm2kmod/Saves/shop_log.txt'


#For parsing
def boolean(val):
	if val == "True" or val == "1":
		return True
	else:
		return False

#FileHandler to avoid closing and opening everytime a setting is saved
class FileHandler():
	def __init__(self,fileName):
		self.fileName = fileName
		self.inMemory = False
		self.lines = []
		self.OpenFile()

	def OpenFile(self):
		self.inMemory = True
		with open(self.fileName,'r') as f:
			self.lines = f.readlines()


	def CloseFile(self):
		if self.inMemory:
			with open(self.fileName,'w') as f:
				f.writelines(self.lines)
		#self.inMemory = False
	
	def SaveFile(self):
		self.CloseFile()

	def ReadConfig(self,Setting):
		if not self.inMemory:
			self.OpenFile()
		for line in self.lines:
			_line = line.rstrip()  # remove '\n' at end of line
			if _line.startswith(Setting):
				return _line.split('=')[1]
		self.lines.append(Setting + "=0\n")
		return 0

	def WriteConfig(self,Setting, Value):
		if not self.inMemory:
			self.OpenFile()
		for index,Line in enumerate(self.lines):
			if Line.startswith(Setting + '='):
				self.lines[index] = Setting + '=' + Value + '\n'
	


files = dict()

################### GENERAL ##########################
def ReadConfig(Setting,file=CONFIG):
	if file not in files:
		files[file] = FileHandler(file)
	return files[file].ReadConfig(Setting)

def WriteConfig(Setting,Value,file=CONFIG):
	#chat.AppendChat(3,Setting+","+Value)
	if file not in files:
		files[file] = FileHandler(file)
	return files[file].WriteConfig(Setting,Value)


#Load and save the entire file at once, the format is the same as ReadConfig
def LoadDictFile(file,dict_,cast_type):
	with open(file,'r') as f:
		for line in f:
			line = line.rstrip()
			lst = line.split('=')
			dict_[cast_type(lst[1])] = lst[0]

def SaveDictFile(file,dict_):
    with open(file,'w') as f:
        for id in dict_:
            f.write(dict_[id] + "=" + str(id)+"\n")

def LoadListFile(file):
	lst = []
	try:
		with open(file,'r') as f:
			for line in f:
				line = line.rstrip()
				lst.append(line)
	except:
		return []
	return lst

def SaveListFile(file,lst):
	lst = [str(i) +"\n" for i in lst]
	if len(lst) == 0:
		return
	with open(file,'w') as f:
		f.writelines(lst)
	return lst
	

#Read and save all elements of an object
def ReadAllElements(name,object,fileName):
    for attr in object.__dict__:
        if attr is int or attr is str:
            object.__dict__[attr] = ReadConfig(name + "." + str(attr),fileName)

def SaveAllElements(name,object,fileName):
    for attr in object.__dict__:
        if attr is int or attr is str:
            WriteConfig(name + "." + str(attr),object.__dict__[attr],fileName)
	Save()

#For a file to be saved, Save must be called for changes to be written to the disk 
def Save(file=CONFIG):
	if file in files:
		files[file].SaveFile()

def SaveAll():
	for file in files:
		file.SaveFile()


#################### MAP RELATED ######################
#Parsing of npc files
#Returns a dictionary where the key is the id of the npc and the value is a list of tuples containing
#the x,y positions of the npcs with same race
def parseNpcList(map_name):
	npc_list = dict()
	file_name = CONFIG_MAP_NPCS + str(map_name) + ".npcs"

	f = 0
	try:
		f =  open(file_name,"r")
	except Exception:
		chat.AppendChat(3,"ERROR: Npc information is not available for map " + str(map_name))
		return []


	for i,line in enumerate(f):
		args = line.split(" ")
		if len(args) != 3:
			chat.AppendChat(3,"There is an error on file " + map_name +", line "+str(i+1))
			continue
		try:
			race = int(args[0])
			x = int(args[1])*100
			y = int(args[2])*100
		except Exception:
			 chat.AppendChat(3,"There is an error on file " + map_name +", line "+str(i+1))
			 continue
		
		if race not in npc_list:
			npc_list[race] = []
		npc_list[race].append((x,y))
	return npc_list


#Parsing of map_link
#Returns a list of MapLinks
def parseMapLinks(file_name=CONFIG_MAP_LINKS):
	f = 0
	try:
		f =  open(file_name,"r")
	except OSError:
		chat.AppendChat(3,"ERROR: Map link information not available")
		return []

	lst = list()
	for i,line in enumerate(f):
		args = line.split(" ")
		#chat.AppendChat(3,str(len(args)))
		if args[0][0] == "#":
			continue
		try:
			dic = dict()
			dic['x'] = int(args[0])*100
			dic['y'] = int(args[1])*100
			dic['orig'] = args[2]
			dic['dest'] = args[3]
			dic['race'] = int(args[4])
			if len(args) >= 6:
				evnt = args[5].split("|")
				dic['event_answer'] = [int(i) for i in evnt]
			else:
				dic['event_answer'] = []

			lst.append(dic)
		except Exception:
			 chat.AppendChat(3,"There is an error on map_link file, line "+str(i+1))
			 continue
		
	return lst

