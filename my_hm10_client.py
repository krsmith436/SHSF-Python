import btfpy

def notify_callback(node,cticn,dat,datlen):
  print("Reply from HM10")
  btfpy.Print_data(dat)
  # end notify_callback

##### START #####

node = 7
cticn = 0

if(btfpy.Init_blue("devices.txt") == 0):
  exit(0)
    
if(btfpy.Connect_node(node,btfpy.CHANNEL_LE,0) == 0):
  print("Connect failed")
  exit(0)
  
  # read services
btfpy.Find_ctics(node)
  # find data characteristic UUID=FFE1
cticn = btfpy.Find_ctic_index(node,btfpy.UUID_2,[0xFF,0xE1])

command = "h"

if(cticn > 0):
  print("Found data characteristic FFE1 index")  
  print("Enabling notifications")
  btfpy.Notify_ctic(node,cticn,btfpy.NOTIFY_ENABLE,notify_callback)
  print(f"Sending: {command}")
  btfpy.Write_ctic(node,cticn,command + "\r",0)
  print("Waiting 3s for a reply from HM10")
  print("Send an ASCII string reply from the HM10")
  btfpy.Read_notify(3000)
  print("3s wait for reply timed out")
else:
  print("Data characteristic FFE1 not found")
   
print("Disconnecting HM10")
btfpy.Disconnect_node(node)
btfpy.Close_all()
