# import cv2
#
# cap = cv2.VideoCapture("nayeon.mp4")
# ret, frame = cap.read()
# while(1):
#    ret, frame = cap.read()
#    cv2.imshow('frame',frame)
#    if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
#        cap.release()
#        cv2.destroyAllWindows()
#        break
#    cv2.imshow('frame',frame)


# import cv2
# import numpy as np
# from ffpyplayer.player import MediaPlayer
#
#
# def getVideoSource(source, width, height):
#     cap = cv2.VideoCapture(source)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#     return cap
#
#
# def running_videos(sourcePath):
#     camera = getVideoSource(sourcePath, 720, 480)
#     player = MediaPlayer(sourcePath)
#
#     while True:
#         ret, frame = camera.read()
#         audio_frame, val = player.get_frame()
#
#         if (ret == 0):
#             print("End of video")
#             break
#
#         frame = cv2.resize(frame, (720, 480))
#         cv2.imshow('Camera', frame)
#
#         if cv2.waitKey(20) & 0xFF == ord('q'):
#             break
#
#         # if val != 'eof' and audio_frame is not None:
#         # frame, t = audio_frame
#         # print("Frame:" + str(frame) + " T: " + str(t))
#
#     camera.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     running_videos(r"nayeon.mp4")


# Import everything needed to edit video clips
from moviepy.editor import *

# loading video dsa gfg intro video
clip = VideoFileClip("dsa_geek.webm")

# getting only first 5 seconds
clip = clip.subclip(0, 5)

# applying speed effect
final = clip.fx(vfx.speed, 0.5)

# showing final clip
final.ipython_display()



