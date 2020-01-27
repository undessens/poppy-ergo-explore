import time

class poppy_motor:
	def __init__(self, _id, _min = -90, _max = 90):
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
		self.position = self.asked_position
		self.moveTo(self.position)

	def moveTo(self, dist):
		#print(" move to "+str(dist))
		time.sleep(0.001)

	def setCompliant(self, isCompliant):
		print(" Motor compliant set to : ")
		print(isCompliant)

	def setLedColor(self, colorMsg):
		print(" Motor led set to : "+colorMsg)

	def setSpeed(self, newSpeed):
		print(" Motor speed set to : "+str(newSpeed))
	
	def setSmooth(self, newSmooth):
		if(newSmooth<100 and newSmooth>0):
			self.smooth = newSmooth/100.0
			print(" Motor smooth set to : "+str(self.smooth))
		else:
			print("Smooth out of range, should be between 0 and 100")

	







