import time

class poppy_motor:
	def __init__(self, _id, min=-130, max=130):
		self.id = _id
		self.position  = 0
		self.asked_position = 0
		self.starting_position = 0
		self.compliant = False
		self.led = "black"
		self.motor_instance = None
		self.smooth = 0.03
		self.posMin = min
		self.posMax = max
		self.speedMin = 15
		self.speedMax = 70

	def setValue(self, newVal):
		
		if(newVal<self.posMin):
			newVal = self.posMin
		if(newVal>self.posMax):
			newVal = self.posMax

		print("Set value")
		print (newVal)
		self.currentValue = newVal
		self.isModified = True
		self.asked_position = newVal
		#MOVE DIRECTLY TO POS BUT SMOOTH USING SPEED
		self.setSpeed(self.speedMin)
		self.moveTo(self.asked_position)
		self.starting_position = self.motor_instance.present_position

	def update(self):
		#UPDATE POSITION
		self.position = self.motor_instance.present_position

		#Todo : IS THE MOTOR MOVING OR NOT, if yes, calculate position
		# send a signal when position is reached.
		# at the app pov, send an OSC signal when all the motor are in a reached position ( position done)

		#CALCUTE POSITION ( 1st half or 2nd half of the entire trajectory)
		if(abs(self.position - self.starting_position) < (abs(self.starting_position - self.asked_position)/2.5)):
			#1st half
			if(self.speed < self.speedMax):
				newSpeed = self.speed*( 1.0 + self.smooth)
				self.setSpeed(newSpeed)
		else:
			#2nd half
			if(self.speed>self.speedMin):
				newSpeed = self.speed*(1.0 - self.smooth)
				self.setSpeed(newSpeed)

		#print(" motor "+str(self.id)+ ": position: "+str(self.position)+" asked: "+str(self.asked_position)+" smoothPos: "+str(smoothPos)+" res: "+str(res)+ "smooth: "+str(self.smooth))


	def moveTo(self, directPos):
		#print(" move to "+str(directPos))
		self.motor_instance.goal_position = directPos

	def setCompliant(self, isCompliant):
		self.motor_instance.compliant = isCompliant
		print(" Motor compliant set to : ")
		print("isCompliant")

	def setLedColor(self, colorMsg):
		self.motor_instance.led = colorMsg
		print(" Motor led set to : "+colorMsg)

	def setSmooth(self, newSmooth):
		if(newSmooth<100 and newSmooth>0):
			self.smooth = newSmooth/100.0
			print(" Motor smooth set to : "+str(self.smooth))
		else:
			print("Smooth out of range, should be between 0 and 100")
	
	def setSpeed(self, newSpeed):
		if(newSpeed<15 ):
			newSpeed = 15
		if(newSpeed>255):
			newSpeed= 255
		self.motor_instance.moving_speed = newSpeed
		self.speed = newSpeed
		print(" Motor speed set to : "+str(newSpeed))

