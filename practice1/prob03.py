#
# 1889043 임동주
# prob03.py
# 문제3번
#

def factorial(n):
    count = 1
    total = 1
    while count <= n:
        total *= count
        count += 1
    return total


n = int(input("팩토리얼 구할 자연수 입력: "))
result = factorial(n)
print(f"{n}! = {result}")