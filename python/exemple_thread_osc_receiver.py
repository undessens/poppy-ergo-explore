import os
import sys
import glob
import time
import threading
import struct
import socket 
from OSC import OSCClient, OSCMessage, OSCServer

class SimpleServer(OSCServer):
    def __init__(self,t):
        OSCServer.__init__(self,t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    
    def handleMsg(self,oscAddress, tags, data, client_address):
        print("OSC message received on : "+oscAddress)

        splitAddress = oscAddress.split("/")
        print(splitAddress)
        
        ############## GLOBAL MESSAGES #############
        if(splitAddress[1]=="machin"):
            print("machin")

        if(splitAddress[1]=="truc"):
            if(splitAddress[2]=="chose"):
                print("chose")
            if(splitAddress[2]=="bidulle"):
                print("bidulle")

        ############## APP itself #############
        if(splitAddress[1]=="app"):
            if(splitAddress[2]=="close"):
                print("closing the app")
                closing_app()



def main():
        
        # OSC CONNECT       
        myip = socket.gethostbyname(socket.gethostname())

        print("IP adress is : "+myip)
        try:
            server = SimpleServer((myip, 12344)) 
        except:
            print(" ERROR : creating server") 
        print("server created") 
        try:
            st = threading.Thread(target = server.serve_forever) 
        except:
            print(" ERROR : creating thread") 
        try:
            st.start()
        except:
            print(" ERROR : startin thread")

        print(" OSC server is running")  

        # MAIN LOOP 
        global runningApp
        runningApp = True

        while runningApp:
            # This is the main loop
            # Do something here
            try:
                time.sleep(1)
            except:
                print("User attempt to close programm")
                runningApp = False
        
        #CLOSING THREAD AND SERVER
        print(" Ending programme") 
        server.running = False
        print(" Join thread") 
        st.join()
        server.close()
        print(" This is probably the end") 

def closing_app():
    global runningApp
    runningApp = False
    print("Closing App")

if __name__ == "__main__":
    main()
