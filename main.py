from src.utils.camera import Camera
from src import MainProcess

camera      = Camera(0)
camera_run  = camera.run()
app         = MainProcess()
skip_frame  = False

while True:
    ret, frame = camera_run.read()
    if not ret:
        camera.release(ret=False)
        capture = camera.run()

    if not skip_frame:
        result = app.main(frame)
        print(result)
        skip_frame = True
    else: skip_frame = False
    
    key_window = camera.show(frame)
    if key_window == 27: break

app.seal_detection.release()
camera.release()
