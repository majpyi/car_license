import cv2

num_num=0
#   提取字符数据库需要的提取文件的路径

# import os
# path = "/Users/Quantum/Desktop/croped/"
# files = os.listdir(path)
# for file in files:
#     file=file[:file.index(".")]
#     print(list(file))
#     print(path+file+".jpg")
#

    #图片前期处理
    # image = cv2.imread(path+file+".jpg")
if(1):
    image = cv2.imread("/Users/Quantum/Desktop/t.jpg")
    file = "GB34114"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg",gray)
    gray = cv2.medianBlur(gray,3)
    cv2.imwrite("/Users/Quantum/Desktop/medianBlur.jpg",gray)


    #  车牌的大小
    sp = image.shape
    print ("维度"+str(sp))
    rows = sp[0]  # height(rows) of image
    colums = sp[1]  # width(colums) of image


    #   找到一个合理的阈值为二值化处理提前准备好条件
    sum =0
    num =0
    for i in range(rows):
        for j in range(colums):
            sum+=gray[i,j]
            num+=1
    mean_value = (int)(sum/num)
    print("所有像素点平均值: "+str(mean_value))


    #  二值化处理,同时存储白色与黑色像素点的多少来判断字母和底色的颜色是黑是白
    black_num = 0
    white_num = 0
    for y in range(colums):
        num=0
        for x in range(rows):
            if(gray[x,y]>mean_value-10):
                gray[x, y]=255
                white_num+=1

            else:
                gray[x,y]=0
                black_num+=1
    if (black_num>white_num):
        tag = 255
        print("白色的字体")
    else:
        tag =0
        print("黑色的字体")
    cv2.imwrite("/Users/Quantum/Desktop/gray.jpg",gray)


    # 横向投影与均值
    sum_rows = [0 for n in range(rows)]
    for x in range(rows):
        num=0
        for y in range((int)(colums/12),(int)(colums*11/12)):
            if(gray[x,y]==tag):
                sum_rows[x]=sum_rows[x]+1
    print("横向的投影: "+str(sum_rows))
    sum_row = 0
    for i in range(rows):
        sum_row+=sum_rows[i]
    tag_row = int(sum_row / rows)
    print("mean_sum_rows:  " +  str(tag_row))


    # 上方的起始点,去掉车牌外部区域
    index1 = 0
    for i in range(rows):
        #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
        if(sum_rows[i]>tag_row/2 and sum_rows[i]< colums*3/4):
            index1=i
            break
    # 下方的起始点,去掉车牌外部区域
    index2 = 0
    for i in range(rows-1,-1,-1):
        #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
        if(sum_rows[i]>tag_row/2 and sum_rows[i]< colums*3/4):
            index2=i-1
            break

    print("index1 :"+str(index1)+"   "+"index2 :"+str(index2))

    #  记录那些行是字符所在行
    tag_rows=[0 for n in range(rows)]
    for i in range(index1,index2):
        if(sum_rows[i]>tag_row*1/3):
            tag_rows[i]=1
        else:
            tag_rows[i]=0
    print("横向标记分割: "+str(tag_rows))


    # 判断是否是双排车辆
    double = 0
    double_start =0
    double_end = 0
    tag1 = 0
    tag2 =0
    for i in range((int)(rows/5),(int)(rows*4/5)):
        #  这里有问题 163, 16, 11, 11, 5, 0, 0, 0, 0   如果是这样的分布就不会判断出来
        # if (sum_rows[i] > tag_row  and sum_rows[i + 1]< tag_row / 2):
        if (tag_rows[i] ==1  and tag_rows[i + 1]==0):
            print(" 双排车牌_start   " +str(i))
            tag1 = 1
            double_start = i
        # if(sum_rows[i] < tag_row/2  and sum_rows[i+1]>tag_row):
        if(tag_rows[i] ==0  and tag_rows[i+1]==1 and i>double_start and double_start!=0 ):
        # if(tag_rows[i] ==0  and tag_rows[i+1]==1 ):
            print(" 双排车牌_end    "+str(i))
            tag2 =1
            double_end = i
        if(tag1 and tag2):
            double =1
            break



    #  对双排车牌的下半部分进行处理,重新进行赋值处理
    if(double==1):
        print("double_start: " + str(double_start))
        print("double_end: " + str(double_end))
        double_avg = (int)((double_start + double_end) / 2)
        print("double_avg: " + str(double_avg))

        # 存储上下两个部分
        cv2.imwrite("/Users/Quantum/Desktop/double_up.jpg", image[range(double_avg + 1), :])
        cv2.imwrite("/Users/Quantum/Desktop/double_down.jpg", image[range((int)(double_avg), rows), :])

        # 存储两排车牌的上方字符
        path_file_1 = "/Users/Quantum/Desktop/mjy/" + file[0] + "____" + file+".jpg"
        cv2.imwrite(path_file_1,
                    image[range(double_avg + 1),:][:, range((int)(colums * 2 / 10), (int)(colums / 2))])
        path_file_2 = "/Users/Quantum/Desktop/mjy/" + file[1] + "____" + file+".jpg"
        cv2.imwrite(path_file_2,
                    image[range(double_avg + 1),:][:, range((int)(colums / 2), (int)(colums * 8 / 10))])


        #  开始对双排车量的下部分非进行预处理,与前一步一致,进行横向分割
        image = cv2.imread("/Users/Quantum/Desktop/double_down.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        sp = image.shape
        rows = sp[0]
        colums = sp[1]

        print("rows: "+str(rows)+"   "+"colums: "+str(colums))
        # 上方的起始点
        index1 = 0
        # for i in range(rows):
        #     #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
        #     if (sum_rows[i] > tag_row / 2 and sum_rows[i] < colums * 3 / 4):
        #         index1 = i - 1
        #         break


        # 二值化处理
        for y in range(colums):
            num = 0
            for x in range(rows):
                if (gray[x, y] > mean_value - 10):
                    gray[x, y] = 255

                else:
                    gray[x, y] = 0


        #   重新横向投影
        sum_rows = [0 for n in range(rows)]
        for x in range(rows):
            num = 0
            for y in range((int)(colums / 12), (int)(colums * 11 / 12)):
                if (gray[x, y] == tag):
                    sum_rows[x] = sum_rows[x] + 1
        print("横向的投影: " + str(sum_rows))


        # 下方的起始点
        # index2 = (int)(rows * (11 / 12))
        for i in range(rows - 1, -1, -1):
            #  判断可能因为边框的选取多出来的黑色区域,所以加上了sum_sum[i]< rows*3/4 ,这个判断条件
            if (sum_rows[i] > tag_row / 2 and sum_rows[i] < colums * 3 / 4):
                index2 = i - 1
                # print(sum_rows[i])
                print("双排车牌index2: " + str(index2))
                break


        #  分割
        tag_rows = [0 for n in range(rows)]
        for i in range(index1, index2):
            if (sum_rows[i] > tag_row*2/3):
                tag_rows[i] = 1
            else:
                tag_rows[i] = 0
        print("横向标记分割: " + str(tag_rows))



    #   rows 的范围
    row_start = 0
    row_end = 0
    for i in range(rows):
        if(tag_rows[i]==0 and tag_rows[i+1]==1):
            row_start = i
            break
    for i in range(rows-1,-1,-1):
        if(tag_rows[i]==0 and tag_rows[i-1]==1):
            row_end = i
            break
    print("row_start:  "+ str(row_start))
    print("row_end:  "+ str(row_end))

    rows_length = row_end-row_start

    print("rows_length: "+str(rows_length))





    #  纵向的投影
    sum_colum = 0
    sum_colums = [0 for n in range(colums)]
    for y in range(colums):
        num=0
        for x in range(row_start,row_end+1):
            if(gray[x,y]==tag):
                sum_colums[y]=sum_colums[y]+1

    print("纵向的投影: "+str(sum_colums))


    #  行平均值
    for i in range(colums):
        sum_colum+=sum_colums[i]
    tag_colum = int(sum_colum/colums)
    print("mean_sum_colum:  " +  str(tag_colum))

    # if(double==1):
    #     rows_length = colums*11/12
    # else:
    #     rows_length = colums*4/5

    #  左边第一个车牌字符内部点
    for i in range(colums):
        if(sum_colums[i]<rows_length*3/4 and sum_colums[i]>tag_colum/2):
            index1 = i-1
            break

    #  右边第一个车牌字符内部点
    for i in range(colums-1,-1,-1):
        if (sum_colums[i] < rows_length * 3 / 4 and sum_colums[i] > tag_colum / 2):
            index2 = i - 1
            break
    print("index1 :"+str(index1)+"   "+"index2: "+str(index2))


    tag_colums=[0 for n in range(colums)]

    for i in range(index1,index2):
        if(sum_colums[i]>tag_colum/2):
            tag_colums[i]=1
        else:
            tag_colums[i]=0

    print("纵向标记分割: "+str(tag_colums))


    #   纵向的分割
    list1 =[]
    list_start = []
    list_end = []
    num = 0
    start=0
    end=0

    #  记录字符的坐标信息,起始位置与终止位置
    for i in range(colums):
        if(tag_colums[i-1]==0 and tag_colums[i]==1):
            start=i
            num=num+1
            list_start.append(i)
            list1.append(start)
        if(tag_colums[i-1]==1 and tag_colums[i]==0):
            end =i
            num=num+1
            list1.append(end)
            list_end.append(i)
    print("纵向分割: "+str(list1))
    print("起始坐标点: "+str(list_start))
    print("终止坐标点: "+str(list_end))


    # 存储分割之后的纵向坐标信息
    cut_colums = []
    for i in range(0,len(list_start)):
        if ( list_end[i]-list_start[i]>colums/15):
            cut_colums.append(list_start[i])
            cut_colums.append(list_end[i])
        elif(list_end[i]-list_start[i]<0):
            if(i>=1 and list_end[i]-list_start[i-1]>colums/15):
                cut_colums.append(list_start[i-1])
                cut_colums.append(list_end[i])
    print("记录的纵向坐标分割点:  "+str(cut_colums))


    #  主要处理因为一个汉字分为左右两个部分,会被判定为两个字符的情况,在这里我们使用判断条件,清除里面的不合理分割点
    # #  这里计算的不是字符的宽度而是字符与字符之间的间隔点
    # tag = 0
    # for i in range(1,len(cut_colums)-1,2):
    #     if(cut_colums[i+1] - cut_colums[i]>=colums/50):
    #         tag = i
    #         break
    # print(tag)
    # # if(tag):
    # cut_colums = cut_colums[:1]+cut_colums[tag:]
    # print("切割坐标 :"+str(cut_colums))


    #  具体处理那些汉字分为左右两个部分或者是像川字分为三个部分的问题,通过字符的中位数间隔的比例,我们进行处理
    cut_length = []
    for i in range(1,len(cut_colums),2):
        cut_length.append(cut_colums[i]-cut_colums[i-1])
    print("切割长度坐标: "+str(cut_length))


    #  分割长度的中位数
    copy = cut_length.copy()
    copy.sort()
    median_length = copy[(int)(len(cut_length)/2)]
    print("切割长度的中位数值: "+str(median_length))
    if (median_length ==0):
        median_length = colums/8


    cut_again_start = []
    cut_again_end = []
    cut_again_num =[]
    for  i in range(0,len(cut_length)):
        cut_num = (cut_length[i] / (median_length * 3 / 4))
        if(cut_num >=1.5):
            cut_again_start.append((i+1)*2-2)
            cut_again_end.append((i+1)*2-1)
            cut_again_num.append(int(cut_num))
    print("cut_again_start: "+str(cut_again_start))
    print("cut_again_end: "+str(cut_again_end))
    print("cut_again_num: "+str(cut_again_num))


    for i in range(0,len(cut_again_start)):
        if (i >0):
            incre_len = (int)((cut_colums[cut_again_end[i]+cut_again_num[i-1]-1]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
            # incre_len = (int)((cut_colums[cut_again_end[i]+2*(cut_again_num[i-1]-1)]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
            print(incre_len)

        else:
            incre_len = (int)((cut_colums[cut_again_end[i]]-cut_colums[cut_again_start[i]])/cut_again_num[i])
            print(incre_len)
        for j in range(1,cut_again_num[i]):
            if(i>0):
                # cut_colums.insert(cut_again_start[i]+j+(cut_again_num[i-1]-1)*2,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
                num1 =  cut_colums[ cut_again_start[i] + cut_again_num[i - 1] - 1] + j * incre_len
                cut_colums.insert(cut_again_start[i]+j+cut_again_num[i-1]-1,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
                cut_colums.append(num1)
                print(str(cut_again_start[i]+j+cut_again_num[i-1]-1) + "     " + str(cut_colums[cut_again_start[i]+cut_again_num[i-1]-1] + j * incre_len))
            #
            else:
                num2 = cut_colums[cut_again_start[i]]+j*incre_len
                cut_colums.insert(cut_again_start[i]+j,cut_colums[cut_again_start[i]]+j*incre_len)
                # cut_colums.insert(cut_again_start[i]+j+1,cut_colums[cut_again_start[i]]+j*incre_len)
                cut_colums.append(num2)
                print(str(cut_again_start[i]+j)+"     "+str(cut_colums[cut_again_start[i]]+j*incre_len))
    cut_colums.sort()
    print("cut_cloums: "+str(cut_colums))



    #  一般出现在首字符和最后的字符,处理那些因为二值化不合理而消失的字符,通过过大的字符间隔判定有字符缺失
    if(cut_colums[0]>colums/8):
        cut_colums.insert(0,cut_colums[0])
        cut_colums.insert(0,5)
    if((colums- cut_colums[len(cut_colums)-1])>colums/8):
        cut_colums.append(cut_colums[len(cut_colums)-1])
        cut_colums.append(colums-5)
    print(cut_colums)
    print("cut_cloums: "+str(cut_colums))


    #  当铆钉接近字符的时候,会造成字符的联通,铆钉的位置一般在
    #  第二个字符与第三个字符之间,和第五个与第六个之间
    # if(double!=1):
    #     cut1 = 0
    #     cut2 = 0
    #     if(cut_colums[3]==cut_colums[4]):
    #         cut1 = cut_colums[3]
    #
    #     if (cut_colums[11] == cut_colums[12]):
    #         cut2 =cut_colums[11]
    #
    #     if(cut1):
    #         while cut1 in cut_colums:
    #             cut_colums.remove(cut1)
    #
    #     if(cut2):
    #         while cut1 in cut_colums:
    #             cut_colums.remove(cut2)


    #  判断剪完之后是不是仍然包括中心的小点
    # if(cut_colums[3]-cut_colums[2]>median_length*1.2):
    #     cut_colums[3]=cut_colums[2]+(int)(median_length*1.2)
    # print("cut_cloums: "+str(cut_colums))


    cut_length_last = []
    for i in range(1,len(cut_colums),2):
        cut_length_last.append(cut_colums[i]-cut_colums[i-1])
    print("last切割长度坐标: "+str(cut_length_last))


    #   只在进行提取字符数据的时候使用,为以后的字符识别做准备,获取与文件名字相等个数的字符,对于多余需要的字符
    #   从最小的字符开始去除
    if(double==1):
        file_length = 5
    else:
        file_length = len(file)
    while(len(cut_colums)/2 >file_length and double==0):
        index = cut_length_last.index(min(cut_length_last))
        cut_colums = cut_colums[:index*2]+cut_colums[index*2+2:]
        cut_length_last = []
        for i in range(1, len(cut_colums), 2):
            cut_length_last.append(cut_colums[i] - cut_colums[i - 1])
    print(cut_colums)




    # 字符与字符之间的间隔太大也需要进行考虑,当字符与字符识别的不相等时
    if(double==0):
        length = len(file)
    else:
        length = 5

    while(len(cut_colums) < length*2):
        cut_interval = []
        for i in range(2,len(cut_colums),2):
            cut_interval.append(cut_colums[i]-cut_colums[i-1])
        index = cut_interval.index(max(cut_interval))
        print("cut_interval: "+str(cut_interval))
        #对于分割的时候一个空余的地方大于 2倍的中位数长度,则有可能里面有包含两个字符
        if(max(cut_interval) > 1.8*median_length):
            cut_colums.append(cut_colums[index*2+1])
            cut_colums.append(cut_colums[index*2+2])
            cut_colums.append((int)( (cut_colums[index*2+1]+cut_colums[index*2+2])/2))
            cut_colums.append((int)( (cut_colums[index*2+1]+cut_colums[index*2+2])/2))
        else:
            cut_colums.append(cut_colums[index * 2 + 1])
            cut_colums.append(cut_colums[index * 2 + 2])
        cut_colums.sort()
        print(cut_colums)


    #  防止对于双排车辆 的最后一个是左右分两部分的汉字,比如  挂
    if(double==1 and len(cut_colums)==12):
        cut_colums = cut_colums[:9]+cut_colums[11:]


    print(cut_colums)
    # 字符分割完成之后进行存储
    if(double==0):
        for i in range(1,len(cut_colums),2):
            path_file = "/Users/Quantum/Desktop/mjy/"+file[(int)(i/2)]+"____"+file+"_____"+str(cut_colums[i])
            cv2.imwrite(path_file  + ".jpg",
                 image[:, range(cut_colums[i-1], cut_colums[i] + 1)][range(row_start, row_end + 1), :])
            num_num+=1
    else:
        for i in range(1, len(cut_colums), 2):
            path_file = "/Users/Quantum/Desktop/mjy/" + file[(int)(i / 2)+2] + "____" + file+"_____"+str(cut_colums[i])
            cv2.imwrite(path_file + ".jpg",
                        image[:, range(cut_colums[i - 1], cut_colums[i] + 1)][
                        range(row_start, row_end + 1), :])
            num_num+=1


