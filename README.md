# MetinPythonBot

Bot to be used with my c++ python library.

## Functions
- PathFinding Algorithm
- WaitHack (Including bow)
- Pickup (with range)
- SearchBot
- LevelBot (with change location)
- FishBot
- Auto-pot and auto-restart
- Shop-creator
- Inventory Manager
- Teleport hack
- Packet Filter

## Notes
- init.py needs to be changed in case the server changes critical modules or functions

### V0.3
- Implemented WaitHack
- Removed some usseless or bugged modules
- Change level bot to make use of IsDead function

### V0.4
- Implemented pathfinding algorithm, for the character to follow a path


# Problems
- WaitHack Not Working
- GetPixelPosition gives the end position after a movement instead of the current position
-- Offsets for Player instance will be needed
