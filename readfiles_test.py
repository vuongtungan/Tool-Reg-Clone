import random

dir = "data/"
ho = dir + "name/ho.txt"
ten = dir + "name/ten.txt"

file_1 = open(ho, "r").readlines()
file_2 = open(ten, "r").readlines()

print(file_1[random.randint(0,20)] + file_2[random.randint(0,20)])
