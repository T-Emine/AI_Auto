import numpy

import socketio
import eventlet
import base64
from PIL import Image
from io import BytesIO
import argparse
from detector import ObjectDetector
import cv2


# create a Socket.IO server
sio = socketio.Server()
# event sent by the simulator
class Angle:
    val=0
ang=Angle()
@sio.on('telemetry')
def telemetry(sid, data):
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--detector", required=True, help="path to trained detector to load...")
    ap.add_argument("-dL", "--detectorL", required=True, help="path to trained detector to load...")
    ap.add_argument("-dR", "--detectorR", required=True, help="path to trained detector to load...")
    ap.add_argument("-i", "--image", required=True, help="path to an image for object detection...")
    ap.add_argument("-a", "--annotate", default=None, help="text to annotate...")
    ap.add_argument("-aL", "--annotateL", default=None, help="text to annotate...")
    ap.add_argument("-aR", "--annotateR", default=None, help="text to annotate...")
    args = vars(ap.parse_args())
    detector = ObjectDetector(loadPath=args["detector"])
    detectorR = ObjectDetector(loadPath=args["detectorR"])
    detectorL = ObjectDetector(loadPath=args["detectorL"])
    if data:
        # The current steering angle of the car
        steering_angle = float(data["steering_angle"])
        # The current throttle of the car, how hard to push peddle
        throttle = float(data["throttle"])
        # The current speed of the car
        speed = float(data["speed"])
        # The current image from the center camera of the car
        im=Image.open(BytesIO(base64.b64decode(data["image"])))
        im.save("img.jpg")
        image = cv2.imread("./img.jpg")
        z = detector.detect(image, annotate=args["annotate"])
        x = detectorR.detect(image, annotate=args["annotateL"])
        y = detectorL.detect(image, annotate=args["annotateR"])
        # Use your model to compute steering and throttle
        if x==1:
            ang.val-=0.018
        # if y==1:
        #     angle -= 0.04
        #     steer = angle
        if z==1:
            ang.val=0
        throttle = 0.2
        # response to the simulator with a steer angle and throttle
        send(ang.val, throttle)
    else:
        # Edge case
        sio.emit('manual', data={}, skip_sid=True)

# event fired when simulator connect
@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send(0, 0)

# to send steer angle and throttle to the simulator
def send(steer, throttle):
    sio.emit("steer", data={'steering_angle': str(steer), 'throttle': str(throttle)}, skip_sid=True)


# wrap with a WSGI application
app = socketio.WSGIApp(sio)

# simulator will connect to localhost:4567
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)