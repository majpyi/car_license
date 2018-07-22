import cv2
import os

path = "/Users/Quantum/Desktop/1/"
files = os.listdir(path)

# 循环遍历文件夹里面的图片
for file in files:
    file = file[:file.index(".")]
    if len(file) == 0:
        continue
    print(list(file))
    print(path+file+".jpg")
    image = cv2.imread(path+file+".jpg")

    # 预处理图像
    gray = cv2.medianBlur(image, 3)
    cv2.imwrite("/Users/Quantum/Desktop/medianBlur.jpg", gray)
    gray1 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg", gray)
    ret2, gray = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("/Users/Quantum/Desktop/bu/"+file+".jpg", gray)