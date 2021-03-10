# MINECRAFT AUTO FISHER
# By Jonathan (TankiHunt)
# Jan 5 2021
# Version 1.1

from PIL import ImageGrab
import numpy as np
import cv2
import keyboard
import time
import ctypes
import pyautogui
import argparse
from playsound import playsound
from datetime import datetime

def main():
    ENABLE_KEY = "z"
    QUIT_KEY = "x"
    WINDOW_SIZE = 20
    REEL_THRESHOLD = 20
    RECAST_ATTEMPTS = 5
    FRAME_DISCARD = 20
    
    enable = False
    just_casted = False
    first = True
    recast_counter = 0
    counter = 0
    frame_counter = 0
    first_min = REEL_THRESHOLD + 1
    
    user32 = ctypes.windll.user32
    cenWidth = user32.GetSystemMetrics(0)/2
    cenHeight = user32.GetSystemMetrics(1)/2
    print("Press {} to start ({} to quit)".format(ENABLE_KEY, QUIT_KEY))
    while (True):
        if (enable):
            img = ImageGrab.grab(bbox=(cenWidth - WINDOW_SIZE, cenHeight - WINDOW_SIZE, cenWidth + WINDOW_SIZE, cenHeight + WINDOW_SIZE))
            frame = np.array(img)
            frame = frame[:,:,::-1]
            
            #cv2.imshow("Desktop", frame)
            #cv2.waitKey(500)
            #cv2.destroyAllWindows()
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            ll_red = np.array([0, 20, 20])
            lu_red = np.array([15, 255, 255])
            
            ul_red = np.array([235, 20, 20])
            uu_red = np.array([255, 255, 255])
            
            mask = cv2.inRange(hsv, ll_red, lu_red)
            red_pixels = cv2.countNonZero(mask)
            mask = cv2.inRange(hsv, ul_red, uu_red)
            red_pixels = cv2.countNonZero(mask) + red_pixels

            if (first): # Disregard the first few frames and they may be inaccurate
                if (frame_counter < FRAME_DISCARD):
                    frame_counter += 1
                    first_min = min(first_min, red_pixels)
                    continue
                red_pixels = first_min

            if (red_pixels < REEL_THRESHOLD):
                if (first):
                    print("Casting Rod")
                    pyautogui.click(button='right')
                    time.sleep(5)
                    first = False
                    continue
                if (just_casted):
                    recast_counter += 1
                    if (recast_counter == RECAST_ATTEMPTS):
                        input("Fishing Rod Broken? Press ENTER to restart")
                        print("Press {} to start ({} to quit)".format(ENABLE_KEY, QUIT_KEY))
                        enable = False
                        just_casted = False
                        first = True
                        recast_counter = 0
                        counter = 0
                        frame_counter = 0
                        first_min = REEL_THRESHOLD + 1
                        continue
                    print("Bait Not Found. Recasting {} more times".format(RECAST_ATTEMPTS - recast_counter))
                    pyautogui.click(button='right')
                    time.sleep(1)
                    pyautogui.click(button='right')
                    time.sleep(2)
                    continue
 
                print("Fish Detected: Reeling In")
                pyautogui.click(button='right')
                time.sleep(1)
                counter += 1
                print("Caught Something at {} (item: {}): Casting Rod".format(datetime.now(), counter))
                pyautogui.click(button='right')
                time.sleep(2)
                just_casted = True
            else:
                first = False
                just_casted = False
                recast_counter = 0
                
            if keyboard.is_pressed(ENABLE_KEY):
                enable = False
                print("Auto Fishing Paused")
                playsound('pause.mp3')
                time.sleep(3)
        else:
            if keyboard.is_pressed(ENABLE_KEY):
                enable = True
                first = True
                frame_counter = 0
                print("Auto Fishing Started")
                playsound('start.mp3')
                time.sleep(1)
        if keyboard.is_pressed(QUIT_KEY):
            print("Script Stopping")
            break
        time.sleep(0.1)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()