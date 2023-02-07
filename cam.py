import cv2

cap = cv2.VideoCapture(0)

r, im =cap.read()
k = cv2.waitKey(30) & 0xff
cv2.imwrite('test.jpg', im) # 사진 저장
cap.release()
cv2.destroyAllWindows()
