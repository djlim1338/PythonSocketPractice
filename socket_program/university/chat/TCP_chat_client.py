"""

TCP_chat_client.py
djlim

"""

import tkinter as tk


main_window = tk.Tk()

main_title = "TCP chat"
main_window.title(main_title)

"""
창 크기 및 생성 위치 설정
"""
window_sw = main_window.winfo_screenwidth()  # 모니터 해상도 width
window_sh = main_window.winfo_screenheight()  # 모니터 해상도 height
window_value = {'width': 500, 'height': 500}  # 창 크기
window_value['x'] = int((window_sw - window_value['width']) / 2)  # 창 위치 x
window_value['y'] = int((window_sh - window_value['height']) / 2)  # 창 위치 y
main_window.geometry(f"{window_value['width']}x{window_value['height']}+{window_value['x']}+{window_value['y']}")  # 창 설정
main_window.resizable(width=False, height=False)

"""
정보가 적혀있는 프레임
"""
frame_information = tk.Frame(main_window, relief="solid", bd=2)
frame_information.pack(side="top", fill="both")

name_tag_label = tk.Label(frame_information, text="your nickname = ", pady=10)
name_tag_label.pack(fill="both")

"""
채팅 보여주는 프레임
"""
frame_chat = tk.Frame(main_window, relief="solid", bd=2)
frame_chat.pack(fill="both")

chat_listbox = tk.Listbox(frame_chat, height=20)
chat_listbox.pack(fill="both")

"""
채팅 동작을 수행 하는 프레임
"""
frame_chat_action = tk.Frame(main_window, relief="solid", bd=2)
frame_chat_action.pack(fill="both")

chat_entry = tk.Entry(frame_chat_action, width=50)
#chat_entry.pack(side="bottom")
chat_entry.grid(row=0, column=0)

chat_send_button = tk.Button(frame_chat_action, text="전송", width=19)
#chat_send_button.pack(side="bottom")
chat_send_button.grid(row=0, column=1)

print(window_value)

main_window.mainloop()
