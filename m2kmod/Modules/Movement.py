import net_packet,ui,net,chr,player,chat
import m2k_lib


STATE_FINISH = 1
STATE_MOVING = 2
STATE_STOPPED = 0

NO_PATH_FOUND = 0
DESTINATION_REACHED = 1
MOVING = 1

#Cooldown horse skill
TIME_STOPPED_ALLOWED = 3


class MovementDialog(ui.ScriptWindow):
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.Show()
        self.path = list()
        self.currDestinationX = 0
        self.currDestinationY = 0
        self.state = STATE_STOPPED
        self.stoppedTimer = m2k_lib.GetTime()
        self.lastPlayerPos = (0,0)
        self.maxDistanceToDest = 50
        
    def Stop(self):
        self.state = STATE_STOPPED
        self.currDestinationX = 0
        self.currDestinationY = 0
    
    def GoToPositionAvoidingObjects(self,x,y,maxDist=250):
        self.maxDistanceToDest = maxDist
        if(round(x) != round(self.currDestinationX) or round(y) != round(self.currDestinationY)):
            my_x,my_y,z = player.GetMainCharacterPosition()
            self.path = net_packet.FindPath(my_x,my_y,x,y)
            if(len(self.path)>0):
                self.currDestinationX = x
                self.currDestinationY = y
                self.state = STATE_MOVING
                self.stoppedTimer = m2k_lib.GetTime()
                return MOVING
            else:
                self.state = STATE_STOPPED
                self.currDestinationX = 0
                self.currDestinationY = 0
                return NO_PATH_FOUND
        else:
            if(self.state == STATE_FINISH):
                state = STATE_STOPPED
                return DESTINATION_REACHED
        return None
            
        
    def GoStraightToPoint(self,x,y):
        m2k_lib.RotateMainCharacter(x,y)
        chr.MoveToDestPosition(player.GetMainCharacterIndex(),x, y)
        
    def OnUpdate(self):
        if not (self.state == STATE_MOVING) or len(self.path) == 0:
            return
        
        next_x,next_y = self.path[0]
        my_x,my_y,my_z = player.GetMainCharacterPosition()
        maxdst = 40
        if(len(self.path) == 1):
            maxdst = self.maxDistanceToDest
        if m2k_lib.dist(next_x,next_y,my_x,my_y) < maxdst:
            self.path.pop(0)
            if(len(self.path) == 0):
                self.state = STATE_FINISH
                self.currDestinationX = 0
                self.currDestinationY = 0
                return
            else:
                next_x,next_y = self.path[0]
        
        if self.lastPlayerPos == (my_x,my_y):
            val, self.stoppedTimer = m2k_lib.timeSleep(self.stoppedTimer,TIME_STOPPED_ALLOWED)
            if val:
                player.ClickSkillSlot(9)

        self.lastPlayerPos = (my_x,my_y)
        self.GoStraightToPoint(next_x,next_y)
    
    def __del__(self):
        ui.ScriptWindow.__del__(self)
        

def GoToPositionAvoidingObjects(x,y,maxDist=250):
    Movement.GoToPositionAvoidingObjects(x,y,maxDist)
    
def GoToPosition(x,y):
    Movement.GoStraightToPoint(x,y)

def StopMovement():
    Movement.Stop()
        
Movement = MovementDialog()
          
        
            
        

        