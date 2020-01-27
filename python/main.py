import os
import sys
import glob
import time
import threading
import struct
import platform
import socket
from os import path
import json


if( platform.system()=='Darwin'):
    from motor_fake import poppy_motor
    print("FAKE")
else:
    from motor import poppy_motor
    from pypot.creatures import PoppyErgoJr
    
from OSC import OSCClient, OSCMessage, OSCServer

global runningApp
global sleepingValue
global list_of_motor
global ergoJr 
global oscClient
global listOfPos

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
            if(splitAddress[2]=="speed"):
                set_speed_robot(data[0])
            if(splitAddress[2]=="speedmax"):
                set_speedMax_robot(data[0])
            if(splitAddress[2]=="speedmin"):
                set_speedMin_robot(data[0])
            if(splitAddress[2]=="smooth"):
                set_smooth_robot(data[0])
            if(splitAddress[2]=="posture"):
                print("do something")

        ############## POS system #############
        if(splitAddress[1]=="pos"):
            if(splitAddress[2]=="load"):
                loadPos(data[0])
            if(splitAddress[2]=="record"):
                recordPos(data[0])
            if(splitAddress[2]=="saveLib"):
                savePosToJSON(data[0])
            if(splitAddress[2]=="loadLib"):
                loadPosFromJSON(data[0])


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

def main():
        # CREATE INSTANCE OF POPPY MOTOR
        global list_of_motor 
        list_of_motor = []

        list_of_motor.append (poppy_motor(1, -90, 65) ) #bas
        list_of_motor.append (poppy_motor(2, -80, 27) )
        list_of_motor.append (poppy_motor(3, -90, 40) )
        list_of_motor.append (poppy_motor(4, -90, 90) )
        list_of_motor.append (poppy_motor(5, -90, 90) )
        list_of_motor.append (poppy_motor(6, -90, 90) ) #haut

        if( platform.system()=='Linux'):
            ergoJr = PoppyErgoJr(camera='dummy')
            print("REAL MOTORS")
   
        # OSC connect
        oscClient = OSCClient()
        oscClient.connect( ("localhost",12345 ))

        #ASSOCIATE ERGOJR TO MOTORS INSTANCE
        if( platform.system()=='Linux'):
            print("REAL MOTORS : motors init")
            for m in list_of_motor :
                m.motor_instance = ergoJr.motors[(m.id -1)]
       
        #INIT ROBOT POS
        init_robot_pos()

        #INIT LIST OF POS
        loadPosFromJSON(1)
        print (listOfPos)
        
        #SET LOCAL IP ADRESS
        if(len(sys.argv)>1):
            myip = str(sys.argv[1])
        else:
            myip = socket.gethostbyname(socket.gethostname())
        print("IP adress is : "+myip)

        # CREATE OSC SERVER
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

        # GLOBAL PARAMETER OF RUNNING APP
        global runningApp
        global sleepingValue
        runningApp = True
        sleepingValue = 0.02 #fps set to 50Hz

        # MAIN LOOP
        while runningApp:
            try:
                update_robot()
                time.sleep(sleepingValue)
            except :
                print("User attempt to close the programm")
                runningApp = False
        
        #CLOSING THREAD AND SERVER
        print(" Ending programme") 
        set_compliant_robot(True)
        server.running = False
        print(" Join thread") 
        st.join()
        server.close()
        print(" This is probably the end") 

def closing_app():
    global runningApp
    runningApp = False
    print("Closing App")

def update_robot():
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].update()

def set_compliant_robot(isCompliant):
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].setCompliant(isCompliant)

def set_smooth_robot(newSmooth):
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].setSmooth(newSmooth)

def set_speed_robot(newSpeed):
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].setSpeed(newSpeed)

def set_speedMax_robot(newSpeed):
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].speedMax = newSpeed

def set_speedMin_robot(newSpeed):
    global list_of_motor
    for i in range(6 ):
            list_of_motor[i].speedMin = newSpeed

def init_robot_pos():
    set_speed_robot(240)
    set_smooth_robot(9) #this is 4%
    set_compliant_robot(False)

def recordPos(nbPos):
    global listOfPos
    print("RECORD POS nb: "+str(nbPos))
    for nbMotor in range(6):
        listOfPos[nbPos][nbMotor]=list_of_motor[nbMotor].position

def loadPos(nbPos):
    global listOfPos
    print("LOAD POS nb: "+str(nbPos))
    for nbMotor in range(6):
        list_of_motor[nbMotor].setValue(listOfPos[nbPos][nbMotor])

# This load the entire list of pos ( todo : call it loadLibPos or loadListOfPos)
def loadPosFromJSON(nbLib):
    global listOfPos
    if(path.isfile("pos/lib"+str(nbLib)+".json")):
        with open("pos/lib"+str(nbLib)+".json") as f:
            data = json.load(f)
            listOfPos=data
    else:
        print("json file does not exist")
        listOfPos = []
        for nbPos in range(8):
            listOfPos.append([])
            for nbMotor in range(6):
                listOfPos[nbPos].append([])
                listOfPos[nbPos][nbMotor] = 0

# This save the entire lib : listOfPos
def savePosToJSON(nbLib):
    print("save list of pos to JSON :"+str(nbLib))
    print(listOfPos)
    with open("pos/lib"+str(nbLib)+".json", 'w') as json_file:
        json.dump(listOfPos, json_file)

if __name__ == "__main__":
    main()
