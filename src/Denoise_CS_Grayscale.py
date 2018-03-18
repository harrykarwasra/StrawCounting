import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt


# Method to process the red band of the image
def normalizeRed(intensity):
    iI      = intensity
    minI    = 86
    maxI    = 230
    minO    = 0
    maxO    = 255
    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO

# Method to process the green band of the image
def normalizeGreen(intensity):
    iI      = intensity
    minI    = 90
    maxI    = 225
    minO    = 0
    maxO    = 255
    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO


# Method to process the blue band of the image
def normalizeBlue(intensity):
    iI      = intensity
    minI    = 100
    maxI    = 210
    minO    = 0
    maxO    = 255
    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO




img = cv2.imread('C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\StrawHead.jpg')

dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)


#plt.subplot(121),plt.imshow(img)
#plt.subplot(122),plt.imshow(dst)
cv2.imwrite('C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\StrawHead_Denoise.png',dst)

imageObject = Image.open('C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\StrawHead_Denoise.png')
#imageObject.save('C:\\Users\\harry\\Desktop\\Hackathon\\Images\\StrawHead3.png')

# Split the red, green and blue bands from the Image

multiBands      = imageObject.split()


# Apply point operations that does contrast stretching on each color band
normalizedRedBand      = multiBands[0].point(normalizeRed)
normalizedGreenBand    = multiBands[1].point(normalizeGreen)
normalizedBlueBand     = multiBands[2].point(normalizeBlue)
 

# Create a new image from the contrast stretched red, green and blue brands
normalizedImage = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))


# Display the image before contrast stretching
imageObject.show()
 

# Display the image after contrast stretching
normalizedImage.show()

# Cconvert image to grayscale
normalizedImage1 = normalizedImage.convert("L")
normalizedImage1.show()
normalizedImage1.save('C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\StrawHead_Denoise_CS_GrayScale.png')


