#
# 1889043 임동주
# prob05.py
# 문제5번
#


temp = float(input("Enter a temperature: "))
op = input("Convert to (F)ahrenhrit or (C)elsius?: ").upper()

if op == "C":
    result = (5/9)*(temp-32)
elif op == "F":
    result = (9/5)*temp+32

print(f"변환 결과 = {result}{op}")
