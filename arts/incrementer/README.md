# 项目描述

分布式主键生成器，支持多机器\|多进程\|多线程并发生成。

# 作者

江南雨上

[主页](https://lcctoor.com/index.html) \| [Github](https://github.com/lcctoor) \| [PyPi](https://pypi.org/user/lcctoor) \| [微信](https://lcctoor.com/cdn/WeChatQRC.jpg) \| [邮箱](mailto:lcctoor@outlook.com) \| [捐赠](https://lcctoor.com/cdn/DonationQRC-0rmb.jpg)

# Bug提交、功能提议

你可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.com/cdn/WeChatQRC.jpg) 与我联系。

# 安装

```
pip install incrementer
```

# 教程

本文将以简洁的方式向你介绍核心知识，而不会让你被繁琐的术语所淹没。

## 导入

```python
from incrementer import Incrementer
```

## 创建生成器

```python
inc = Incrementer()
```

## 创建自增主键

```python
inc.get_incpk()  # >>> '1_1'
inc.get_incpk()  # >>> '1_2'
inc.get_incpk()  # >>> '1_3'
```

`_` 左边的 `1` 表示线程编码。

如果是在单线程情况下使用，可以调用 `get_simple_incpk` 方法：

```python
inc.get_simple_incpk()  # >>> '1'
inc.get_simple_incpk()  # >>> '2'
inc.get_simple_incpk()  # >>> '3'
```

get_incpk 同时适用于单线程和多线程情况下，而 get_simple_incpk 仅适用于单线程情况下。

## 获取编码后的时间戳

```python
inc.get_encoded_time()  # >>> 'lwdnayli'
```

## 获取编码后的进程ID

```python
inc.encoded_pid  # >>> '30g'
```
