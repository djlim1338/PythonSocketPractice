

# prac3.py
# 리스트 배우는중..
# 60page ~


import random


def prac3_1():
    list1 = []
    print(list1)
    for i in range(10):
        list1.append(str(random.randrange(1, 100)))
    print(list1)
    while len(list1) > 0:
        print(list1.pop(), end="\t")
    print(list1)
    return


# dictionary
def prac3_2():
    dic = {
        "name1": "n1",
        "name2": "n2",
        "name3": "n3",
        "name4": "n4",
        "name5": "n5",
    }
    print(dic)
    print(dic["name5"])
    return


# 67-68page 16-17
# 이름을 쭉 입력받아서 리스트에 저장 후 정렬하여 출력
def prac3_3():
    nameList = []
    while True:
        print("종료 원할시 -1 입력")
        inputName = input("이름을 입력하세요. : ")
        if inputName == "-1":
            break
        nameList.append(inputName)
    nameList.sort()
    print("입력한 이름 : ")
    print(nameList)
    for nameData in nameList:
        print(nameData)
    return


# 바로 위 함수 다른 방식으로 만들어봄. 수업 강의자료에서 영향을 받음
def prac3_4():
    nameList = []
    inputName = ""
    while inputName != "-1":
        print("종료 원할시 -1 입력")
        inputName = input("이름을 입력하세요. : ")
        nameList.append(inputName)
    del nameList[-1]
    nameList.sort()
    print("입력한 이름 : ")
    print(nameList)
    for nameData in nameList:
        print(nameData)
    return


# file read write. file system
# 73page ~
def prac3_5():
    fileName = "prac3_5_data.txt"
    option = "a"
    # option
    # r = 읽기
    # w = 덮어쓰기
    # a = 이어쓰기
    # r+ = write권한도 추가
    # w+ =
    # +붙은 것들은 제대로 알고 사용하지 않으면 이상하게 작동함
    # 
    try:
        file1 = open(fileName, option)
        for i in range(100):
            file1.write("돌돌돌돌돌\n")
    finally:
        file1.close()
        print("파일 입출력이 종료되었습니다. 파일은 닫혔습니다.")
        return


# with as
def prac3_6():
    fileName = "prac3_5_data.txt"
    option = "a"
    try:
        with open(fileName, option) as file1:
            file1.write("돌돌돌돌돌\n")
    finally:
        print("파일 입출력이 종료되었습니다. 파일은 닫혔습니다.")
        return


def prac3_7():
    fileName = "prac3_5_data.txt"
    option = "r"
    try:
        with open(fileName, option) as file1:
            readLine = file1.readline()
            while readLine != "":
                print(readLine)
                readLine = file1.readline()
    finally:
        print("파일 입출력이 종료되었습니다. 파일은 닫혔습니다.")
        return


# 함수
# 80page ~
# parameter : 가인수, 매개변수
# argument : 실인수, 인수
def prac3_8():
    
    return  # 반환값이 없는경우 Null반환


# 85 page
def f():
    s = "I love London!"
    print(s)


# 86page
# parameter로 파일 이름과 파일에 저장할 문자열을 받음
# file로 쓰고 저장
def prac3_9(fileName, writeData):
    with open(fileName, "w") as file1:  # with as로 파일을 열면 구문이 끝남과 동시에 파일을 자동으로 닫음
        file1.write(writeData)


if __name__ == "__main__":
    fileName1 = "prac3_9_data.txt"
    writeData1 = "practice 3-9\n86page (13p)\n솔직히 다 해봤던 내용들이라.. 파이썬 덕분에 프로젝트 많이 진행했었지.."
    print(prac3_9(fileName1, writeData1))  # None = Null 같은의미.. 인줄 알았는데 java의 null과는 근본적으로 다르다고 함. 비어있는.. 값인가?
    print(type(None))
