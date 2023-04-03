import math
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import login_user, login_required, current_user
import cv2
import mediapipe as mp
import pyautogui
from . import db
from flask_mail import Message
from .models import User
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

views = Blueprint('views', __name__)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False
)
screen_w, screen_h = pyautogui.size()
drawing_spec = mp_drawing.DrawingSpec(
    thickness=1, circle_radius=1)

# def gen_frames():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Cannot open camera")
#         return
#     face_count = 0
#     landmark_x0 = 0.5
#     landmark_y0 = 0.5
#     while cap.isOpened():
#         # generate frame by frame from camera
#         success, image = cap.read()

#         if not success:
#             print("Ignoring empty camera frame.")
#             # If loading a video, use 'break' instead of 'continue'.
#             break
#             # flip the frame
#         image = cv2.flip(image, 1)
#         # convert the frame to RGB
#         imageRBG = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         # process the rgb_frame using face_mesh
#         results = face_mesh.process(imageRBG)
#         # Draw the face mesh annotations on the image.
#         image.flags.writeable = True
#         if results.multi_face_landmarks:
#             face_count += 1
#             for face_landmarks in results.multi_face_landmarks:
#                 # mp_drawing.draw_landmarks(
#                 #     image=image,
#                 #     landmark_list=face_landmarks,
#                 #     connections=mp_face_mesh.FACEMESH_IRISES,
#                 #     landmark_drawing_spec=None,
#                 #     connection_drawing_spec=mp_drawing_styles
#                 #     .get_default_face_mesh_iris_connections_style())
#                 mp_drawing.draw_landmarks(
#                     image=image,
#                     landmark_list=face_landmarks,
#                     connections=mp_face_mesh.FACEMESH_TESSELATION,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=mp_drawing_styles
#                     .get_default_face_mesh_tesselation_style())
#                 # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
#                 landmark_points = results.multi_face_landmarks
#                 # get the height and width of the frame
#                 frame_h, frame_w, _ = image.shape
#                 # check if there are landmarks
#                 if landmark_points:
#                     # get the landmarks of the first face
#                     landmarks = landmark_points[0].landmark
#                     # loop through all the landmark points; select a range of index as we are only interested in the eyes
#                     nose_tip = landmarks[5]

#                     if face_count == 3:
#                         landmark_x0 = nose_tip.x
#                         landmark_y0 = nose_tip.y
#                     # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
#                     x = int(nose_tip.x * frame_w)
#                     y = int(nose_tip.y * frame_h)

#                     # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
#                     # right eye
#                     cv2.circle(image, (x, y), 3, (0, 255, 0))

#                     # make the cursor move a bigger amount of pixels at a time
#                     k = 6
#                     screen_x = (nose_tip.x - landmark_x0) * \
#                         (screen_w * k) + screen_w * landmark_x0
#                     screen_y = (nose_tip.y - landmark_y0) * \
#                         (screen_h * k) + screen_h * landmark_y0
#                     # set pyauto gui to false
#                     pyautogui.FAILSAFE = False
#                     pyautogui.moveTo(screen_x, screen_y)
#                     left = [landmarks[145], landmarks[159]]
#                     for landmark in left:
#                         x = int(landmark.x * frame_w)
#                         y = int(landmark.y * frame_h)
#                         cv2.circle(image, (x, y), 3, (0, 255, 255))
#                     if (left[0].y - left[1].y) < 0.004:
#                         pyautogui.click()
#                         pyautogui.sleep(1)
#         else:
#             print("No face detected")

#          # encode the image as JPEG
#         ret, buffer = cv2.imencode('.jpg', image)
#         # convert the image buffer to bytes
#         image = buffer.tobytes()
#         # yield the output frame in the byte format
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    face_count = 0
    landmark_x0 = 0.5
    landmark_y0 = 0.5
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
            face_count += 1
            for face_landmarks in results.multi_face_landmarks:
                # mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=mp_face_mesh.FACEMESH_IRISES,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=mp_drawing_styles
                #     .get_default_face_mesh_iris_connections_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
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
                        if face_count == 3:
                            landmark_x0 = landmark.x
                            landmark_y0 = landmark.y
                        # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)

                        # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
                        # right eye
                        cv2.circle(image, (x, y), 3, (0, 255, 0))

                        if id == 1:
                            # make the cursor move a bigger amount of pixels at a time
                            k = 6
                            screen_x = (landmark.x - landmark_x0) * \
                                (screen_w * k) + screen_w * landmark_x0
                            screen_y = (landmark.y - landmark_y0) * \
                                (screen_h * k) + screen_h * landmark_y0
                            # set pyauto gui to false
                            pyautogui.FAILSAFE = False
                            pyautogui.moveTo(screen_x, screen_y)
                    left = [landmarks[145], landmarks[159]]
                    for landmark in left:
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        cv2.circle(image, (x, y), 3, (0, 255, 255))
                    if (left[0].y - left[1].y) < 0.004:
                        pyautogui.click()
                        pyautogui.sleep(1)
        else:
            # display the text if no face is detected
            cv2.putText(image, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

         # encode the image as JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        # convert the image buffer to bytes
        image = buffer.tobytes()
        # yield the output frame in the byte format
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


# def gen_frames():
#     scale = 20
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Cannot open camera")
#         return
#     face_count = 0
#     landmark_x0 = 0.5
#     landmark_y0 = 0.5
#     while cap.isOpened():
#         # generate frame by frame from camera
#         success, image = cap.read()

#         if not success:
#             print("Ignoring empty camera frame.")
#             # If loading a video, use 'break' instead of 'continue'.
#             break
#             # flip the frame
#         image = cv2.flip(image, 1)

#         # get the height and width of the frame
#         frame_h, frame_w, _ = image.shape

#         # prepare the crop
#         centerX, centerY = int(frame_h/2), int(frame_w/2)
#         radiusX, radiusY = int(scale*frame_h/100), int(scale*frame_w/100)

#         minX, maxX = centerX-radiusX, centerX+radiusX
#         minY, maxY = centerY-radiusY, centerY+radiusY
#         cropped = image[minX:maxX, minY:maxY]
#         resized_cropped_image = cv2.resize(cropped, (frame_w, frame_h))
#         # convert the frame to RGB
#         imageRBG = cv2.cvtColor(resized_cropped_image, cv2.COLOR_BGR2RGB)

#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         resized_cropped_image.flags.writeable = False
#         # process the rgb_frame using face_mesh
#         results = face_mesh.process(imageRBG)
#         # Draw the face mesh annotations on the image.
#         resized_cropped_image.flags.writeable = True

#         if results.multi_face_landmarks:
#             face_count += 1
#             for face_landmarks in results.multi_face_landmarks:
#                 # mp_drawing.draw_landmarks(
#                 #     image=image,
#                 #     landmark_list=face_landmarks,
#                 #     connections=mp_face_mesh.FACEMESH_IRISES,
#                 #     landmark_drawing_spec=None,
#                 #     connection_drawing_spec=mp_drawing_styles
#                 #     .get_default_face_mesh_iris_connections_style())
#                 # mp_drawing.draw_landmarks(
#                 #     image=resized_cropped_image,
#                 #     landmark_list=face_landmarks,
#                 #     connections=mp_face_mesh.FACEMESH_TESSELATION,
#                 #     landmark_drawing_spec=None,
#                 #     connection_drawing_spec=mp_drawing_styles
#                 #     .get_default_face_mesh_tesselation_style())
#                 # landmarks of the face at this point if we print this the system is able to tell if there s a face present or not
#                 landmark_points = results.multi_face_landmarks

#                 # check if there are landmarks
#                 if landmark_points:
#                     # get the landmarks of the first face
#                     landmarks = landmark_points[0].landmark
#                     # loop through all the landmark points; select a range of index as we are only interested in the eyes
#                     for id, landmark in enumerate(landmarks[474:478]):
#                         if face_count == 3:
#                             landmark_x0 = landmark.x
#                             landmark_y0 = landmark.y
#                         # get the x and y coordinates of the landmarks, to draw the circle we need to cast to a integer number (its required)
#                         x = int(landmark.x * frame_w)
#                         y = int(landmark.y * frame_h)
#                         # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
#                         # right eye
#                         cv2.circle(resized_cropped_image,
#                                    (x, y), 3, (0, 255, 0))

#                         if id == 1:
#                             # make the cursor move a bigger amount of pixels at a time
#                             k = 6
#                             screen_x = (landmark.x - landmark_x0) * \
#                                 (screen_w * k) + screen_w * landmark_x0
#                             screen_y = (landmark.y - landmark_y0) * \
#                                 (screen_h * k) + screen_h * landmark_y0
#                             # set pyauto gui to false
#                             pyautogui.FAILSAFE = False
#                             pyautogui.moveTo(screen_x, screen_y)
#                     left = [landmarks[145], landmarks[159]]
#                     for landmark in left:
#                         x = int(landmark.x * frame_w)
#                         y = int(landmark.y * frame_h)
#                         cv2.circle(resized_cropped_image,
#                                    (x, y), 3, (0, 255, 255))
#                     if (left[0].y - left[1].y) < 0.004:
#                         pyautogui.click()
#                         pyautogui.sleep(1)
#         else:
#             cv2.putText(resized_cropped_image, "No face detected", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#          # encode the image as JPEG
#         ret, buffer = cv2.imencode('.jpg', resized_cropped_image)
#         # convert the image buffer to bytes
#         resized_cropped_image = buffer.tobytes()
#         # yield the output frame in the byte format
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + resized_cropped_image + b'\r\n')
#   # release the capture and destroy all windows
#     cap.release()
#     cv2.destroyAllWindows()

@ views.route('/')
def index():
    return render_template("index.html", user=current_user)

# Fix so that we cant access this page if we are not logged in as admin


@ views.route('/video')
# @ login_required
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


def update_details(user):
    msg = Message('Account Details Updated',
                  sender='noreply@headmouseweb.com', recipients=[user.email])
    msg.body = f'''Hi {user.firstName},

 You have successfully updated your account details. If you did not make this change, please contact us immediately!
'''
    from . import mail
    mail.send(msg)


@ views.route('/users/<int:user_id>/edit',  methods=['GET', 'POST'])
@ login_required
def userProfileEdit(user_id):
    # Get the user with the specified ID from the database
    user = User.query.get(user_id)

    if user is None:
        # If the user is not found, redirect to a 404 page
        return render_template('404.html'), 404

    if not current_user.is_admin:
        # If the user is not an admin, check if they are the owner of the account being edited
        if current_user.id != user_id:
            # If the user is not the owner, redirect to their own edit page
            return redirect(url_for('views.userProfileEdit', user_id=current_user.id))

    if request.method == 'POST':
      # Update the user information based on the form data
        user_to_edit = User.query.get(user_id)
        user_to_edit.firstName = request.form.get('firstName')
        user_to_edit.lastName = request.form.get('lastName')
        user_to_edit.email = request.form.get('email')
        user_to_edit.country = request.form.get('country')
        user_to_edit.gender = request.form.get('gender')

        if len(user_to_edit.firstName) < 2:
            flash('First name must be greater than 1 character.',
                  category='error')

            return redirect(url_for('views.userProfileEdit'))

        else:
            if user_to_edit.email != user.email:

                existing_user = User.query.filter_by(
                    email=user_to_edit.email).first()
                if existing_user:
                    flash('Email already exists.', category='error')

                    return redirect(url_for('views.userProfileEdit'))

                elif len(user_to_edit.email) < 4:
                    flash('Email must be greater than 3 characters.',
                          category='error')

                    return redirect(url_for('views.userProfileEdit'))

                user_to_edit.firstName = user.firstName
                user_to_edit.lastName = user.lastName
                user_to_edit.email = user.email
                user_to_edit.country = user.country
                user_to_edit.gender = user.gender
                db.session.commit()
                update_details(user)
                flash('Details Updated Successfully', category='success')

            elif user_to_edit.email == user.email:

                user_to_edit.firstName = user.firstName
                user_to_edit.lastName = user.lastName
                user_to_edit.country = user.country
                user_to_edit.gender = user.gender
                db.session.commit()
                update_details(user)
                flash('Details Updated Successfully', category='success')

        return redirect(url_for('views.userProfile', user_id=user.id))
    return render_template("userProfileEdit.html", user=user)

# remove user account


@views.route('/deleteAccount/<int:user_id>', methods=['GET', 'POST'])
@ login_required
def deleteAccount(user_id):
    # Get the user with the specified ID from the database
    user = User.query.get(user_id)

    if user is None:
        # If the user is not found, redirect to a 404 page
        return render_template('404.html'), 404

    # Check if the logged in user is an admin
    if not current_user.is_admin:
        # If the user is not an admin, check if they are the owner of the account being edited
        if current_user.id != user_id:
            # If the user is not the owner, redirect to their own edit page
            return redirect(url_for('views.userProfile', user_id=current_user.id))

    # Delete the user from the database
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()
    if current_user.is_admin:
        flash('User Deleted Successfully', category='success')
        return redirect(url_for('auth.adminPanel'))
    else:
        flash('Account Deleted Successfully', category='success')
        return redirect(url_for('views.index'))


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
