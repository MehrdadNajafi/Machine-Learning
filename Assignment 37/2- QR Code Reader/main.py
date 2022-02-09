import cv2
import numpy as np
import keyboard
from pyzbar.pyzbar import decode

video_cap = cv2.VideoCapture(0)
video_cap.set(3, 640)
video_cap.set(4, 480)

while True:
    ret, frame = video_cap.read()
    if not ret or keyboard.is_pressed("esc"):
        break
    
    width  = video_cap.get(3)
    height = video_cap.get(4)
    
    mask = np.ones((15, 15)) / 15**2
    min_y, max_y = int(height * (1.3/4)), int(height * (2.7/4))
    min_x, max_x =  int(width * (1.4/4)), int(width * (2.6/4))
    
    result = cv2.filter2D(frame, -1, mask)
    result[min_y:max_y, min_x:max_x] = frame[min_y:max_y, min_x:max_x]
    cv2.rectangle(result, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
    
    for barcode in decode(result):
        my_data = barcode.data.decode("utf-8")
        # print(my_data)
        
        pts = np.array([barcode.polygon], dtype=np.int32) # Points
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(result, [pts], True, (255, 0, 255), 2)
        
        pts2 = barcode.rect # Points 2
        cv2.putText(result, my_data, (pts2[0], pts2[1]-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 0, 255), 1)
        
    cv2.imshow("Cam-0", result)
    cv2.waitKey(1)
cv2.destroyAllWindows()