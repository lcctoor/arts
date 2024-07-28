# 项目描述

Cliapi 是一个专为 Python 初学者设计的 WEB 包，目的是让学者能够以非常简单的方式搭建一个 web 服务，进而提高对 Python 的兴趣，步入 Python 的世界。

# 作者

江南雨上

[主页](https://lcctoor.com/index.html) \| [Github](https://github.com/lcctoor) \| [PyPi](https://pypi.org/user/lcctoor) \| [微信](https://lcctoor.com/cdn/WeChatQRC.jpg) \| [邮箱](mailto:lcctoor@outlook.com) \| [捐赠](https://lcctoor.com/cdn/DonationQRC-0rmb.jpg)

# Bug提交、功能提议

你可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.com/cdn/WeChatQRC.jpg) 与我联系。

# 安装

在命令行执行：

```
pip install cliapi
```

# 教程

## 运行一个服务

```python
import asyncio
from cliapi import server, Request


def get_1(request: Request):
    return 'Hi, cliapi GET request successful!'

def post_1(request: Request):
    return 'Hi, cliapi POST request successful!'


async def main():
    app1 = server(get=get_1, post=post_1, port=8887)
    await asyncio.Event().wait()

asyncio.run(main())
```

此时，你可以在浏览器中访问 [http://localhost:8887/](http://localhost:8887/) ，并看到页面上显示【Hi, cliapi GET request successful!】。

## 说明

以下是 `request` 参数的常用属性及其描述：

| 属性                   | 描述                                                |
| ---------------------- | --------------------------------------------------- |
| request.full_url       | 完整的请求URL，包括协议、主机名和查询字符串         |
| request.uri            | 请求的URI路径，包含查询字符串                       |
| request.path           | 请求的路径部分，不包括查询字符串                    |
| request.arguments      | 查询字符串参数的字典，键是参数名，值是参数值的列表  |
| request.body           | 请求体的原始字节数据                                |
| request.body_arguments | 请求体中的参数字典，键是参数名，值是参数值的列表    |
| request.cookies        | 请求中的所有 cookie，键是 cookie 名，值是 cookie 值 |
| request.headers        | 请求头的字典，键是头的名称，值是头的值              |
| request.host           | 请求的主机名和端口                                  |
| request.host_name      | 请求的主机名，不包含端口                            |
| request.files          | 上传的文件字典，键是文件名，值是文件对象的列表      |

## 进一步引导兴趣 —— 完成《在线阅读四大名著》网站

当你的学员能够正确部署一个服务后，你可以让他尝试做一个《在线阅读四大名著》网站。在此计划中，学员须要完成以下事项：

1、收集四大名著（西游记、三国演义、水浒传、红楼梦）每部小说的前 5 章。

2、部署服务，根据上面的 `request参数表` 重新设计 `get_1` 函数，使服务按照 `/{book}/pages/{n}` 的路径返回各小说的章节，例如：访问 [http://localhost:8887/xiyouji/pages/1](http://localhost:8887/xiyouji/pages/1) 时，返回《西游记》的第一章。然后在浏览器上体验该网站。

3、有条件的话，注册一个域名，购买一个便宜的云服务器，将服务部署在云端，然后在本地设备上体验云网站。
