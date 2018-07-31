
n = 1

str = str(n)

if len(str) < 3:
    if len(str) == 1:
        str = "00" + str
    elif len(str) == 2:
        str = "0" + str

print("数据是:" + str)