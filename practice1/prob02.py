#
# 1889043 임동주
# prob02.py
# 문제2번
#

N = int(input("자연수를 입력하세요: "))
count = 0
hap = 0
while count <= N:
    if count % 2 == 0:
        hap += count
    count += 1
print(f"1~{N} 까지의 짝수의 합: {hap}")