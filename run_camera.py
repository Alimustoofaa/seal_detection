import cv2
import time

from src.utils.camera import Camera

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2)
		self.camera_run  	= self.camera.run()

	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(4)), int(self.camera_run.get(3)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (1080,1920))

	def run(self):
		# Define Write Video
		time_now = time.time()
		#out_video =  self.__write_video(time_now)

		while True:
			ret, frame = self.camera_run.read()
			if not ret:
				print('aaa')
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
				continue
			else:
				frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
				#out_video.write(frame)
				resized = cv2.resize(frame, (480, 720), interpolation = cv2.INTER_AREA);# cv2.imwrite(f'frame_6.jpg', frame)
				key_window = self.camera.show(resized)
				if key_window == 27: break

		out_video.release()
		self.camera.release()

if __name__ == '__main__':
	application  = RunApplication()
	application.run()

