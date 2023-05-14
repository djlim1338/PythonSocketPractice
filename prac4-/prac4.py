#
# prac4.py
# 오늘은 파이썬 마지막. 오류 처리와 class
# 다음부터는 본 수업
#
import sys
W_LINE = "--------------------------------------------------"


def print_msg(msg):
    print(W_LINE)
    #for msgData in msg:
    print(msg)
    print(W_LINE)


def ex4_1():
    first = input("Enter the first number ")
    second = input("Enter the second number ")
    firstNumber = float(first)
    secondNumber = float(second)
    result = firstNumber / secondNumber
    print(first + " / " + second + " = " + str(result))


if __name__ == "__main__":
    try:
        print(f"파이썬 버전 [{sys.version}]")
        ex4_1()
    except ZeroDivisionError:
        print_msg("분모에 0이 올 수 없습니다.")
        sys.exit("Error")
    except ValueError:
        print_msg("숫자만 입력해야 합니다.")
        sys.exit("Error")
    except Exception as e:
        print_msg(f"오류 발생! : [{e}]\n오류 타입 : [{type(e)}]")
        sys.exit("Error")
    else:
        print_msg("오류가 발생하지 않았습니다.")
    finally:
        print_msg("코드 종료")
    print_msg("try종료")
