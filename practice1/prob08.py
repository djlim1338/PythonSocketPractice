#
# 1889043 임동주
# prob08.py
# 문제8번
#

def listProd(a, b):
    hap = 0
    for i in range(len(a)):
        hap += a[i] * b[i]
    return hap


a = [1, 0, 1]
b = [1, 1, 2]

print(f"{a} , {b} => {listProd(a, b)}")

