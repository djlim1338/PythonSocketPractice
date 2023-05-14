#
#
# class_tuto.py
#
#


class Tuto:
    _var1 = "var1"
    _var3 = ""

    def __init__(self):
        self._var2 = "var2"

    def set_var3(self):
        self._var3 = "var3"

    def get_var1(self):
        return self._var1

    def get_var2(self):
        return self._var2

    def get_var3(self):
        return self._var3


ct = Tuto()

print(f"var1 = {ct.get_var1()}")
print(f"var2 = {ct.get_var2()}")
print(f"var3 = {ct.get_var3()}")
print("set_var3")
ct.set_var3()
print(f"var1 = {ct.get_var1()}")
print(f"var2 = {ct.get_var2()}")
print(f"var3 = {ct.get_var3()}")
