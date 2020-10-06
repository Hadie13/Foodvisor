# Quick find a tomato on an image
import cv2
import numpy as np

# Load input image and convert to grayscale
image = cv2.imread('tomates.jpg')
cv2.imshow('Where is the tomato ?', image)
cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load Template image
template = cv2.imread('tomate.jpg', 0)

result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
min_val, max_val, min_loc = cv2.minMaxLoc(result)

# Create Bounding Box
top_left = max_loc
bottom_right = (top_left[0] + 1, top_left[1] + 1)
cv2.rectangle(image, top_left, bottom_right, (0,0,255), 5)

cv2.imshow('Where is the tomato ?', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

