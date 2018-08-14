import cv2


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print('width :', cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print('height :', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('frame :', cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('fps :', cap.get(cv2.CAP_PROP_FPS))
