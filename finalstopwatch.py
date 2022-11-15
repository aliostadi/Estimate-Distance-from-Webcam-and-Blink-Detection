

import tkinter
from tkinter import *
from tkinter import messagebox
import numpy as np
import cvzone
import mediapipe as mp
from cvzone.FaceMeshModule import  FaceMeshDetector
import cv2
import numpy as np
import math
# import tk
from win10toast import ToastNotifier
from sys import exit
import tkinter as tk
import time
from winotify import Notification , audio

import PySimpleGUI as sg
#
window = sg.Window('face stopwach ', layout=[[sg.ProgressBar(max_value=50, size=(30,10), key='bar')]])
#
progress = 0
step = 5

while True:
	window.read(timeout=70)
	window['bar'].update_bar(progress)
	# progress += step
	if progress <= 100:
		progress += step
	if progress>=100:
		window.Close()
		break






mp_face_mesh = mp.solutions.face_mesh


# ws=tk.Tk()
ws = Tk()
ws.resizable(0,0)
# ws.iconbitmap('binaicon.ico')
ws.config(bg='blue')
# ws.iconbitmap('binaicon.ico')
x = ws.winfo_screenwidth() # width of the screen
y= ws.winfo_screenheight() # height of the screen
w=150
h=160

ws.attributes('-topmost', True)

ws.geometry('%dx%d+%d+%d' % (w, h, x-(h+15), 335))
blue_frame=tk.Frame(ws, bg="blue", height=100, width=200)


counter = 1
cam_on = True
TOTAL_BLINKS =0



#set webcam
width, height = 500, 800
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def stop():
    global cam_on
    cam_on = False

    if cap:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            cap.release()
            cv2.destroyAllWindows()
            ws.quit()





def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  tt = "Time  = {0}:{1}:{2}".format(int(hours), int(mins), int(sec))
  return tt


def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    oqlidusdis = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return oqlidusdis

def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes
    # horizontal line
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    # draw lines on right eyes
    # cv.line(img, rh_right, rh_left, utils.GREEN, 2)
    # cv.line(img, rv_top, rv_bottom, utils.WHITE, 2)

    # LEFT_EYE
    # horizontal line
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance


    ratio = (reRatio+leRatio)/2
    return ratio


# N = ToastNotifier()




def remove_func():
    emptyMenu = Menu(ws)
    ws.config(menu=emptyMenu)
    ws.update()


def distance():
    remove_func()



    global d
    global BLINKS
    global img


    global faces
    total_blinks=0
    coef = 1


    # Check if the webcam is opened correctly
    if not cap.isOpened():
        cam_on = False
        response = messagebox.showerror('Camera Error', 'Cannot open webcam')
        stop()

    face_mesh=mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)

        # raise IOError("Cannot open webcam")
    detector = FaceMeshDetector(maxFaces=1)

    while True :
        if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)

        success, img1 = cap.read()

        img, faces = detector.findFaceMesh(img1, draw=False)

        # frame = cv2.flip(img1, 1)

        # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_h, img_w = img1.shape[:2]
        results = face_mesh.process(img1)

        count=0
        total=[]
        BLINKS =False

        LEFT_IRIS = [474, 475, 476, 477]
        RIGHT_IRIS = [469, 470, 471, 472]
        if faces:
            # print(int(time.process_time()))
            # print(time.perf_counter())

            ss=time.perf_counter()
            tt=time_convert(ss)
            cvzone.putTextRect(img, f'{tt}', (10, 460), colorT=(0, 0, 0), scale=2, colorR=(255, 255, 255),
                               thickness=2)
            if results.multi_face_landmarks:
                mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int)for p in results.multi_face_landmarks[0].landmark])
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                cv2.circle(img, center_left, int(l_radius), (0, 255, 0), 2, cv2.LINE_AA)
                cv2.circle(img, center_right, int(r_radius), (0, 255, 0), 2, cv2.LINE_AA)
                print(int(l_radius))

                if int(l_radius)>12:
                    cvzone.putTextRect(img,"Iris Warning", (10, 200), colorT=(0, 0, 0), scale=2, colorR=(255, 255, 255),
                                       thickness=2)

            face = faces[0]
            RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
            LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
            pointLeft = face[145]
            pointRight=face[374]


            ##lefteye
            cv2.polylines(img, [np.array([face[p] for p in LEFT_EYE ], dtype=np.int32)],True, (255, 0, 255), 1, cv2.LINE_AA)
            cv2.polylines(img, [np.array([face[p] for p in  RIGHT_EYE ], dtype=np.int32)],True,(255, 0, 255), 1, cv2.LINE_AA)
            cv2.line(img, pointLeft, pointRight, (255, 0, 0), 3)  ## khat bein do cheshm
            # cv2.circle(frame, center_left, int(l_radius), (0, 255, 0), 2, cv2.LINE_AA)
            # cv2.circle(frame, center_right, int(r_radius), (0, 255, 0), 2, cv2.LINE_AA)

            ratio = blinkRatio(img, face, RIGHT_EYE, LEFT_EYE)


            if ratio >5.1:

                    cvzone.putTextRect(img,'eye close', (10, 400), colorT=(0, 0, 0), scale=2, colorR=(255, 255, 255),
                                   thickness=2)


                    BLINKS=True
                    total_blinks+=0.3

            a="{:.1f}".format(ss)
            if float(a)%60==0:

                if total_blinks<(10*coef):
                    cvzone.putTextRect(img,"Blink Warning ", (165, 70), colorT=(0, 0, 255), scale=2,colorR=(0,255,255),
                                       thickness=2)
                    # N.show_toast("BINA SANJESH", " BLINK WARNING", duration=3)
                    n=Notification("BINA SANJESH","BLINK WARNING")
                    time.sleep(0.5)
                    n.show()
                    coef += 1
                    # print(coef)
                else:
                    time.sleep(0.5)
                    coef+=1
                    # print(coef)





            cvzone.putTextRect(img,  f' total Blinks = {int(total_blinks)}', (350, 460), scale=2)






            w, _ = detector.findDistance(pointLeft,
                                             pointRight)  # mohasebeye faseleye bein do chshm . vahed in fasele pixel ast
            ## ba jolo va aghab shoden in khat bozorg va koochak mishavad va meari ast baraye be dast avardan fasele
            # chehre ta camera   .
            # print(w)

            W = 6.3  ## tool vaghee faseleye beyn do chesh ke be toor motevaset 6.3 cm ast

            # ### Formoul of Focal length (fasele kanooni)
            # d=50 ## faseleye man ta webcam dar lahze code zadan . vahed an cm ast
            # f=(w*d)/W
            # print(f)

            ###Finding distance
            f = 525



            d = (W * f) / w
            cvzone.putTextRect(img, f'Distance:{int(d)}cm', (face[10][0] - 120, face[10][1] - 50), scale=2)
            if d <30:
                # time.sleep(1)
                # N.show_toast("BINA SANJESH", "DISTANCE IS SHORT", duration=2)


                cvzone.putTextRect(img, 'your distance is short!', (face[10][0] -180, face[10][1] - 100),scale=2)

                toast = Notification(app_id="BINA SANJESH",title=" WARNING", msg="DISTANCE IS SHORT")
                time.sleep(1)

                toast.show()


        img = cv2.resize(img, (250, 300))
        # im = ax.imshow(value, vmax=1.0, vmin=0.0)


        winname='your image'
        cv2.namedWindow(winname)  # Create a named window
        cv2.moveWindow(winname,  x-(h+120), 15)  # Move it to (40,30)
        cv2.imshow(winname, img)

        #cv2.imshow('iris', frame)



        if cv2.waitKey(30) == 27 :



            if cap:
                if messagebox.askokcancel("Close Camera", "Do you want to Close?"):
                    menu()
                    ws.update()

                    cv2.destroyAllWindows()

                    break


def view():
    ws.resizable(0,0)
    ws.resizable(False,False)
    ws.attributes('-topmost', False)

def view1():
    ws.resizable(False,False)
    ws.resizable(0,0)
    ws.attributes('-topmost', True)



def notif():
    messagebox.showwarning('Notification', 'please turn on your action notificatio')

def lock1():
    distance()


def menu():
    global menubar
    menubar = tk.Menu(ws)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label="Static", command=view1)
    filemenu.add_command(label="Dynamic", command=view)
    filemenu.add_command(label="Exit", command=ws.quit)
    menubar.add_cascade(label="Viwe", menu=filemenu)

    help = Menu(menubar, tearoff=0)
    help.add_command(label="About", command=notif)
    menubar.add_cascade(label="Help", menu=help)

    ws.config(menu=menubar)
    return menubar



menu()

def disable():
    # menubar.entryconfig('Viwe', state=DISABLED)
    # menubar.entryconfig('Help', state=DISABLED)


    # menubar.delete(index1='Viwe',index2='Help'0
    # menubar.delete(2, END)
    distance()












esc=Label(ws,text="Press ESC to close Webcam",font="Verdana 7 bold" )
esc.place(x=2,y=50)


btn2=Button(ws,text='Start',command=lambda :{distance()},fg='#2c3e50',bg='#ef629f',font="Verdana 6 bold")
btn2.place(x =12, y = 120)


TurnCameraOff = Button(ws, text="close and exit", fg='#2c3e50',bg='#ef629f',font="Verdana 6 bold", command=stop)
TurnCameraOff.place(x =55, y = 120)





ws.mainloop()