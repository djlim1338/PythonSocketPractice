#
# 1889043 임동주
# prob07.py
# 문제7번
#
import math
import random

N = int(input("주사위 던질 수 입력: "))
rn = []  # 결과 저장할 리스트
hap = 0  # 총 합
vsum = 0  # 분산
for i in range(N):
    rn.append(random.randint(1, 6))

for data in rn:
    hap += data
mean = hap / N

for data in rn:
    vsum = vsum + (data - mean)**2
variance = vsum / N
std = math.sqrt(variance)

print(f"평균={mean}\n표준 편차={variance}")