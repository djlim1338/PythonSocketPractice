

#
# prac1.py
# 자료 Python Math 9page
# page 22
#
# 자료 Python Math 22page
# page 28
#

import sys
from test import Test
import math


def prac1_0():
    print(sys.version)
    print("It's", end='돌돌돌')
    print("돌돌돌")
    text = ("There once was a movie star icon\nwho preferred to sleep with the light on,\nThey learned how to \"code a device\"")
    print(text)
    print(f"This __name__ = {__name__}")

    #        name = input("이름 입력 = ")
    #        print(name)

    test2 = Test()
    print(f"불러온 파일 __name__ = {test2.get_name()}")

    message = 'Hello world'
    print(message.find('world'))
    print(message.count('o'))
    print(message.capitalize())
    print(message.replace('Hello', 'Hi'))
    msgArr = message.split(" ")
    print(msgArr)


def prac1_1(a, b, c):
    return 1 / ((1+a)/(b+c))


def prac1_2(a, b, c):
    x1 = (-b+(((b**2)-(4*a*c))**(1/2))) / (2*a)
    x2 = (-b-(((b**2)-(4*a*c))**(1/2))) / (2*a)
    return x1, x2


def prac1_3(r):
    return 3.1415926*r**2


def prac1_4(b, g):
    return (b * 2.71828)**(-g)


def prac1_5(x, y):
    return math.sqrt(x**2 + y**2)


def prac1_6(x, u, p):
    p1 = (1 / (math.sqrt(2 * 3.1415926 * p)))
    p2 = 2.71828
    p3 = ((x-u)**2)/2*(p**2)
    return p1*p2**p3


def input_num(n_type):
    try:
        in_arr = input().split()
        if n_type == 'i':
            in_arr_num = list(map(int, in_arr))
        elif n_type == 'f':
            in_arr_num = list(map(float, in_arr))
        else:
            return
    except:
        if n_type == 'i':
            in_arr_num = int(in_arr)
        elif n_type == 'f':
            in_arr_num = float(in_arr)
        else:
            return
    #print(in_arr_num)
    #for i in in_arr_num:
    #    print(f"[{i}] type = '{type(i)}'")
    return in_arr_num


def prac1():
    print("문제 1번 : ", prac1_1(3, 4, 5))
    print("문제 2번 : ", prac1_2(1, 1, -6))
    print("문제 3번 : ", prac1_3(5))
    print("문제 4번 : ", prac1_4(2.0, 3.2))
    print("문제 5번 : ", prac1_5(4, 5))
    print("문제 6번 : ", prac1_6(0.0, 1.5, 2.0))

    return

    print("문제 1: 세 정수를 띄어쓰기로 입력 : ")
    n = input_num('i')
    print("문제 1번 : ", prac1_1(n[0], n[1], n[2]))

    print("문제 2: 세 정수를 띄어쓰기로 입력 : ")
    n = input_num('i')
    print("문제 2번 : ", prac1_2(n[0], n[1], n[2]))

    print("문제 3: 정수 입력 : ")
    n = input_num('i')
    print("문제 3번 : ", prac1_3(n[0]))

    print("문제 4: 두 실수를 띄어쓰기로 입력 : ")
    n = input_num('f')
    print("문제 4번 : ", prac1_4(n[0], n[1]))

    print("문제 5: 두 정수를 띄어쓰기로 입력 : ")
    n = input_num('i')
    print("문제 5번 : ", prac1_5(n[0], n[1]))

    print("문제 6: 세 실수를 띄어쓰기로 입력 : ")
    n = input_num('f')
    print("문제 6번 : ", prac1_6(n[0], n[1], n[2]))


def prac2_0(l = 1000000, i = 50, n = 12): # L:빌릴 돈, i:이자율, n:갚는 기간
    i = (i / 100) / 12
    m = ((l*(i*(1+i)**n)) / ((1+i)**n-1))
    return m


if __name__ == "__main__":
    try:
        prac1()
        l = int(input("빌릴 금액을 입력하세요 [원] : "))
        i = int(input("이자율을 입력하세요 [%] : "))
        n = int(input("갚는 기간을 입력하세요 [달] : "))
        print(f"매달 갚아야 하는 돈은 {prac2_0(l, i, n)}원 입니다.")

        print("-----모든 코드 실행 완료-----")
    except BaseException:  # 예외 처리시 어떤 예외인지 명시하는것이 좋음.
        print("오류 발생")
    finally:
        print("종료")
