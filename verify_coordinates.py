import os, sys

import numpy as np
import cv2


img = cv2.imread(str(sys.argv[1]))
img = cv2.rectangle(img, (860, 500), (1084, 724), (0, 255, 0), 3)
cv2.imshow('image', img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('verify_coordinates.png', img)
    cv2.destroyAllWindows()





