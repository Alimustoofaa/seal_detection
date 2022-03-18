import cv2
from src import MainProcess

app = MainProcess()

image = cv2.imread('20220223_093915.jpg')
app.main(image)