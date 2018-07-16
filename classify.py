import os
import shutil

path = "/Users/Quantum/Desktop/bu/"
files = os.listdir(path)
for file in files:
    file=file[:file.index(".")]
    if(len(file)==0):
        continue
    print(file)
    filepath = "/Users/Quantum/Desktop/class/"+file[0]
    if(os.path.exists(filepath)==False):
        os.mkdir("/Users/Quantum/Desktop/class/"+file[0])
    shutil.copy("/Users/Quantum/Desktop/bu/" + file + ".jpg", "/Users/Quantum/Desktop/class/"+file[0])
