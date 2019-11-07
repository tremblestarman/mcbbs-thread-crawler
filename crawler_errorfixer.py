import os, json, time, gc
from mcbbs_thread import bbsthread, get_ip_list
use_proxy = False
log = r'@.log'

if use_proxy:
    get_ip_list(0)
todo = []
with open(log, 'r+') as f:
    for i in f.read().splitlines():
        if not re.findall('tid= (\d+) banned-ip', i) == []:
            tid = re.findall('tid= (\d+)', i)[0]
            todo.append(tid)
with open(log, 'w+') as f:
    f.write('['+','.join(tids)+']')
# rewrite
for c in range(todo.__len__()):
    print('thread=', todo[c], str(c+1), '/' , todo.__len__())
    t = bbsthread(todo[c],use_proxy)
    if (os.path.exists('data_'+str(todo[c] - todo[c] % 100)+'.txt')):
        datas = {}
        with open('database/data_'+str(todo[c] - todo[c] % 100)+'.txt', 'r+', encoding='utf-8') as f:
            datas = json.loads(f.read())
            for i in datas:
                if (i['tid'] == todo[c]):
                    i['data'] = t.dict()
        with open('database/data_'+str(todo[c] - todo[c] % 100)+'.txt', 'w+', encoding='utf-8') as f:
            print('updated', 'data_'+str(todo[c] - todo[c] % 100)+'.txt')
            f.write(json.dumps(datas))
        del(datas)
    time.sleep(0.5 if use_proxy else 1) #avoid ban-ip
    del(t)
    gc.collect()