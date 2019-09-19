'''
webframe
模拟网站的后端应用框架
从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
将需要的数据反馈给httpserver
'''
from socket import *
from urls import *
import json
from config import  *
from threading import Thread
class Applacation:
    def __init__(self):
        self.s = socket()
        self.s.bind((frame_host, frame_port))
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def start(self):
        self.s.listen(3)
        while True:
            connfd,addr = self.s.accept()
            client = Thread(target=self.handle,
                            args=(connfd,))
            client.setDaemon(True)
            client.start()
    def get_data(self,info):
        for url,func in urls:
            if url == info:
                print(url)
                return {'status':'200','data':func()}
        else:
            print('-----进入elsel '+url + info)
            return {'status':'404','data':'NOT FOUND'}
    def get_html(self,request):
        if request['info'] == '/':
            f = open('./static/Mysql.html', 'r')
            print('输出fff')
            return {'status':'200','data':f.read()}
        elif request['info'] == '/mysql.html':
            f = open('./static/Mysql.html', 'r')
            return {'status':'200','data':f.read()}
        elif request['info'] == '/python.html':
            f = open('./static/pythonNet.html', 'r')
            return {'status':'200','data':f.read()}
        elif request['info'] == '/re.html':
            f = open('./static/RE.html', 'r')
            return {'status':'200','data':f.read()}
        else:
            f = open('./static/404.html', 'r')
            return {'status':'404','data':f.read()}

    def handle(self,connfd):
        request = json.loads(connfd.recv(1024).decode())
        # print(request)
        # print(request['info'][-5:])
        dic = dict()

        if request['info'] == '/' or request['info'][-5:] == '.html':
            data = self.get_html(request)
        else:
            print(request['info']+'-----------')
            data = self.get_data(request['info'])


        connfd.send(json.dumps(data).encode())
        connfd.close()



# c.send(json.dumps({'status':'200','data':'http test'}).encode())
if __name__ == '__main__':
    app = Applacation()
    app.start()