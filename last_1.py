import cv2
import os

path = "/Users/Quantum/Desktop/ok/"
files = os.listdir(path)

# if (1):

# 循环遍历文件夹里面的图片
for file in files:
    file=file[:file.index(".")]
    if(len(file)==0):
        continue
    print(list(file))
    print(path+file+".jpg")
    image = cv2.imread(path+file+".jpg")

    # image = cv2.imread(path + "川A14EE2.jpg")
    # file = "川A14EE2"

    # 预处理图像
    gray = cv2.medianBlur(image, 3)
    cv2.imwrite("/Users/Quantum/Desktop/medianBlur.jpg", gray)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg", gray)
    ret2, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 图片大小获取
    sp = image.shape
    print("维度" + str(sp))
    rows = sp[0]  # height(rows) of image
    colums = sp[1]  # width(colums) of image

    #  黑白字体判断
    black_num = 0
    white_num = 0
    for y in range(colums):
        num = 0
        for x in range(rows):
            if (gray[x, y] == 255):
                white_num += 1

            else:
                black_num += 1
    if (black_num > white_num):
        tag = 255
        print("白色的字体")
    else:
        tag = 0
        print("黑色的字体")
    cv2.imwrite("/Users/Quantum/Desktop/gray.jpg", gray)

    #  对横向 row 的投影
    sum_rows = [0 for n in range(rows)]
    for x in range(rows):
        num = 0
        for y in range(0, colums):
            if (gray[x, y] == tag):
                sum_rows[x] = sum_rows[x] + 1
    print("横向的投影: " + str(sum_rows))
    sum_row = 0
    for i in range(rows):
        sum_row += sum_rows[i]
    tag_row = int(sum_row / rows)
    print("mean_sum_rows:  " + str(tag_row))

    # 上方的起始点,去掉车牌外部区域
    index1 = 0
    for i in range(rows - 1):
        #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
        if (sum_rows[i] < colums * 1 / 5 and sum_rows[i + 1] > colums * 1 / 5):
            index1 = i
            break

    # 下方的起始点,去掉车牌外部区域
    index2 = 0
    for i in range(rows - 1, -1, -1):
        #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
        if (sum_rows[i] < colums * 1 / 5 and sum_rows[i - 1] > colums * 1 / 5):
            index2 = i - 1
            break

    rows_length = index2 - index1+1



    print("index1 :" + str(index1) + "   " + "index2 :" + str(index2))
    cv2.imwrite("/Users/Quantum/Desktop/88.jpg",image[range(index1, index2),:] )
    cv2.imwrite("/Users/Quantum/Desktop/89.jpg",gray[range(index1, index2),:] )



    #  纵向 colums 的投影
    sum_colums = [0 for n in range(colums)]
    for y in range(colums):
        num=0
        # for x in range(index1,index2+1):
        for x in range(int(rows/4),int(rows*3/4)):
            if(gray[x,y]==tag):
                sum_colums[y]=sum_colums[y]+1

    print("纵向的投影: "+str(sum_colums))

    #  平均列长度
    sum_colum = 0
    for i in range(colums):
        sum_colum += sum_colums[i]
    tag_colum = int(sum_colum / colums)
    print("mean_sum_colum:  " + str(tag_colum))

    #  标记列的,排除可能的噪声
    tag_colums = [0 for n in range(colums)]
    for i in range(colums):
        # if (sum_colums[i] > tag_colum / 3):
        if (sum_colums[i] > 0):
            tag_colums[i] = 1
        else:
            tag_colums[i] = 0

    print("纵向的标记: "+str(tag_colums))


    #  记录列分割时,列的长度情况
    len_cos = []
    len_cos_start = []
    len_cos_end = []
    i = 0
    oo =-1
    for i in range(len(tag_colums)):
        if(i<=oo):
            continue
        if(tag_colums[i]==1):
            start = i
            len_cos_start.append(start)
            len_co = 1
            for j in range(start+1,len(tag_colums)+1):
                if(j==len(tag_colums)):
                    len_cos_end.append(j-1)
                    len_cos.append(len_co)
                    oo = j
                elif(tag_colums[j]==0):
                    len_cos_end.append(j-1)
                    oo = j
                    len_cos.append(len_co)
                    break
                len_co+=1

    #  如果长度小于7个字符,表示字符的连接或者缺失, pass
    if(len(len_cos)<7):
        continue

    print("len_cos :"+str(len_cos) )
    print("len_cos_start :"+str(len_cos_start) )
    print("len_cos_end :"+str(len_cos_end) )

    #  每个字符的平均所占大小
    sum_len_cos = 0
    for i in range(len(len_cos)):
        sum_len_cos+=len_cos[i]
    mean_len_cos = int(sum_len_cos/len(len_cos))
    print("mean_len_cos: "+str(mean_len_cos))


    # 针对那些比如像  使,领的车牌  ,因为字体是红色的,在二值化的时候会消失  这些字体只在第一位和最后一位
    if( (colums- len_cos_end[-1]) > mean_len_cos*1.2):
        len_cos_start.append(len_cos_end[-1]+2)
        len_cos_end.append(colums-2)



    #  对于那些分割的片段
    tag_stop = 0
    first_len = 0

    if(len(len_cos)>7):
        print("长度大于7")
        for i in range(len(len_cos)-7+1):
            # if(len_cos[i]>=mean_len_cos*4/5 and i >3):
            # if(len_cos[i]>=mean_len_cos or first_len > mean_len_cos):
            if(len_cos[i]>=mean_len_cos and first_len > mean_len_cos):
                tag_stop = i
                print("********")
                break
            # if(first_len > mean_len_cos):
            #     tag_stop =i
            #     print("%%%%%%%%")
            #     break
            if(i==len(len_cos)-7):
                tag_stop = len(len_cos)-7+1
                print("########")
                break
            first_len+=len_cos[i]

    #  第一个汉字是左右结构的进行合并处理
    if(tag_stop!=0):
        print("汉字分隔")
        cos_start = len_cos_start[0]
        len_cos_start =  len_cos_start[tag_stop:]
        len_cos_start.insert(0,cos_start)
        len_cos_end = len_cos_end[tag_stop-1:]
        print("汉字分隔len_cos_start :" + str(len_cos_start))
        print("汉字分隔len_cos_end :" + str(len_cos_end))


    # 寻找最大的前七个字符分割点
    len_cos_again = []
    for  i in range(len(len_cos_start)):
        len_cos_again.append(len_cos_end[i]-len_cos_start[i]+1)
    print("len_cos_again: "+str(len_cos_again))
    len_cos_again_copy = len_cos_again.copy()
    len_cos_again_copy.sort(reverse = True)
    print(str(len_cos_again_copy))
    last_end = []
    last_start = []
    for i in range(7):
        pos = len_cos_again.index( len_cos_again_copy[i] )
        len_cos_again[pos] = -1
        last_start.append(len_cos_start[pos])
        last_end.append(len_cos_end[pos])

    print("last_start :" + str(last_start))
    print("last_end :" + str(last_end))

    last_end.sort()
    last_start.sort()

    print("七个最大的分隔last_start :" + str(last_start))
    print("七个最大的分割last_end :" + str(last_end))

    # 存储图片
    for i in range(len(last_start)):
        # path_file = "/Users/Quantum/Desktop/char/" + file[i] + "____" + file + "_____" + str(
        path_file = "/Users/Quantum/Desktop/bu/" + file[i] + "____" + file + "_____" + str(
            last_start[i]) + "   " + str(last_end[i])
        # cv2.imwrite(path_file + ".jpg",
        #             image[range(index1, index2), :][:, range(last_start[i], last_end[i])])
        if(i==0):
            cv2.imwrite(path_file + ".jpg",
                       gray[range(index1, index2), :][:, range(last_start[i], last_start[i + 1])])
        elif(i==6):
            cv2.imwrite(path_file + ".jpg",
                        gray[range(index1, index2), :][:, range(last_end[i - 1], last_end[i])])
        else:
            cv2.imwrite(path_file + ".jpg",
                    gray[range(index1, index2), :][:, range(last_end[i-1], last_start[i+1])])


        # cv2.imwrite("/Users/Quantum/Desktop/"+str(last_start[i])+"   "+str(last_end[i])+".jpg", image[range(index1, index2), :][:,range(last_start[i],last_end[i])])


