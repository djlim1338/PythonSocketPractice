#
# 1889043 임동주
# prob04.py
# 문제4번
#


n = int(input("별모양 그릴 자연수 입력: "))
count = 1

while count < n:
    print("*"*count)
    count += 1

while count > 0:
    print("*"*count)
    count -= 1
