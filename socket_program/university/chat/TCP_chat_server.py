"""

TCP_chat_server.py
djlim

"""

from TCP_chat_lib import *


host = ''
port = 50000
BUF_SIZE = 1024
BACK_LOG = 5


conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
conn_server_address = (host, port)

chat_room_dictionary = {}
nickname_list = []


def broadcast(msg_byte):
    for user_socket in chat_room_dictionary:
        chat_room_dictionary[user_socket].sendall(msg_byte)


def thread_tcp_chat(client_socket, client_address):
    global chat_room_dictionary
    global nickname_list
    nickname = None
    chat_room_dictionary[client_address] = client_socket
    print(f"client connect! {client_address}")
    print(f"connect {chat_room_dictionary}")
    print(f"nickname {nickname_list}")
    client_socket.send(HELLO_MSG.encode())
    while True:
        try:
            data_byte = client_socket.recv(BUF_SIZE)
        except Exception as e:
            print(f"ERROR! {e}")
            break
        data = data_byte.decode()
        #print(f"{client_address} : {data}")
        if data:
            if data.upper() in COMMEND_EXIT:
                if nickname:
                    send_msg = f"[{nickname}] good bye!"
                    client_socket.sendall(send_msg.encode())
                    time.sleep(0.1)
                    send_msg = " "
                    client_socket.sendall(send_msg.encode())
                break
            if nickname:
                send_msg = f"{nickname} > {data}"
                broadcast(send_msg.encode())
            else:
                if data in nickname_list:
                    send_msg = f"[{data}] nickname that already exists. re send your nickname."
                    client_socket.sendall(send_msg.encode())
                else:
                    nickname = data
                    nickname_list.append(nickname)
                    send_msg = f"========== your nickname is [{data}] start chatting! =========="
                    client_socket.sendall(send_msg.encode())
                    time.sleep(0.1)
                    send_msg = EXIT_GUIDE_MSG
                    client_socket.sendall(send_msg.encode())
                    time.sleep(0.1)
                    send_all_msg = f"---------- [{nickname}] has entered the chat room. ----------"
                    broadcast(send_all_msg.encode())
        else:
            break
    del chat_room_dictionary[client_address]
    if nickname:
        send_msg = f"[{nickname}] left the chat room."
        broadcast(send_msg.encode())
        nickname_list.remove(nickname)
    client_socket.close()
    print(f"client disconnected! {client_address}")
    print(f"connect {chat_room_dictionary}")
    print(f"nickname {nickname_list}")


if __name__ == "__main__":
    conn_sock.bind(conn_server_address)
    conn_sock.listen(BACK_LOG)
    print("server start")
    try:
        while True:
            print("Waiting for connection...")
            data_socket, address = conn_sock.accept()

            thread_add_chat = threading.Thread(target=thread_tcp_chat, args=(data_socket, address), daemon=True)
            thread_add_chat.start()
    except Exception as e:
        print(f"ERROR! {e}")
    finally:
        conn_sock.close()
        print("exit..")


