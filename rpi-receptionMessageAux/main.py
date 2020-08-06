import serial
import time
import os
import sys
import glob
from OSC import OSCServer, OSCMessage

global serialManager
global OSCserver



def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ports = []
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port,115200)
            s.close()
            print "Serial found in "+port
            result.append(port)
        except :
            print "probleme ouverture serial : "+port
            pass
    return result



class SimpleServer(OSCServer):
	global serialManager
	# OpenStageControls script pings every 3 seconds
	def __init__(self,t):
		OSCServer.__init__(self,t)
		self.selfInfos = t
		self.addMsgHandler('default', self.handleMsg)

	
	def handleMsg(self,oscAddress, tags, data, client_address):
		
		print "************** SEQUENCE ******************"
		print( "OSC message : "+oscAddress )

		splitAddress = oscAddress.split("/")
		
		############## SEQUENCE #############
		if(splitAddress[1]=="short"):
			serialManager.write('a')
			print(" Serial write short message")
		if(splitAddress[1]=="long"):
			serialManager.write('b')
			print(" Serial write long message")


			

if __name__ == '__main__':

	#Serial print port available
	serialNames = serial_ports()
	print "liste des ports serial"
	print serialNames

	#Serial connect
	try:
		if sys.platform.startswith('darwin'):
			serialManager = serial.Serial((serial_ports())[1],115200)
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			serialManager = serial.Serial('/dev/ttyACM0',115200)
			#ser = serial.Serial('/dev/ttyACM1', 115200)
		elif sys.platform.startswith('win'):
			serialManager = serial.Serial(serialNames[0],115200)
		else:
			serialManager = None
	except :
		print "Impossible to connect to Serial"
		serialManager = None	

	#OSC SERVER
	if(len(sys.argv)>1):
		print ("bridge OSC serial Arg Found : start server on :"+str(sys.argv[1]))
		OSCServer = SimpleServer((str(sys.argv[1]), 12348))
	else:
		print ("Sequence.py No Arg Found : start server on localhost")
		OSCServer = SimpleServer(('127.0.0.1', 12348))

	try:
		OSCServer.serve_forever()
	except:
		print(" ERROR : sequence -  on running OSC server")

	print "************** BRIDGE OSC SERIAL ******************"
	print "sequence- exiting"
	exit(0)


