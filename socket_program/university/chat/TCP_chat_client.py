"""

TCP_chat_client.py
djlim

"""

from TCP_chat_lib import *
import tkinter as tk


host = '127.0.0.1'
port = 50000
BUF_SIZE = 1024
BACK_LOG = 5


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
server_address = (host, port)
connect_state = False

COMMEND_EXIT = ["-EXIT", "-QUIT"]


def thread_recv_message(server_conn_socket):
    while True:
        try:
            data_byte, address = server_conn_socket.recvfrom(BUF_SIZE)
            if data_byte:
                data = data_byte.decode()
                print(f"from server({address}) : {data}")
                chat_listbox.insert("end", data)
            else:
                break
        except Exception as e:
            print(f"ERROR! {e}")
            break
    server_conn_socket.close()


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
frame_information = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_information.pack(side="top", fill="both")

name_tag_label = tk.Label(frame_information, text="your nickname = ", pady=10)
name_tag_label.pack(fill="both")

"""
채팅 보여주는 프레임
"""
frame_chat = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_chat.pack(fill="both")

chat_listbox = tk.Listbox(frame_chat, height=20)
chat_listbox.pack(fill="both")

"""
채팅 동작을 수행 하는 프레임
"""
frame_chat_action = tk.Frame(main_window)  #, relief="solid", bd=2)
frame_chat_action.pack(fill="both")

chat_entry = tk.Entry(frame_chat_action, width=50)
#chat_entry.pack(side="bottom")
chat_entry.grid(row=0, column=0)


def clicked(event=None):
    send_msg()


def send_enter(Return):
    send_msg()


def send_msg():
    global connect_state
    message = chat_entry.get()
    chat_entry.delete(0, "end")
    if connect_state:
        try:
            sock.send(message.encode())
        except Exception as e:
            print(f"ERROR! {e}")
    else:
        try:
            sock.connect(server_address)
            recv_thread = threading.Thread(target=thread_recv_message, args=(sock, ), daemon=True)
            recv_thread.start()
            connect_state = True
            chat_send_button["text"] = "전송"
            print(f"connect server!")
        except Exception as e:
            print(f"ERROR! {e}")


chat_send_button = tk.Button(frame_chat_action, text="참가", width=19, command=clicked)
#chat_send_button.pack(side="bottom")
chat_send_button.grid(row=0, column=1)

print(window_value)

main_window.bind('<Return>', send_enter)
main_window.mainloop()

sock.close()
