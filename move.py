import os
import shutil
path = "/Users/Quantum/Desktop/croped_img/"
files = os.listdir(path)
for file in files:
    file=file[:file.index(".")]
    if(len(file)==0):
        continue
    if(len(file)==8):
        shutil.move("/Users/Quantum/Desktop/croped_img/"+file+".jpg","/Users/Quantum/Desktop/8")