#! python3
# -*- coding:UTF-8 -*-
import socket

# 서버 정보
# localhost:50007
HOST = '127.0.0.1'
PORT = 50007

BUFFSIZE = 1024    # 소켓 통신에서 사용하는 버퍼 크기

# 자주사용하는 sendall, recv 함수 정의
def recv(conn, size=BUFFSIZE):
    return conn.recv(size).decode()

def send(conn, string):
    conn.sendall(string.encode())
    
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))    # 소켓 연결
        except Exception as e:
            print(e)
        else:
            try:
                # 날짜 정보 수신
                time = recv(s)
                if time:
                    print(time)

                    # 문자열 송/수신
                    data = recv(s)
                    while(True):
                        string = input(data)
                        if string: # 아무것도 입력안하고 엔터치면 예외처리
                            break
                    send(s, string)

                    # 전송한 문자열 길이 수신
                    Len = int(recv(s))

                    print('LEN : %d'%Len)    # 출력!
                else:
                    print('Server Connection Max')
            except ConnectionResetError: # 연결 에러 예외처리
                print('Server Connection Error')
            
if __name__ == '__main__':
    main()
