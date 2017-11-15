import sys, os

vars = ["objectX", "objectY", "targetPosY", "targetPosX", "targetMap", "currentMap", "animationDirection", \
        "targetMapFile", "objectType"]

for i in range(0, len(vars)):
    with open(vars[i], "r") as myfile:
        exec(vars[i] + " = []")
        data = myfile.readlines()
        splitList = data[0].split(", ")
        for j in range(0, len(splitList)):
##                eval(vars[i]).append(splitList[j].rstrip())
            exec(eval("vars[i]")+".append(splitList[j].rstrip())")

for var in vars:
    os.system("rm {} && touch {}".format(var, var))
with open("Table.csv", 'r') as csv_file:
    contents = csv_file.readlines()
    for j, content in enumerate(contents):
        items = content.split(",")
        for i, item in enumerate(items):
            with open(vars[i], 'a') as file:
                file.write(item)
                if j != len(contents)-1:
                    file.write(", ")
