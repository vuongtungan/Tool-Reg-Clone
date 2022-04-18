import random
dir = "data/"
ho = dir + "name/ho.txt"
ten = dir + "name/ten.txt"

def name():
    name, mid = '',''
    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_1 = file_1[random.randint(0,1375)]
    for i in range(len(file_1)):
        if file_1[i] == ' ':
            name = file_1[:i]
            mid = file_1[i+1:]
    return name,mid

print(name())
