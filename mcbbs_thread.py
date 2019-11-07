#!/usr/bin/python3
import requests, lxml, re, bs4, random, threading
import jieba,jieba.analyse
from bs4 import BeautifulSoup
jieba.analyse.set_idf_path('idf.txt.big')
jieba.analyse.set_stop_words('stop_words.utf8')
class timeout(BaseException):
    pass
#ip proxy
proxy_list = []
def get_ip_list(id = 0):
    '''
    Refresh proxies pool every 30s. \n
    id = 0 : from www.xicidaili.com/nn \n
    id = 1 : from www.ip3366.net
    '''
    proxy_list.clear()
    if id == 0:
        get_ip_list_xici()
    else:
        get_ip_list_ip3366()
    threading.Timer(30,get_ip_list,(id,)).start()# refresh ip list every 30s
def get_ip_list_xici(url='http://www.xicidaili.com/nn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    print('ip pool refreshed.')
    print(proxy_list)
def get_ip_list_ip3366(url='http://www.ip3366.net/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    print('ip pool refreshed.')
    print(proxy_list)
#headers pool
headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
class bbsthread:
    def __init__(self, tid, use_proxy=False):
        '''
        Get bbsthread Model from a thread.

        :param tid: tid of the thread.\n
        :param use_proxy: use proxy or not. default is true.\n
        '''
        self.crawl_state = False
        self.info = {
            # basic info
            'title' : '',           #标题
            'author' : '',          #作者
            'time' : 0,             #发帖时间
            'view' : 0,             #查看次数
            'reply' : 0,            #回帖次数
            'category' : '',        #板块
            'subcategory' : '',     #子版块
            # viewratings
            'participation' : 0,    #参与人数
            'participants' : [],    #参与者
            'popularity' : 0,       #人气
            'golden-nugget' : 0,    #金粒
            'contribution' : 0,     #贡献
            'golden-ingot' : 0,     #金锭
            'emerald' : 0,          #绿宝石
            'nether-star' : 0,      #下界之星
            'heart' : 0,            #爱心
            'reasons' : [],         #评分理由
            # tag
            'seal' : '',            #图章
            'appraisal' : 0,        #评价指数
            'heat' : 0,             #热度
            'state' : [],          #帖子状态
            # technic
            'profits' : 0,          #积分总收益
            'title-keywords' : [],  #标题关键词
            'content-keywords' : [],#内容关键词
            'image-amount' : 0,     #图片数
            'iframe-amount' : 0,    #iframe数
            'table-amount' : 0,     #表格数
            'redirect-amount' : 0,  #外链数
            'operation' : 0,        #帖子被操作数
            'group' : ''            #来自小组
        }
        #try:
        header={}
        header['user-agent']= self.header_choice()
        url = 'https://www.mcbbs.net/thread-' + str(tid) + '-1-1.html'
        thread = BeautifulSoup(requests.get(url,headers=header,proxies=self.proxy_choice() if use_proxy else None,timeout=2).text,'lxml')
        self.crawl_state = 'ok' if thread.find('div', id='messagetext', attrs={'class': re.compile('alert_error|alert_info')}) == None else 'no-admission'
        if self.crawl_state == 'no-admission':
            return
        # prepare
            #location
        location = thread.find('div', id="pt", attrs={'class': 'bm cl'}).find('div', attrs={'class': 'z'})
            #posts
        posts = thread.find('div', id='postlist', attrs={'class': 'pl bm', 'id': 'postlist'})
            #head
        post_head = posts.find('table', attrs={'cellspacing': '0', 'cellpadding': '0'})
        head_info = post_head.find('div', attrs={'class': 'hm ptn'})
            #main post
        main_post = posts.find('div', id=re.compile(r'post_\d+'))
        pid = re.findall('\d+',main_post.attrs['id'])[0]
            #text
        text = main_post.find('td', id ='postmessage_' + pid, attrs={'class': 't_f'})
        if not text.find('div', attrs={'class': 'attach_nopermission attach_tips'}) == None:
            text.find('div', attrs={'class': 'attach_nopermission attach_tips'}).extract()
        if not text.find('i', attrs={'class': 'pstatus'}) == None:
            text.find('i', attrs={'class': 'pstatus'}).extract()
            #stamp
        stamp = main_post.find('div', id='threadstamp')
            #tags
        tags = post_head.find('td', attrs={'class': 'plc ptm pbn vwthd'}).find('span', attrs={'class': 'xg1'})
            #
        rates = main_post.find('dl', attrs={'class': 'rate'}).find('table', attrs={'class': 'ratl'}) if not main_post.find('dl', attrs={'class': 'rate'}) == None else None
        # basic info
        self.info['category'] = location.find('a', attrs={'href': re.compile(r'forum-\S+-1.html')}).string
        self.info['subcategory'] = post_head.find('h1',attrs={'class': 'ts'}).find('a').string if not post_head.find('h1', attrs={'class': 'ts'}).find('a') == None else ''
        self.info['title'] = post_head.find('h1', attrs={'class': 'ts'}).find('span', id='thread_subject').string
        self.info['view'] = int(head_info.findAll('span', attrs={'class': 'xi1'})[0].string)
        self.info['reply'] = int(head_info.findAll('span', attrs={'class': 'xi1'})[1].string)
        self.info['author'] = '匿名' if str(main_post.find('div', attrs={'class': 'pls favatar'}).find('div', attrs={'class': 'pi'}).string).strip() == '匿名' else main_post.find('div', attrs={'class': 'pls favatar'}).find('a', attrs={'class': 'xw1'}).string #avoid anonymous
        if main_post.find('td', attrs={'class': 'plc'}).find('div', attrs={'class': 'pti'}).find('em', id=re.compile(r'authorposton\d+')).find('span') == None:
            self.info['time'] = re.findall('^发表于\s(.+)$', main_post.find('td', attrs={'class': 'plc'}).find('div', attrs={'class': 'pti'}).find('em', id=re.compile(r'authorposton\d+')).string)[0]
        else:
            self.info['time'] = main_post.find('td', attrs={'class': 'plc'}).find('div', attrs={'class': 'pti'}).find('em', id=re.compile(r'authorposton\d+')).find('span').get('title')
        # feedback (visitors may not see)
        # tag
        self.info['seal'] = '' if stamp == None else stamp.find('img').attrs['title']
        self.info['appraisal'] = 0 if tags == None or tags.find('img', attrs={'title': re.compile('评价指数')}) == None else int(re.findall(r'\d+', tags.find('img', attrs={'title': re.compile('评价指数')}).attrs['title'])[0])
        self.info['heat'] = 0 if tags == None or tags.find('img', attrs={'title': re.compile('热度')}) == None else int(re.findall(r'\d+', tags.find('img', attrs={'title': re.compile('热度')}).attrs['title'])[0])
        self.info['state'] = [] if tags == None or tags.find('img', attrs={'alt': re.compile('\S+')}) == None else [x.attrs['alt'] for x in tags.findAll('img', attrs={'alt': re.compile('\S+')})]
        # viewratings
        if not rates == None:
            url_rate = 'https://www.mcbbs.net/forum.php?mod=misc&action=viewratings&tid=' + str(tid) + '&pid=' + str(pid)
            viewratings = BeautifulSoup(requests.get(url_rate,headers=header,proxies=self.proxy_choice() if use_proxy else None,timeout=2).text,'lxml')
            self.info['participation'] = int(rates.find('a', attrs={'title': '查看全部评分'}).span.string)
            raw_ratings = viewratings.find('div', attrs={'class': 'bm bw0'})
            if not raw_ratings == None:
                rate_list = raw_ratings.find('table', attrs={'class': 'list'})
                rate_sum = raw_ratings.find('div', attrs={'class': 'o pns'}).string
                self.info['popularity'] = int(re.findall(u'人气 ([\+\-]\d+) 点', rate_sum)[0]) if not re.findall('人气 ([\+\-]\d+) 点', rate_sum) == [] else 0
                self.info['golden-nugget'] = int(re.findall(u'金粒 ([\+\-]\d+) 粒', rate_sum)[0]) if not re.findall('金粒 ([\+\-]\d+) 粒', rate_sum) == [] else 0
                self.info['contribution'] = int(re.findall(u'贡献 ([\+\-]\d+) 点', rate_sum)[0]) if not re.findall('贡献 ([\+\-]\d+) 点', rate_sum) == [] else 0
                self.info['golden-ingot'] = int(re.findall(u'金锭 ([\+\-]\d+) 块', rate_sum)[0]) if not re.findall('金锭 ([\+\-]\d+) 块', rate_sum) == [] else 0
                self.info['emerald'] = int(re.findall(u'绿宝石 ([\+\-]\d+) 颗', rate_sum)[0]) if not re.findall('绿宝石 ([\+\-]\d+) 颗', rate_sum) == [] else 0
                self.info['nether-star'] = int(re.findall(u'下界之星 ([\+\-]\d+) 枚', rate_sum)[0]) if not re.findall('下界之星 ([\+\-]\d+) 枚', rate_sum) == [] else 0
                self.info['heart'] = int(re.findall(u'爱心 ([\+\-]\d+) 心', rate_sum)[0]) if not re.findall('爱心 ([\+\-]\d+) 心', rate_sum) == [] else 0
                self.info['participants'] = [x.find('a').string for x in rate_list.contents if type(x) == bs4.element.Tag and not x.find('a') == None]
                self.info['reasons'] = [x.findAll('td')[3].string for x in rate_list.contents if type(x) == bs4.element.Tag and not x.find('a') == None]
            else:
                print('banned.')
                self.crawl_state = 'banned-ip'
                return
        # technic
        self.info['profits'] = self.info['popularity'] * 3 + self.info['contribution'] * 10 + self.info['heart'] * 4
        self.info['image-amount'] = int(text.findAll('img').__len__())
        self.info['iframe-amount'] = int(text.findAll('iframe').__len__())
        self.info['table-amount'] = int(text.findAll('table').__len__())
        self.info['redirect-amount'] = int(text.findAll('a', attrs={'href': re.compile('https\:\/\/www\.mcbbs\.net/plugin\.php\?id=link_redirect\&target\=\S*'), 'target': '_blank'}).__len__())
        [i.extract() for i in text.findAll('div', attrs={'class': re.compile('.*tip.*')})] #remove tips to get raw text
        [i.extract() for i in text.findAll('div', attrs={'class': 'locked'})]
        raw_text = text.get_text()
        self.info['content-keywords'] = [x[0] for x in jieba.analyse.extract_tags(raw_text, topK=20, withWeight=True, allowPOS=())]
        self.info['title-keywords'] = [x[0] for x in jieba.analyse.extract_tags(self.info['title'], topK=5, withWeight=True, allowPOS=())]
        self.info['group'] = text.findAll('a', attrs={'href': re.compile('forum-\d+-1\.html')})[-1].string if not text.find('a', attrs={'href': re.compile('forum-\d+-1\.html')}) == None else ''
        url_operation = 'https://www.mcbbs.net/forum.php?mod=misc&action=viewthreadmod&tid=' + str(tid)
        operations = BeautifulSoup(requests.get(url_operation,headers=header,proxies=self.proxy_choice() if use_proxy else None,timeout=2).text,'lxml')
        self.info['operation'] = int(operations.find('table', attrs={'class': 'list'}).findAll('tr').__len__() - 1) if not operations.find('table', attrs={'class': 'list'}) == None else 0
        end = True
        #except:
        #    print('unknown error.')
        #    self.crawl_state = 'unknown-error'
    def dict(self):
        '''
        return info if succeeded otherwise state.
        '''
        return self.info if self.crawl_state == 'ok' else self.crawl_state
    def header_choice(self):
        global headers
        return random.choice(headers)
    def proxy_choice(self):
        global proxy_list
        return {'http': random.choice(proxy_list)}