from tkinter import *

top = Tk()
top.geometry("320x320")
# this is to prevent from resizing the window
#top.resizable(0, 0)
top.title("Simple Calculator")

#variable to store expression
expression = ""

# This Function continuously updates the
# input field whenever you enter a number
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)


# This is used to clear the input field
def bt_clear():
    global expression
    expression = ""
    input_text.set("")

# This function calculates the expression
# present in input field
def bt_equal():
    global expression
    # 'eval':This function is used to evaluates the string expression directly
    result = str(eval(expression))
    input_text.set(result)
    expression = ""

# this is used to get the instance of input field
input_text = StringVar()

# Let us creating a frame for the input field
input_frame = Frame(top, width=300, height=50)
input_frame.pack(side=TOP)

# Let us create a input field inside the 'Frame'
input_field = Entry(input_frame, textvariable=input_text, width=50, justify=RIGHT)
input_field.grid(row=0, column=0)
# 'ipady' is internal padding to increase the height of input field
input_field.pack(ipady=10)

# another 'Frame' for the button below the 'input_frame'
btns_frame = Frame(top)
btns_frame.pack()

# first row
clear = Button(btns_frame, text="Clear", width=34, height=3, command=lambda: bt_clear())
#clear = Button(btns_frame, text="Clear", width=34, height=3, command= bt_clear())
clear.grid(row=0, column=0, columnspan=3)
divide = Button(btns_frame, text="/",  width=10, height=3, command=lambda: btn_click("/"))
divide.grid(row=0, column=3)

# 두번째 줄
seven = Button(btns_frame, text="7", width=10, height=3, command=lambda: btn_click(7))
seven.grid(row=1, column=0)
eight = Button(btns_frame, text="8",  width=10, height=3, command=lambda: btn_click(8))
eight.grid(row=1, column=1)
nine = Button(btns_frame, text="9", width=10, height=3, command=lambda: btn_click(9))
nine.grid(row=1, column=2)
multiply = Button(btns_frame, text="*", width=10, height=3, command=lambda: btn_click("*"))
multiply.grid(row=1, column=3)

# 세번째 줄
four = Button(btns_frame, text="4", width=10, height=3, command=lambda: btn_click(4))
four.grid(row=2, column=0)
five = Button(btns_frame, text="5", width=10, height=3, command=lambda: btn_click(5))
five.grid(row=2, column=1, padx=1, pady=1)
six = Button(btns_frame, text="6", width=10, height=3, command=lambda: btn_click(6))
six.grid(row=2, column=2)
minus = Button(btns_frame, text="-", width=10, height=3, command=lambda: btn_click("-"))
minus.grid(row=2, column=3)

# 네번째 줄
one = Button(btns_frame, text="1", width=10, height=3,command=lambda: btn_click(1))
one.grid(row=3, column=0)
two = Button(btns_frame, text="2", width=10, height=3, command=lambda: btn_click(2))
two.grid(row=3, column=1, padx=1, pady=1)
three = Button(btns_frame, text="3", width=10, height=3, command=lambda: btn_click(3))
three.grid(row=3, column=2)
plus = Button(btns_frame, text="+",width=10, height=3, command=lambda: btn_click("+"))
plus.grid(row=3, column=3)

# 다섯번째 줄
zero = Button(btns_frame, text="0", width=22, height=3, command=lambda: btn_click(0))
zero.grid(row=4, column=0, columnspan=2)
point = Button(btns_frame, text=".",width=10, height=3, command=lambda: btn_click("."))
point.grid(row=4, column=2)
equals = Button(btns_frame, text="=", width=10, height=3, command=lambda: bt_equal())
equals.grid(row=4, column=3)
top.mainloop()