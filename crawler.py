#!/usr/bin/python3
import os,json,threading,time,gc
from mcbbs_thread import bbsthread, get_ip_list
datas = []
last = 9000 # avoid stopping unexpectedly (= tid / 100)
use_proxy = False
MAX = 923416 # max tid

if use_proxy:
    get_ip_list(0)

def crawler(f: int, t: int, c: int, i: int):
    global MAX
    '''
    A crawler.
    
    :param f: tid from \n
    :param t: tid to \n
    :param c: loop cycle \n
    :param i: thread-id in multi-thread
    '''
    for tid in range(f, t+1):
        if (tid > MAX):
            break
        print('thread=', i, 'cycle=', c, 'tid=', tid, 'start')
        t = bbsthread(tid,use_proxy)
        datas.append({'tid': tid, 'data': t.dict()})
        print('thread=', i, 'cycle=', c, 'tid=', tid, t.crawl_state)
        if tid % 500 == 0: #backup
            with open('database/data_'+str(c*100)+'.txt', 'w+', encoding='utf-8') as f:
                f.write(json.dumps(datas))
        time.sleep(1.5 if use_proxy else 2) #avoid ban-ip
        del(t)
        gc.collect()

# get small-pack (100 t/p)
for c in range(last, 10000):
    if c > MAX / 100:
        break
    threads = []
    try:
        # using multi-crawler
        for i in range(0,10):
            f = c*100+10*i
            t = f+9
            t = threading.Thread(target=crawler,args=(f,t,c,i))
            threads.append(t)
            t.start()
    except:
        print('error')
    for t in threads:
        t.join()
    with open('database/data_'+str(c*100)+'.txt', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(datas))
    for t in threads:
        del(t)
    gc.collect()
    datas.clear()