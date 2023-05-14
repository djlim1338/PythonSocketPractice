


# prac2.py
#

import turtle as tt


# 41page 24
def prac24_1():
    value = float(input("물건의 가격을 입력 : "))
    if value < 50:
        value += 10
    print(f"입금해야할 금액은 ${value}입니다.")

# 42page 25
def prac24_2():
    pay = float(input("주문한 금액을 입력 : "))
    contry = input("구입 국가 입력 : ").upper()
    tax = 0
    if contry == "CANADA":
        state = input("구입 지역 입력 : ").upper()
        if state == "ALBERTA":
            tax = pay * 0.05
        elif state == "ONTARIO" or state == "NOVA SCOTIA":
            tax = pay * 0.13
        else:
            tax = pay * 0.06 + pay * 0.05
    print(f"지불해야할 금액은 [${pay}] + 세금 [${tax}] = [${pay + tax}] 입니다.")


# 45page 3
def prac2_3():
    tt.color('green')
    tt.forward(100)
    tt.right(45)
    tt.color('blue')
    tt.forward(50)
    tt.right(45)
    tt.color('pink')
    tt.forward(100)
    tt.exitonclick() # 클릭시 종료


def prac2_4():
    tt.speed(100)
    tt.color('blue')
    for steps in range(4):
        tt.forward(300)
        tt.right(90)
    tt.exitonclick() # 클릭시 종료


def prac2_5():
    tt.speed(1000)
    for steps in range(500):
        tt.color('green')
        tt.forward(200)
        tt.right(179)
        tt.color('red')
        tt.forward(200)
        tt.right(3)
        tt.color('blue')
        tt.forward(200)
        tt.right(2)
    tt.exitonclick() # 클릭시 종료


def prac2_6():
    staps = int(input("n각형 : "))
    tt.speed(1000)
    tt.color('green')
    for i in range(staps):
        tt.forward(1000 / staps)
        tt.right(360/staps)
    tt.exitonclick() # 클릭시 종료


def prac2_7():
    tt.speed(1)
    tt.color('blue')
    for i in range(4):
        tt.forward(200)
        tt.right(90)
        for j in range(4):
            tt.forward(100)
            tt.right(90)
    tt.exitonclick() # 클릭시 종료


# 53page 19
# 변의 수와 몇각형인지를 입력받아 그림
def prac2_8():
    staps = int(input("몇각형인지 입력 : "))
    forward = int(input("변의 길이 입력 : "))
    tt.speed(1000)
    tt.color('green')
    for i in range(staps):
        tt.forward(forward)
        tt.right(360/staps)
    tt.exitonclick() # 클릭시 종료


def prac2_9():  # 별1
    tt.speed(10)
    tt.color('green')
    for i in range(5):
        tt.forward(100)
        tt.right((360/5)*2)
        tt.forward(100)
        tt.left((360/5))
    tt.exitonclick()  # 클릭시 종료


def prac2_10():  # 별2
    tt.speed(10)
    tt.color('green')
    for i in range(5):
        tt.forward(200)
        tt.right((360/5)*2)
    tt.exitonclick()  # 클릭시 종료


def prac2_11(loX, loY, width):  # 별 지정된곳
    tt.speed(100)
    tt.color('blue')
    tt.penup()
    tt.goto(loX, loY)
    tt.pendown()
    for i in range(5):
        tt.forward(width)
        tt.right((360/5)*2)


if __name__ == "__main__":
    fSet = 350
    loXt = -fSet
    loYt = fSet
    widtht = 100
    for j in range(5):
        for i in range(5):
            print(f"[{loXt}][{loYt}][{widtht}]")
            prac2_11(loXt, loYt, widtht)
            loXt += widtht + 50
        loYt -= widtht + 50
        loXt = -fSet
    tt.exitonclick()  # 클릭시 종료
