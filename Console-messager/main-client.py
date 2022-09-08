import socket
import threading
import time
import subprocess


subprocess.call('clear', shell=True)
thread_get_message = True

username = ''
username_mode = None


def thread_get_message(name, sock):
    global username_mode
    global username
    while thread_get_message:
        try:
            data, addr = sock.recvfrom(1024)
            raw_data = data.decode().split()[0]
            if raw_data == '345345235345235345345345345': # This account already exists
                message = data.decode().split()[1:]
                print(" ".join(message))

            elif raw_data == '856784565647864567662346667': # Account created successfully
                username_mode = True
                message = data.decode().split()[1:]
                print(" ".join(message))

            elif raw_data == '463245672356463564362754655': # You are successfully logged in
                username_mode = True
                username = data.decode().split()[1]
                message = data.decode().split()[2:]
                print(" ".join(message))

            elif raw_data == '236432456235462354652364623': # wrong login or password
                message = data.decode().split()[1:]
                print(" ".join(message))
            print(data.decode())
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = 0
server = ("localhost", 9112)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((host, port))
client_socket.setblocking(0)


thr = threading.Thread(target=thread_get_message, args=('Thread_get_data', client_socket))
thr.start()



join = False


print('1. Create account')
print('2. Sing in')
choice = int(input(': '))

if choice == 1:
    subprocess.call('clear', shell=True)
    login = input('Login: ')
    username = input('Username: ')
    password = input('Password: ')
    mode = 478365784365763486576345436
    data_for_create_account = f'{mode} {login} {username} {password}'
    client_socket.sendto(data_for_create_account.encode(), server)
if choice == 2:
    subprocess.call('clear', shell=True)
    login = input('Login: ')
    password = input('Password: ')
    mode = 573485356565656745465785346
    data_for_sing_in = f'{mode} {login} {password}'
    client_socket.sendto(data_for_sing_in.encode(), server)

client_mode = True

while client_mode:
    if join == False:
        if username_mode == True:
            mode = 123123465687565476476567567
            client_socket.sendto(f'{mode} [ {username} ] Online'.encode(), server)
            join = True
        else:
            pass

    else:
        try:
            if username_mode == True:
                message = input(': ')
                if message == '/help':
                    print('1. Write a message to the user')
                    print('2. ...')
                    print('3. ...')
                    print('4. ...')
                    choice = int(input(': '))
                    if choice == 1:
                        mode = 312312565364362462354762344
                        username = input('Username: ')
                        message = input('Message: ')
                        data = f'{mode} {username} {message}'
                        client_socket.sendto(data.encode(), server)

                    if choice == 2:
                        pass
                    if choice == 3:
                        pass
                    if choice == 4:
                        pass
                if message != '':
                    message = f'[ {username} ] -> {message}'
                    client_socket.sendto(message.encode(), server)
            else:
                pass

        except:
            if username_mode == True:
                mode = 787544376574564327587534785
                client_socket.sendto(f'{mode} [ {username} ] Offlain'.encode(), server)
                client_mode = False
            else:
                pass


thr.join()
