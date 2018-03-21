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

path_orig = 'C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\'
path_mdfd = 'C:\\Users\\harry\\Documents\\Github\\StrawCounting\\Images\\Modified\\' 
path_l = []
for i in range(44):
    path_l.append(str(i+1))
print (path_l)

print(i)
img = cv2.imread(path_orig + path_l[i] + '.png')

dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)


#plt.subplot(121),plt.imshow(img)
#plt.subplot(122),plt.imshow(dst)
cv2.imwrite(path_mdfd + path_l[i] + "_Denoise" + '.png',dst)

imageObject = Image.open(path_mdfd + path_l[i] + "_Denoise" + '.png')
#imageObject.save('C:\\Users\\harry\\Desktop\\Hackathon\\Images\\StrawHead3.png')

# Split the red, green andyblue bands from the Image

multiBands      = imageObject.split()


# Apply point operations that does contrast stretching on each color band
normalizedRedBand      = multiBands[0].point(normalizeRed)
normalizedGreenBand    = multiBands[1].point(normalizeGreen)
normalizedBlueBand     = multiBands[2].point(normalizeBlue)
 

# Create a new image from the contrast stretched red, green and blue brands
normalizedImage = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))


# Display the image before contrast stretching
#imageObject.show()
 

# Display the image after contrast stretching
#normalizedImage.show()


# Cconvert image to grayscale
normalizedImage1 = normalizedImage.convert("L")
#normalizedImage1.show()
normalizedImage1.save(path_mdfd + path_l[i] + '_Denoise_CS_GrayScale.png')

img = cv2.imread(path_mdfd + path_l[i] + '_Denoise_CS_GrayScale.png',0)
edges = cv2.Canny(img,200,100)

##plt.s ubplot(121),plt.imshow(img,cmap = 'gray')
##plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##plt.subplot(122),plt.imshow(edges,cmap = 'gray')
##plt.title('Edge Image'), plt.xticks([]), plt.yticks([])


cv2.imwrite(path_mdfd + 'Canny\\' + path_l[i] + '_Denoise_CS_GrayScale_Canny.png', edges)


