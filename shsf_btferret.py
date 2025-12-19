# Pi is the LE client and Smiths Valley is the LE server.
# Copied from hm10_client.py

import btfpy

node = 7 # Defined in 'devices.txt'.
cticn = 0   # Found FFE1 characteristic with btfpy.Find_ctics()
            # and set as index 0 in 'devices.txt'.

bluetooth_response = ""

def notify_callback(node,cticn,dat,datlen):
  global bluetooth_response
  print("Reply:")
  btfpy.Print_data(dat)
  print("")
  
  if(datlen > 0):
      bluetooth_response = dat.decode('utf-8')
  else:
      bluetooth_response = "NOK"
  print(f"Bluetooth Reply: {bluetooth_response}")

  return(0)

def send_command(command):
    global bluetooth_response
    bluetooth_response = ""
    print(f"Sending command: {command}")
    btfpy.Write_ctic(node,cticn,command + "\r",0)
    btfpy.Read_notify(100)
    return(bluetooth_response)

def connect():
    if(btfpy.Init_blue("devices.txt") == 0):
        return(0)

    if(btfpy.Connect_node(node,btfpy.CHANNEL_LE,0) == 0):
        print("Connect failed")
        return(0)

    if(btfpy.Ctic_ok(node,cticn) == 1):
        name = btfpy.Device_name(node)
        print("")
        print(f"Connect OK to LE server: {name}")
        print("Enabling LE server notifications")
        print("")
        btfpy.Notify_ctic(node,cticn,btfpy.NOTIFY_ENABLE,notify_callback)
        return(1)
    else:
        print("")
        print("Data characteristic FFE1 not found")
        return(0)
       
def disconnect():     
    print("Disconnecting HM10")
    btfpy.Disconnect_node(node)
    btfpy.Close_all()
