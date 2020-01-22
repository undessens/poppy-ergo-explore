import time

class poppy_motor:
	def __init__(self, _id):
		self.id = _id
		self.position  = 0
		self.asked_position = 0
		self.starting_position = 0
		self.compliant = False
		self.led = "black"
		self.motor_instance = None
		self.smooth = 0.08

	def setValue(self, newVal):
		if(newVal>=-90 and newVal <= 90):
			print("Set value")
			print (newVal)
			self.currentValue = newVal
			self.isModified = True
			self.asked_position = newVal
			#MOVE DIRECTLY TO POS BUT SMOOTH USING SPEED
			self.moveTo(self.asked_position)
			self.setSpeed(15)
			self.starting_position = self.motor_instance.present_position

	def update(self):
		#UPDATE POSITION
		self.position = self.motor_instance.present_position

		#CALCUTE POSITION ( 1st half or 2nd half of the entire trajectory)
		if(abs(self.position - self.starting_position) < (abs(self.starting_position - self.asked_position)/2)):
			#1st half
			if(self.speed < 255):
				newSpeed = self.speed*1.08
				self.setSpeed(self.newSpeed)
		else:
			#2nd half
			if(self.speed>15):
				newSpeed = self.speed*0.93
				self.setSpeed(self.newSpeed)

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







