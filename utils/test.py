import cv2
import numpy as np

frame = cv2.imread("D:/BMU/Semester6/MajorProject/BMU-AVES/utils/test_car.jpg")
cv2.imshow("frame", frame)

cv2.waitKey(0)
cv2.destroyAllWindows()