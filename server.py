import socket
import time
import threading


HOST = "127.0.0.1"
PORT = 12345
clients = []
addresses = []
aliases = []

def get_index(client):
    return clients.index(client)

def broadcast(message):
    for client in clients:
        client.send(message)

def welcome_client(client, address):
    print('Connection is established with ', address)
    client.send('Alias?'.encode('utf-8'))
    alias = client.recv(4096)
    aliases.append(alias)
    clients.append(client)
    addresses.append(address)
    broadcast(alias + ' has connected to the chat room'.encode('utf-8'))
    client.send('You are now connected!'.encode('utf-8'))
    print('The alias of this client is '.encode('utf-8') + alias)
    return alias

def send_message(client, message):
    for destination in clients:  
        if destination != client:
            i = get_index(client)
            addr = ' ' + str(addresses[i]) + ': '
            content = aliases[i] + addr.encode('utf-8') + message
            destination.send(content)
            time.sleep(0.1)

def delete_client(client):
    i = get_index(client)
    alias = aliases[i]
    del aliases[i]
    del clients[i]
    broadcast(alias + ' has left the chat room\n'.encode('utf-8'))

def handle_client(client, address):
    alias = welcome_client(client, address)

    while True:
        try:
            message = client.recv(4096)
            if message.decode('utf-8') == 'exit':
                delete_client(client)
                client.send('Exit allowed'.encode('utf-8'))
                print(alias + ' has left the chat room'.encode('utf-8'))
                break
            else:
                send_message(client, message)
        except:
            delete_client(client)
            print(alias + ' has left the chat room'.encode('utf-8'))
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        client, address = s.accept()
        thread = threading.Thread(target=handle_client, args=(client, address,))
        thread.start()