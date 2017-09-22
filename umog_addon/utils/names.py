import re
import random
import keyword

def getRandomString(length):
    random.seed()
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length))

def toVariableName(name):
    variable = re.sub("\W+", "", name)
    if keyword.iskeyword(variable): variable += "_"
    if variable == "": variable = "_"
    return variable
