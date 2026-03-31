import cv2
import os
from playsound import playsound

base_path = os.path.dirname(__file__)

face_cascade = cv2.CascadeClassifier(os.path.join(base_path, 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(base_path, 'haarcascade_eye.xml'))

cap = cv2.VideoCapture(0)

alarm_on = False

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) == 0:
            cv2.putText(frame, "ALERT! Eyes Closed", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

            if not alarm_on:
                alarm_on = True
                playsound(os.path.join(base_path, 'alarm.mp3'))

        else:
            cv2.putText(frame, "Eyes Open", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            alarm_on = False

    cv2.imshow('Driver Monitoring System', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()