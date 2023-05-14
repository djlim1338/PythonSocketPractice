#
# Polygon.py
# 하나의 모듈로 정의
#

import turtle as tt


class Polygon:
    shapes = {3: 'triangle', 4: 'rectangle', 5: 'pentagon'}

    def __init__(self, numSide):  # self가 아니라도 됨 하지만 self를 보통 사용함
        self.sideNumber = numSide
        self.sideLen = 0

    def set_side(self):
        self.sideLen = float(input("변의 길이를 입력"))

    def get_shape(self):
        print(f"Shape : {Polygon.shapes[self.sideNumber]}")

    def draw(self):
        tt.speed(100)
        tt.color("green")
        for i in range(self.sideNumber):
            tt.forward(self.sideLen)
            tt.right(360/self.sideNumber)
        tt.exitonclick() # 클릭시 종료