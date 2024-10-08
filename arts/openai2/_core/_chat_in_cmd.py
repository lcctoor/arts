import sys
from .chat import Chat, AKPool
from arts.cooltypes import moduledb


mdb = moduledb.DB('https://pypi.org/project/openai2', depth=3)['_chat_in_cmd']
apikeys: moduledb.File = mdb['apikeys']['data_1']
apikeys.setdefault('list', [])
record: moduledb.File = mdb['records']['chat_1']
record.setdefault('messages', [])


def _chat_in_cmd(apikeys:list, newchat=False, model='gpt-4-turbo', msg_max_count=30):
    print(f"\n\033[0m你已进入命令行聊天模式, 当前使用'{model}'模型, 请确保你的apikey支持该模型.", end='')
    gpt = Chat(api_key=AKPool(apikeys), model=model, msg_max_count=msg_max_count)
    if not newchat:
        gpt.add_dialogs(*record['messages'])
    while True:
        user = input('\n\n\033[32;1m:')
        print('\033[0m')
        for x in gpt.stream_request(user):
            print(x, end='', flush=True)
        record['messages'] = gpt.fetch_messages()


命令提示 = '''指令集:
openai2 add_apikey <apikey> | 添加1个apikey              | 如需添加多个, 可执行多次
openai2 read_apikey         | 查看所有apikey             |
openai2 clear_apikey        | 清除所有apikey             |
openai2 chat                | 继续上次的对话              |
openai2 newchat             | 清空对话记录, 然后开始新对话 |
'''


def _ParseCmd():
    kws = sys.argv[1:]
    if kws:
        kw = kws[0].lower()
        
        # 添加apikey
        if kw == 'add_apikey' and len(kws) > 1:
            apikeys['list'].append( kws[1] )
            apikeys.save()
            print('添加 apikey 成功.')

        # 继续上次的对话
        elif kw == 'chat':
            _chat_in_cmd(apikeys['list'], newchat=False)
        
        # 清空对话记录, 然后开始新对话
        elif kw == 'newchat':
            _chat_in_cmd(apikeys['list'], newchat=True)
        
        # 查看所有apikey
        elif kw == 'read_apikey':
            for x in apikeys['list']:
                print(x)
        
        # 清除所有apikey
        elif kw == 'clear_apikey':
            apikeys['list'] = []
            print('已清除所有 apikey .')

        else:
            print(命令提示)
    else:
        print(命令提示)