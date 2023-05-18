"""

tkinter_study2.py
djlim

"""

import tkinter
import tkinter.messagebox


def clicked(event=None):
    message = "Hello "+ input_text.get()
    tkinter.messagebox.showinfo('Greetings', message)


top = tkinter.Tk()
top.geometry('200x100')

input_text = tkinter.StringVar()
input_text.set("Tkinter")

text_field = tkinter.Entry(top, textvariable=input_text)
text_field.pack()

button = tkinter.Button(top, text='Enter', command = clicked)
button.pack()

top.mainloop()
