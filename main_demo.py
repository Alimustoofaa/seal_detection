import cv2
import time
from src import MainProcess
from adam_io import DigitalOutput
from src.utils import Adam6050DInput
from src.utils.camera import Camera
from adam_io import DigitalOutput

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2)
		self.camera_run  	= self.camera.run()
		self.adam			= Adam6050DInput()
		self.app         	= MainProcess()
		self.current_B1		= 1
		self.next_frame		= 2
	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(4)), int(self.camera_run.get(3)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (1080,1920))

	def run(self):
		# Condition start capture and running app
		print('Starting Application')
		while True:
			adam_inputs = self.adam.di_inputs()
			B1 			= adam_inputs[2][1]

			ret, frame = self.camera_run.read()
			if not ret:
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
				continue
			else:
				if self.current_B1 == 1 and B1 == 0:
					self.adam.di_output(DigitalOutput(array=[1,0,1,0,0,0]))
				if self.current_B1 == 0 and B1 == 1:
					time_start = int(time.time())
					frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
					#if self.next_frame == True:
					print('Capture Photo')
					drawed = self.app.main(frame, id=time_start)
					#cv2.imwrite(f'{time_start}.jpg', drawed)
					time.sleep(2)
					self.adam.di_output(DigitalOutput(array=[0,0,0,0,0,0]))
				#key_window = self.camera.show(resized)
			#self.adam.di_output(DigitalOutput(array=[0,0,0,0,0,0]))
			self.current_B1 = B1
			key = cv2.waitKey(30)
			if key == 27: break

		self.camera.release()

if __name__ == '__main__':
	application  = RunApplication()
	application.run()

