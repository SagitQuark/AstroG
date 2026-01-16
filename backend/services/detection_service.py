# # services/detection_service.py

# import cv2
# from backend.moving import VIDEO_PATH

# def detect_motion(video_path=VIDEO_PATH):

#     cap = cv2.VideoCapture(video_path)

#     bg = cv2.createBackgroundSubtractorMOG2(
#         history=50,
#         varThreshold=16,
#         detectShadows=False
#     )

#     results=[]
#     frame_id=0

#     last_box=None
#     lost_frames=0
#     MAX_LOST=12   # how long we remember

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         fgmask = bg.apply(frame, learningRate=0.005)

#         kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
#         fgmask=cv2.morphologyEx(fgmask,cv2.MORPH_CLOSE,kernel)
#         fgmask=cv2.dilate(fgmask,None,iterations=3)

#         contours,_=cv2.findContours(
#             fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE
#         )

#         biggest=None
#         max_area=0

#         for c in contours:
#             area=cv2.contourArea(c)
#             if area<400: continue

#             if area>max_area:
#                 max_area=area
#                 biggest=c

#         detected=False

#         if biggest is not None:

#             x,y,w,h=cv2.boundingRect(biggest)

#             roi=frame[y:y+h,x:x+w]
#             bright=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY).mean()

#             if bright>120:
#                 last_box=(x,y,w,h)
#                 lost_frames=0
#                 detected=True

#         # ---- PERSISTENCE ----
#         if detected or last_box is not None:

#             if not detected:
#                 lost_frames+=1

#             if lost_frames<MAX_LOST:

#                 x,y,w,h=last_box

#                 results.append({
#                     "frame":frame_id,
#                     "x":x,"y":y,"w":w,"h":h
#                 })

#                 cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#                 cv2.putText(frame,"ASTEROID (TRACKING)",
#                             (x,y-10),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.6,(0,255,0),2)
#             else:
#                 last_box=None

#         cv2.imshow("AstroGuard Detection",frame)

#         if cv2.waitKey(30)&0xFF==27:
#             break

#         frame_id+=1

#     cap.release()
#     cv2.destroyAllWindows()
#     return results

import cv2
import numpy as np
from backend.moving import VIDEO_PATH

PIXEL_TO_KM = 500
TRAIL_LENGTH = 60

def detect_motion(video_path=VIDEO_PATH):

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_pos = None
    trail = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(9,9),0)

        _,_,_,maxLoc = cv2.minMaxLoc(blur)
        cx,cy = maxLoc

        # Save path
        trail.append((cx,cy))
        if len(trail) > TRAIL_LENGTH:
            trail.pop(0)

        # SPEED
        if prev_pos:
            d = np.linalg.norm(
                np.array((cx,cy))-np.array(prev_pos)
            )
            speed_km = d * fps * PIXEL_TO_KM
        else:
            speed_km = 0

        prev_pos = (cx,cy)

        # BOX
        s = 30
        cv2.rectangle(frame,
            (cx-s,cy-s),(cx+s,cy+s),
            (0,255,0),2)

        cv2.putText(frame,"COMET",
            (cx-s,cy-s-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,(0,255,0),2)

        cv2.putText(frame,
            f"Speed: {speed_km:,.1f} km/s",
            (cx-s,cy+s+25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,(0,255,255),2)

        # CLEAN TRAIL
        for i in range(1,len(trail)):
            fade = int(255*i/len(trail))
            cv2.line(frame,
                trail[i-1],trail[i],
                (0,fade,255),2)

        # DIRECTION ARROW
        if len(trail)>8:
            cv2.arrowedLine(frame,
                trail[-8],trail[-1],
                (0,0,255),3)

        cv2.imshow("AstroGuard Path",frame)

        if cv2.waitKey(30)&0xFF==27:
            break

    cap.release()
    cv2.destroyAllWindows()
