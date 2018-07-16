import cv2
import os

double = 0
num_num=0


path = "/Users/Quantum/Desktop/ok/"
files = os.listdir(path)

if (1):
# for file in files:
#     file=file[:file.index(".")]
#     if(len(file)==0):
#         continue
#     print(list(file))
#     print(path+file+".jpg")
#     image = cv2.imread(path+file+".jpg")

    image = cv2.imread(path+"川A7HN79.jpg")
    file = "川A7HN79"

    gray = cv2.medianBlur(image, 3)
    cv2.imwrite("/Users/Quantum/Desktop/medianBlur.jpg", gray)

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg",gray)


    # gray = cv2.equalizeHist(gray)

    # ret2, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    ret2, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

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
            if(gray[x,y]==255):
                # gray[x, y]=255
                white_num+=1

            else:
                # gray[x,y]=0
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
        for y in range(0,colums):
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
        if(sum_rows[i]>tag_row*1/5):
            tag_rows[i]=1
        else:
            tag_rows[i]=0
    print("横向标记分割: "+str(tag_rows))







    #   rows 的范围
    row_start = 0
    row_end = 0
    for i in range(rows-1):
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


    #  列平均值
    for i in range(colums):
        sum_colum+=sum_colums[i]
    tag_colum = int(sum_colum/colums)
    print("mean_sum_colum:  " +  str(tag_colum))


    rows_length = row_end-row_start
    #  左边第一个车牌字符内部点
    for i in range(colums):
        # if(sum_colums[i]<rows_length*3/4 and sum_colums[i]>tag_colum/2):
        if(sum_colums[i]>rows_length/5):
            index1 = i
            break

    #  右边第一个车牌字符内部点
    for i in range(colums-1,-1,-1):
        # if (sum_colums[i] < rows_length * 3 / 4 and sum_colums[i] > tag_colum / 2):
        if ( sum_colums[i] > rows_length/5):
            index2 = i
            break
    print("index1 :"+str(index1)+"   "+"index2: "+str(index2))


    tag_colums=[0 for n in range(colums)]

    for i in range(index1,index2+1):
        if(sum_colums[i]>rows_length/5):
            tag_colums[i]=1
        else:
            tag_colums[i]=0

    print("纵向标记分割: "+str(tag_colums))

    print(row_start)
    print(row_end)
    print(index1)
    print(index2)

    # 存储记录过的上下左右
    cv2.imwrite("/Users/Quantum/Desktop/8848.jpg",image[:, range(index1, index2)][range(row_start, row_end + 1), :])
    cv2.imwrite("/Users/Quantum/Desktop/8849.jpg",gray[:, range(index1, index2)][range(row_start, row_end + 1), :])


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
    # 保留哪些主要的,没有被污染的字符坐标信息,在下面根据这些字符再细分处理
    # 去除哪些范围较小的可能错误信息
    interval = []
    cut_length_first = []
    cut_colums = []
    tag_length_p = 15
    # while(len(cut_colums)<=3):
    #     for i in range(0,len(list_start)):
    #         if ( list_end[i]-list_start[i]>colums/tag_length_p):
    #             cut_colums.append(list_start[i])
    #             cut_colums.append(list_end[i])
    #             cut_length_first.append(list_end[i]-list_start[i])
    #             if(i!=len(list_start)-1):
    #                 interval.append(list_start[i+1] - list_end[i])
    #         elif(list_end[i]-list_start[i]<0):
    #             if(i>=1 and list_end[i]-list_start[i-1]>colums/15):
    #                 cut_colums.append(list_start[i-1])
    #                 cut_colums.append(list_end[i])
    #                 cut_length_first.append(list_end[i] - list_start[i - 1])
    #                 interval.append(list_start[i]-list_end[i])
    #     tag_length_p+=1
    rever =0
    if(list_end[0]-list_start[0]<0):
        rever = 1

    for i in range(0,len(list_start)):
        if ( list_end[i]-list_start[i]>0):
            cut_length_first.append(list_end[i]-list_start[i])
        else:
            if(i>=1):
                cut_length_first.append(list_end[i] - list_start[i - 1])

    print("第一次所有切割点的长度:"+str(cut_length_first) )
    cut_length_first_copy = cut_length_first.copy()
    cut_length_first_copy.sort(reverse = True)

    print("排序后的"+str(cut_length_first_copy))
    tag_first = [0 for n in range(len(cut_length_first))]

    for i in range(len(cut_length_first)):
        if(cut_length_first[i] > cut_length_first_copy[7]):
            tag_first[i]=1

    print("tag_first: "+str(tag_first))
    if(rever==1):
        s =len(list_start)-1
    else:
        s = len(list_start)

    for i in range(s):
        if(rever==0 and tag_first[i]==1):
            cut_colums.append(list_start[i])
            cut_colums.append(list_end[i])
        else:
            if(i>=1 and tag_first[i]==1):
                cut_colums.append(list_start[i - 1])
                cut_colums.append(list_end[i])

    print("记录的纵向坐标标记点:  "+str(tag_first))
    print("记录的纵向坐标分割点:  "+str(cut_colums))


    # 如果第一个是汉字的话,可能分为左右两个部分
    # 这里进行判定,如果第一个前面的有一个完整的分割区域
    # 并且这个分割区域之间的间隔小于间隔中位数的二分之一那么就就行合并处理
    # interval.sort()
    # pos =list1.index(cut_colums[0])
    # if( cut_colums[0]-list1[pos-1] < interval[ (int)(len(interval)/2) ]/2):
    #     if(pos-2>=0):
    #         print("cut_colums[0]-list1[pos-1]: "+str(cut_colums[0]-list1[pos-1]) )
    #         cut_colums[0]=list1[pos-2]
    #
    # print("fisrt切割长度坐标: " + str(cut_length_first))
    # print("intervel :"+str(interval))
    # print("记录的纵向坐标分割点:  "+str(cut_colums))



    #  具体处理那些汉字分为左右两个部分或者是像川字分为三个部分的问题,通过字符的中位数间隔的比例,我们进行处理
    # cut_length = []
    # for i in range(1,len(cut_colums),2):
    #     cut_length.append(cut_colums[i]-cut_colums[i-1])
    # print("切割长度坐标: "+str(cut_length))
    #
    #
    # #  分割长度的中位数
    # copy = cut_length.copy()
    # copy.sort()
    # median_length = copy[(int)(len(cut_length)/2)]
    # print("切割长度的中位数值: "+str(median_length))
    # if (median_length ==0):
    #     median_length = colums/8
    # #
    # #
    # # cut_again_start = []
    # # cut_again_end = []
    # # cut_again_num =[]
    # # for  i in range(0,len(cut_length)):
    # #     cut_num = (cut_length[i] / (median_length * 3 / 4))
    # #     if(cut_num >=1.5):
    # #         cut_again_start.append((i+1)*2-2)
    # #         cut_again_end.append((i+1)*2-1)
    # #         cut_again_num.append(int(cut_num))
    # # print("cut_again_start: "+str(cut_again_start))
    # # print("cut_again_end: "+str(cut_again_end))
    # # print("cut_again_num: "+str(cut_again_num))
    #
    #
    # # for i in range(0,len(cut_again_start)):
    # #     if (i >0):
    # #         incre_len = (int)((cut_colums[cut_again_end[i]+cut_again_num[i-1]-1]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
    # #         # incre_len = (int)((cut_colums[cut_again_end[i]+2*(cut_again_num[i-1]-1)]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
    # #         print(incre_len)
    # #
    # #     else:
    # #         incre_len = (int)((cut_colums[cut_again_end[i]]-cut_colums[cut_again_start[i]])/cut_again_num[i])
    # #         print(incre_len)
    # #     for j in range(1,cut_again_num[i]):
    # #         if(i>0):
    # #             # cut_colums.insert(cut_again_start[i]+j+(cut_again_num[i-1]-1)*2,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
    # #             num1 =  cut_colums[ cut_again_start[i] + cut_again_num[i - 1] - 1] + j * incre_len
    # #             cut_colums.insert(cut_again_start[i]+j+cut_again_num[i-1]-1,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
    # #             cut_colums.append(num1)
    # #             print(str(cut_again_start[i]+j+cut_again_num[i-1]-1) + "     " + str(cut_colums[cut_again_start[i]+cut_again_num[i-1]-1] + j * incre_len))
    # #         #
    # #         else:
    # #             num2 = cut_colums[cut_again_start[i]]+j*incre_len
    # #             cut_colums.insert(cut_again_start[i]+j,cut_colums[cut_again_start[i]]+j*incre_len)
    # #             # cut_colums.insert(cut_again_start[i]+j+1,cut_colums[cut_again_start[i]]+j*incre_len)
    # #             cut_colums.append(num2)
    # #             print(str(cut_again_start[i]+j)+"     "+str(cut_colums[cut_again_start[i]]+j*incre_len))
    # # cut_colums.sort()
    # # print("cut_cloums: "+str(cut_colums))
    #
    #
    #
    # #  一般出现在首字符和最后的字符,处理那些因为二值化不合理而消失的字符,通过过大的字符间隔判定有字符缺失
    # if(cut_colums[0]>colums/8):
    #     cut_colums.insert(0,cut_colums[0])
    #     cut_colums.insert(0,5)
    # if((colums- cut_colums[len(cut_colums)-1])>colums/8):
    #     cut_colums.append(cut_colums[len(cut_colums)-1])
    #     cut_colums.append(colums-5)
    # print(cut_colums)
    # print("cut_cloums: "+str(cut_colums))
    #
    #
    #
    # cut_length_last = []
    # for i in range(1,len(cut_colums),2):
    #     cut_length_last.append(cut_colums[i]-cut_colums[i-1])
    # print("last切割长度坐标: "+str(cut_length_last))
    #
    #
    # # 字符与字符之间的间隔太大也需要进行考虑,当字符与字符识别的不相等时
    # if(double==0):
    #     length = len(file)
    # else:
    #     length = 5
    #
    # ## 如果不够相应的长度,则有可能中间有忽略的字符串
    # # 前面已经处理过一个字符间隔过长的情况
    # # 这里处理字符与字符之间的间隔过程的情况
    # while(len(cut_colums) < length*2):
    #     cut_interval = []
    #     for i in range(2,len(cut_colums),2):
    #         cut_interval.append(cut_colums[i]-cut_colums[i-1])
    #     index = cut_interval.index(max(cut_interval))
    #     print("cut_interval: "+str(cut_interval))
    #     #对于分割的时候一个空余的地方大于 2倍的中位数长度,则有可能里面有包含两个字符
    #     #这里也需要处理一下,因为这个间隔点可能是包含点的点
    #     if(max(cut_interval) > 1.8*median_length and len(cut_colums)<=10 and index!=1):
    #         cut_colums.append(cut_colums[index*2+1])
    #         cut_colums.append(cut_colums[index*2+2])
    #         cut_colums.append((int)( (cut_colums[index*2+1]+cut_colums[index*2+2])/2))
    #         cut_colums.append((int)( (cut_colums[index*2+1]+cut_colums[index*2+2])/2))
    #     else:
    #         cut_colums.append(cut_colums[index * 2 + 1])
    #         cut_colums.append(cut_colums[index * 2 + 2])
    #     cut_colums.sort()
    #
    #     print(cut_colums)
    #
    #



    print(cut_colums)
    # 字符分割完成之后进行存储
    if(double==0):
        for i in range(1,len(cut_colums),2):
            path_file = "/Users/Quantum/Desktop/char/"+file[(int)(i/2)]+"____"+file+"_____"+str(cut_colums[i-1])+"   "+str(cut_colums[i])
            cv2.imwrite(path_file  + ".jpg",
                 # image[:, range(cut_colums[i-1], cut_colums[i] + 1)][range(row_start, row_end + 1), :])
                 image[:, range(cut_colums[i-1], cut_colums[i] + 1)][range(row_start, row_end + 1), :])
            num_num+=1
    else:
        for i in range(1, len(cut_colums), 2):
            path_file = "/Users/Quantum/Desktop/2/" + file[(int)(i / 2)+2] + "____" + file+"_____"+str(cut_colums[i-1])+"   "+str(cut_colums[i])
            cv2.imwrite(path_file + ".jpg",
                        image[:, range(cut_colums[i - 1], cut_colums[i] + 1)][
                        range(row_start, row_end + 1), :])
            num_num+=1


