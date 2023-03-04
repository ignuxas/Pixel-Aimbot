#Made by ignuxas
import numpy as np
import time
import cv2
import dxcam
import win32api, win32con

MOUSE_LEFTDOWN = 0x0002     # left button down
MOUSE_LEFTUP = 0x0004       # left button up

lower_red = np.array([170,0,0]) #BGR
upper_red = np.array([255,50,80]) #BGR

targetFps = 75 # Fps at witch the screen is captured

screenSize = (1920, 1080) # Screen size

halfScreenWith = screenSize[0] / 2
halfScreenHeight = screenSize[1] / 2

camera = dxcam.create() # Create camera object

region = (830, 460, 1090, 620) # Activation region
camera.start(target_fps=targetFps, region=region) # 75 fps

looptimes = 0 # For timer
loopTimesList = [] # For timer

def setCursor(x,y): # Set cursor position
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

while True: 
    start = time.time() # Timer
    image = camera.get_latest_frame() # Get image from screen

    mask = cv2.inRange(image, lower_red, upper_red) # Filter image

    #cv2.imshow("Raw", image) # Show raw image
    #cv2.imshow("redMask", mask) # Show filtered image

    kernel = np.ones((20,20), np.uint8)
    d_im = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(d_im, kernel, iterations=1) 

    analysis = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis # Get values from filtered image
    componentMask = np.zeros(image.shape, dtype="uint8") # Create empty image
    biggestArea = 0 
    if totalLabels > 1: 
        for i in range(1, totalLabels): 
            area = values[i, cv2.CC_STAT_AREA] # Get area of each component
            
            if area > biggestArea: # Get biggest component
                componentMask = (label_ids == i).astype("uint8") * 255 
                biggestArea = area
        mask = componentMask # Set biggest component as mask

    redPixels = np.argwhere(mask == 255) # Get all red pixels
       
    if len(redPixels) > 10:
        # Find contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour, hier in zip(contours, hierarchy):
            (x,y,w,h) = cv2.boundingRect(contour) 

        topLeft = x, y 
        bottomRight = x + w, y + h

        #get the middle of the object
        middle = ( int((topLeft[0] + bottomRight[0]) / 2), int((topLeft[1] + bottomRight[1]) / 2) )
        
        image = cv2.circle(image, middle, 4, (0, 255, 0), 4)
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

        snapTo = [round(region[0] + middle[0] - halfScreenWith), round(region[1] + middle[1] - halfScreenHeight)]

        setCursor(snapTo[0], snapTo[1])

        # draw a box around the object and add a circle in the middle
        #image = cv2.circle(image, middle, 4, (0, 255, 0), 4)
        #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

    #cv2.imshow("Filtered", mask)
    #cv2.imshow("Result", image)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        cv2.destroyAllWindows()
    end = time.time()

    #----------------------
    #       Timer
    #-----------------------
    looptimes += 1
    loopTimesList.append(end-start)
    if(looptimes > 100):
        print("avg (100 loops):", sum(loopTimesList)/len(loopTimesList))
        looptimes = 0
    