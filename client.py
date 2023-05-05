import threading
import socket


HOST = "127.0.0.1"
PORT = 12345
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def destroy_client():
    print('You have exited the chat room.')
    client.close()

def client_receive():
    while True:
        try: 
            message_in = client.recv(4096).decode('utf-8')
            if message_in == "Alias?":
                client.send(alias.encode('utf-8'))
            elif message_in == 'Exit allowed':
                destroy_client()
                break
            else:
                print(message_in)
        except:
            client.close()
            break

def client_send():
    while True:
        try:
            message_out = input()
            client.send(message_out.encode('utf-8')) 
        except:
            client.close()
            break

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()