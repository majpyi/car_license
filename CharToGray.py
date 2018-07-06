import os
import cv2
import shutil

path = "/Users/Quantum/Desktop/all/"
files = os.listdir(path)
for file in files:
    path_pic = path+file
    if(os.path.isdir(path_pic)==False):
        continue
    pic_files = os.listdir(path_pic)

    movepath = "/Users/Quantum/Desktop/bina/"+file
    if (os.path.exists(movepath) == False):
        os.mkdir(movepath)
    # print("movepath:   "+movepath)

    for pic_file in pic_files:
        # shutil.copy(path_pic+"/"+pic_file, movepath)
        filepath = movepath+"/"+pic_file
        image = cv2.imread(path_pic +"/"+pic_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        ret2,th2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        # ret2, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(filepath)
        cv2.imwrite(filepath,th2)
        # print("imread:  "+path_pic +"/"+pic_file)
        # print("filepath:  "+filepath)
        # break