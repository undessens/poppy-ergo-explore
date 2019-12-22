import os
import sys
import glob
import time
import struct
from motor import poppy_motor
from pypot.creatures import PoppyErgoJr

from OSC import OSCClient, OSCMessage, OSCServer

class SimpleServer(OSCServer):
    maxPingDelay = 6
    # OpenStageControls script pings every 3 seconds
    def __init__(self,t):
        OSC.OSCServer.__init__(self,t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    
    def handleMsg(self,oscAddress, tags, data, client_address):
        splitAddress = oscAddress.split("/")
        
        ############## MOTOR #############
        if(splitAddress[1]=="motor"):
            print("motor id:"+splitAddress[2]+" angle: "+str(data[0]))
            num = int(splitAddress[2])
            list_of_motor[num].setValue(data[0])
            list_of_motor[num].update()


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
        

        global list_of_motor 
        list_of_motor = []
        for i in range(6 ):
            list_of_motor.append (poppy_motor(i+1) )

        global ergoJr 
        ergoJr = PoppyErgoJr(camera='dummy')

        
        # OSC connect
        global oscClient
        oscClient = OSCClient()
        oscClient.connect( ("localhost",12345 ))
        

        for m in list_of_motor :
            m.motor_instance = ergoJr.motors[(m.id -1)]

        server = SimpleServer(('127.0.0.1', 12344))    
        try:
            server.serve_forever()
        except:
            print(" ERROR : sequence -  on running OSC server")

                          


if __name__ == "__main__":
    main()
