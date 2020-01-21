import os
import sys
import glob
import time
import threading
import struct
import platform
import socket


if( platform.system()=='Darwin'):
    from motor_fake import poppy_motor
    print("FAKE")
else:
    from motor import poppy_motor
    from pypot.creatures import PoppyErgoJr
    
from OSC import OSCClient, OSCMessage, OSCServer

class SimpleServer(OSCServer):
    maxPingDelay = 6
    
    # OpenStageControls script pings every 3 seconds
    def __init__(self,t):
        OSCServer.__init__(self,t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    
    def handleMsg(self,oscAddress, tags, data, client_address):
        global sleepingValue
        #print("OSC message received on : "+oscAddress)
        splitAddress = oscAddress.split("/")
        #print(splitAddress)
        
        ############## individual MOTOR #############
        if(splitAddress[1]=="motor"):
            #print("motor id:"+splitAddress[2]+" angle: "+str(data[0]))
            num = int(splitAddress[2])
            list_of_motor[num].setValue(data[0])

        if(splitAddress[1]=="compliant"):
            value = data[0] > 0
            if(value):
                print("compliant id:"+splitAddress[2]+"true")
            else:
                print("compliant id:"+splitAddress[2]+" false")    
            num = int(splitAddress[2])
            list_of_motor[num].setCompliant(data[0])
        
        if(splitAddress[1]=="led"):
            print("motor id:"+splitAddress[2]+" led: "+str(data[0]))
            num = int(splitAddress[2])
            list_of_motor[num].setLedColor(data[0])

        if(splitAddress[1]=="speed"):
            print("motor id:"+splitAddress[2]+" speed: "+str(data[0]))
            num = int(splitAddress[2])
            list_of_motor[num].setSpeed(data[0])
        
        if(splitAddress[1]=="smooth"):
            print("motor id:"+splitAddress[2]+" smooth: "+str(data[0]))
            num = int(splitAddress[2])
            list_of_motor[num].setSmooth(data[0])

        ############## entire robot #############
        if(splitAddress[1]=="robot"):
            if(splitAddress[2]=="compliant"):
                set_compliant_robot(data[0]>0)
            if(splitAddress[2]=="posture"):
                print("do something")

        ############## APP itself #############
        if(splitAddress[1]=="app"):
            if(splitAddress[2]=="close"):
                print("closing the app")
                closing_app()
            if(splitAddress[2]=="fps"):
                print("changing fps - sleeping value: "+str(data[0]))
                sleepingValue = data[0]

        




def send_osc(address, value):
        print ("OSC addresse: "+str(address)+" value: "+str(value))
        oscMsg = OSCMessage()
        oscMsg.setAddress(address)
        oscMsg.append(int(value))
        try:
                oscClient.send(oscMsg)
        except: 
                print ("error sending osc message")

def update_robot():
    #for i in range(6 ):
    #        list_of_motor[i].update()
    list_of_motor[5].update()

def set_compliant_robot(isCompliant):
    for i in range(6 ):
            list_of_motor[i].setCompliant(isCompliant)

def main():
        
        global list_of_motor 
        list_of_motor = []
        for i in range(6 ):
            list_of_motor.append (poppy_motor(i+1) )
 
        global ergoJr 
        if( platform.system()=='Linux'):
            ergoJr = PoppyErgoJr(camera='dummy')
            print("REAL MOTORS")
   
        # OSC connect
        global oscClient
        oscClient = OSCClient()
        oscClient.connect( ("localhost",12345 ))

        if( platform.system()=='Linux'):
            print("REAL MOTORS : motors init")
            for m in list_of_motor :
                m.motor_instance = ergoJr.motors[(m.id -1)]
        
        if(len(sys.argv)>1):
            myip = str(sys.argv[1])
        else:
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

        print("thread created") 
        try:
            print(" Serve forever")
            st.start()
        except:
            print(" ERROR : sequence -  on running OSC server")

        print(" This is after serving forever")  
        time.sleep(4)

        global runningApp
        global sleepingValue
        runningApp = True
        sleepingValue = 1

        while runningApp:
            try:
                update_robot()
                time.sleep(sleepingValue)
            except :
                print("User attempt to close the programm")
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
