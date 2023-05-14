#
# 1889043 임동주
# prob11.py
# 문제11번
# except FileNotFoundError: 예외처리로 경로 내 파일 없으면 다시 입력하게 만드는 방식
#

#fileName = "file.txt"

while True:
    try:
        fileName = input("파일 이름을 확장자와 함께 입력하여 주세요: ")
        with open(fileName, "r") as file:  # 전체 읽어옴
            fileData = file.read()
        lineData = fileData.split("\n")  # 읽은 데이터 줄바꿈 문자로 구분하여 리스트에 한줄씩 저장
        lineNumber = 0  # 카운터
        with open(fileName, "w") as file:  # 읽기로 열기
            while lineNumber < len(lineData):  # 번호를 넣기위해 일부러 len() 사용
                write_data = f"{lineNumber+1}: {lineData[lineNumber]}\n"
                print(write_data, end="")
                file.writelines(write_data)
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
