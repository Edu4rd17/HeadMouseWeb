from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
import cv2
import mediapipe as mp
import pyautogui


views = Blueprint('views', __name__)

camera = cv2.VideoCapture(0)
# the refine landmarks is used to get more accurate landmarks on the face
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = pyautogui.size()


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        # flip the frame
        frame = cv2.flip(frame, 1)
        # convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process the rgb_frame using face_mesh
        results = face_mesh.process(rgb_frame)
        # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
        landmark_points = results.multi_face_landmarks
        # get the height and width of the frame
        frame_height, frame_width, _ = frame.shape
        # check if there are landmarks
        if landmark_points:
            landmarks = landmark_points[0].landmark
            # loop through all the landmark points; select a range of index as we are only interested in the eyes
            for id, landmark in enumerate(landmarks[474:478]):
                # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
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
            # check if the distance between the two points is less than 0.004
            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # concat frame one by one and show result
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@ views.route('/')
def index():
    return render_template("index.html", user=current_user)


# Fix so that we cant access this page if we are not logged in as admin
@ views.route('/video')
@ login_required
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


@ views.route('/about')
def about():
    return render_template("about.html", user=current_user)


@ views.route('/userProfile')
@ login_required
def userProfile():
    return render_template("userProfile.html", user=current_user)
