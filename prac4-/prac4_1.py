#
# prac4_1.py
# class
#

import turtle as tt


class TestClass:
    num1 = 0  # 클래스 변수. 클래스에 속함. 오브젝트가 아님.. 지금앎ㅋㅋㅋ

    def __init__(self):
        self.num1 = 100
        self.num2 = 100  # 인스턴스 변수
        TestClass.num1 += 1

    def get_num1(self):
        return self.num1, TestClass.num1


class Polygon:
    shapes = {3: 'triangle', 4: 'rectangle', 5: 'pentagon'}

    def __init__(self, numSide):  # self가 아니라도 됨 하지만 self를 보통 사용함
        self.sideNumber = numSide
        self.sideLen = 0
        tt.speed(100)
        tt.color("green")

    def set_side(self):
        self.sideLen = float(input("변의 길이를 입력"))

    def get_shape(self):
        print(f"Shape : {Polygon.shapes[self.sideNumber]}")

    def draw(self):
        for i in range(self.sideNumber):
            tt.forward(self.sideLen)
            tt.right(360/self.sideNumber)
        tt.exitonclick() # 클릭시 종료
        #pass


def prac4_1():
    #print('Shape: {}'.format(Polygon.shapes[5]))
    a = int(input("3, 4, 5중 하나 입력"))
    p = Polygon(a)
    print("number of sides : {}".format(p.sideNumber))
    print("length of side : {}".format(p.sideLen))
    p.set_side()
    print("length of side : {}".format(p.sideLen))
    p.get_shape()
    p.draw()


if __name__ == "__main__":
    try:
        #tc = TestClass()
        #print(tc.get_num1())
        prac4_1()
    except Exception as e:
        print(f"오류 발생! : [{e}]\n오류 타입 : [{type(e)}]")
    else:
        print("오류가 발생하지 않았습니다.")
    finally:
        print("코드 종료")
