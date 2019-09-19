'''
http3.0
获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端
'''
from socket import *
import sys
from threading import Thread
from config import *
import re
import json

#与frame进行交互
def connect_frame(env):
    conn_to_frame_socket = socket()
    try:
        #连接webframe
        conn_to_frame_socket.connect((frame_host,frame_port))
    except:
        return

    data = json.dumps(env)  #转换为json
    conn_to_frame_socket.send(data.encode())  #发送
    data = conn_to_frame_socket.recv(1024*1024*10).decode()
    return json.loads(data)  #{'status':200,'data':'cccc'}


class Http_Server:
    def __init__(self):
        self.host = host
        self.port = port
        self.add = (host,port)
        #创建套接字
        self.create_socket()
        #绑定
        self.bind()
    def create_socket(self):
        self.socket = socket()
        self.socket.setsockopt(SOL_SOCKET,
                               SO_REUSEADDR,
                               DEBUG)
    def bind(self):
        self.socket.bind(self.add)
    def server_forever(self):
        self.socket.listen(5)
        print('Connect the port %s'%self.port)
        while True:
            connfd,addr = self.socket.accept()
            client = Thread(target=self.handle,
                            args=(connfd,))
            client.setDaemon(True)
            client.start()
    def handle(self,connfd):
        request = connfd.recv(1024).decode()
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern,request).groupdict()
        except:
            connfd.close(0)
            return
        else:
            response = connect_frame(env)
            if response:
                self.send_response(response,connfd)
    #组织http响应,发送给浏览器
    def send_response(self, response,cnnfd):
        #response ->{'status': '200', 'data': 'http test'}
        if response['status'] == '200':
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += response['data']
            cnnfd.send(data.encode())
        elif response['status'] == '404':
            data = "HTTP/1.1 404 NOT FOUND\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += response['data']
            cnnfd.send(data.encode())
        elif response['status'] == '500':
            # cnnfd.send(data.encode())
            pass



if __name__ == '__main__':
    h = Http_Server()
    h.server_forever()    #启动服务