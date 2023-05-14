#
# 1889043 임동주
# prob11.py
# 문제11번
#
#

#fileName = "file.txt"

while True:
    try:
        fileName = input("파일 이름을 확장자와 함께 입력하여 주세요: ")
        with open(fileName, "r") as file:  # 전체 읽어옴
            fileData = file.read()
        lintData = fileData.split("\n")  # 읽은 데이터 줄바꿈 문자로 구분하여 리스트에 한줄씩 저장
        lineNumber = 0  # 카운터
        with open(fileName, "w") as file:  # 읽기로 열기
            while lineNumber < len(lintData):
                file.writelines(f"{lineNumber+1}: {lintData[lineNumber]}\n")
                lineNumber += 1
        print("변환 완료")
    except FileNotFoundError:
        print(f"오류 발생! 해당 파일이 존재하지 않습니다! 파일명=[{fileName}]")
        print("파일명을 다시 입력하여 주십시오.")
        continue
    except Exception as e:
        print(f"오류 발생! {e}")
    finally:
        print("코드 종료")
    break
