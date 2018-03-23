import cv2
import numpy as np
import dynamic_find as dt

image = '2_Denoise_CS_GrayScale_Canny.png'
imgC = '2.png'

#Pass to the dynamic calculator to get optimal parameters
params = dt.pass_me(image)

img = cv2.imread(image,0)
imgC = cv2.imread(imgC,0)
#img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(imgC,cv2.COLOR_GRAY2BGR)
#print(params)

R_min = int(params[2])-5
R_max = int(params[2])+3

if (int(params[2]) > 45):
    R_min = int(params[2])-20
    R_max = int(params[2])+20

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,int(params[0]),int(params[2]),param1=50,param2=int(params[1]),minRadius=R_min,maxRadius=R_max)
#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,28*2,param1=50,param2=29,minRadius=18,maxRadius=38)

#print(circles)
print("Total Circles =",len(circles[0]))

if True:
    circles = np.int16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    
    cv2.imshow('detected circles',cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("FY")



cv2.waitKey(0)
cv2.destroyAllWindows()
