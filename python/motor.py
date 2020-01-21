import time

class poppy_motor:
	def __init__(self, _id):
		self.id = _id
		self.speed = 50
		self.position  = 0
		self.asked_position = 0
		self.compliant = False
		self.led = "black"
		self.motor_instance = None
		self.smooth = 0.1

	def setValue(self, newVal):
		if(newVal>=-90 and newVal <= 90):
			print("Set value")
			print (newVal)
			self.currentValue = newVal
			self.isModified = True
			self.asked_position = newVal

	def update(self):
		#Can smooth the final value send in OSC, using an easing method
		print("update")
		self.position = self.motor_instance.present_position
		diff = self.asked_position - self.position
		if(abs(diff)>1):
			smoothPos = self.position + (diff*self.smooth)
			self.moveTo(smoothPos)
		else:
			print("Position reached")
			smoothPos = self.position
		print(" motor "+str(self.id)+ ": position: "+str(self.position)+" asked: "+str(self.asked_position)+" smoothPos: "+str(smoothPos))


	def moveTo(self, directPos):
		print(" move to "+str(directPos))
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
		self.motor_instance.moving_speed = newSpeed
		print(" Motor speed set to : "+str(newSpeed))







