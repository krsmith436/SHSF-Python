# Pi is the WiFi server and Giebel Throttle is the WiFi client.
# To service WiFi commands, Pi uses btferret to be an LE client 
# and Smiths Valley is the LE server.
#
# Copied from ChatGPT conversation.

import socket
import subprocess
import threading
from gpiozero import LED
import shsf_btferret

led = LED(17) # Example LED
running = True  # control the main loop

def handle_wifi_command(cmd: str) -> str:
    global running
    if (cmd == "h" or cmd == "w"): # Locomotive sound request.
        led.toggle()
        if (shsf_btferret.send_command(cmd) == 0):
            return "NOK"
        else:
            return "ACK"
    elif cmd == "LED_ON":
        led.on()
        return "ACK: LED turned ON"
    elif cmd == "LED_OFF":
        led.off()
        return "ACK: LED turned OFF"
    elif cmd == "SHUTDOWN":
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])
        return "ACK: Shutting down Pi"
    elif cmd == "REBOOT":
        subprocess.Popen(["sudo", "reboot"])
        return "ACK: Rebooting Pi"
    elif cmd == "HELLO":
        return "ACK: Hello from Pi!"
    elif cmd == "EXIT":
        running = False
        return "ACK: Server exiting"
    else:
        return f"ACK: Unknown command '{cmd}'"

def keyboard_listener():
    """Background thread to watch for keyboard input"""
    global running
    while running:
        user_input = input()
        if user_input.strip().lower() == "q":
            print("Keyboard exit requested")
            running = False
            break
        else:
            print("Type 'q' + Enter to quit.")

# Start keyboard listener thread
threading.Thread(target=keyboard_listener, daemon=True).start()

# Connect to bluetooth module
if (shsf_btferret.connect() == 0):
    print("Bluetooth not connected.")
    exit()
    
# Connect to WiFi server
HOST = ''      
PORT = 5000    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print(f"WiFi server listening on port {PORT}... (type 'q' + Enter to quit)")
print("")

while running:
    try:
        conn, addr = s.accept()
    except OSError:
        break  # socket closed
    data = conn.recv(1024).decode().strip()
    if data:
        print(f"Received from Giebel Throttle {addr}: {data}")
        response = handle_wifi_command(data)
        conn.sendall((response + "\n").encode())
    conn.close()

s.close()
shsf_btferret.disconnect
