import net_packet,app,m2k_lib,chat,sys,background
from m2k_lib import ByteMatrix

ATTR_WIDTH = 256
ATTR_HEIGHT = 256
HEADER_SIZE = 6
        
#Extracts every attr file and joins them
#Call isCollision to check if is there a collision
#Call printMapToFile to print the entire map to a text file
class MapCollision:
    def __init__(self,name_map):
        global ATTR_WIDTH,ATTR_HEIGHT,ByteMatrix
        self.curr_map_name = name_map
        self.init_map = self.getMapAttrFiles(name_map)
        sort_keys = sorted(self.init_map)
        self.max_x, self.max_y = sort_keys[-1]
        self.max_x =(self.max_x + 1)*ATTR_WIDTH
        self.max_y =(self.max_y + 1)*ATTR_HEIGHT
        self.matrix_map = ByteMatrix(self.max_x,self.max_y)
            
        
        for sector in sort_keys:
            self.appendMapSector(sector)
        self.debugFilePrint("test.txt")
        
    def getMapAttrFiles(self,name_map):
        path = name_map + "\\"
        loop = True
        _map = dict()
        a_last_range = 0
        for x in xrange(0,999999):
            _mapPieceName[2] = str(x)
            for a in xrange(0,999999):
                _mapPieceName[5] = str(a)
                curr_file = path
                curr_file += "".join(_mapPieceName)
                curr_file += '\\attr.atr'
                #chat.AppendChat(3,str(curr_file))
                if app.IsExistFile(curr_file) == False :
                    a_last_range = a
                    break
                else:
                    _map[(x,a)] = curr_file
            if a_last_range == 0:
                break
        return _map

    def appendMapSector(self,sector):
        global ATTR_WIDTH,ATTR_HEIGHT,HEADER_SIZE
        x, y = sector
        path = self.init_map[sector]
        buffer = net_packet.Get(path)
        start_x = x*ATTR_WIDTH
        start_y = y*ATTR_HEIGHT
        max_x = start_x + ATTR_WIDTH
        max_y = start_y + ATTR_HEIGHT
        counter = HEADER_SIZE
        byte_arr = bytearray(buffer)
        for _y in xrange(start_y,max_y):
            x_counter = 0
            for _x in xrange(start_x,max_x):
                self.matrix_map.Set(_x,_y,byte_arr[counter])
                counter+= 1
        
    def printMapToFile(self,file_name):
        global ATTR_WIDTH,ATTR_HEIGHT
        with open(file_name,"w") as f:
            for _y in xrange(0,self.max_y):              
                for _x in xrange(0,self.max_x):
                    by = self.matrix_map.Get(_x,_y)
                    if (by & (1<<0)): 
                        f.write("1")
                    else:
                        f.write("0")
                f.write("\n")
    
    def isCollision(self,x,y):
        by = self.matrix_map.Get(x,y)
        if (by & (1<<0)):
            return True
        else:
            return False
        
    def getSucessors(self,_tuple):
        x,y = _tuple
        sucs = list()
        
        try:
            if not isCollision(x,y-1):
                sucs.append((x,y-1))
        try:
            if not isCollision(x-1,y-1):
                sucs.append((x-1,y-1))
        try:
            if not isCollision(x+1,y-1):
                sucs.append((x+1,y-1))
        try:
            if not isCollision(x+1,y+1):
                sucs.append((x+1,y+1))
        try:
            if not isCollision(x,y+1):
                sucs.append((x,y+1))
        try:
            if not isCollision(x-1,y+1):
                sucs.append((x-1,y+1))
        try:
            if not isCollision(x-1,y):
                sucs.append((x-1,y))
        try:
            if not isCollision(x+1,y):
                sucs.append((x+1,y))            
        return sucs
    
    def heuristic(self,node_1,node_end):
        (x1,y1) = node_1
        (x2,y2) = node_end
        
        return m2k_lib.dist(x1,y1,x2,y2)           
            

class A_Star():
    def __init__(self,graph):
        self.graph = graph

    def traceToOrigin(self,state):
        data = list()
        curr_state = state
        while(curr_state.parent != None):
            data.append(curr_state.data)
        return data
        
    def solve(self,initial_state,end_state):
        open_list = list()
        closed_list = list()
        
        initial_state = Node(initial_state,None)
        end_state = Node(end_state,None)
        
        self.open_list.append(initial_state)
        
        while len(open_list)!= 0:
            #a) find node with lowest f
            q = open_list[0]
            curr_f = q.f()
            for node in open_list:
                if node.f() < curr_f:
                    q = node
                    curr_f = node.f()
    
            #b) pop q
            open_list.remove(q)
            
            #c) generate successors
            sucs = self.graph.getSucessors()
            
            for suc in sucs:
                node = Node(suc,q)
                
                #d) Found the end
                if node.data == end_state.data:
                    return traceToOrigin(self,suc)
                
                suc.g(q.g+1)    # Unit distance
                suc.h(self.graph.heuristic(suc.data,end_state.data))
                
                #if a node with the same position as 
                #successor is in the OPEN list which has a 
                #lower f than successor, skip this successor
                skip = False
                for node in open_list:
                    if node.data == suc.data and suc.f() > node.f():
                        skip = True
                        break
                    
                if(skip):
                    continue
                
                #if a node with the same position as 
                #successor  is in the CLOSED list which has
                #a lower f than successor, skip this successor
                #otherwise, add  the node to the open list
                for node in closed_list:
                    if node.data == suc.data and suc.f() > node.f():
                        skip = True
                        break
                
                if(skip):
                    continue
                
                open_list.append(suc)
                
            closed_list.append(q)

    
    class Node():
        def __init__(self,to_store,parent):
            self.h_vaue = 0
            self.g_value = 0
            self.f_value = 0
            self.data = to_store
            self.parent = parent
            
        def g(self,value=None):
            if(value!=None):
                self.g_value = value
                self.f_value = self.g_value + self.h_value
            return self.g
        
        def h(self,value=None):
            if(value!=None):
                self.h_value = value
                self.f_value = self.g_value + self.h_value
            return self.h
        
        def f(self):
            return self.f_value
    

    
#chat.AppendChat(3,"Done!")