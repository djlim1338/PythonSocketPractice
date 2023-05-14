#
# 1889043 임동주
# prob01.py
# 문제1번
#

N = int(input("자연수를 입력하세요: "))
count = 0
hap = 0
while count <= N:
    hap += count
    count += 1
print(f"1~{N} 까지의 합: {hap}")
