#!/usr/bin/env python
#!/usr/bin/python3

from picamera import PiCamera
from time import sleep

#camera=PiCamera()
#camera.start_preview()
#sleep(10)
#camera.stop_preview()

camera=PiCamera()
camera.start_preview()
camera.start_recording('/home/pi/Desktop/video.h264')
#camera.start_recording('/home/pi/Desktop/video.mp4')
sleep(10)
camera.stop_recording()
camera.stop_preview()