from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
import cv2

views = Blueprint('views', __name__)

camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces = face_cascade.detectMultiScale(frame, 1.1, 7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey),
                                  (ex+ew, ey+eh), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # concat frame one by one and show result
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@ views.route('/')
def index():
    return render_template("index.html", user=current_user)


@ views.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@ views.route('/home')
@ login_required
def home():
    return render_template("home.html", user=current_user)
