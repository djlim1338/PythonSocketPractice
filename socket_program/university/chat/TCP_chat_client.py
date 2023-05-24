"""

TCP_chat_client.py
djlim

"""

from TCP_chat_lib import *
import tkinter as tk


BUF_SIZE = 1024
BACK_LOG = 5

sock = None
host = '127.0.0.1'
port = 50000
connect_state = False
last_chat = None


def reset_widget():
    global connect_state
    connect_state = False
    chat_send_button["text"] = "참가"
    name_tag_label["text"] = CLIENT_NICKNAME_LABEL
    chat_entry.delete(0, "end")
    chat_listbox.delete(0, "end")
    chat_entry.config(state="disable")


def set_widget():
    global connect_state
    connect_state = True
    chat_send_button["text"] = "전송"
    chat_entry.config(state="normal")


def on_closing(event=None):
    global sock
    if sock:
        sock.sendall("-exit".encode())
    main_window.destroy()


def thread_recv_message():
    global sock
    global last_chat
    while True:
        try:
            data_byte, address = sock.recvfrom(BUF_SIZE)
            if data_byte:
                data = data_byte.decode()
                #print(f"from server({address}) : {data}")
                chat_listbox.insert("end", data)
                chat_listbox.yview(tk.END)
                if data == EXIT_GUIDE_MSG:
                    name_tag_label["text"] = CLIENT_NICKNAME_LABEL + last_chat
            else:
                break
        except Exception as e:
            print(f"ERROR! {e}")
            break
    sock.close()
    sock = None


main_window = tk.Tk()

main_title = "TCP chat"
main_window.title(main_title)
main_window.protocol("WM_DELETE_WINDOW", on_closing)

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
frame_information = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_information.pack(side="top", fill="both")

name_tag_label = tk.Label(frame_information, text=CLIENT_NICKNAME_LABEL, pady=10)
name_tag_label.pack(fill="both")

"""
채팅 보여주는 프레임
"""
frame_chat = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_chat.pack(fill="both")

chat_scrollbar = tk.Scrollbar(frame_chat)
chat_listbox = tk.Listbox(frame_chat, height=20, width=69)

chat_scrollbar.configure(command=chat_listbox.yview)
chat_listbox.configure(yscrollcommand=chat_scrollbar.set)

chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

"""
채팅 동작을 수행 하는 프레임
"""
frame_chat_action = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_chat_action.pack(fill="both")

chat_entry = tk.Entry(frame_chat_action, width=50)
#chat_entry.pack(side="bottom")
chat_entry.grid(row=0, column=0)
chat_entry.config(state="disable")

"""
def clicked(event=None):
    send_msg()


def send_enter(Return):
    send_msg()
"""


def send_msg(event=None):
    global sock
    global connect_state
    global last_chat
    message = chat_entry.get()
    last_chat = message
    chat_entry.delete(0, "end")
    if connect_state:
        try:
            sock.sendall(message.encode())
            if message.upper() in COMMEND_EXIT:
                reset_widget()
        except Exception as e:
            print(f"ERROR! {e}")
    else:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
            server_address = (host, port)
            sock.connect(server_address)
            recv_thread = threading.Thread(target=thread_recv_message, daemon=True)
            recv_thread.start()
            set_widget()
            print(f"connect server!")
        except Exception as e:
            print(f"ERROR! {e}")


chat_send_button = tk.Button(frame_chat_action, text="참가", width=19, command=send_msg)
#chat_send_button.pack(side="bottom")
chat_send_button.grid(row=0, column=1)

print(window_value)

main_window.bind('<Return>', send_msg)
main_window.mainloop()

try:
    sock.close()
except:
    pass
