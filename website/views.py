from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
import cv2
import mediapipe as mp
import pyautogui


views = Blueprint('views', __name__)

camera = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = pyautogui.size()

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        #flip the frame
        frame = cv2.flip(frame, 1)
        # convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process the frame using face_mesh
        results = face_mesh.process(rgb_frame)
        # landmarks of the face
        landmark_points = results.multi_face_landmarks
        # draw the landmarks on the frame
        frame_height, frame_width, _ = frame.shape
        if landmark_points:
            # loop through all the landmark points
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                # get the x and y coordinates of the landmarks
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # draw a circle on the landmark
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_width / frame_width * x
                    screen_y = screen_height / frame_height * y
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # concat frame one by one and show result
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def gen_frames():  # generate frame by frame from camera
#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     eye_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + 'haarcascade_eye.xml')

#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             faces = face_cascade.detectMultiScale(frame, 1.1, 7)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             # Draw rectangle around the faces
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#                 roi_gray = gray[y:y+h, x:x+w]
#                 roi_color = frame[y:y+h, x:x+w]
#                 eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
#                 for (ex, ey, ew, eh) in eyes:
#                     cv2.rectangle(roi_color, (ex, ey),
#                                   (ex+ew, ey+eh), (0, 255, 0), 2)

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         # concat frame one by one and show result
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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


@views.route('/youtube')
@login_required
def youtube():
    return render_template("youtube.html", user=current_user)
