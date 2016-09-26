import cv2
import numpy as np
#
element_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,( 7,7 ),( 0, 0))
element_close = cv2.getStructuringElement(cv2.MORPH_RECT,( 7,7 ),( 0, 0))
# im = cv2.imread('soccer_1.png')
# cv2.imshow("XYZZZ",im[len(im)-100:len(im),1:100])

for i in xrange(1,11):
    im = cv2.imread('soccer_'+str(i)+'.png')

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    lower_green = np.array([37,16,70])
    upper_green = np.array([56,256,256])

    #selecting image within HSV-Range
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #Removing Median noise
    mask = cv2.medianBlur(mask,3)

    #Finding connected components of Above
    retval, thres = cv2.threshold(mask.copy(), 150, 255, cv2.THRESH_OTSU)
    retval, labels = cv2.connectedComponents(thres)
    output = np.zeros_like(labels, dtype=np.uint8)
    cv2.normalize(labels, output, 0 , 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    #selecting Largest connected component :- Ground
    counts = np.bincount(output.flatten())
    max_label = np.argmax(counts)
    output[output != max_label] = 0
    output[output == max_label] = 255

    #Selecting Area not on the Ground
    output = cv2.bitwise_not(output)
    # output = cv2.erode(cv2.dilate(output,element_dilate),element_close)

    ret,image_thresh = cv2.threshold(output.copy(), 125, 255, cv2.THRESH_OTSU)
    _,contour,_ = cv2.findContours(image_thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #output = cv2.drawContours(output.copy(),contour,0,150,cv2.FILLED)

    #Eliminating Area of Crowd :- Largest Contour of the inverted Area
    img = np.zeros( (im.shape[0],im.shape[1]))
    # cv2.drawContours(img, contour[:-2], -1,255,-1)
    for cnt in contour[:-2]:
        x,y,w,h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        # if h > w:
        if h*1.0/w > 1 and h*1.0/w < 5:
            cv2.drawContours(img, [cnt], -1,255,-1)
    #print cv2.convexHull(output)
    # im = cv2.blur(im,(3,3))
    # gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # temp = np.zeros((im.shape[0],im.shape[1]),dtype=np.uint8)
    # edges = cv2.Canny(gray,50,100,apertureSize = 3)
    # _,cnt,_ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(temp, cnt, -1, 255,cv2.FILLED)
    #
    # _,temp = cv2.threshold(temp, 128, 255, cv2.THRESH_BINARY)
    # mask = cv2.bitwise_and(im,im,mask=output)
    cv2.imshow('soccer_orig'+str(i)+'.png',im)
    cv2.imshow('soccer_'+str(i)+'.png',img)
    cv2.waitKey(0)
