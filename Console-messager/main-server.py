import socket
import sqlite3
import time
import subprocess


#-------------------------------------------------------
#mode = 478365784365763486576345436 # Mode for create account
#mode = 573485356565656745465785346 # Mode for sign in

#mode = 345345235345235345345345345 # This account already exists
#mode = 856784565647864567662346667 # Account created successfully

#mode = 236432456235462354652364623 # You are successfully logged in
#mode = 463245672356463564362754655 # wrong login or password

#mode = 123123465687565476476567567 # join chat
#mode = 787544376574564327587534785 # left chat

#mode = 312312565364362462354762344 # Enter message
#-------------------------------------------------------

subprocess.call('clear', shell=True)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(('localhost', 9112))

""" Function to create an account and check if the account exists """
def create_account(login, password, username, ip, port):
    with sqlite3.connect('Accounts.db') as con:
        try:
            cur = con.cursor()
            data_login = cur.execute(""" SELECT login, username FROM users WHERE login = (?) OR username = (?) """, (login, username))
            for item in data_login:
                data_user = item
            if data_user != '':
                mode = 345345235345235345345345345
                message = 'This account already exists!'
                data = f'{mode} {message}'
                server_socket.sendto(data.encode(), addr)

        except:
            online = 1
            cur.execute(""" INSERT INTO users (login, password, username, online, ip, port) VALUES (?, ?, ?, ?, ?, ?) """, (login, password, username, online, ip, port))
            mode = 856784565647864567662346667
            message = 'Account created successfully'
            data = f'{mode} {message}'
            server_socket.sendto(data.encode(), addr)

""" Function for authorization """
def sign_in(login, password, ip, port):
    global sign_in__item_username
    with sqlite3.connect('Accounts.db') as con:
        try:
            cur = con.cursor()
            data_login_and_password = cur.execute(""" SELECT login, password, username FROM users WHERE login = (?) AND password = (?) """, (login, password))
            for item in data_login_and_password:
                item_login = item[0]
                item_password = item[1]
                sign_in__item_username = item[2]
            if item_login != '' and item_password != '':
                cur = con.cursor()
                cur.execute(""" UPDATE users SET online = 1 WHERE login = (?) """, (login,))
                cur.execute(""" UPDATE users SET ip = (?), port = (?) WHERE login = (?) """, (ip, port, login))
                mode = 463245672356463564362754655
                message = 'You are successfully logged in'
                data = f'{mode} {sign_in__item_username} {message}'
                server_socket.sendto(data.encode(), addr)
        except:
            mode = 236432456235462354652364623
            message = 'wrong login or password'
            data = f'{mode} {message}'
            server_socket.sendto(data.encode(), addr)

""" online """
def offline(username):
    with sqlite3.connect('Accounts.db') as con:
        try:
            cur = con.cursor()
            cur.execute(""" UPDATE users SET online=0, ip=NULL, port=NULL WHERE username = (?) """, (username,))
        except:
            pass

def search_username(username):
    with sqlite3.connect('Accounts.db') as con:
        try:
            cur = con.cursor()
            ip_port = cur.execute(""" SELECT online, ip, port FROM users WHERE username = (?) """, (username,))
            for item in ip_port:
                online = item[0]
                ip = item[1]
                port = item[2]
            return online, ip, port
        except:
            pass

print('[ Server started ]')

server_mode = True

clients = []

while server_mode:
    try:
        data, addr = server_socket.recvfrom(1024)

        raw_data = data.decode().split()[0]
        if raw_data == '478365784365763486576345436': # create an account
            login = data.decode().split()[1]
            password = data.decode().split()[2]
            username = data.decode().split()[3]
            ip = list(addr)[0]
            port = list(addr)[1]
            create_account(login, password, username, ip, port)

        elif raw_data == '573485356565656745465785346': # authorization
            login = data.decode().split()[1]
            password = data.decode().split()[2]
            ip = list(addr)[0]
            port = list(addr)[1]
            sign_in(login, password, ip, port)

        elif raw_data == '123123465687565476476567567': # connection
            username = data.decode().split()[2]
            raw_addr = list(addr)
            raw_addr.append(username)
            raw_addr = tuple(raw_addr)
            clients_online.append(raw_addr)

        elif raw_data == '787544376574564327587534785': # online
            username = data.decode().split()[2]
            offline(username)

        elif raw_data == '312312565364362462354762344': # private messages
            username = data.decode().split()[1]
            message = data.decode().split()[2:]
            #message = " ".join(message)
            online, ip, port = search_username(username)
            print(online, ip, port)
            if online == 0:
                pass
            else:
                addr_user = [ip, int(port)]
                addr_user = tuple(addr_user)
                print(addr_user)
                server_socket.sendto('sdfsd'.encode(), addr_user)

        else:
            pass

        #for item in clients:
        #    if addr != item:
        #        server_socket.sendto(data, item)

    except:
        server_mode = False
        print('[ Server stopped ]')
