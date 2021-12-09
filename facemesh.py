import cv2
import mediapipe as mp
import itertools
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# For static images:
IMAGE_FILES = ["testcamera.jpg"]
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
      continue
    annotated_image = image.copy()
###################################################################################################
    print("X of Landmark at index 0 : ",results.multi_face_landmarks[0].landmark[0].x)  # <<<< THIS TOO
    indexes = list(itertools.chain(mp_face_mesh.FACEMESH_IRISES))
    #print(indexes)
###################################################################################################
    for face_landmarks in results.multi_face_landmarks:
###############################################################################################
      for i in range(478):   # Number of face landmarks in total is 477
        print(i,'face_landmarks:', face_landmarks.landmark[i].x)  #  <<<  THIS SOMEWHAT WORKS
#################################################################################################
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_TESSELATION,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_tesselation_style())
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_CONTOURS,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_contours_style())
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_iris_connections_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
#cw=640
cw=1280
#ch=480
ch=720
contours = np.array([[50,50], [50,150], [150,150], [150,50]])
cap.set(3,cw)
cap.set(4,ch)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
#############################################################################
    #indexes = list(itertools.chain(results.multi_face_landmarks.FACEMESH_IRISES))
    #print(indexes)
    #print(results.multi_face_landmarks.landmark[0])
#############################################################################
    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    color = (0,0,255)
    #cw = cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH)
    #ch = cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        #cv2.putText(image,"0",(int(face_landmarks.landmark[0].x*cw),int(face_landmarks.landmark[0].y*ch)),cv2.FONT_HERSHEY_PLAIN, 0.5, color, 1)
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())
    # Flip the image horizontally for a selfie-view display.
    for i in range(478):
      #cv2.putText(image,f"{i}",(int(face_landmarks.landmark[i].x*cw),int(face_landmarks.landmark[i].y*ch)),cv2.FONT_HERSHEY_PLAIN, 0.5, color, 1)
      if face_landmarks.landmark[i].z < 0.11 :
        cv2.putText(image,f"{i}",(int(face_landmarks.landmark[i].x*cw),int(face_landmarks.landmark[i].y*ch)),cv2.FONT_HERSHEY_PLAIN, 0.5, color, 1)
        #cv2.putText(image,f"{face_landmarks.landmark[i].z}",(int(face_landmarks.landmark[i].x*cw),int(face_landmarks.landmark[i].y*ch)),cv2.FONT_HERSHEY_PLAIN, 0.5, color, 1)
    cv2.fillPoly(image, pts = [contours], color =(255,255,255))
    cv2.imshow('MediaPipe Face Mesh', image)
    #cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
