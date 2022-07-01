#! /usr/bin/python

from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from multiprocessing import Process
import RPi.GPIO as GPIO
from pybo.views import attendance_views

def camera_work():
    pir_sensor = 4
    # PIR Sensor setting
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_sensor, GPIO.IN)
    print("PIR Sensor Ready...")
    time.sleep(2)   # PIR 센서 준비 시간

    #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    #Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    is_detected = False
    detected_period = 0

    # loop over frames from the video file stream
    while True:
        if GPIO.input(pir_sensor) == 1:
            is_detected = True
            detected_period = 10
            print("motion detected!")
            
        elif GPIO.input(pir_sensor) == 0:
            detected_period -= 1
            print("no motion")
        
        if detected_period <=0:
            is_detected= False

        if is_detected:
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            encodings = face_recognition.face_encodings(frame)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                    encoding)
                name = "Unknown" #if face is not recognized, then print Unknown

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)
                    print(name)
                    attendance_views.check_attend(name)

                names.append(name)

            # display the image to our screen
            cv2.imshow("Facial Recognition is Running", frame)
            
        elif not is_detected:
            time.sleep(0.3)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()

    
def parallel_camera_work():
    camera_proc = Process(target=camera_work, args=())
    camera_proc.start()


if __name__ == "__main__":
    pass