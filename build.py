import pickle
from time import sleep
import sys

FOREST = 'forest.tmx'


stats = {"pos": [1949, 1903],
         "playTime": 10,
         "restarts": 0,
         "map": FOREST,
         "level" :15,
         "skill" : 25,
         "strength" : 50,
         "speed" : 10,
         "health" : 100,
         "blocking": 50,
         "attack" : "sword"
         }

inventory = ["2", "4"]

options = {"width": 1024,
         "height": 768,
         "fps": 160,
         "debug": False
          }

used = [ False, False, False, False, False, False, False, False, False, \
         False, False, False, False, False, False, False, False, False, \
         False, False, False, False, False, False, False, False, False, \
         False]

chestContents = []
taken = []

def run():
    build = input('Do you wish to build \'stats\', \'options\', \'inventory\', \'used\' or all?: ')

    if build == "stats":
        pickle.dump(stats, open("data/saves/save.dat", "wb"))
        print("Loaded " +build +"...")

    elif build == "options":
        pickle.dump(options, open("data/saves/options.dat", "wb"))
        print("Loaded " +build +"...")

    elif build == "inventory":
        pickle.dump(inventory, open("data/saves/inventory.dat", "wb"))
        print("Loaded " +build +"...")

    elif build == "used":
        pickle.dump(used, open("data/saves/used.dat", "wb"))
        for i in range(0, len(used)):
            chestContents.append(None)
        pickle.dump(chestContents, open("data/saves/chestContents.dat", "wb"))
        for i in range(0, len(used)):
            taken.append(False)
        pickle.dump(chestContents, open("data/saves/taken.dat", "wb"))

        print("Loaded " +build +"...")
   
    elif build == "all":
        pickle.dump(options, open("data/saves/options.dat", "wb"))
        pickle.dump(inventory, open("data/saves/inventory.dat", "wb"))
        pickle.dump(used, open("data/saves/used.dat", "wb"))
        for i in range(0, len(used)):
            chestContents.append(None)
        pickle.dump(chestContents, open("data/saves/chestContents.dat", "wb"))

        print("Loaded " +build +"...")
        sys.exit()

    else:
        print("Option not valid.")
        start = input("Would you like to retry? (yes/no) ")
        if start == "yes":
            run()
        if start == "no":
            print("Exiting...")
            sys.exit()
            
run()


