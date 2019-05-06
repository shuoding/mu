import socket
import threading

def handler(cli_s, cli_addr):
    request = cli_s.recv(1048576)
    flag = request[0].decode('utf-8')
    requestBody = request[1:]
    if flag == 'D':
        key = requestBody.decode('utf-8')
        try:
            with open(key, 'rb') as f:
                cli_s.send('Y'.encode('utf-8') + f.read())
        except:
            cli_s.send('N'.encode('utf-8'))
    elif flag == 'U':
        key = ''
        while requestBody[0].decode('utf-8') != '*':
            key += requestBody[0].decode('utf-8')
            requestBody = requestBody[1:]
        requestBody = requestBody[1:]
        try:
            with open(key, 'wb') as f:
                f.write(requestBody)
        except:
            pass
    else:
        print('unknown request')

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('172.17.0.1', 6000))
    s.listen(10)
    while True:
        cli_s, cli_addr = s.accept()
        threading.Thread(target = handler, args = (cli_s, cli_addr)).start()

main()
