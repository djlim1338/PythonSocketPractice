"""

tkinter_study.py
djlim

"""

import tkinter as tk
import tkinter.messagebox


def close_window(event):
    print(event)
    top.destroy()


def clicked(event = None):
    message = "Hello " + input_text1.get()
    tk.messagebox.showinfo('Greetings', message)


top = tk.Tk()
top.geometry("200x100")

frame1 = tk.Frame

label1 = tk.Label(top, text="GLHF")
label1.pack()

input_text1 = tkinter.StringVar()
input_text1.set("Tkinter")

text_field = tk.Entry(top, textvariable=textvariable=input_text1, width=10)
text_field.pack()


#button1 = tk.Button(top, text="Quit", command=close_window)
button1 = tk.Button(top, text="Quit")
button1.bind("<Button-1>", close_window)  # 마우스 좌클릭시
button1.pack()


button2 = tk.Button(top, text='Enter', command = clicked)
button2.pack()


top.mainloop()

#print(f"돌돌돌")
