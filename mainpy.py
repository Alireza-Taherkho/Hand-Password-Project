
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from pycaw.pycaw import AudioUtilities
from math import floor

from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from concurrent.futures import ThreadPoolExecutor




# voting from a list of numbers; actually "mode"
def choose_num(l):
    num_dict = {}
    for i in l:
        if i in num_dict:
            num_dict[i] += 1
        else:
            num_dict[i] = 1

    max_num = 0
    mode_num = 0
    for i in num_dict:
        if num_dict[i] > max_num:
            max_num = num_dict[i]
            mode_num = i

    return mode_num



# rescaling frame
def rescale_frame(frame):
    return cv.resize(frame, (800, 700), interpolation= cv.INTER_AREA)



# UI Functionn
def user_welcome_UI(frame_name):
    global black_pic
    if frame_name == 'black_pic':
        black_pic = np.zeros((700,800,3), np.uint8)
        cv.putText(black_pic, f"Welcome!", (320,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        
        cv.putText(black_pic, "Painting ->", (5,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.rectangle(black_pic, (350, 70), (410, 110), (255,0,0), -1)

        cv.putText(black_pic, "Face Contorol ->", (5,170), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.rectangle(black_pic, (350, 140), (410, 180), (0,255,0), -1)

        cv.putText(black_pic, "Sound Contorol ->", (5,240), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.rectangle(black_pic, (350, 210), (410, 250), (150,150,0), -1)

        cv.putText(black_pic, "back to login ->", (5,310), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.rectangle(black_pic, (350, 280), (410, 320), (0,0,255), -1)

        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 380), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)


    if frame_name == 'empty_password':
        cv.putText(black_pic, f"new password: {password}", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "eraise -> only left fingers up", (5,70), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, f"*Length = {len(password_ready)}", (5,110), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 150), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        


    if frame_name == 'log_in':
        cv.putText(black_pic, f"password: {pass_list}", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "eraise -> only left fingers up", (5,70), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "change -> only four of right fingers up", (5,110), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 150), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)


    if frame_name == 'paint':
        black_pic = np.zeros((700,800,3), np.uint8)
        cv.putText(black_pic, "to paint -> only index finger up", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "to stop -> index finger down", (5,70), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "to eraise -> only the fingers of one hand up", (5,110), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "exit to main menu -> all fingers up", (5,150), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 190), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)


    
    
    if frame_name == 'face':
        black_pic = np.zeros((700,800,3), np.uint8)
        cv.putText(black_pic, "counting faces", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "blink detection", (5,70), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "exit to main menu -> all fingers up", (5,110), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 150), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)


    if frame_name == 'sound':
        black_pic = np.zeros((700,800,3), np.uint8)
        cv.putText(black_pic, "volume control", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "with index and thump fingers", (5,70), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "exit to main menu-> all fingers up", (5,110), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv.putText(black_pic, "quit -> Enter 'Esc'", (5, 150), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)

        



# creating an object
detector = HandDetector(detectionCon=0.6, maxHands=2)
fm_detector = FaceMeshDetector()


cap = cv.VideoCapture(0)

# black_pic
black_pic = np.zeros((700,800,3), np.uint8)
cv.namedWindow('black_pic')

# password_values
password = []
password_ready = [False, False]
prnum = 0
pass_list = []
seen_numbers = []
user_welcome = False



paint_page = False
face_page = False
sound_page = False
app = False
exit_num_list = []


paint_points = []



from pycaw.pycaw import AudioUtilities
devices = AudioUtilities.GetSpeakers()
volume_control = devices.EndpointVolume




while True:
    rec, frame = cap.read()

    frame = rescale_frame(frame)


    hands, img = detector.findHands(frame, draw=True)

    # showing main menu
    if not user_welcome and not app:
        if all(password_ready) == False:
            user_welcome_UI('empty_password')
            
        else:   
            user_welcome_UI('log_in')


    if paint_page:
        for xy, r, c in paint_points:
            cv.circle(frame, xy, r, c, -1)
        


    if hands:
        # hand1 configeration
        hand1 = hands[0]
        lm = hand1['lmList']
        fingersUp1 = detector.fingersUp(hand1)
        fingersUp1_Num = fingersUp1.count(1)

        cv.putText(frame, f"hands: {hand1['type'][0]}", (5,25), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)


        # eraiser & change password
        if len(hands) == 1 and not user_welcome and not app:
            # eraise
            if hand1['type'] == 'Left' and fingersUp1_Num == 5:
                if all(password_ready) == False:
                    black_pic = np.zeros((700,800,3), np.uint8)
                    user_welcome_UI('empty_password')
                    password.clear()
                    prnum = 0
                    password_ready = [False, False]

                else:
                    black_pic = np.zeros((700,800,3), np.uint8)
                    user_welcome_UI('log_in')
                    pass_list.clear()


            # change
            if hand1['type'] == 'Right' and fingersUp1_Num == 4 and all(password_ready) == True:
                black_pic = np.zeros((700,800,3), np.uint8)
                password.clear()
                pass_list.clear()
                user_welcome_UI('empty_password')
                prnum = 0
                password_ready = [False, False]

            


        if len(hands) == 2:
            # hand2 configeration, L.R detection, counting fingers, cheching password
            hand2 = hands[1]
            cv.putText(frame, f"hands: {hand1['type'][0]}.{hand2['type'][0]}", (5,25), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)

            if (hand1['type'][0] == 'L' and hand2['type'][0] == 'R') or (hand2['type'][0] == 'L' and hand1['type'][0] == 'R'):
                
                fingersUp2 = detector.fingersUp(hand2)
                fingersUp2_Num = fingersUp2.count(1)
                main_num = fingersUp1_Num + fingersUp2_Num
                cv.putText(frame, f"Number: {main_num}", (200,25), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 1)




                if not app:
                    # choosing number in each 50 cycles
                    seen_numbers.append(main_num)

                    
                    if user_welcome == False and len(seen_numbers) > 50:
                        voted_num = choose_num(seen_numbers)
                        seen_numbers.clear()
                        

                        if all(password_ready) == False:
                            password.append(voted_num)
                            password_ready[prnum] = True
                            prnum += 1

                        else:
                            pass_list.append(voted_num)

                        black_pic = np.zeros((700,800,3), np.uint8)


                    # pass_list reseting
                    if user_welcome == False and len(pass_list) > len(password):
                        pass_list.clear()


                    # welcome
                    if all(password_ready) == True and pass_list == password:
                        user_welcome = True

                else:
                    exit_num_list.append(main_num)

                    if len(exit_num_list) > 50:
                        voted_num_exit = choose_num(exit_num_list)
                        exit_num_list.clear()
                        
                        if voted_num_exit == 10:
                            paint_page = False
                            face_page = False
                            sound_page = False
                            app = False
                            user_welcome = True
                            black_pic = np.zeros((700,800,3), np.uint8)
                            user_welcome_UI('black_pic')



    if app:
        if paint_page:
            user_welcome_UI('paint')
            if fingersUp1[1] == 1:
                cv.circle(frame, (lm[8][:-1]), 5, (255,0,0), -1)
                paint_points.append([(lm[8][:-1]), 5, (255,0,0)])

            if fingersUp1.count(1) == 5:
                paint_points.clear()



        elif face_page:
            user_welcome_UI('face')
            frame, faces = fm_detector.findFaceMesh(frame, draw=False)

            cv.putText(frame, f'faces: {len(faces)}', (200,60), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)

            if faces:

                face1 = faces[0]
                lp_159 = face1[159]
                lp_144 = face1[144]

                left_blink, info = fm_detector.findDistance(p1=lp_159, p2=lp_144)


                rp_388 = face1[388]
                rp_374 = face1[374]
                right_blink, info = fm_detector.findDistance(p1=rp_388, p2=rp_374)


                p_173 = face1[173]
                p_414 = face1[414]
                dis_two_eyes, info = fm_detector.findDistance(p1=p_173, p2=p_414)


                if dis_two_eyes >= 110:
                    cv.circle(frame, (700, 600), 70, (0, 0, 255), -1)
                    cv.putText(frame, 'CLOSE', (650,610), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 4)

                
                left_blink_percent = (left_blink * 100) / dis_two_eyes
                right_blink_percent = (right_blink * 100) / dis_two_eyes

                if left_blink_percent <= 25 and right_blink_percent > 33:
                    cv.putText(frame, f'blink', (30,60), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    
                elif left_blink_percent > 25 and right_blink_percent <= 33:
                    cv.putText(frame, f'blink', (30,60), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                else:
                    cv.putText(frame, f'blink', (30,60), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)





        elif sound_page:
            user_welcome_UI('sound')
            distance, info, img = detector.findDistance(lm[4][:-1], lm[8][:-1], frame)
            floor_distance = floor(distance)

            cv.rectangle(frame, (757,577), (783,683), (0,0,255), 2)

            if floor_distance >= 50 and floor_distance <= 150:
                volume = floor_distance - 50
                cv.rectangle(frame, (760, 680-volume), (780,680), (0,255,0), -1)

                speaker_vol = volume / 100
                speaker_vol = max(0.0, min(1.0, speaker_vol)) 
                volume_control.SetMasterVolumeLevelScalar(speaker_vol, None)


            elif floor_distance < 50:
                cv.rectangle(frame, (760, 680), (780,680), (0,255,0), -1)
                volume_control.SetMasterVolumeLevelScalar(0.0, None)


            elif floor_distance > 150:
                cv.rectangle(frame, (760, 581), (780,680), (0,255,0), -1)
                volume_control.SetMasterVolumeLevelScalar(1.0, None)


                    


    # -----

        
    if user_welcome and app == False:
        user_welcome_UI('black_pic')


        if hands and fingersUp1[1] == 1:
            circle = lm[8][:-1]
            cv.circle(black_pic, (circle), 5, (255,255,255), -1)
            
            
            if circle[0] > 350 and circle[0] < 410:

                if circle[1] > 70 and circle[1] < 110: 
                    cv.putText(black_pic, "paint", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    app = True
                    user_welcome = False
                    paint_page = True


                elif circle[1] > 140 and circle[1] < 180: 
                    cv.putText(black_pic, "face", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    app = True
                    user_welcome = False
                    face_page = True
                    

                elif circle[1] > 210 and circle[1] < 250: 
                    cv.putText(black_pic, "sound", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    app = True
                    user_welcome = False
                    sound_page = True
                    

                elif circle[1] > 280 and circle[1] < 310: 
                    cv.putText(black_pic, "back", (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    user_welcome = False
                    pass_list.clear()
                    seen_numbers.clear()
                    black_pic = np.zeros((700,800,3), np.uint8)
                    user_welcome_UI('log_in')
                    

                


        
    # showing the film or camera, exiting
    cv.imshow('frame', frame)
    cv.imshow('black_pic', black_pic)
    key_exit = cv.waitKey(1) & 0xFF
    if key_exit == 27:
        break

    

# the end
cv.destroyAllWindows()
cap.release()




























