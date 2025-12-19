# Pi is the WiFi server and Giebel Throttle is the WiFi client.
# To service WiFi commands, Pi uses btferret to be an LE client 
# and Smiths Valley is the LE server.
#
# Copied from Microsoft Copilot conversation.

import socketserver
import threading
import shsf_btferret
from guizero import *

#-----------------------------------------------------------------
# Setup server
#-----------------------------------------------------------------
class CommandHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip().decode()
        print(f"Received: {data}")

        # Decide response based on command
        if data == "EXIT":
            response = "SHUTTING DOWN"
            threading.Thread(target=stop_server, daemon=True).start()
        elif data == "?" or data == "f" or data == "v":
            response = "NOT SUPPORTED"
        else:
            response = shsf_btferret.send_command(data)

        # Send response back to Arduino
        self.request.sendall(response.encode())

def stop_server():
    server.shutdown()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
#-----------------------------------------------------------------
# Control panel functions
#-----------------------------------------------------------------
def hornButton_clicked():
    data = "h"
    response = shsf_btferret.send_command(data)
    
#-----------------------------------------------------------------
# Setup control panel
#-----------------------------------------------------------------
app = App(title="Smith Huotari & Santa Fe", layout="grid", width=400, height=400)
app.bg = "#00b33c"

# Row 0
Picture(app, image="shsf_logo.jpg", width=100, height=100, grid=[0,0])
TextBox(app, grid=[1,0])
hornButton = PushButton(app, command=hornButton_clicked, text="HORN", grid=[2,0])

# Row 1
CheckBox(app, text="Checkbox", grid=[0,1])
ListBox(app, items=["red", "green", "blue"], grid=[1,1])
Combo(app, options=["red", "green", "blue"], grid=[2,1])

# Row 2
ButtonGroup(app, options=["portrait", "landscape"], selected="portrait", grid=[0,2])
Slider(app, start=0, end=10, grid=[1,2])
Text(app, text="Label", grid=[2,2])
#-----------------------------------------------------------------

if __name__ == "__main__":
	#-----------------------------------------------------------------
    # Connect to bluetooth module
    #-----------------------------------------------------------------
    if (shsf_btferret.connect() == 0):
        print("Bluetooth not connected.")
        exit()
    
    #-----------------------------------------------------------------
    # Start server for Smiths Valley
    #-----------------------------------------------------------------
    HOST, PORT = "0.0.0.0", 5000
    server = ThreadedTCPServer((HOST, PORT), CommandHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server running on {HOST}:{PORT}")
    print("-----------------------")
    print("Press CTRL + C to exit.")

    
    #-----------------------------------------------------------------
    # Display control panel
    #-----------------------------------------------------------------
    app.display()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Keyboard interrupt, shutting down...")
        server.shutdown()
        server.server_close()
        shsf_btferret.disconnect()
        exit()
