import cv2
image = cv2.imread("/Users/Quantum/Desktop/湘BB6302.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
gray1=cv2.equalizeHist(gray)
cv2.imwrite("/Users/Quantum/Desktop/11.jpg",gray1)

