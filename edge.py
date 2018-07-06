import cv2
image = cv2.imread("/Users/Quantum/Desktop/藏AA9189.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
canny_src=cv2.Canny(gray, 150, 100, 3)
cv2.imwrite("/Users/Quantum/Desktop/canny_src.jpg",canny_src)
#  车牌的大小
sp = image.shape
print("维度" + str(sp))
rows = sp[0]  # height(rows) of image
colums = sp[1]  # width(colums) of image

#   找到一个合理的阈值为二值化处理提前准备好条件
sum = 0
num = 0
for i in range(rows):
    for j in range(colums):
        sum += gray[i, j]
        num += 1
mean_value = (int)(sum / num)
print("所有像素点平均值: " + str(mean_value))

#  二值化处理,同时存储白色与黑色像素点的多少来判断字母和底色的颜色是黑是白
black_num = 0
white_num = 0
for y in range(colums):
    num = 0
    for x in range(rows):
        if (gray[x, y] > mean_value - 10):
            gray[x, y] = 255
            white_num += 1

        else:
            gray[x, y] = 0
            black_num += 1
cv2.imwrite("/Users/Quantum/Desktop/two.jpg",gray)
