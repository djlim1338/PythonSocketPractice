#
# main.py
# djlim
# 2023/03/06 ~
# 수업 실습을 위한 코드
#


import sys
from test import Test
import math

if __name__ == "__main__":
    try:

        print("-----모든 코드 실행 완료-----")
    except BaseException:  # 예외 처리시 어떤 예외인지 명시하는것이 좋음.
        print("오류 발생")
    finally:
        print("종료")
