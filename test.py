#
# test.py
# djlim
# 2023/03/06 ~
# 수업 실습을 위한 코드 서브
#

class Test:
    name = ""

    def __init__(self):
        self.name = __name__
        if __name__ == "__main__":
            print("test file run!")
        elif __name__ == "test":
            print("test is not main!!")

    def get_name(self):
        return self.name


test = Test()
