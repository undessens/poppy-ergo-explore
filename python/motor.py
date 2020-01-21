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
			self.moveTo(newVal)

	def update(self):
		#Can smooth the final value send in OSC, using an easing method
		print("update")
		self.position = self.motor_instance.present_position
		print("Update motor "+str(id+ ": position: "+str(self.position)+" asked: "+str(self.asked_position)))
		diff = self.asked_position - self.position
		if(abs(diff)>0):
			smoothPos = self.position + (diff*self.smooth)
			#self.moveTo(smoothPos)
		print(" motor "+str(id+ ": position: "+str(self.position)+" asked: "+str(self.asked_position)+" smoothPos: "+str(smoothPos)))


	def moveTo(self, dist):
		print(" move to "+str(dist))
		self.motor_instance.goal_position = dist


	def setCompliant(self, isCompliant):
		self.motor_instance.compliant = isCompliant
		print(" Motor compliant set to : ")
		print("isCompliant")

	def setLedColor(self, colorMsg):
		self.motor_instance.led = colorMsg
		print(" Motor led set to : "+colorMsg)
	
	def setSpeed(self, newSpeed):
		self.motor_instance.moving_speed = newSpeed
		print(" Motor speed set to : "+str(newSpeed))







