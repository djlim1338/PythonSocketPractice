#
# 1889043 임동주
# prob10.py
# 문제10번
#
import random

w = "-------------------------"
n = 0
count = 0  # 문제 수
corr = 0  # 맞은 수
while n != -1:
    print(w)  # 벽 출력
    print("-1 입력시 종료")
    num1 = random.randint(1,9)
    num2 = random.randint(1,9)
    dap = num1 * num2
    inData = int(input(f"{num1} * {num2} = "))
    if inData == -1:  # 종료 입력시
        break
    if inData == dap:  # 정답일 경우
        print("정답입니다.")
        corr += 1
    else:  # 오답인 경우
        print("오답입니다.")
    count += 1
    print(w)  # 벽 출력

corrP = (corr / count) * 100  # 정답률

print(f"정답률: {corrP}%")
