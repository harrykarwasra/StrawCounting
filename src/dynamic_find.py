'''
Dynamically find the optimal parameters for hough transform

'''

import numpy as np
import cv2
import signal


from functools import wraps
import errno
import os
import copy


def dynamic_threshold(image):
    '''
        Input: Image path
        Return values:
            Array with values: [dp_optimal, param2_optimal, radius_optimal]
    '''
    image = cv2.imread(image)
    orig_image = np.copy(image)
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #cv2.imshow("gray", gray)
    #cv2.waitKey(0)
    # Variables for sum to take average
    sum_dp = []
    sum_param2 = []
    
    circles = None

    minimum_circle_size = 3      # Minimum number of circles we expect to find
    maximum_circle_size = 200     # Minimum number of circles we are willing to find

    guess_dp = 1.0

    number_of_circles_expected = 2          # initially we expect to find just one circle
    breakout = False

    max_guess_accumulator_array_threshold = 60     #minimum of 1, no maximum, (300 maybe?) the quantity of votes 
                                                    #needed to qualify for a circle to be found.
    circleLog = []

    guess_accumulator_array_threshold = max_guess_accumulator_array_threshold

    while guess_accumulator_array_threshold > 1 and breakout == False:
        #start with smallest resolution possible, to find the most precise circle, then creep bigger if none found
        guess_dp = 1.0
        #print("resetting guess_dp:" + str(guess_dp))
        while guess_dp < 9 and breakout == False:
            guess_radius = maximum_circle_size
            #print("setting guess_radius: " + str(guess_radius))
            #print(circles is None)
            while True:

                # Hough Circles is not very helpful till we provide it a radius within 3 pixels of the
                # actual circles in the image.
                # Because Hough transform is a linear algorithm,
                # we will brute force our way through

                #print("guessing radius: " + str(guess_radius) + 
                   #     " and dp: " + str(guess_dp) + " vote threshold: " + 
                    #    str(guess_accumulator_array_threshold))

                circles = cv2.HoughCircles(gray, 
                    cv2.HOUGH_GRADIENT, 
                    dp=guess_dp,               #resolution of accumulator array.
                    minDist=(guess_radius-2),                #number of pixels center of circles should be from each other, hardcoded
                    param1=50,
                    param2=guess_accumulator_array_threshold,
                    minRadius=(guess_radius-2),    #HoughCircles will look for circles minimum this size
                    maxRadius=(guess_radius+2)     #HoughCircles will look for circles maximum this size
                    )

                if circles is not None:
                    if len(circles[0]) == number_of_circles_expected:
                        #print("len of circles: " + str(len(circles)))
                        circleLog.append(copy.copy(circles))

                        # Add for average
                        sum_dp.append(guess_dp)
                        sum_param2.append(guess_accumulator_array_threshold)
                        #print("k1")
                    break
                    circles = None
                guess_radius -= 5 
                if guess_radius < 3:
                    break;

            guess_dp += 1.5

        guess_accumulator_array_threshold -= 2

    #Return the circleLog with the highest accumulator threshold

    # ensure at least some circles were found
    radii= []
    for cir in circleLog:
        # convert the (x, y) coordinates and radius of the circles to integers
        output = np.copy(orig_image)

        if (len(cir) > 1):
            print("Dynamic thresholding failed")
            exit()

        #print("Radius of circle:",cir[0, :])
        
        cir = np.round(cir[0, :]).astype("int")
        radii.append(cir[0][-1])

        for (x, y, r) in cir:
            cv2.circle(output, (x, y), r, (0, 0, 255), 2)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        #cv2.imshow("output", np.hstack([orig_image, output]))
        #cv2.waitKey(0)
    #print("radii array:",radii)
    radii = np.sort(radii)
    radii_len = len(radii)
    #radii_important = (int)((1.0/4)*radii_len)
    radii_important = 1
    if(radii_len<2):
        radii_important = 1
    #print("Sorted array:",radii)
    avg_radius = np.average(radii[0:radii_important])
    avg_dp = np.average(sum_dp)
    avg_param2 = np.average(sum_param2)
    #print("Average dp array:",sum_dp)
    #print("Average dp:",avg_dp)
    #print("Average PARAM2 array:",sum_param2)
    #print("Average PARAM2:",avg_param2)
    
    #print("Optimal Radius = ",avg_radius)
    
    final_arr = [avg_dp, avg_param2, avg_radius]
    return final_arr

def pass_me(image):
    return dynamic_threshold(image)

#Main
if(__name__=="__main__"):
    dynamic_threshold("17_Denoise_CS_GrayScale_Canny.png")
