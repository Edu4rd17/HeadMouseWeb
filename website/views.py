from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, login_required, current_user
import cv2
import mediapipe as mp
import pyautogui
from . import db
from flask_mail import Message
from .models import User


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

# def gen_frames():
#     # generate frame by frame from camera
#     camera = cv2.VideoCapture(0)
#     # the refine landmarks is used to get more accurate landmarks on the face
#     face_mesh = mp.solutions.face_mesh.FaceMesh(
#         refine_landmarks=True, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#     # get the screen size
#     screen_width, screen_height = pyautogui.size()
#     while camera.isOpened():
#         # read the camera frame
#         success, frame = camera.read()
#         frame = cv2.flip(frame, 1)
#         # if not success:
#         #     print("Ignoring empty camera frame.")
#         #     # If loading a video, use 'break' instead of 'continue'.
#         #     continue

#         # to improve performance, optionally mark the image as not writeable to pass by reference
#         frame.flags.writeable = False
#         # convert the frame to RGB
#         rbg_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # process the rgb_frame using face_mesh
#         results = face_mesh.process(rbg_frame)
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
#                 cv2.circle(frame, (x, y), 3, (0, 255, 0))
#                 if id == 1:
#                     screen_x = (screen_width + 2) / frame_width * x
#                     screen_y = (screen_height + 2) / frame_height * y
#                     pyautogui.moveTo(screen_x, screen_y)
#             left = [landmarks[145], landmarks[159]]
#             for landmark in left:
#                 x = int(landmark.x * frame_width)
#                 y = int(landmark.y * frame_height)
#                 cv2.circle(frame, (x, y), 3, (0, 255, 255))
#             # check if the distance between the two points is less than 0.004
#             if (left[0].y - left[1].y) < 0.004:
#                 pyautogui.click()
#                 pyautogui.sleep(1)
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         # concat frame one by one and show result
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# webcam input
# def gen_frames():
#     drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
#     cap = cv2.VideoCapture(0)
#     with mp_face_mesh.FaceMesh(
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5) as face_mesh:
#         while cap.isOpened():
#             success, image = cap.read()
#             if not success:
#                 print("Ignoring empty camera frame.")
#                 continue

#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             results = face_mesh.process(image)

#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             if results.multi_face_landmarks:
#                 for face_landmarks in results.multi_face_landmarks:
#                     mp_drawing.draw_landmarks(
#                         image=image,
#                         landmark_list=face_landmarks,
#                         connections=mp_face_mesh.FACEMESH_TESSELATION,
#                         landmark_drawing_spec=None,
#                         connection_drawing_spec=mp_drawing_styles
#                         .get_default_face_mesh_tesselation_style())
#                     mp_drawing.draw_landmarks(
#                         image=image,
#                         landmark_list=face_landmarks,
#                         connections=mp_face_mesh.FACEMESH_CONTOURS,
#                         landmark_drawing_spec=None,
#                         connection_drawing_spec=mp_drawing_styles
#                         .get_default_face_mesh_contours_style())
#                     mp_drawing.draw_landmarks(
#                         image=image,
#                         landmark_list=face_landmarks,
#                         connections=mp_face_mesh.FACEMESH_IRISES,
#                         landmark_drawing_spec=None,
#                         connection_drawing_spec=mp_drawing_styles
#                         .get_default_face_mesh_iris_connections_style())

#             # flip the image horizontally for a mirror-view display
#             cv2.imshow('MediaPipe FaceMesh', cv2.flip(image, 1))
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
#             if cv2.waitKey(5) & 0xFF == 27:
#                 break
#     cap.release()


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
