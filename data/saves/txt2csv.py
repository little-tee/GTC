#!/usr/bin/python3
import sys, os

os.system("rm csv.txt && touch csv.txt")
vars = ["objectX", "objectY", "targetPosY", "targetPosX", "targetMap", "currentMap", "animationDirection", \
        "targetMapFile", "objectType"]
with open('csv.txt', 'a') as csv_file:
    csv_file.write(str(vars).strip("[]").replace("'", "").replace(", ,", ", ")+'\n')
for i in range(0, len(vars)):
    with open(vars[i], "r") as myfile:
        exec(vars[i] + " = []")
        data = myfile.readlines()
        splitList = data[0].split(", ")
        for j in range(0, len(splitList)):
            exec(eval("vars[i]")+".append(splitList[j].rstrip())")
        print(eval(vars[i]))

csv = []

for i in range(0, 1000):
    for j, file in enumerate(vars):
        with open(file) as text:
            contents = text.read().split(", ")
            try:
                csv.append(contents[i].strip("\n")+ ', ')
                with open('csv.txt', 'a') as csv_file:
                    if j == len(vars)-1:
                        csv_file.write(str(csv).strip("[]").replace("'", "").replace(", ,", ", ")[:-2])
                    else:
                        csv_file.write(str(csv).strip("[]").replace("'", "").replace(", ,", ", "))
                    csv[:] = []
                    if j == len(vars)-1:
                        csv_file.write("\n")
            except IndexError:
                    sys.exit()

