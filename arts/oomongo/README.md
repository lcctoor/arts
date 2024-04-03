# 项目描述

一个非常优雅的 MongoDB ODM 。

# 作者

[江南雨上](mailto:lcctoor@outlook.com)

[主页](https://lcctoor.github.io/arts) \| [Github](https://github.com/lcctoor) \| [PyPi](https://pypi.org/user/lcctoor) \| [微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) \| [邮箱](mailto:lcctoor@outlook.com) \| [捐赠](https://lcctoor.github.io/arts/arts/ip_static/DonationQRC-0rmb.jpg)

# Bug提交、功能提议

你可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) 与我联系。

# 安装

```
pip install oomongo
```

# 教程 ([查看美化版](https://lcctoor.github.io/arts/arts/oomongo) 👈)

本文将以最简洁的方式向你介绍核心知识，而不会让你被繁琐的术语所淹没。

## 导入

```python
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from oomongo import ODM, mc, mf, mo
```

## 创建ODM

```python
class ODM_2(ODM):

    def mkconn(self):  # 定义同步连接器
        return MongoClient(host='localhost', port=27017)
  
    async def amkconn(self):  # 定义异步连接器
        return AsyncIOMotorClient(host='localhost', port=27017)

odm = ODM_2()          # 账户ODM
db = odm['泉州市']      # 库ODM
sheet = db['希望小学']  # 表ODM
```

## 基础功能 —— 增、查、改、删

【增、查、改、删】的同步方法名称分别为：insert、find、update、delete 。

对应的异步方法名称为各同步方法名前加 `a` ，即：ainsert、afind、aupdate、adelete 。

### 示例

```python
row1 = {'姓名':'小一', '年龄':11, '幸运数字':[1, 2, 3], '成绩':{'语文':81, '数学':82}}
row2 = {'姓名':'小二', '年龄':12, '幸运数字':[2, 3, 4], '成绩':{'语文':82, '数学':83}}
row3 = {'姓名':'小三', '年龄':13, '幸运数字':[3, 4, 5], '成绩':{'语文':83, '数学':84}}
row4 = {'姓名':'小四', '年龄':14, '幸运数字':[4, 5, 6], '成绩':{'语文':84, '数学':85}}
row5 = {'姓名':'小五', '年龄':15, '幸运数字':[5, 6, 7], '成绩':{'语文':85, '数学':86}}
row6 = {'姓名':'小六', '年龄':16, '幸运数字':[6, 7, 8], '成绩':{'语文':86, '数学':87}}
```

|            | 同步方式                      | 异步方式                                                 |
| :---------: | ----------------------------- | -------------------------------------------------------- |
| 增（1 条） | sheet.insert( row1 )          | **await** sheet.**a**insert( row2 )          |
| 增（批量） | sheet.insert( row3, row4 )    | **await** sheet.**a**insert( row5, row6 )    |
|     查     | sheet.find( )                 | **await** sheet.**a**find( )                 |
|     改     | sheet.update( {'年龄': 100} ) | **await** sheet.**a**update( {'年龄': 200} ) |
|     删     | sheet.delete( )               | **await** sheet.**a**delete( )               |

### 新增时，查看分配到的主键：

```python
row1 = {'姓名':'小一', '年龄':11, '幸运数字':[1, 2, 3], '成绩':{'语文':81, '数学':82}}
row2 = {'姓名':'小二', '年龄':12, '幸运数字':[2, 3, 4], '成绩':{'语文':82, '数学':83}}
row3 = {'姓名':'小三', '年龄':13, '幸运数字':[3, 4, 5], '成绩':{'语文':83, '数学':84}}

r1 = sheet.insert( row1 )
r2 = sheet.insert( row2, row3 )
```

方法1：使用 insert 添加数据成功后，row1~row3 已各自多了一个叫‘_id’的键，该键的值即分配到的主键。

方法2：

```python
r1.inserted_id
r2.inserted_ids
```

## 注：下文中所有示例都同时支持同步方式和异步方式，将同步示例中的 insert、delete、update、find 替换为 ainsert、adelete、aupdate、afind 即为异步方式，当然，须加上 await 前缀。

## 条件筛选

### 示例一：理解条件筛选的基本范式

筛选【年龄>13，且视力≧4.6，且性别为女】的数据，并进行查改删：

**查询**：`sheet[mc.年龄 > 13][mc.视力 >= 4.6][mc.性别 == '女'].find( )`

**修改**：`sheet[mc.年龄 > 13][mc.视力 >= 4.6][mc.性别 == '女'].update( {'年级':'初一', '爱好':'画画,跳绳'} )`

**删除**：`sheet[mc.年龄 > 13][mc.视力 >= 4.6][mc.性别 == '女'].delete( )`

### 筛选操作清单

| **代码**                                                                 | 解释                                            |
| ------------------------------------------------------------------------------ | ----------------------------------------------- |
| mc.年龄 > 10                                                                   | 大于                                            |
| mc.年龄 >= 10                                                                  | 大于或等于                                      |
| mc.年龄 < 10                                                                   | 小于                                            |
| mc.年龄 <= 10                                                                  | 小于或等于                                      |
| mc.年龄 == 10                                                                  | 等于                                            |
| mc.年龄 != 10                                                                  | 不等于                                          |
| mc.年级 == mf.isin( '初三', '高二' )                                           | 若字段值是传入值的成员，则符合                  |
| mc.年龄 == mf.notin( 10, 30, 45 )                                              | 若字段值不是传入值的成员，则符合                |
| mc.爱好 == mf.contain_all( '画画', '足球' )                                    | 若（列表）字段值包含传入值的所有元素，则符合    |
| mc.爱好 == mf.contain_any( '画画', '足球' )                                    | 若（列表）字段值包含传入值的至少1个元素，则符合 |
| mc.爱好 == mf.contain_none( '画画', '足球' )                                   | 若（列表）字段值不包含传入值的任何元素，则符合  |
| mc.姓名 == mf.re( '小' )                                                       | 正则匹配                                        |
| \[mc.年龄 > 3\][mc.年龄 < 100]                                                 | 交集（方式一）                                  |
| [ (mc.年龄 > 3) & (mc.年龄 < 100) ]                                            | 交集（方式二）                                  |
| [(mc.年龄<30)&#124; (mc.年龄>30) &#124; (mc.年龄==30) &#124; (mc.年龄==None)] | 并集                                            |
| [ (mc.年龄 > 3) - (mc.年龄 > 100) ]                                            | 差集                                            |
| [ ~(mc.年龄 > 100) ]                                                           | 补集                                            |

注：

1、isin、notin 用于判断（普通）字段的值是否传入值的成员，针对普通字段。

2、contain_any、contain_none 用于判断传入值是否（列表）字段的值的成员，针对列表字段。

3、isin、notin、contain_all、contain_any、contain_none 的传入值都不必是同类型的数据，以 isin 为例：可以这样使用：mc.tag == mf.isin( 3, 3.5, '学生', None )，传入值含有 int、float、str、NoneType 等多种类型。

4、成员运算符未传入任何值时的处理方式：

| **代码**                | **处理方式** |
| ----------------------------- | ------------------ |
| mc.年级 == mf.isin( )         | 所有数据都 不符合  |
| mc.年级 == mf.notin( )        | 所有数据都 符合    |
| mc.爱好 == mf.contain_all( )  | 所有数据都 符合    |
| mc.爱好 == mf.contain_any( )  | 所有数据都 不符合  |
| mc.爱好 == mf.contain_none( ) | 所有数据都 符合    |

5、四种集合运算可以相互嵌套，且可以无限嵌套。

### 示例二：理解并集、交集、补集的使用

筛选【年龄>13或视力≧4.6、且姓名含有‘小’、且年龄不高于15】的数据：

**查询**：`sheet[(mc.年龄>13) | (mc.视力>=4.6)][mc.姓名 == mf.re('小')][~(mc.年龄>15)].find( )`

**修改**：`sheet[(mc.年龄>13) | (mc.视力>=4.6)][mc.姓名 == mf.re('小')][~(mc.年龄>15)].update( {'年级':'初三'} )`

**删除**：`sheet[(mc.年龄>13) | (mc.视力>=4.6)][mc.姓名 == mf.re('小')][~(mc.年龄>15)].delete( )`

### 根据子元素过滤

可使用  mc.xxx.xxx.xxx...  的形式来表示子孙元素。

查询【语文成绩>80】的数据：

```python
sheet[mc.成绩.语文 > 80].find()
```

## 特殊字段名的表示方法

MongoDB 支持各种特殊的字段名，如：数字、符号、emoji 表情，这些字符在 Python 中不是合法变量名，因此使用  mc.1、mc.+  等格式会报错，可用  mc['1']、mc['+']、mc['👈']  这种格式代替。

## 切片

1、切片格式为  [start: stop: step]  ，start 表示从哪条开始，stop 表示到哪条停止，step 表示步长。

2、start 和 stop

* 当为正值时，表示正序第 x 条，例如：1 表示第 1 条、2 表示第 2 条。
* 当为负值时，表示倒数第 x 条，例如：-1 表示倒数第 1 条、-2 表示倒数第 2 条。
* 不可为 0 。

3、step

* 须为正整数。
* 当 step >= 2  时表示间隔式切片。
* 当 step = 1 时可省略 `: step` ，即：[start: stop] 等价于 [start: stop: 1] 。

### 示例

```python
sheet[过滤器]...[过滤器][:].find()                      # 查询符合条件的全部数据
sheet[过滤器]...[过滤器][:].delete()                    # 删除符合条件的全部数据
sheet[过滤器]...[过滤器][:].update({'年级':'初一'})      # 修改符合条件的全部数据

sheet[过滤器]...[过滤器][1].find()                      # 查询符合条件的第1条
sheet[过滤器]...[过滤器][1].delete()                    # 删除符合条件的第1条
sheet[过滤器]...[过滤器][1].update({'年级':'初一'})      # 修改符合条件的第1条

sheet[过滤器]...[过滤器][3:7].find()                    # 查询符合条件的第3~7条
sheet[过滤器]...[过滤器][3:7].delete()                  # 删除符合条件的第3~7条
sheet[过滤器]...[过滤器][3:7].update({'年级':'初一'})    # 修改符合条件的第3~7条

sheet[过滤器]...[过滤器][3:7:2].find()                  # 查询符合条件的第3、5、7条
sheet[过滤器]...[过滤器][3:7:2].delete()                # 删除符合条件的第3、5、7条
sheet[过滤器]...[过滤器][3:7:2].update({'年级':'初一'})  # 修改符合条件的第3、5、7条
```

值得注意的地方：  [3: 8: 2]  操作第  3、5、7  条，而  [8: 3: 2]  操作第  8、6、4  条。

更多示例：

```python
[:]           # 所有数据
[1:-1]        # 所有数据
[-1:1]        # 所有数据（逆序）
[1:]          # 所有数据
[:1000]       # 第1条 ~ 第1000条
[:-1000]      # 第1条 ~ 倒数第1000条
[100:200]     # 第100条 ~ 第200条
[200:100]     # 第200条 ~ 第100条
[-300:-2]     # 倒数第300条 ~ 倒数第2条
[50:-2]       # 第50条 ~ 倒数第2条
[250:]        # 第250条 ~ 最后1条
[-250:]       # 倒数第250条 ~ 最后1条
[1]           # 第1条
[-1]          # 最后1条
[::3]         # 以3为间距, 间隔操作所有数据
[100:200:4]   # 以4为间距, 间隔操作第100条 ~ 第200条
```

## 字段提示

变量 mc 无字段提示功能，输入‘mc.’后，编辑器不会提示可选字段。

为了获得字段提示功能，可自建一个‘mc2’：

```python
class mc2(mc):
    姓名 = 年龄 = 幸运数字 = None
    class 成绩:
        语文 = 数学 = None

sheet[mc.姓名 == '小王'][mc2.年龄 > 10].find()
sheet[mc.姓名 == '小王'][mc2.成绩.语文 > 80].find()
```

注：

1、mc2 与 mc 用法完全一致，可混用。

2、mc2 设置字段提示后，仅具备提示效果，而不产生任何实际约束。

## 排序

对所有年龄>12的数据，优先按年龄降序，其次按姓名升序，排序后返回第 2\~4 条数据：

```python
sheet[mc.年级=='高一'].order(年龄=False, 姓名=True)[2:4].find()
```

有趣的，以下两行代码的返回结果相同：

```python
sheet[mc.年级=='高一'].order(年龄=True)[1:-1].find()

sheet[mc.年级=='高一'].order(年龄=False)[-1:1].find()
```

解释：order(年龄=False) 表示按年龄降序，[-1:1]表示逆序切片，产生了类似‘负负得正’的效果。

注：

1、筛选器、切片器、排序器、限定字段器的位置可任意，位置不影响其效果。当然，它们都应该在 sheet 之后，且在 find/update/delete 之前。

2、可反复排序，find/update/delete 时是根据最后1次指定的顺序提取数据。以下代码最终是按年龄降序后提取数据：

```python
sheet.order(年龄=True, 姓名=False).order(年龄=False).find()
```

3、若想取消排序，则再次调用order方法，但不传入任何值。

```python
sheet.order(年龄=True, 姓名=False).order().find()
```

## 限定字段

只返回姓名、年龄这2个字段：

```python
sheet[mc.年级=='高一']['姓名','年龄'].find()
```

注：

1、限定字段只对 find 有作用，对 update/delete 无作用但不会报错。

2、筛选器、切片器、排序器、限定字段器的位置可任意，位置不影响其效果。当然，它们都应该在 sheet 之后，且在 find/update/delete 之前。

3、可反复限定字段，查询时是根据最后一次指定的字段提取数据。以下代码返回结果中只有‘年龄’字段：

```python
sheet[mc.年级=='高一']['姓名']['年龄'].find()
```

4、若想恢复提取全部字段，则限定字段为 `None` ，`None` 即代表“全部字段”。

```python
sheet[mc.年级=='高一']['姓名'][None].find()
```

## 统计 与 删库删表

|                        | 同步方式                    | 异步方式                                               |
| ---------------------- | --------------------------- | ------------------------------------------------------ |
| 统计库的数量           | odm.len( )                  | **await** odm.**a**len( )                  |
| 统计表的数量           | db.len( )                   | **await** db.**a**len( )                   |
| 统计行的数量           | sheet.len( )                | **await** sheet.**a**len( )                |
| 统计符合条件的行的数量 | sheet[ mc.age > 8 ].len( ) | **await** sheet[ mc.age > 8 ].**a**len( ) |
| 获取库名清单           | odm.get_db_names( )         | **await** odm.**a**get_db_names( )         |
| 获取表名清单           | db.get_sheet_names( )       | **await** db.**a**get_sheet_names( )       |
| 删除某个库             | db.delete_db( )             | **await** db.**a**delete_db( )            |
| 删除某张表             | sheet.delete_sheet( )       | **await** sheet.**a**delete_sheet( )      |

## 迭代所有 库ODM 和 表ODM

```python
# 同步方式迭代
for db in odm:
    for sheet in db:
        print(sheet.sheet_name)

# 异步方式迭代
async for db in odm:
    async for sheet in db:
        print(sheet.sheet_name)
```

## 特殊操作

### 示例：自增

由于新年到了，令所有学生的年龄增加 1 岁：

```python
sheet.update( {'年龄': mo.inc( 1 )} )
```

### 特殊操作清单：

| **语法**        | **含义**                                     |
| --------------------- | -------------------------------------------------- |
| mo.inc( 1.5 )         | 自增 1.5                                           |
| mo.inc( -1.5 )        | 自减 1.5                                           |
| mo.add( 1, 2, 3 )     | 向列表字段添加元素，仅当被添加的元素不存在时才添加 |
| mo.push( 1, 2, 3 )    | 向列表字段添加元素，无论被添加的元素是否存在都添加 |
| mo.pull( 15 )         | 从列表字段删除 1 个等于 15 的值                    |
| mo.popfirst           | 从列表字段删除第 1 个元素                          |
| mo.poplast            | 从列表字段删除最后 1 个元素                        |
| mo.rename( '新名称' ) | 重命名字段                                         |
| mo.unset              | 删除字段                                           |
| mo.delete             | 删除字段（与 mo.unset 等价）                       |

示例：

```python
sheet[mc.姓名=='小六'].update({
    '姓名': 'xiaoliu',          # 修改为‘xiaoliu’
    '年龄': mo.inc(6),          # 自增6
    '幸运数字': mo.push(666),   # 添加666
    '视力': mo.rename('眼力'),  # 字段名改为‘眼力’
    '籍贯': mo.delete,          # 删除此字段
    '成绩.语文': 60,            # 改为60分
    '成绩.数学': mo.inc(-6)     # 减6分
})
```
