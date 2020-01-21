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
			self.moveTo(newVal)

	def update(self):
		#Can smooth the final value send in OSC, using an easing method
		diff = self.asked_position - self.position
		if(abs(diff)>0):
			self.moveTo(self.position + diff*self.smooth)

	def moveTo(self, dist):
		print(" move to "+str(dist))

	def setCompliant(self, isCompliant):
		print(" Motor compliant set to : ")
		print(isCompliant)

	def setLedColor(self, colorMsg):
		print(" Motor led set to : "+colorMsg)







