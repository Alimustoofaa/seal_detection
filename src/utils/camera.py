import cv2
import time

class Camera:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    
    def run(self):
        while not self.cap.isOpened():
            print("Error opening video stream or file")
            self.cap.release(); time.sleep(1)
            self.__init__(self.camera_id)
        return self.cap
    
    def release(self, ret=True):
        self.cap.release()
        if not ret: self.run()
        cv2.destroyAllWindows()
    
    def show(self,frame, window_name='Frame'):
        cv2.imshow(window_name, frame)
        return cv2.waitKey(30)