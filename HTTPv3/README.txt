httpserver 的简单构建

httpserver部分
获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端

WebFrame部分
从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
将需要的数据反馈给httpserver
项目结构:
         |--httpserver --HttpServer.py (主程序)
         |             --config (httpserver配置)
         |
project--|
         |
         |
         |--WebFrame --WebFrame.py (主程序代码)
                     --static (存放静态网页)
                     --views.py ( 应用处理程序)
                     --urls.py (存放路由)
                     --settings (框架配置)
交互数据格式协议
httpserver-->webframe {method:'GET',info:'/'}
webframe-->httpserver {status:'200',data:'ccccc'}