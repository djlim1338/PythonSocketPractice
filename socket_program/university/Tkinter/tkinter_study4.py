"""

tkinter_study3.py
djlim

Scrollbar widget

lambda x: x**2
     인수: 표현식
위 아래 비슷함
def fun(x):
    return x**2
람다의 경우 보통 한번 사용하고 버릴 때 사용

"""

import tkinter
import tkinter.messagebox
top = tkinter.Tk()


def clicked(event=None):
    message_box.insert(tkinter.END, input_text.get())
    message_box.yview(tkinter.END)
    input_text.set("")


input_text = tkinter.StringVar()
input_text.set("")
text_field = tkinter.Entry(top, textvariable=input_text)
text_field.bind("<Return>", clicked)
text_field.pack()
message_box = tkinter.Listbox(top, height=10, width=20)
message_box.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
scrollbar = tkinter.Scrollbar(top)
scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
message_box.configure(yscrollcommand = scrollbar.set)
scrollbar.configure(command = message_box.yview)
top.mainloop()

