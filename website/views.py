import math
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import login_user, login_required, current_user
import cv2
import mediapipe as mp
import pyautogui
from . import db
from flask_mail import Message
from .models import User
import numpy as np
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

views = Blueprint('views', __name__)


# camera = cv2.VideoCapture(0)
# # the refine landmarks is used to get more accurate landmarks on the face
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# screen_width, screen_height = pyautogui.size()


# def gen_frames():  # generate frame by frame from camera
#     while True:
#         # Capture frame-by-frame
#         success, frame = camera.read()  # read the camera frame
#         # flip the frame
#         frame = cv2.flip(frame, 1)
#         # convert the frame to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # process the rgb_frame using face_mesh
#         results = face_mesh.process(rgb_frame)
#         # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
#         landmark_points = results.multi_face_landmarks
#         # get the height and width of the frame
#         frame_height, frame_width, _ = frame.shape
#         # check if there are landmarks
#         if landmark_points:
#             landmarks = landmark_points[0].landmark
#             # loop through all the landmark points; select a range of index as we are only interested in the eyes
#             for id, landmark in enumerate(landmarks[474:478]):
#                 # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
#                 x = int(landmark.x * frame_width)
#                 y = int(landmark.y * frame_height)
#                 # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
#                 #right eye
#                 cv2.circle(frame, (x, y), 3, (0, 255, 0))
#                 if id == 1:
#                     screen_x = screen_width / frame_width * x
#                     screen_y = screen_height / frame_height * y
#                     pyautogui.moveTo(screen_x, screen_y)
#             left = [landmarks[145], landmarks[159]]
#             for landmark in left:
#                 x = int(landmark.x * frame_width)
#                 y = int(landmark.y * frame_height)
#                 #left eye
#                 cv2.circle(frame, (x, y), 3, (0, 255, 255))
#             # check if the distance between the two points is less than 0.004
#             if (left[0].y - left[1].y) < 0.004:
#                 pyautogui.click()
#                 pyautogui.sleep(1)
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         # concat frame one by one and show result
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def gen_frames():  # generate frame by frame from camera
#     pass
#     while True:
#         #         # Capture frame-by-frame
#         success, frame = camera.read()  # read the camera frame
# #         # flip the frame
#         frame = cv2.flip(frame, 1)
#         # convert the frame to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # process the rgb_frame using face_mesh
#         results = face_mesh.process(rgb_frame)
#         # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
#         landmark_points = results.multi_face_landmarks
#         # get the height and width of the frame
#         frame_height, frame_width, _ = frame.shape
#         # check if there are landmarks
#         if landmark_points:
#             landmarks = landmark_points[0].landmark
#             # loop through all the landmark points; select a range of index as we are only interested in the eyes
#             for id, landmark in enumerate(landmarks[474:478]):
#                 # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
#                 x = int(landmark.x * frame_width)
#                 y = int(landmark.y * frame_height)
#                 # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
#                 # right eye
#                 cv2.circle(frame, (x, y), 3, (0, 255, 0))
#                 if id == 1:
#                     screen_x = screen_width / frame_width * x
#                     screen_y = screen_height / frame_height * y
#                     pyautogui.moveTo(screen_x, screen_y)
#             left = [landmarks[145], landmarks[159]]
#             for landmark in left:
#                 x = int(landmark.x * frame_width)
#                 y = int(landmark.y * frame_height)
#                 # left eye
#                 cv2.circle(frame, (x, y), 3, (0, 255, 255))
#             # check if the distance between the two points is less than 0.004
#             if (left[0].y - left[1].y) < 0.004:
#                 pyautogui.click()
#                 pyautogui.sleep(1)
# ret, buffer = cv2.imencode('.jpg', frame)
# frame = buffer.tobytes()
# # concat frame one by one and show result
# yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_face_mesh = mp.solutions.face_mesh
# cap = cv2.VideoCapture(0)
# screen_width, screen_height = pyautogui.size()
# LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249,
#             263, 466, 388, 387, 386, 385, 384, 398, 362]
# RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155,
#              133, 173, 157, 158, 159, 160, 161, 246, 33]

# RIGHT_IRIS = [474, 475, 476, 477]
# LEFT_IRIS = [469, 470, 471, 472]
# L_H_LEFT = [33]  # RIGHT EYE RIGHT CORNER
# L_H_RIGHT = [133]  # RIGHT EYE LEFT CORNER
# R_H_LEFT = [362]  # LEFT EYE LEFT CORNER
# R_H_RIGHT = [263]  # LEFT EYE RIGHT CORNER


# def euclidean_distance(point1, point2):
#     x1, y1 = point1.ravel()
#     x2, y2 = point2.ravel()
#     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#     return distance


# def iris_position(iris_center, right_point, left_point):
#     center_to_right_distance = euclidean_distance(iris_center, right_point)
#     total_distance = euclidean_distance(right_point, left_point)
#     ratio = center_to_right_distance / total_distance
#     iris_position = ''
#     if ratio < 0.32:
#         iris_position = 'left'
#     elif ratio > 0.32 and ratio < 0.57:
#         iris_position = 'center'
#     else:
#         iris_position = 'right'
#     return iris_position, ratio


# def gen_frames():
#     drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
#     with mp_face_mesh.FaceMesh(
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5) as face_mesh:
#         while True:

#             success, image = cap.read()
#             if not success:
#                 print("Ignoring empty camera frame.")
#                 # If loading a video, use 'break' instead of 'continue'.
#                 break

#             # To improve performance, optionally mark the image as not writeable to
#             # pass by reference.
#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             results = face_mesh.process(image)
#             # Draw the face mesh annotations on the image.
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             img_height, img_width = image.shape[:2]
#             if results.multi_face_landmarks:
#                 # print(results.multi_face_landmarks)
#                 # for face_landmarks in results.multi_face_landmarks:
#                 mesh_points = np.array([np.multiply([p.x, p.y], [img_width, img_height]).astype(
#                     int) for p in results.multi_face_landmarks[0].landmark])
#                 # print(mesh_points.shape)
#                 cv2.polylines(image, [mesh_points[LEFT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)
#                 cv2.polylines(image, [mesh_points[RIGHT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)
#                 (left_cx, left_cy), left_radius = cv2.minEnclosingCircle(
#                     mesh_points[LEFT_IRIS])
#                 (right_cx, right_cy), right_radius = cv2.minEnclosingCircle(
#                     mesh_points[RIGHT_IRIS])
#                 center_left = np.array([left_cx, left_cy], dtype=np.int32)
#                 center_right = np.array([right_cx, right_cy], dtype=np.int32)
#                 cv2.circle(image, center_left, int(left_radius), (0, 255, 255), 1, cv2.LINE_AA)
#                 cv2.circle(image, center_right, int(
#                     right_radius), (0, 255, 255), 1, cv2.LINE_AA)
#                 cv2.circle(
#                     image, mesh_points[R_H_RIGHT][0], 2, (255, 255, 255), -1, cv2.LINE_AA)
#                 cv2.circle(image, mesh_points[R_H_LEFT]
#                            [0], 2, (0, 255, 255), -1, cv2.LINE_AA)
#                 iris_pos, ratio = iris_position(
#                     center_right, mesh_points[R_H_RIGHT], mesh_points[R_H_LEFT][0])
#                 print(iris_pos)
#             image = cv2.flip(image, 1)
#             ret, buffer = cv2.imencode('.jpg', image)
#             image = buffer.tobytes()
#             # concat frame one by one and show result
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
screen_w, screen_h = pyautogui.size()
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
# cap = cv2.VideoCapture(0)

# generate frame by frame from camera


def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while cap.isOpened():
        # generate frame by frame from camera
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            break
            # flip the frame
        image = cv2.flip(image, 1)
        # convert the frame to RGB
        imageRBG = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        # process the rgb_frame using face_mesh
        results = face_mesh.process(imageRBG)
        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
                landmark_points = results.multi_face_landmarks
                # get the height and width of the frame
                frame_h, frame_w, _ = image.shape
                # check if there are landmarks
                if landmark_points:
                    # get the landmarks of the first face
                    landmarks = landmark_points[0].landmark
                    # loop through all the landmark points; select a range of index as we are only interested in the eyes
                    for id, landmark in enumerate(landmarks[474:478]):
                        # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
                        # right eye
                        cv2.circle(image, (x, y), 3, (0, 255, 0))

                        if id == 1:
                            screen_x = screen_w * landmark.x
                            screen_y = screen_h * landmark.y
                            pyautogui.moveTo(screen_x, screen_y)
                    left = [landmarks[145], landmarks[159]]
                    for landmark in left:
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        cv2.circle(image, (x, y), 3, (0, 255, 255))
                    if (left[0].y - left[1].y) < 0.004:
                        pyautogui.click()
                        pyautogui.sleep(1)
        # else:
            # with init.create_app().app_context():
            #     message = "No face detected"
            #     category = "error"
            #     response = {'message': message, 'category': category}
            # return jsonify(response)'
            # print("No face detected")

         # encode the image as JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        # convert the image buffer to bytes
        image = buffer.tobytes()
        # yield the output frame in the byte format
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

#   # release the capture and destroy all windows
#     cap.release()
#     cv2.destroyAllWindows()


click_thread = None
click_stop_event = threading.Event()


def auto_click(stop_event):
    while not stop_event.is_set():
        x, y = pyautogui.position()
        time.sleep(0.5)  # wait 1 second before checking again
        x2, y2 = pyautogui.position()
        if abs(x - x2) < 5 and abs(y - y2) < 5:  # if mouse position hasn't changed much
            pyautogui.click()


@views.route('/start-click', methods=['POST'])
def start_click():
    global click_thread
    if click_thread and click_thread.is_alive():
        message = "Auto-clicking already in progress."
        category = "error"
    else:
        click_stop_event.clear()  # clear the stop event
        click_thread = threading.Thread(
            target=auto_click, args=(click_stop_event,))
        click_thread.start()
        message = "Auto-clicking started."
        category = "success"
    response = {'message': message, 'category': category}
    return jsonify(response)


@views.route('/stop-click', methods=['POST'])
def stop_click():
    global click_thread
    if click_thread and click_thread.is_alive():
        click_stop_event.set()  # set the stop event
        click_thread.join()  # wait for the thread to finish
        click_thread = None
        message = "Auto-clicking stopped."
        category = "success"
    else:
        message = "Auto-clicking not in progress."
        category = "error"
    response = {'message': message, 'category': category}
    return jsonify(response)


@ views.route('/')
def index():
    return render_template("index.html", user=current_user)

# Fix so that we cant access this page if we are not logged in as admin


@ views.route('/video')
# @ login_required
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@ views.route('/home', methods=['GET', 'POST'])
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


def update_details(user):
    msg = Message('Account Details Updated',
                  sender='noreply@headmouseweb.com', recipients=[user.email])
    msg.body = f'''Hi {user.firstName},

 You have successfully updated your account details. If you did not make this change, please contact us immediately!
'''
    from . import mail
    mail.send(msg)


@ views.route('/userProfileEdit',  methods=['GET', 'POST'])
@ login_required
def userProfileEdit():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        country = request.form.get('country')
        gender = request.form.get('gender')

        if len(firstName) < 2:
            flash('First name must be greater than 1 character.',
                  category='error')

            return redirect(url_for('views.userProfileEdit'))

        else:
            if email != current_user.email:

                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Email already exists.', category='error')

                    return redirect(url_for('views.userProfileEdit'))

                elif len(email) < 4:
                    flash('Email must be greater than 3 characters.',
                          category='error')

                    return redirect(url_for('views.userProfileEdit'))

                current_user.firstName = firstName
                current_user.lastName = lastName
                current_user.email = email
                current_user.country = country
                current_user.gender = gender
                db.session.commit()
                update_details(current_user)
                flash('Details Updated Successfully', category='success')

            elif email == current_user.email:

                current_user.firstName = firstName
                current_user.lastName = lastName
                current_user.country = country
                current_user.gender = gender
                db.session.commit()
                update_details(current_user)
                flash('Details Updated Successfully', category='success')

        return redirect(url_for('views.userProfile'))
    return render_template("userProfileEdit.html", user=current_user)

# remove user account


@ views.route('/deleteAccount',  methods=['GET', 'POST'])
@ login_required
def deleteAccount():
    db.session.delete(current_user)
    db.session.commit()
    flash('Account Deleted Successfully', category='success')
    return redirect(url_for('views.index'))
