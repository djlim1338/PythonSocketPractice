"""

tkinter_study3.py
djlim

Listbox widget

"""

import tkinter
import tkinter.messagebox


top = tkinter.Tk()


def clicked(event=None):
    message_box.insert(tkinter.END, input_text.get())
    input_text.set("")


input_text = tkinter.StringVar()
input_text.set("")
text_field = tkinter.Entry(top, textvariable=input_text)
text_field.bind("<Return>", clicked)
text_field.pack()
button = tkinter.Button(top, text='Enter', command = clicked)
button.pack()
message_box = tkinter.Listbox(top, height=10, width=30)
message_box.pack()

top.mainloop()
