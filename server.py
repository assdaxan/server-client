#! python3
# -*- coding:UTF-8 -*-
import socket
from threading import Thread, Lock
from time import strftime, localtime

# 서버 정보
HOST = ''
PORT = 50007

count = 0        # 사용자 카운트
MaxConnect = 10  # 동시 접속 세션 수
BUFFSIZE = 1024  # 소켓 통신에서 사용하는 버퍼 크기

connList = []    # 소켓연결 리스트
result = {}      # 스레드 결과
threadList = []  # 스레드 리스트
LOCK = Lock()    # 스레드 Lock

# 자주사용하는 sendall, recv 함수 정의
def recv(conn, size=BUFFSIZE):
    return conn.recv(size).decode()

def send(conn, string):
    conn.sendall(string.encode())
    
def service(conn, result):
    try:
        # 시간 문자열 생성 및 전송
        time_Str = strftime('%H:%M:%S', localtime())
        send(conn, time_Str)

        # 문자열 송/수신
        send(conn, 'input string : ')
        s = conn.recv(BUFFSIZE).decode()

        # 문자열 길이 송신
        Len = len(s)
        send(conn, '%d'%Len)

        result.update({conn:Len}) # 스레드 실행결과 저장
    except ConnectionResetError: # 연결도중 끊김 예외처리
        result.update({conn:False})

def threadFun(conn):
    global count, connList, result    # 전역변수 명시
    with conn:
        # service 스레드 시작
        t = Thread(target=service, args=(conn, result))
        t.start()
        t.join()    # 스레드 시작 및 종료까지 대기
        connList.remove(conn)    # 스레드 리스트에서 삭제
        
        LOCK.acquire()    # 경쟁을 피하기 위해 스레드 Lock
        if result[conn]:
            count += 1    # count 증가
            print('result : %d'%result[conn])    # service 스레드 실행결과 출력
            print('count : %d'%count)
        LOCK.release()    # Lock 해제

def main():
    # 소켓 생성
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))    # 소켓 설정
        except Exception as a:
            print(a)
        else:
            while(True):
                s.listen(1)    # 연결 대기
                conn, addr = s.accept()
                # 종료된 스레드 자원 회수
                for t in threadList:
                    if not t.isAlive():
                        t.join()
                # 연결 MaxCount 까지 제한
                if len(connList) < MaxConnect:
                    print('Connected by', addr) # 연결정보 출력
                    connList.append(conn)
                    t = Thread(target=threadFun, args=(conn, ))
                    t.start()
                    threadList.append(t)
                else:
                    with conn:
                        send(conn, '')
                        print('more than the maximum connection')

if __name__ == '__main__':
    main()
