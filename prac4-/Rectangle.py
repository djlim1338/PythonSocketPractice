#
# Rectangle.py
#

import Polygon as pg


class Rectangle(pg.Polygon) :
    def __init__(self) :
        pg.Polygon.__init__(self, 4)

    def get_area(self) :
        self.area = self.sideLen * self.sideLen
        print(self.area)


if __name__ == "__main__":
    try:
        r = Rectangle()
        r.set_side()
        r.get_area()
        r.get_shape()
    except Exception as e:
        print(f"오류 발생 [{e}]")
    finally:
        print("코드 종료")
