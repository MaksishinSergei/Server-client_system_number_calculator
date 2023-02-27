# Импорт модулей
import socket
import threading
from time import time
import time
import datetime

# Переменные для подключения и работы функций сервера
IP = "127.0.0.1"
PORT = 2000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "exit"
CALCULATE_MSG = "calc"
HELP_MSG = "help"
HELP = '''
----------------------------------------------------------------------------
                        SERVER-CALCULATOR by Maksishin_S
----------------------------------------------------------------------------

                  This server is designed to translate numbers
            specified by the user from one number system to another!
                  The number systems are also set by the user!

----------------------------------------------------------------------------
Command list:
    help               - A brief summary of the server functions
    calc               - Calculator Mode
    exit               - Disconnection
    Y:
    log                - Autorization
    reg                - Registration
----------------------------------------------------------------------------
                                                             © GulaG Company
        '''
chars = '0123456789abcdefghijklmnopqrstuvwxyz'
now = datetime.datetime.now()

# Функция подключения и взаимодествия клиента с сервером


def handle_client(conn, addr):

    try:
        start_session = time.time()
        print(f"[NEW CONNECTION] {addr} connected.")
        hello_msg = f'''Welcome to the server-calculator! Enter the command "{HELP_MSG}" to view the server help
[SIGN IN/SIGN UP] Do you want to log in or register to use the calculator?(Enter Y/N):'''
        conn.send(hello_msg.encode(FORMAT))
        check_flag = False
        connected = True
        while connected:

            msg = conn.recv(SIZE).decode(FORMAT)

            if msg == 'Y':
                conn.send(msg.encode(FORMAT))
                msg = conn.recv(SIZE).decode(FORMAT)
                if msg == 'log':
                    print(f"[{addr}] The client is being authorized")
                    msg = "[AUTORIZATION] Enter your login:"
                    conn.send(msg.encode(FORMAT))
                    login = conn.recv(SIZE).decode(FORMAT)
                    msg = "[AUTORIZATION] Enter your password:"
                    conn.send(msg.encode(FORMAT))
                    password = conn.recv(SIZE).decode(FORMAT)
                    check_flag = found_log_pass(login, password)
                    if check_flag == True:
                        print(f"[{addr}] [AUTORIZATION] {check_flag}")
                        msg = f"You have successfully logged in! Hello, {login}!"
                        conn.send(msg.encode(FORMAT))
                        msg = conn.recv(SIZE).decode(FORMAT)
                    else:
                        msg = "[WARNING] Invalid login or password!"
                        print(f"[{addr}] [AUTORIZATION] {check_flag}")
                        conn.send(msg.encode(FORMAT))
                        msg = conn.recv(SIZE).decode(FORMAT)
                elif msg == 'reg':
                    print(f"[{addr}] The client is being registered")
                    msg = "[REGISTRATION] Enter your login:"
                    conn.send(msg.encode(FORMAT))
                    new_login = conn.recv(SIZE).decode(FORMAT)
                    msg = "[REGISTRATION] Enter your password:"
                    conn.send(msg.encode(FORMAT))
                    new_password = conn.recv(SIZE).decode(FORMAT)
                    check_flag = registr_log_pass(new_login, new_password)
                    if check_flag == True:
                        print(f"[{addr}] [REGISTRATION] {check_flag}")
                        msg = f"You have successfully registered! Hello, {new_login}"
                        conn.send(msg.encode(FORMAT))
                        msg = conn.recv(SIZE).decode(FORMAT)
                    else:
                        msg = "[WARNING] Sorry, But client with this login is already registered"
                        print(f"[{addr}] [REGISTRATION] {check_flag}")
                        conn.send(msg.encode(FORMAT))
                        msg = conn.recv(SIZE).decode(FORMAT)
            elif msg == 'N':
                msg = '''Without authorization or registration, you will not be able to use the calculator
But you can log in or register at any time (to do this, enter Y)'''
                conn.send(msg.encode(FORMAT))
                msg = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                print(f'[CONNECTION] {addr} disconnected at {now.strftime("%H:%M")}. Session duration - ',
                      str(round((time.time() - start_session), 2)), 'seconds')
                msg = "[DISCONNECTION] Enter any NOT EMPTY string"
                conn.send(msg.encode(FORMAT))
                connected = False
            elif msg == HELP_MSG:
                print(f"[{addr}] {msg}")
                msg = HELP
                conn.send(msg.encode(FORMAT))
            elif msg == CALCULATE_MSG and check_flag == True:
                # Необходимы переменные для перевода из одной СС в другую
                msg = "Enter the number:"
                conn.send(msg.encode(FORMAT))
                number = conn.recv(SIZE).decode(FORMAT)
                print(f"[{addr}] {number}")
                msg = "Enter the number system (from):"
                conn.send(msg.encode(FORMAT))
                system_number_from = conn.recv(SIZE).decode(FORMAT)
                print(f"[{addr}] {system_number_from}")
                msg = "Enter the number system (to):"
                conn.send(msg.encode(FORMAT))
                system_number_to = conn.recv(SIZE).decode(FORMAT)
                print(f"[{addr}] {system_number_to}")

                # Получения и отправка результата перевода числа клиенту
                if system_number_from.isdigit() and system_number_to.isdigit():
                    if int(system_number_from) == 10 and int(system_number_to) != 10:
                        if convert_10s_to_ns(number, system_number_to) == "Error chars":
                            result = "Error chars"
                            print(f"[{addr}] Result: {result}")
                            msg = "[WARNING] Invalid character! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        elif convert_10s_to_ns(number, system_number_to) == None:
                            msg = "[WARNING]The base of the number system is too large, enter the base no more 36! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        else:
                            result = convert_10s_to_ns(
                                number, system_number_to)
                            print(f"[{addr}] Result: {result}")
                            msg = f"Calculations performed successfully! Calculation result: {result}"
                            conn.send(msg.encode(FORMAT))
                    elif int(system_number_from) != 10 and int(system_number_to) == 10:
                        if convert_ns_to_10s(number, system_number_from) == "Error chars":
                            result = "Error chars"
                            print(f"[{addr}] Result: {result}")
                            msg = "[WARNING] Invalid character! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        elif convert_ns_to_10s(number, system_number_from) == "Error base":
                            result = "Error base"
                            print(f"[{addr}] Result: {result}")
                            msg = f"[WARNING] The number {max(number)} is not in the {system_number_from}-digit number system! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        elif convert_ns_to_10s(number, system_number_from) == None:
                            msg = "[WARNING]The base of the number system is too large, enter the base no more 36! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        else:
                            result = convert_ns_to_10s(
                                number, system_number_from)
                            print(f"[{addr}] Result: {result}")
                            msg = f"Calculations performed successfully! Calculation result: {result}"
                            conn.send(msg.encode(FORMAT))
                    elif int(system_number_from) != 10 and int(system_number_to) != 10:
                        if convert_ns_to_ns(number, system_number_from, system_number_to) == "Error chars":
                            result = "Error chars"
                            print(f"[{addr}] Result: {result}")
                            msg = "[WARNING] Invalid character! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        elif convert_ns_to_ns(number, system_number_from, system_number_to) == "Error base":
                            result = "Error base"
                            print(f"[{addr}] Result: {result}")
                            msg = f"[WARNING] The number {max(number)} is not in the {system_number_from}-digit number system! Try enter again"
                            conn.send(msg.encode(FORMAT))
                        else:
                            result = convert_ns_to_ns(
                                number, system_number_from, system_number_to)
                            print(f"[{addr}] Result: {result}")
                            result_msg = f"Calculations performed successfully! Calculation result: {result}"
                            conn.send(result_msg.encode(FORMAT))
                else:
                    result = "Error chars"
                    print(f"[{addr}] Result: {result}")
                    msg = "[WARNING] Invalid character! Try enter again"
                    conn.send(msg.encode(FORMAT))
            elif msg == CALCULATE_MSG and check_flag == False:
                msg = '[WARNING] the calculator is not available! Log in or register'
                conn.send(msg.encode(FORMAT))
            # Переотправка сообщений клиента с сервера клиенту
            else:
                print(f"[{addr}] {msg}")
                msg = f"Msg received: {msg}"
                conn.send(msg.encode(FORMAT))

        session_duration = round(time.time() - start_session, 2)
        session_protocol(session_duration, addr)
        conn.close()
    except (ConnectionResetError, ConnectionAbortedError):
        print(f'[{addr}] >>> The user is forcibly disabled')
        session_duration = round(time.time() - start_session, 2)
        session_protocol(session_duration, addr)
# Функция перевода из любой системы счисления в любую


def convert_ns_to_ns(number, system_number_from, system_number_to):
    for i in range(len(number)):
        if number[i] not in chars:
            return "Error chars"
    if int(system_number_from) <= chars.find(max(number)):
        return "Error base"
    elif int(system_number_from) > len(chars) or int(system_number_to) > len(chars):
        return None
    else:
        system_number_from = int(system_number_from)
        system_number_to = int(system_number_to)
        mid_result = int(number, system_number_from)
        result = ''
        while mid_result > 0:
            result = chars[mid_result %
                           system_number_to] + result
            mid_result //= system_number_to
        return result

# Функция перевода из 10-ой СС в любую систему счислению


def convert_10s_to_ns(number, system_number_to):
    for i in range(len(number)):
        if number[i] not in chars:
            return "Error chars"
    system_number_to = int(system_number_to)
    number = int(number)
    if system_number_to > len(chars):
        return None
    result = ''
    while number > 0:
        result = chars[number % system_number_to] + result
        number //= system_number_to
    return result

# Функция перевода из любой системы счисления в 10-ую СС


def convert_ns_to_10s(number, system_number_from):
    for i in range(len(number)):
        if number[i] not in chars:
            return "Error chars"
    if int(system_number_from) <= chars.find(max(number)):
        return "Error base"
    else:
        if int(system_number_from) > len(chars):
            return None
        else:
            result = int(number, int(system_number_from))
            return result

# функция логин-пароля


def found_log_pass(login, password):
    lp = open('login_password/login_password.txt', 'r')

    while True:
        line = lp.readline()
        if line.split(' ')[0] == login and line.split(' ')[1].strip() == password:
            lp.close()
            return True

        elif not line:
            break

    lp.close()
    return False

# функция регистрации


def registr_log_pass(new_login, new_password):
    lp = open('login_password/login_password.txt', 'r+')

    while True:
        line = lp.readline()
        if line.split(' ')[0] == new_login:
            lp.close()
            return False

        elif not line:
            break

    lp.write(f'\n{new_login} {new_password}')
    lp.close()
    return True

# Функция протоколирования длительности сессии


def session_protocol(session_duration, addr):
    p = open(f'time_protocol/ protocol-{now.strftime("%d-%m-%Y")}.txt', 'a')
    p.write(
        f'[{addr}]: Session duration - {session_duration} seconds, disconnect - {now.strftime("%H:%M")}\n')
    p.close()

# Основная функция для старта и работы сервера


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    # Многопоточность(возможность подключения к серверу нескольких программ-клиентов)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
