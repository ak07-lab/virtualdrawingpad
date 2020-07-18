import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

#creating trackbar for finding threshold for mask
cv2.namedWindow('trackbar', 0)
cv2.createTrackbar('lowerh', 'trackbar', 80, 255, nothing)
cv2.createTrackbar('lowers', 'trackbar', 140, 255, nothing)
cv2.createTrackbar('lowerv', 'trackbar', 55, 255, nothing)
cv2.createTrackbar('upperh', 'trackbar', 190, 255, nothing)
cv2.createTrackbar('uppers', 'trackbar', 255, 255, nothing)
cv2.createTrackbar('upperv', 'trackbar', 255, 255, nothing)

#creating a pad
pad = None

#switching between marker and eraser
val = 1

#intial position of marker
x1, y1 = 0, 0
x2, y2 = 0, 0

while True:
    _, frame = cap.read()
    #flipping the frame horizontally
    frame = cv2.flip(frame,1)

    #converting bgr to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #applying gaussian blur to remove noise
    blur = cv2.GaussianBlur(hsv, (5,5), 100)

    #get current position of trackbar
    lh = cv2.getTrackbarPos('lowerh', 'trackbar')
    ls = cv2.getTrackbarPos('lowers', 'trackbar')
    lv = cv2.getTrackbarPos('lowerv', 'trackbar')
    rh = cv2.getTrackbarPos('upperh', 'trackbar')
    rs = cv2.getTrackbarPos('uppers', 'trackbar')
    rv = cv2.getTrackbarPos('upperv', 'trackbar')

    #defining mask
    lower = np.array([lh,ls,lv])
    upper = np.array([rh,rs,rv])
    mask = cv2.inRange(blur, lower, upper)

    #detecting conntour from mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #creating pad on which we will draw(white color pad)
    if pad is None:
        pad = 255 *np.ones_like(frame)

    #finding centroid of contour if area is greater than 100
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 100:
        M = cv2.moments(mask)
        x2 = int(M['m10']/M['m00'])
        y2 = int(M['m01']/M['m00'])

    if x1 == 0 and y1 == 0:
        x1, y1 = x2, y2
    else:
        if val == 1:
            pad = cv2.line(pad, (x1,y1), (x2,y2), (0, 0, 255) , 3)
        else:
            pad = cv2.line(pad, (x1, y1), (x2, y2), (255, 255, 255), 3)

    x1,y1 = x2,y2

    frame = cv2.circle(frame, (x1,y1), 5, (0, 0, 255), -1)

    #showing frame, pad and image
    cv2.imshow('frame', frame)
    cv2.imshow('pad', pad)
    cv2.imshow('mask', mask)

    #to stop the program press q
    if cv2.waitKey(1) == ord('q'):
        break

    #to convert marker into eraser
    elif cv2.waitKey(1) == ord('e'):
        val = not(val)

    #to clear the pad
    elif cv2.waitKey(1) == ord('c'):
        pad = 255*np.ones_like(frame)

cap.release()
cv2.destroyAllWindows()