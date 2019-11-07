# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
#import matplotlib.dates as mdate
from pywaffle import Waffle
import json,os,random,requests,re,uuid
from stat_util import value_multi_conditional
cp = {'r-':'#f16889','y-':'#ffd981','g-':'#33ddb1','b-':'#3c9fc0','d-':'#345e6c',
    'r':'#ef476f','y':'#ffd166','g':'#06d6a0','b':'#118ab2','d':'#073b4c',
    'r+':'#c43b5b','y+':'#d1ac54','g+':'#05b083','b+':'#0e7192','d+':'#06313f'
}
occupy_cates = {
    'view': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'reply': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'participation': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'popularity': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'golden-nugget': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'contribution': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'golden-ingot':[('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')] ,
    'emerald': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'nether-star': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'heart': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'profits': [('<0', '<0', 'b'),('=0', '=0', 'y'),('>0', '>0', 'g')],
    'appraisal': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'heat': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'image-amount': [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'iframe-amount':  [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'table-amount':  [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'redirect-amount':  [('=0', '=0', 'y'),('>0', '>0', 'g')],
    'operation': [('=0', '=0', 'y'),('>0', '>0', 'g')]
}
hist_cates = {
    'view': [('1~100', '>=1,<=100', 'd'),('101~1k', '>100,<=1000', 'd-'),('1k~3k', '>1000,<=3000', 'b+'),('3k~5k', '>3000,<=5000', 'b'),('5k~10k', '>5000,<=10000', 'g+'),('10k~50k', '>10000,<=50000', 'g'),('50k~100k', '>50000,<=100000', 'y-'),('100k~500k', '>100000,<=300000', 'y'),('300k~1m', '>300000,<=1000000', 'r'),('>1m', '>1000000', 'r+')],
    'reply': [('1~3', '>=1,<=3', 'd'),('4~7', '>=4,<=7', 'd-'),('8~15', '>=8,<=15', 'b+'),('16~30', '>15,<=30','b'),('31~80', '>30,<=80', 'g+'),('81~150', '>80,<=150', 'g'),('151~300', '>150,<=300', 'y'),('301~1k', '>300,<=1000', 'y+'),('1k~2k', '>1000,<=2000', 'r'),('>2k', '>2000', 'r+')],
    'participation': [('1', '=1', 'd'),('2~5', '>1,<=5', 'b'),('6~10', '>5,<=10', 'g'),('11~20', '>10,<=20', 'y'),('21~50', '>20,<=50', 'y+'),('51~120', '>50,<=120', 'r'),('>120', '>120', 'r+')],
    'popularity': [('<0', '<0', 'd+'),('1~2', '>=1,<=2', 'b+'),('3~5', '>=3,<=5', 'b'),('6~10', '>5,<=10', 'g+'),('11~20', '>10,<=20','g'),('21~50', '>20,<=50', 'y'),('51~100', '>50,<=100', 'y+'),('101~200', '>101,<=200', 'r'),('>200', '>200', 'r+')],
    'golden-nugget': [('<0', '<0', 'd+'),('1~5', '>=1,<=5', 'b'),('6~20', '>5,<=20', 'g+'),('21~50', '>20,<=50', 'g'),('51~100', '>50,<=100', 'y'),('101~200', '>101,<=200', 'y+'),('201~500', '>200,<=500', 'r'),('>500', '>500', 'r+')],
    'contribution': [('<0', '<0', 'b'),('1~2', '>=1,<=2', 'g'),('3~4', '>=3,<=4', 'y'),('5~6', '>=5,<=6', 'y+'),('7~8', '>=7,<=8', 'r'),('>8', '>8', 'r+')],
    'golden-ingot': [('<0', '<0', 'b'),('1~2', '>=1,<=2', 'g'),('3~5', '>=3,<=5', 'y'),('6~10', '>=6,<=10', 'y+'),('11~20', '>=11,<=20', 'r'),('>20', '>20', 'r+')],
    'emerald': [('<0', '<0', 'b'),('1~2', '>=1,<=2', 'g'),('3~5', '>=3,<=5', 'y'),('6~10', '>=6,<=10', 'y+'),('11~20', '>=11,<=20', 'r'),('>20', '>20', 'r+')],
    'nether-star': [('<0', '<0', 'b'),('1~2', '>=1,<=2', 'g'),('3~5', '>=3,<=5', 'y'),('6~10', '>=6,<=10', 'y+'),('11~20', '>=11,<=20', 'r'),('>20', '>20', 'r+')],
    'heart': [('<0', '<0', 'b'),('1~2', '>=1,<=2', 'g'),('3~5', '>=3,<=5', 'y'),('6~10', '>=6,<=10', 'y+'),('11~20', '>=11,<=20', 'r'),('>20', '>20', 'r+')],
    'profits': [('<0', '<0', 'd'),('1~6', '>=1,<=6', 'b'),('7~30', '>=7,<=30', 'g'),('31~100', '>=31,<=100', 'y'),('101~200', '>=101,<=200', 'y+'),('201~500', '>=201,<=500', 'r'),('>500', '>500', 'r+')],
    'appraisal': [('20~50', '>=20,<=50', 'g'),('51~100', '>=51,<=100', 'y'),('101~200', '>=101,<=200', 'y+'),('201~500', '>=201,<=500', 'r'),('>500', '>500', 'r+')],
    'heat': [('1~200', '>=1,<=200', 'y-'),('201~500', '>=201,<=500', 'y'),('501~1k', '>=501,<=1000', 'r-'),('1k~3k', '>=1001,<=3000', 'r'),('>3k', '>3000', 'r+')],
    'image-amount': [('1~2', '>=1,<=2','d'),('3~5', '>=3,<=5','b'),('6~10', '>5,<=10','g'),('11~20', '>10,<=20','y'),('>20', '>20','r')],
    'iframe-amount':  [('1', '=1','d'),('2', '=2','b'),('=3', '=3','g'),('=4', '=4','y'),('>4', '>4','r')],
    'table-amount':  [('1', '=1','d'),('2~3', '>=2,<=3','b'),('4~6', '>=4,<=6','g'),('7~10', '>6,<=10','y'),('>10', '>10','r')],
    'redirect-amount':  [('1~2', '>=1,<=2','d'),('3~5', '>=3,<=5','b'),('6~10', '>=6,<=10','g'),('11~20', '>=11,<=20','y'),('>20', '>20','r')],
    'operation':  [('1', '=1','d'),('2~3', '>=2,<=3','b'),('4~6', '>=4,<=6','g'),('7~10', '>6,<=10','y'),('>10', '>10','r')]
}
seal_color = {
	"授权搬运": 'b',
	"置顶": 'y',
	"过期": 'r+',
	"优秀": 'y+',
	"原创": 'g+',
	"精华": '#00CED1',
	"推荐": 'y-',
	"版主推荐": 'r-',
	"美图": 'g-',
	"爆料": 'b-',
	"热帖": 'r',
	"公益": 'g',
	"版主回复": 'd-'
}
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
img_dir = ''
def new_img_dir(dir: str):
    global img_dir
    img_dir = dir + '/'
    if not os.path.exists('imgs/' + dir):
        os.mkdir('imgs/' + dir)
def sv_upload():
    global img_dir
    url='imgs/' + img_dir + str(uuid.uuid1()) + '.png'
    plt.savefig(url)
    #plt.show()
    plt.close('all')
    return url
'''
single figure
'''
def occupation_conditional(ax, cate: list, data: list, display: str = ''):
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    total = sum([data[x[1]] for x in cate])
    ax.set_xlim(0, total)
    left=0
    for x in cate:
        ax.barh([0], [data[x[1]]], left=[left], height=0.5, align='center', color=cp[x[2]], label=display+str(x[0])+'的帖子 ( '+str(data[x[1]])+', '+str(round(data[x[1]]*100/total,2))+'% ) ')
        left+=data[x[1]]
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', fontsize='6.5', fancybox=True, shadow=True)
def piecewise_hist(ax, cate: list, countdata: list, sumdata: list = None, display: str = ''):
    max_height = max(countdata.values())
    if max_height == 0:
        max_height = 1
    ax.set_ylim(0, max_height*1.1)
    height_rate = 0
    del_text = max_height*1.1*0.018
    if not sumdata == None:
        max_height = max(countdata.values())
        height_rate = max_height / max(sumdata.values()) if max(sumdata.values()) > 0 else 1
        plt.plot([x[0] for x in cate],[sumdata[x[0]]*height_rate for x in cate],label=display + '合计 ( 共' + str(sum(sumdata.values())) + ' )',linewidth=2,color='#222333',marker='.',alpha=0.5)
    for t, cond, col in cate:
        ax.bar([t], countdata[t], color=cp[col])
        ax.text(t, countdata[t], '帖数: ' + str(countdata[t]), ha='center', va= 'bottom',fontsize='6')
        if not sumdata == None:
            fley = 0 if sumdata[t] <= 0 else sumdata[t]*height_rate+max_height*1.1*0.005
            if abs(fley - countdata[t]) < del_text:
                if countdata[t] + 2 * del_text <= max_height: 
                    fley = countdata[t] + del_text    
                elif countdata[t] - 2 * del_text >= 0: 
                    fley = countdata[t] - del_text * 1.1
            colr= '#bbbccc' if fley < countdata[t] - del_text and ('d' in col or col == 'b+') else '#222333'
            ax.text(t, fley, '合计: ' + str(sumdata[t]), ha='center', va= 'bottom', fontsize='6', fontdict={'color':colr})
    ax.set_xlabel(display)
    ax.set_ylabel('帖子数量')
    ax.legend(fancybox=True, shadow=True, fontsize='6.5')
    ax.set_title('分段统计', fontdict={'fontweight': 'bold'})
def pie_percent(ax, part: int, body: int, display: str = '', display_nagetive: str = None):
    if display_nagetive == None:
        display_nagetive = '未' + display
    labels = [display, display_nagetive]
    fracs = [part, body - part]
    explode = [0.05, 0]
    ax.pie(radius=1.2, x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=False, labeldistance=10000, startangle=90, pctdistance=0.8, center=(0, 0.2),textprops={'fontsize': 'small'})
    ax.legend(loc=7, bbox_to_anchor=(0.2, 0.9), ncol=3, fancybox=True, shadow=True, fontsize='small')
    ax.set_title('总计: ' + str(body))
def pie_occupation(ax, data: dict, title: str):
    it = sorted(data.items(), key=lambda x: x[1], reverse=True)
    fracs = [x[1] for x in it]
    summary = sum(fracs)
    labels = [str(x[0]) + ' (' + str(round(x[1]*100/summary, 2)) + '%) ' for x in it]
    ax.pie(radius=1.4, x=fracs, labels=labels, autopct='%3.1f %%', shadow=False, labeldistance=10000, startangle=90, pctdistance=10000, center=(0, 0.2),wedgeprops=dict(width=0.35, edgecolor='w'))
    ax.legend(loc=10, ncol=3, fancybox=True, shadow=True, fontsize='7')
    ax.set_title(title + ' (总计: ' + str(summary) + ')', fontdict={'fontweight': 'bold'})
def occupation_splitted(ax, data: dict, col: list = None):
    backup_col = list(cp.keys())
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    total = sum([x[1] for x in data.items()])
    ax.set_xlim(0, total)
    left=0
    for x in data.items():
        colr = 'd'
        if col == None:
            colr = backup_col[random.randrange(1, backup_col.__len__() - 1)]
            backup_col.remove(colr)
        else:
            colr = col[x[0]]
        ax.barh([0], [x[1]], left=[left], height=0.5, align='center', color=cp[colr], label=x[0]+' ( '+str(x[1])+', '+str(round(x[1]*100/total,2))+'% ) ')
        left+=x[1]
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', fontsize='6.5', fancybox=True, shadow=True)
'''
combined figure
'''
def rich_hist(occupy_cate: list, hist_cate: list, data: dict, display: str, width = 8):
    f, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[1, 12]}, figsize=(width, 8))
    occupation_conditional(ax1,occupy_cate,data['occupy'],display)
    piecewise_hist(ax2,hist_cate,data['count'],data['sum'],display)
    return '![' + display + '的分段统计](' + sv_upload() + ')'
def occupation_bar(data: list, col: list = None):
    f, ax = plt.subplots(figsize=(8, 4))
    occupation_splitted(ax, data, col)
    plt.show()
def occupation_pie_figure(data: dict, title: str):
    f, ax = plt.subplots(figsize=(8, 8))
    folded_data = data
    pie_occupation(ax, folded_data, title)
    return '![' + title + '](' + sv_upload() + ')'
def rate_pie_figure(part: int, body: int, display: str, display_nagetive: str = None):
    f, ax = plt.subplots(figsize=(8, 4))
    pie_percent(ax, part, body, display, display_nagetive)
    if display_nagetive == None:
        display_nagetive = '未' + display
    return '![' + display + ' / ' + display_nagetive + '](' + sv_upload() + ')'
def waffle_figure(data, title = '', color = None):
    cols = []
    if type(color) == list:
        cols = [cp[x] if not '#' in x else x for x in color]
    elif type(color) == dict:
        cols = [cp[color[x]] if not '#' in color[x] else color[x] for x in data.keys()]
    plt.figure(
        FigureClass=Waffle,
        figsize=(8, 6),
        rows=30,
        columns=40,
        values=data,
        colors=cols,
        legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
    )
    plt.title(title)
    return '![' + title + '](' + sv_upload() + ')'
def trend_plot_month(data: dict, title: str):
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(1,1,1)
    top = max([x[1] for x in data.items()])
    plt.plot([x[0] for x in data.items()],[x[1] for x in data.items()],linewidth=2,color='#222333',marker='.',alpha=0.5)
    cy = ''
    for x in data.items():
        if x[0].split('-')[0] == cy:
            ax.text(x[0], -top*0.02, x[0].split('-')[1], ha='center', va= 'bottom',fontsize='5',rotation=90)
        else:
            ax.text(x[0], -top*0.05, x[0].split('-')[0], ha='center', va= 'bottom',fontsize='9')
            ax.text(x[0], -top*0.02, x[0].split('-')[1], ha='center', va= 'bottom',fontsize='5',rotation=90)
            cy = x[0].split('-')[0]
    ax.xaxis.set_visible(False)
    plt.title(title)
    return '![' + title + '](' + sv_upload() + ')'
def table_thread(rank, target: str, max: int = 50, rank_condition: str = None):
    if max > 50:
        max = 50
    if not rank_condition == None:
        rank = [x for x in rank if value_multi_conditional(x[0], rank_condition)]
    rank = rank[:max]
    rich_rank = ['排名 | tid | 标题 | 作者 | ' + target, '-|-|-|-|-']
    ra = 1
    for i in rank:
        with open(BASE_DIR + '/database/data_' + str(i[1]-i[1]%100) + '.txt', 'r') as f:
            p = json.loads(f.read())
            for t in p:
                if t['tid'] == i[1]:
                    title = t['data']['title']
                    author = t['data']['author']
                    rich_rank.append(str(ra) + ' | [' + str(i[1]) + ']( https://www.mcbbs.net/thread-' + str(i[1]) + '-1-1.html ) | ' + title.replace('|','&#124;') + ' | ' + author.replace('|','&#124;') + ' | ' + str(i[0]))
                    ra += 1
                    break
    return '\n'.join(rich_rank)
def table_counter(rank, target: str, max: int = 50, rank_condition: str = None, value_name: str = '数量'):
    rua = rank.items()
    if not rank_condition == None:
        rua = [x for x in rank.items() if value_multi_conditional(x[1], rank_condition)]
    l =  sorted(rua, key=lambda x: x[1] ,reverse=True)[:max]
    rich_rank = ['排名 | ' + value_name + ' | ' + target, '-|-|-']
    for i in range(len(l)):
        count = l[i][1]
        t = l[i][0]
        rich_rank.append(str(i + 1) + ' | ' + str(count) + ' | ' + str(t))
    return '\n'.join(rich_rank)
def most_active(stats):
    active = {}
    for x in stats['authors'].items():
        active[x[0]] = x[1] * 0.1
    for x in stats['author_jh'].items():
        if x[0] in active:
            active[x[0]] += x[1] * 0.9
    for x in stats['author_yx'].items():
        if x[0] in active:
            active[x[0]] += x[1] * 0.4
    for x in stats['author_tj'].items():
        if x[0] in active:
            active[x[0]] += x[1] * 0.4
    for x in stats['author_zd'].items():
        if x[0] in active:
            active[x[0]] += x[1] * 0.2
    for x in stats['author_yc'].items():
        if x[0] in active:
            active[x[0]] += x[1] * 0.1
    for x,y in active.items():
        active[x] = round(y, 2)
    return active
def most_valuable(stats):
    value = {}
    for x in stats['author_jh'].items():
        if not x[0] in value:
            value[x[0]] = x[1]
        else:
            value[x[0]] += x[1]
    for x in stats['author_yx'].items():
        if not x[0] in value:
            value[x[0]] = x[1] * 0.5
        else:
            value[x[0]] += x[1] * 0.5
    for x in stats['author_tj'].items():
        if not x[0] in value:
            value[x[0]] = x[1] * 0.5
        else:
            value[x[0]] += x[1] * 0.5
    for x in stats['author_zd'].items():
        if not x[0] in value:
            value[x[0]] = x[1] * 0.3
        else:
            value[x[0]] += x[1] * 0.3
    for x in stats['author_yc'].items():
        if not x[0] in value:
            value[x[0]] = x[1] * 0.2
        else:
            value[x[0]] += x[1] * 0.2
    for x,y in value.items():
        value[x] = round(y / stats['authors'][x], 2)
    return value
BASE_DIR = os.path.dirname(__file__)
# general_stat
def general():
    global hist_cates, occupy_cates
    with open(BASE_DIR + '/stats/@.txt', 'r') as f:
        stats = json.loads(f.read())
        md = ['''# 论坛总览\n\n## 概况\n\n- #### 访问有效的帖子\n\n（注：指的是游客能进入、并看到内容的帖子）\n\n''']
        md.append(rate_pie_figure(stats['valid_thread_count'], stats['thread_count'], '访问有效的帖子', '访问无效的帖子'))
        md.append('''\n\n- #### 被屏蔽的帖子\n\n（注：指的是内容被屏蔽的帖子）\n\n''')
        md.append(rate_pie_figure(stats['blocked_thread'], stats['thread_count'] - stats['valid_thread_count'], '被屏蔽的帖子', '无权访问的帖子\n(被删除或权限限制)'))
        md.append('''\n\n------------\n\n- #### 被回复的帖子\n\n''')
        md.append(rate_pie_figure(stats['replied_thread'], stats['valid_thread_count'], '被回复的帖子'))
        md.append('\n\n- #### 被评分的帖子\n\n')
        md.append(rate_pie_figure(stats['rewarded_thread'], stats['valid_thread_count'], '被评分的帖子'))
        md.append('\n\n- #### 被关闭的帖子\n\n')
        md.append(rate_pie_figure(stats['closed_thread'], stats['valid_thread_count'], '被关闭的帖子', '状态正常的帖子'))
        md.append('\n\n- #### 查看与回帖\n\n')
        md.append(rate_pie_figure(sum(x[1] for x in stats['hists']['reply']['sum'].items()), sum(x[1] for x in stats['hists']['view']['sum'].items()), '查看并回帖', '查看无回帖'))
        md.append('\n\n- #### 有图章的帖子\n\n')
        md.append(rate_pie_figure(sum(x[1] for x in stats['seals'].items()), stats['valid_thread_count'], '有图章', '无图章'))
        md.append('''\n\n**（接下来的所有统计数据来源于访问有效的帖子，造成访问无效可能原因是帖子被删除、屏蔽、高权限隐藏等）**\n\n## 分段统计\n\n- #### 查看量\n\n''')
        md.append(rich_hist(occupy_cates['view'],hist_cates['view'],stats['hists']['view'],'查看',10))
        md.append('\n\n- #### 回复量\n\n')
        md.append(rich_hist(occupy_cates['reply'],hist_cates['reply'],stats['hists']['reply'],'回复'))
        md.append('\n\n- #### 评分参与人数\n\n')
        md.append(rich_hist(occupy_cates['participation'],hist_cates['participation'],stats['hists']['participation'],'参与人数'))
        md.append('\n\n- #### 人气\n\n')
        md.append(rich_hist(occupy_cates['popularity'],hist_cates['popularity'],stats['hists']['popularity'],'人气'))
        md.append('\n\n- #### 金粒\n\n')
        md.append(rich_hist(occupy_cates['golden-nugget'],hist_cates['golden-nugget'],stats['hists']['golden-nugget'],'金粒'))
        md.append('\n\n- #### 贡献\n\n')
        md.append(rich_hist(occupy_cates['contribution'],hist_cates['contribution'],stats['hists']['contribution'],'贡献'))
        md.append('\n\n- #### 金锭\n\n')
        md.append(rich_hist(occupy_cates['golden-ingot'],hist_cates['golden-ingot'],stats['hists']['golden-ingot'],'金锭'))
        md.append('\n\n- #### 绿宝石\n\n')
        md.append(rich_hist(occupy_cates['emerald'],hist_cates['emerald'],stats['hists']['emerald'],'绿宝石'))
        md.append('\n\n- #### 下界之星\n\n')
        md.append(rich_hist(occupy_cates['nether-star'],hist_cates['nether-star'],stats['hists']['nether-star'],'下界之星'))
        md.append('\n\n- #### 爱心\n\n')
        md.append(rich_hist(occupy_cates['heart'],hist_cates['heart'],stats['hists']['heart'],'爱心'))
        md.append('\n\n- #### 积分收益\n\n')
        md.append(rich_hist(occupy_cates['profits'],hist_cates['profits'],stats['hists']['profits'],'收益'))
        md.append('\n\n- #### 好评度\n\n')
        md.append(rich_hist(occupy_cates['appraisal'],hist_cates['appraisal'],stats['hists']['appraisal'],'好评度'))
        md.append('\n\n- #### 热度\n\n')
        md.append(rich_hist(occupy_cates['heat'],hist_cates['heat'],stats['hists']['heat'],'热度'))
        md.append('\n\n- #### 图片数\n\n')
        md.append(rich_hist(occupy_cates['image-amount'],hist_cates['image-amount'],stats['hists']['image-amount'],'图片数'))
        md.append('\n\n- #### iframe数\n\n')
        md.append(rich_hist(occupy_cates['iframe-amount'],hist_cates['iframe-amount'],stats['hists']['iframe-amount'],'iframe数'))
        md.append('\n\n- #### 表格数\n\n')
        md.append(rich_hist(occupy_cates['table-amount'],hist_cates['table-amount'],stats['hists']['table-amount'],'表格数'))
        md.append('\n\n- #### 外链数\n\n')
        md.append(rich_hist(occupy_cates['redirect-amount'],hist_cates['redirect-amount'],stats['hists']['redirect-amount'],'外链数'))
        md.append('\n\n- #### 帖子被操作次数\n\n')
        md.append(rich_hist(occupy_cates['operation'],hist_cates['operation'],stats['hists']['operation'],'被操作数'))
        md.append('\n\n- #### 图章占比\n\n')
        md.append(waffle_figure(stats['seals'],'图章占比',['b','y','r+','y+','g+','#00CED1','y-','r-','g-','b-','r','g','d-']))
        md.append('\n\n----\n\n## 排名\n\n')
        md.append('- #### 查看最多的帖子\n\n')
        md.append(table_thread(stats['rank_view'],'查看数'))
        md.append('\n\n- #### 回复最多的帖子\n\n')
        md.append(table_thread(stats['rank_reply'],'回复数'))
        md.append('\n\n- #### 回帖率最高的帖子\n\n')
        md.append(table_thread(stats['rank_replyrate'],'回帖率'))
        md.append('\n\n- #### 回帖率最低的帖子\n\n')
        md.append(table_thread(stats['rank_replyrate_negative'],'回帖率升序'))
        md.append('\n\n- #### 参与评分人数最多的帖子\n\n')
        md.append(table_thread(stats['rank_participation'],'参与评分人数'))
        md.append('\n\n- #### 获得人气最多的帖子\n\n')
        md.append(table_thread(stats['rank_popularity'],'人气'))
        md.append('\n\n- #### 获得金粒最多的帖子\n\n')
        md.append(table_thread(stats['rank_golden_nugget'],'金粒'))
        md.append('\n\n- #### 获得贡献最多的帖子\n\n')
        md.append(table_thread(stats['rank_contribution'],'贡献'))
        md.append('\n\n- #### 获得金锭最多的帖子\n\n')
        md.append(table_thread(stats['rank_golden_ingot'],'金锭'))
        md.append('\n\n- #### 获得绿宝石最多的帖子\n\n')
        md.append(table_thread(stats['rank_emerald'],'绿宝石'))
        md.append('\n\n- #### 获得下界之星最多的帖子\n\n')
        md.append(table_thread(stats['rank_nether_star'],'下界之星'))
        md.append('\n\n- #### 获得爱心最多的帖子\n\n')
        md.append(table_thread(stats['rank_heart'],'爱心',2))
        md.append('\n\n- #### 积分收益最高的帖子\n\n')
        md.append(table_thread(stats['rank_profits'],'积分收益'))
        md.append('\n\n- #### 积分收益最低的帖子\n\n')
        md.append(table_thread(stats['rank_profits_negative'],'积分收益倒序'))
        md.append('\n\n- #### 好评度最高的帖子\n\n')
        md.append(table_thread(stats['rank_appraisal'],'好评度'))
        md.append('\n\n- #### 热度最高的帖子\n\n')
        md.append(table_thread(stats['rank_heat'],'热度'))
        md.append('\n\n- #### 图片最多的帖子\n\n')
        md.append(table_thread(stats['rank_image'],'图片数'))
        md.append('\n\n- #### iframe最多的帖子\n\n')
        md.append(table_thread(stats['rank_iframe'],'iframe数'))
        md.append('\n\n- #### 表格最多的帖子\n\n')
        md.append(table_thread(stats['rank_table'],'表格数'))
        md.append('\n\n- #### 外链最多的帖子\n\n')
        md.append(table_thread(stats['rank_url'],'外链数'))
        md.append('\n\n- #### 被操作最多次的帖子\n\n')
        md.append(table_thread(stats['rank_operation'],'被操作数'))
        md.append('\n\n----\n\n## 技术统计\n\n')
        md.append('\n\n- #### 标题关键词\n\n')
        md.append(table_counter(stats['title_keyword'],'标题关键词',100))
        md.append('\n\n- #### 内容关键词\n\n')
        md.append(table_counter(stats['content_keyword'],'内容关键词',100))
        md.append('\n\n- #### 评分评语\n\n')
        md.append(table_counter(stats['reasons'],'评语',100))
        md.append('\n\n- #### 有效发帖者\n\n')
        md.append(table_counter(stats['authors'],'有效发帖者',100))
        md.append('\n\n- #### 评分者\n\n')
        md.append(table_counter(stats['generous'],'评分者',100))
        md.append('\n\n- #### 精华帖作者\n\n')
        md.append(table_counter(stats['author_jh'],'精华帖作者',100))
        md.append('\n\n- #### 优秀贴作者\n\n')
        md.append(table_counter(stats['author_yx'],'优秀帖作者',100))
        md.append('\n\n- #### 置顶帖作者\n\n')
        md.append(table_counter(stats['author_zd'],'置顶帖作者',100))
        md.append('\n\n- #### 版主推荐帖作者\n\n')
        md.append(table_counter(stats['author_tj'],'版主推荐帖作者',100))
        md.append('\n\n- #### 原创帖作者\n\n')
        md.append(table_counter(stats['author_yc'],'原创帖作者',100))
        md.append('\n\n- #### 爆料贴作者\n\n')
        md.append(table_counter(stats['author_bl'],'爆料帖作者',100))
        md.append('\n\n- #### 授权搬运贴作者\n\n')
        md.append(table_counter(stats['author_by'],'授权搬运帖作者',100))
        md.append('\n\n- #### 过期贴作者\n\n')
        md.append(table_counter(stats['author_gq'],'过期帖作者',100))
        md.append('\n\n- #### 关闭贴作者\n\n')
        md.append(table_counter(stats['author_gb'],'关闭帖作者',100))
        md.append('\n\n- #### 发帖小组\n\n')
        md.append(table_counter(stats['group'],'发帖来自小组',20))
        md.append('\n\n----\n\n- ## 逼榜 / 2bindex\n\n- ### 最活跃发帖者\n\n```\n逼值 = 精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2 + 其他发帖数 * 0.1\n```\n\n')
        md.append(table_counter(most_active(stats),'用户',rank_condition='>0',value_name='逼值'))
        md.append('\n\n- ### 最有价值发帖者\n\n```\n逼度 = (精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2) / 总发帖量\n```\n\n')
        md.append(table_counter(most_valuable(stats),'用户',rank_condition='>0',value_name='逼度'))
        with open(BASE_DIR + '/mds/@.md', 'w+', encoding='utf-8') as _f:
            _f.write(''.join(md))
        print('@', 'done.')
# category
def category():
    global hist_cates, occupy_cates, new_img_dir
    category_stats = {
        'valid_thread_count' : {},
        'replied_thread' : {},
        'rewarded_thread' : {},
        'closed_thread' : {},
        'seals' : {},
    }
    for s in os.listdir(BASE_DIR + '/stats'):
        if not re.findall('(^[^\d-]+).txt', s) == [] and not '@' in s:
            cate = re.findall('(^[^\d-]+).txt', s)[0]
            with open(os.path.join(BASE_DIR + '/stats', s), 'r', encoding='utf-8') as f:
                stats = json.loads(f.read())
                # category_stats
                category_stats['valid_thread_count'][cate] = stats['valid_thread_count']
                category_stats['replied_thread'][cate] = stats['replied_thread']
                category_stats['rewarded_thread'][cate] = stats['rewarded_thread']
                category_stats['closed_thread'][cate] = stats['closed_thread']
                if stats['seals'].__len__() > 0:
                    for i in stats['seals'].items():
                        if not i[0] in category_stats['seals']:
                            category_stats['seals'][i[0]] = {}
                        category_stats['seals'][i[0]][cate] = i[1]
                for k,c in hist_cates.items():
                    if not k in category_stats:
                        category_stats[k] = {}
                    category_stats[k][cate] = sum([x[1] for x in stats['hists'][k]['sum'].items()])
                # private stats
                new_img_dir(cate)
                md = ['''# 总览\n\n## 概况\n\n''']
                md.append('''\n\n- #### 被回复的帖子\n\n''')
                md.append(rate_pie_figure(stats['replied_thread'], stats['valid_thread_count'], '被回复的帖子'))
                md.append('\n\n- #### 被评分的帖子\n\n')
                md.append(rate_pie_figure(stats['rewarded_thread'], stats['valid_thread_count'], '被评分的帖子'))
                md.append('\n\n- #### 被关闭的帖子\n\n')
                md.append(rate_pie_figure(stats['closed_thread'], stats['valid_thread_count'], '被关闭的帖子', '状态正常的帖子'))
                md.append('\n\n- #### 查看与回帖\n\n')
                md.append(rate_pie_figure(sum(x[1] for x in stats['hists']['reply']['sum'].items()), sum(x[1] for x in stats['hists']['view']['sum'].items()), '查看并回帖', '查看无回帖'))
                md.append('\n\n- #### 有图章的帖子\n\n')
                md.append(rate_pie_figure(sum(x[1] for x in stats['seals'].items()), stats['valid_thread_count'], '有图章', '无图章'))
                md.append('''\n\n**（接下来的所有统计数据来源于访问有效的帖子，造成访问无效可能原因是帖子被删除、屏蔽、高权限隐藏等）**\n\n## 分段统计\n\n- #### 查看量\n\n''')
                md.append(rich_hist(occupy_cates['view'],hist_cates['view'],stats['hists']['view'],'查看',10))
                md.append('\n\n- #### 回复量\n\n')
                md.append(rich_hist(occupy_cates['reply'],hist_cates['reply'],stats['hists']['reply'],'回复'))
                md.append('\n\n- #### 评分参与人数\n\n')
                md.append(rich_hist(occupy_cates['participation'],hist_cates['participation'],stats['hists']['participation'],'参与人数'))
                md.append('\n\n- #### 人气\n\n')
                md.append(rich_hist(occupy_cates['popularity'],hist_cates['popularity'],stats['hists']['popularity'],'人气'))
                md.append('\n\n- #### 金粒\n\n')
                md.append(rich_hist(occupy_cates['golden-nugget'],hist_cates['golden-nugget'],stats['hists']['golden-nugget'],'金粒'))
                md.append('\n\n- #### 贡献\n\n')
                md.append(rich_hist(occupy_cates['contribution'],hist_cates['contribution'],stats['hists']['contribution'],'贡献'))
                md.append('\n\n- #### 金锭\n\n')
                md.append(rich_hist(occupy_cates['golden-ingot'],hist_cates['golden-ingot'],stats['hists']['golden-ingot'],'金锭'))
                md.append('\n\n- #### 绿宝石\n\n')
                md.append(rich_hist(occupy_cates['emerald'],hist_cates['emerald'],stats['hists']['emerald'],'绿宝石'))
                md.append('\n\n- #### 下界之星\n\n')
                md.append(rich_hist(occupy_cates['nether-star'],hist_cates['nether-star'],stats['hists']['nether-star'],'下界之星'))
                md.append('\n\n- #### 爱心\n\n')
                md.append(rich_hist(occupy_cates['heart'],hist_cates['heart'],stats['hists']['heart'],'爱心'))
                md.append('\n\n- #### 积分收益\n\n')
                md.append(rich_hist(occupy_cates['profits'],hist_cates['profits'],stats['hists']['profits'],'收益'))
                md.append('\n\n- #### 好评度\n\n')
                md.append(rich_hist(occupy_cates['appraisal'],hist_cates['appraisal'],stats['hists']['appraisal'],'好评度'))
                md.append('\n\n- #### 热度\n\n')
                md.append(rich_hist(occupy_cates['heat'],hist_cates['heat'],stats['hists']['heat'],'热度'))
                md.append('\n\n- #### 图片数\n\n')
                md.append(rich_hist(occupy_cates['image-amount'],hist_cates['image-amount'],stats['hists']['image-amount'],'图片数'))
                md.append('\n\n- #### iframe数\n\n')
                md.append(rich_hist(occupy_cates['iframe-amount'],hist_cates['iframe-amount'],stats['hists']['iframe-amount'],'iframe数'))
                md.append('\n\n- #### 表格数\n\n')
                md.append(rich_hist(occupy_cates['table-amount'],hist_cates['table-amount'],stats['hists']['table-amount'],'表格数'))
                md.append('\n\n- #### 外链数\n\n')
                md.append(rich_hist(occupy_cates['redirect-amount'],hist_cates['redirect-amount'],stats['hists']['redirect-amount'],'外链数'))
                md.append('\n\n- #### 帖子被操作次数\n\n')
                md.append(rich_hist(occupy_cates['operation'],hist_cates['operation'],stats['hists']['operation'],'被操作数'))
                if stats['seals'].__len__() > 0:
                    md.append('\n\n- #### 图章占比\n\n')
                    global seal_color
                    md.append(waffle_figure(stats['seals'],'图章占比',seal_color))
                md.append('\n\n----\n\n## 排名\n\n')
                md.append('- #### 查看最多的帖子\n\n')
                md.append(table_thread(stats['rank_view'],'查看数',rank_condition='>0'))
                md.append('\n\n- #### 回复最多的帖子\n\n')
                md.append(table_thread(stats['rank_reply'],'回复数',rank_condition='>0'))
                md.append('\n\n- #### 回帖率最高的帖子\n\n')
                md.append(table_thread(stats['rank_replyrate'],'回帖率',rank_condition='>0'))
                md.append('\n\n- #### 回帖率最低的帖子\n\n')
                md.append(table_thread(stats['rank_replyrate_negative'],'回帖率升序',rank_condition='>0'))
                md.append('\n\n- #### 参与评分人数最多的帖子\n\n')
                md.append(table_thread(stats['rank_participation'],'参与评分人数',rank_condition='>0'))
                md.append('\n\n- #### 获得人气最多的帖子\n\n')
                md.append(table_thread(stats['rank_popularity'],'人气',rank_condition='>0'))
                md.append('\n\n- #### 获得金粒最多的帖子\n\n')
                md.append(table_thread(stats['rank_golden_nugget'],'金粒',rank_condition='>0'))
                md.append('\n\n- #### 获得贡献最多的帖子\n\n')
                md.append(table_thread(stats['rank_contribution'],'贡献',rank_condition='>0'))
                md.append('\n\n- #### 获得金锭最多的帖子\n\n')
                md.append(table_thread(stats['rank_golden_ingot'],'金锭',rank_condition='>0'))
                md.append('\n\n- #### 获得绿宝石最多的帖子\n\n')
                md.append(table_thread(stats['rank_emerald'],'绿宝石',rank_condition='>0'))
                md.append('\n\n- #### 获得下界之星最多的帖子\n\n')
                md.append(table_thread(stats['rank_nether_star'],'下界之星',rank_condition='>0'))
                md.append('\n\n- #### 获得爱心最多的帖子\n\n')
                md.append(table_thread(stats['rank_heart'],'爱心',2,rank_condition='>0'))
                md.append('\n\n- #### 积分收益最高的帖子\n\n')
                md.append(table_thread(stats['rank_profits'],'积分收益',rank_condition='>0'))
                md.append('\n\n- #### 积分收益最低的帖子\n\n')
                md.append(table_thread(stats['rank_profits_negative'],'积分收益倒序',rank_condition='>0'))
                md.append('\n\n- #### 好评度最高的帖子\n\n')
                md.append(table_thread(stats['rank_appraisal'],'好评度',rank_condition='>0'))
                md.append('\n\n- #### 热度最高的帖子\n\n')
                md.append(table_thread(stats['rank_heat'],'热度',rank_condition='>0'))
                md.append('\n\n- #### 图片最多的帖子\n\n')
                md.append(table_thread(stats['rank_image'],'图片数',rank_condition='>0'))
                md.append('\n\n- #### iframe最多的帖子\n\n')
                md.append(table_thread(stats['rank_iframe'],'iframe数',rank_condition='>0'))
                md.append('\n\n- #### 表格最多的帖子\n\n')
                md.append(table_thread(stats['rank_table'],'表格数',rank_condition='>0'))
                md.append('\n\n- #### 外链最多的帖子\n\n')
                md.append(table_thread(stats['rank_url'],'外链数',rank_condition='>0'))
                md.append('\n\n- #### 被操作最多次的帖子\n\n')
                md.append(table_thread(stats['rank_operation'],'被操作数',rank_condition='>0'))
                md.append('\n\n----\n\n## 技术统计\n\n')
                md.append('\n\n- #### 标题关键词\n\n')
                md.append(table_counter(stats['title_keyword'],'标题关键词',100,rank_condition='>0'))
                md.append('\n\n- #### 内容关键词\n\n')
                md.append(table_counter(stats['content_keyword'],'内容关键词',100,rank_condition='>0'))
                md.append('\n\n- #### 评分评语\n\n')
                md.append(table_counter(stats['reasons'],'评语',100,rank_condition='>0'))
                md.append('\n\n- #### 有效发帖者\n\n')
                md.append(table_counter(stats['authors'],'有效发帖者',100,rank_condition='>0'))
                md.append('\n\n- #### 评分者\n\n')
                md.append(table_counter(stats['generous'],'评分者',100,rank_condition='>0'))
                md.append('\n\n- #### 精华帖作者\n\n')
                md.append(table_counter(stats['author_jh'],'精华帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 优秀贴作者\n\n')
                md.append(table_counter(stats['author_yx'],'优秀帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 置顶帖作者\n\n')
                md.append(table_counter(stats['author_zd'],'置顶帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 版主推荐帖作者\n\n')
                md.append(table_counter(stats['author_tj'],'版主推荐帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 原创帖作者\n\n')
                md.append(table_counter(stats['author_yc'],'原创帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 爆料贴作者\n\n')
                md.append(table_counter(stats['author_bl'],'爆料帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 授权搬运贴作者\n\n')
                md.append(table_counter(stats['author_by'],'授权搬运帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 过期贴作者\n\n')
                md.append(table_counter(stats['author_gq'],'过期帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 关闭贴作者\n\n')
                md.append(table_counter(stats['author_gb'],'关闭帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 发帖小组\n\n')
                md.append(table_counter(stats['group'],'发帖来自小组',20,rank_condition='>0'))
                md.append('\n\n----\n\n- ## 逼榜 / 2bindex\n\n- ### 最活跃发帖者\n\n```\n逼值 = 精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2 + 其他发帖数 * 0.1\n```\n\n')
                md.append(table_counter(most_active(stats),'用户',rank_condition='>0',value_name='逼值'))
                md.append('\n\n- ### 最有价值发帖者\n\n```\n逼度 = (精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2) / 总发帖量\n```\n\n')
                md.append(table_counter(most_valuable(stats),'用户',rank_condition='>0',value_name='逼度'))
                with open(BASE_DIR + '/mds/' + cate + '.md', 'w+', encoding='utf-8') as _f:
                    _f.write(''.join(md))
                print(cate, 'done.')
    print(category_stats)
def category_general(category_stats: dict = None):
    if category_stats == None:
        new_img_dir('category')
        category_stats = {'valid_thread_count': {'CubeWorld(魔方世界)': 242, 'Hytale[封测中]': 27, 'MCBBS创意馆（比赛结束）': 583, 'MCBBS擂台': 1002, 'Mod发布': 10946, 'Mod教程': 1286, 'Mod讨论': 2171, 'Mod问答': 57303, 'Nukkit服务端专区': 391, 'PocketMine服务端专区': 297, '公告和反馈': 14416, '匠人酒馆': 3614, '原版问答': 50342, '周边创作': 11116, '周边问答': 6605, '基岩版作品发布': 1934, '基岩版多人联机': 282, '基岩版技巧教程': 942, '基岩版软件资源': 770, '基岩版问答': 2, '展示&共享': 42247,'我的世界：地球[逐步公测]': 23, '我的世界：故事模式': 648, '搬运&鉴赏': 3619, '整合包发布': 5739, '新闻资讯': 3719, '服务器': 4833, '服务端插件': 8676, '服务端整合包': 1738, '材质资源': 2604, '游戏技巧': 12333, '皮肤分享': 12752, '矿工茶馆': 183469, '综合游戏讨论区': 4838, '编程开发': 5346, '翻译&Wiki': 1121, '联机教程': 2640, '联机问答': 112135, '视频实况': 36551, '软件资源': 2092}, 'replied_thread': {'CubeWorld(魔方世界)': 227, 'Hytale[封测中]': 21, 'MCBBS创意馆（比赛结束）': 582, 'MCBBS擂台': 988, 'Mod发布': 10800, 'Mod教程': 1253, 'Mod讨论': 2095, 'Mod问答': 52964, 'Nukkit服务端专区': 359, 'PocketMine服务端专区': 291, '公告和反馈': 13227, '匠人酒馆': 3527, '原版问答': 49218, '周边创作': 10288, '周边问答': 6490, '基岩版作品发布': 1912, '基岩版多人联机': 241, '基岩版技巧教程': 921, '基岩版软件资源': 748, '基岩版问答': 2, '展示&共享': 41770, '我的世界：地球[逐步公测]': 21, '我的世界：故事模式': 533, '搬运&鉴赏': 3510, '整合包发布':5631, '新闻资讯': 3693, '服务器': 1771, '服务端插件': 8479, '服务端整合包': 1680, '材质资源': 2584, '游戏技巧': 12158, '皮肤分享': 12596, '矿工茶馆': 176994, '综合游戏讨论区': 4433, '编程开发': 4639, '翻译&Wiki': 1023, '联机教程': 2070,'联机问答': 105805, '视频实况': 23435, '软件资源': 2043}, 'rewarded_thread': {'CubeWorld(魔方世界)': 46, 'Hytale[封测中]': 7, 'MCBBS创意馆（比赛结束）': 579, 'MCBBS擂台': 813, 'Mod发布': 9295, 'Mod教程': 926, 'Mod讨论': 730, 'Mod问答': 2889, 'Nukkit服务端专区': 250, 'PocketMine服务端专区': 204, '公告和反馈': 6542, '匠人酒馆': 2914, '原版问答': 4015, '周边创作': 8179, '周边问答': 737, '基岩版作品发布': 1569, '基岩版多人联机': 87, '基岩版技巧教程': 528, '基岩版软件资源':549, '基岩版问答': 0, '展示&共享': 36316, '我的世界：地球[逐步公测]': 14, '我的世界：故事模式': 121, '搬运&鉴赏': 3343, '整合包发布': 4750, '新闻资讯': 3234, '服务器': 2424, '服务端插件': 7020, '服务端整合包': 1400, '材质资源': 1998, '游戏技巧': 7394, '皮肤分享': 7936, '矿工茶馆': 41712, '综合游戏讨论区': 1177, '编程开发': 1072, '翻译&Wiki': 952, '联机教程': 1050, '联机问答': 3821, '视频实况': 7839, '软件资源': 1600}, 'closed_thread': {'CubeWorld(魔方世界)': 240, 'Hytale[封测中]': 1, 'MCBBS创意馆（比赛结束）': 13, 'MCBBS擂台': 93, 'Mod发布': 766, 'Mod教程': 50, 'Mod讨论': 120, 'Mod问答': 1734, 'Nukkit服务端专区': 36, 'PocketMine服务端专区': 9, '公告和反馈': 12668, '匠人酒馆': 65, '原版问答': 1619, '周边创作': 592, '周边问答': 211, '基岩版作品发布': 381, '基岩版多人联机': 99, '基岩版技巧教程': 28, '基岩版软件资源': 141, '基岩版问答': 0, '展示&共享': 1389, '我的世界：地球[逐步公测]': 8, '我的世界：故事模式': 1, '搬运&鉴赏': 367, '整合包发布': 58, '新闻资讯': 1473, '服务器': 2771, '服务端插件': 448, '服务端整合包': 310, '材质资源': 998, '游戏技巧': 2098, '皮肤分享': 145, '矿工茶馆': 14894, '综合游戏讨论区': 463, '编程开发': 88, '翻译&Wiki': 65, '联机教程': 355, '联机问答': 4039, '视频实况': 212, '软件资源': 448}, 'seals': {'精华': {'CubeWorld(魔方世界)': 1, 'MCBBS创意馆（比赛结束）': 1, 'MCBBS擂台': 50, 'Mod发布': 77, 'Mod教程': 28, 'Mod讨论': 3, 'Nukkit服务端专区': 1, 'PocketMine服务端专区': 1, '匠人酒馆': 2, '周边创作': 84, '基岩版作品发布': 44, '基岩版技巧教程': 10, '基岩版软件资源': 9, '展示&共享': 410, '搬运&鉴赏': 4, '整合包发布': 5, '新闻资讯': 1, '服务端插件': 37, '服务端整合包': 1, '材质资源': 41, '游戏技巧': 66, '皮肤分享': 174, '矿工茶馆': 4, '综合游戏讨论区': 4, '编程开发': 17, '翻译&Wiki': 46, '联机教程': 19, '视频实况': 24, '软件资源': 30}, '置顶': {'CubeWorld(魔方世界)': 2, 'Hytale[封测中]': 1, 'MCBBS创意馆（比赛结束）': 31, 'MCBBS擂台': 32, 'Mod发布': 40, 'Mod讨论': 12, 'Nukkit服务端专区': 8, 'PocketMine服务端专区': 4, '公告和反馈': 41, '匠人酒馆': 15, '原版问答': 25, '周边创作': 62, '基岩版作品发布': 3, '基岩版多人联机': 6, '基岩版技巧教程': 12, '基岩版软件资源': 17, '展示&共享': 227, '我的世界：地球[逐步公测]': 1, '我的世界：故事模式': 2, '搬运&鉴赏': 13, '整合包发布': 13, '新闻资讯': 424, '服务器': 15, '服务端插件': 35, '服务端整合包': 20, '材质资源': 19, '游戏技巧': 15, '皮肤分享': 5, '矿工茶馆': 71, '综合游戏讨论区': 26, '编程开发': 5, '翻译&Wiki': 27, '联机教程': 28, '视频实况': 18, '软件资源': 54}, '原创': {'MCBBS创意馆（比赛结束）': 307, 'Mod发布': 29, 'Mod讨论': 2, 'Nukkit服务端专区': 40, 'PocketMine服务端专区': 31, '匠人酒馆': 16, '周边创作': 60, '基岩版作品发布': 80, '基岩版技巧教程': 16, '基岩版软件资源': 4, '展示&共享': 308, '新闻资讯': 5, '服务器': 1, '服务端插件': 626, '服务端整合包': 8, '材质资源': 16, '游戏技巧': 30, '皮肤分享': 6, '矿工茶馆': 12, '综合游戏讨论区': 17, '视频实况': 54, '软件资源': 6}, '优秀': {'MCBBS创意馆（比赛结束）': 27, 'MCBBS擂台': 3, 'Mod发布': 59, 'Mod教程': 38, 'Mod讨论': 9, 'Nukkit服务端专区': 5, 'PocketMine服务端专区': 15, '匠人酒馆': 6, '周边创作': 124, '基岩版作品发布': 87, '基岩版多人联机': 7, '基岩版技巧教程': 13, '基岩版软件资源': 14, '展示&共享': 268, '搬运&鉴赏': 6, '整合包发布': 107, '新闻资讯': 13, '服务端插件': 145, '服务端整合包': 17, '材质资源': 45, '游戏技巧': 110, '皮肤分享': 175, '矿工茶馆': 12, '综合游戏讨论区': 24, '编程开发': 28, '翻译&Wiki': 23, '联机教程': 27, '视频实况': 65, '软件资源': 21}, '授权搬运': {'MCBBS创意馆（比赛结束）': 2, 'Mod发布': 464, 'Mod教程': 2, 'Nukkit服务端专区': 7, 'PocketMine服务端专区':2, '公告和反馈': 8, '周边创作': 1, '基岩版多人联机': 8, '基岩版技巧教程': 1, '基岩版软件资源': 18, '搬运&鉴赏': 435, '整合包发布': 5, '新闻资讯': 156, '服务端插件': 584, '服务端整合包': 1, '材质资源': 38, '游戏技巧': 3, '皮肤分享': 3, '矿工茶馆': 1, '综合游戏讨论区': 8, '视频实况': 2, '软件资源': 369}, '过期': {'MCBBS创意馆（比赛结束）': 1, 'Mod发布': 10, 'Mod教程': 17, 'Mod讨论': 8, 'Nukkit服务端专区': 1, 'PocketMine服务端专区': 2, '公告和反馈': 13, '原版问答': 1, '基岩版作品发布': 2, '基岩版技巧教程': 1, '基岩版软件资源': 195, '展示&共享': 5, '搬运&鉴赏': 5, '整合包发布': 4, '新闻资讯': 687, '服务端插件': 8, '服务端整合包': 1, '材质资源': 4, '游戏技巧': 59, '矿工茶馆': 19, '综合游戏讨论区': 161, '编程开发': 30, '翻译&Wiki': 3, '联机教程': 2, '视频实况': 4, '软件资源': 6}, '版主推荐': {'MCBBS擂台': 3, 'Mod发布': 9, 'Mod教程': 14, 'Mod讨论': 10, 'Nukkit服务端专区': 1, '公告和反馈': 1, '匠人酒馆': 16, '周边创作': 19, '基岩版作品发布': 3, '基岩版软件资源': 2, '展示&共享': 148, '搬运&鉴赏': 3, '整合包发布': 17, '新闻资讯': 22, '材质资源': 5, '游戏技巧': 30, '皮肤分享': 4, '矿工茶馆': 22, '综合游戏讨论区': 20, '翻译&Wiki': 1, '联机教程': 6, '视频实况': 13, '软件资源': 1}, '美图': {'Mod发布': 1, 'Mod讨论': 2, '匠人酒馆': 3, '周边创作': 17, '展示&共享': 59, '搬运&鉴赏': 1, '整合包发布': 1, '新闻资讯': 1, '服务端整合包': 1, '材质资源': 1, '游戏技巧': 9, '皮肤分享': 1, '矿工茶馆': 3, '翻译&Wiki': 2}, '爆料': {'Mod发布': 2, 'Mod讨论': 13, '公告和反馈': 1, '周边创作': 3, '展示&共享': 5, '我的世界：故事模式': 1, '新闻资讯': 17, '服务器': 1, '游戏技巧': 6, '矿工茶馆': 15, '综合游戏讨论区': 1, '联机教程': 3, '视频实况': 1, '软件资源': 2}, '推荐': {'Mod发布': 4, 'Mod教程': 13, 'Mod讨论': 18, 'PocketMine服务端专区': 2, '公告和反馈': 2, '匠人酒馆': 8, '周边创作': 44, '基岩版作品发布': 8, '基岩版技巧教程': 10, '基岩版软件资源': 1, '展示&共享': 285, '搬运&鉴赏': 8, '整合包发布':21, '新闻资讯': 6, '服务端插件': 1, '材质资源': 21, '游戏技巧': 28, '皮肤分享': 1, '矿工茶馆': 14, '综合游戏讨论区': 6, '编程开发': 1, '翻译&Wiki': 1, '联机教程': 8, '视频实况': 9, '软件资源': 10}, '热帖': {'Mod发布': 1, '匠人酒馆': 1, '周边创作': 2, '基岩版技巧教程': 1, '展示&共享': 3, '材质资源': 1, '游戏技巧': 5, '矿工茶馆': 15}, '公益': {'Mod教程': 2, 'Mod讨论': 2, '展示&共享': 1, '新闻资讯': 1, '服务器': 239}, '版主回复': {'匠人酒馆': 3, '展示&共享': 128}}, 'view': {'CubeWorld(魔方世界)': 479769, 'Hytale[封测中]': 9893, 'MCBBS创意馆（比赛结束）': 3680031, 'MCBBS擂台': 4440370, 'Mod发布': 337201486, 'Mod教程': 20161496, 'Mod讨论': 10534307, 'Mod问答': 84570226, 'Nukkit服务端专区': 933106, 'PocketMine服务端专区': 2307826, '公告和反馈': 27566431, '匠人酒馆': 12181356, '原版问答': 83769018, '周边创作': 20290938, '周边问答': 6212292, '基岩版作品发布': 12542914, '基岩版多人联机': 1863785, '基岩版技巧教程': 5507312, '基岩版软件资源': 9867421, '基岩版问答': 696, '展示&共享': 223097768, '我的世界：地球[逐步公测]': 45368, '我的世界：故事模式': 1191707, '搬运&鉴赏': 29260428, '整合包发布': 142921502, '新闻资讯': 25096414, '服务器': 16452155, '服务端插件': 117247640, '服务端整合包': 32993922, '材质资源': 68650298, '游戏技巧': 73637414, '皮肤分享': 88082985, '矿工茶馆': 166484065, '综合游戏讨论区': 14178546, '编程开发': 10112874, '翻译&Wiki': 6381128, '联机教程': 20702274, '联机问答': 93400610, '视频实况': 37871106, '软件资源': 94857732}, 'reply': {'CubeWorld(魔方世界)': 2294, 'Hytale[封测中]': 151, 'MCBBS创意馆（比赛结束）': 8205, 'MCBBS擂台': 22612, 'Mod发布': 577244, 'Mod教程': 36701, 'Mod讨论': 35297, 'Mod问答': 245343, 'Nukkit服务端专区': 3310, 'PocketMine服务端专区': 11635, '公告和反馈': 179497, '匠人酒馆': 73323, '原版问答': 331350, '周边创作': 125655, '周边问答': 35179, '基岩版作品发布': 181741, '基岩版多人联机': 5014, '基岩版技巧教程': 14574, '基岩版软件资源':45091, '基岩版问答': 13, '展示&共享': 1544251, '我的世界：地球[逐步公测]': 315, '我的世界：故事模式': 5091, '搬运&鉴赏': 112220, '整合包发布': 555038, '新闻资讯': 94386, '服务器': 31686, '服务端插件': 555058, '服务端整合包': 254276, '材质资源': 974359, '游戏技巧': 260337, '皮肤分享': 1178602, '矿工茶馆': 2746593, '综合游戏讨论区': 48070, '编程开发': 51039, '翻译&Wiki': 17236, '联机教程': 79007, '联机问答': 525757, '视频实况': 139519, '软件资源': 378278}, 'participation': {'CubeWorld(魔方世界)': 114, 'Hytale[封测中]': 14, 'MCBBS创意馆（比赛结束）': 2694, 'MCBBS擂台': 3934, 'Mod发布': 119791, 'Mod教程': 6909, 'Mod讨论': 2503, 'Mod问答': 3232, 'Nukkit服务端专区': 695, 'PocketMine服务端专区': 497, '公告和反馈': 24901, '匠人酒馆': 11281, '原版问答': 5750, '周边创作': 32938, '周边问答': 866, '基岩版作品发布': 4801, '基岩版多人联机': 312, '基岩版技巧教程': 1379, '基岩版软件资源': 1793, '基岩版问答': 0, '展示&共享': 156852, '我的世界：地球[逐步公测]': 55, '我的世界：故事模式': 306, '搬运&鉴赏': 16010, '整合包发布': 90555, '新闻资讯': 18150, '服务器': 11440, '服务端插件': 66672, '服务端整合包': 22043, '材质资源': 27530, '游戏技巧': 34913, '皮肤分享': 38242, '矿工茶馆': 125628, '综合游戏讨论区': 3246, '编程开发': 5521, '翻译&Wiki': 5086, '联机教程': 8162, '联机问答': 4210, '视频实况': 18288, '软件资源': 20099}, 'popularity': {'CubeWorld(魔方世界)': 138, 'Hytale[封测中]': 20, 'MCBBS创意馆（比赛结束）': 6028, 'MCBBS擂台': 6711, 'Mod发布': 107331, 'Mod教程': 7846, 'Mod讨论': 3365, 'Mod问答': 129, 'Nukkit服务端专区': 1012, 'PocketMine服务端专区': 665, '公告和反馈': 28797, '匠人酒馆': 14921, '原版问答': 1969, '周边创作': 58219, '周边问答': 132, '基岩版作品发布': 6675, '基岩版多人联机': 380, '基岩版技巧教程': 1823, '基岩版软件资源': 2276, '基岩版问答': 0, '展示&共享': 199867, '我的世界：地球[逐步公测]': 136, '我的世界：故事模式': 299, '搬运&鉴赏': 20410, '整合包发布': 69973, '新闻资讯': 22053, '服务器': 10560, '服务端插件': 65826, '服务端整合包': 16887, '材质资源': 28050, '游戏技巧': 39843, '皮肤分享': 50594, '矿工茶馆': 153403, '综合游戏讨论���': 3766, '编程开发': 6729, '翻译&Wiki': 9262, '联机教程': 8463, '联机问答': 429, '视频实况': 23030, '软件资源': 20770}, 'golden-nugget': {'CubeWorld(魔方世界)': 867, 'Hytale[封测中]': 130, 'MCBBS创意馆（比赛结束）': 141472, 'MCBBS擂台': 71504, 'Mod发布': 643998, 'Mod教程': 62569, 'Mod讨论': 24128,'Mod问答': -9494, 'Nukkit服务端专区': 6830, 'PocketMine服务端专区': 5775, '公告和反馈': 135337, '匠人酒馆': 113121, '原版问答': 3194, '周边创作': 477759, '周边问答': -301, '基岩版作品发布': 59617, '基岩版多人联机': 3240, '基岩版技巧教程': 15760, '基岩版软件资源': 17894, '基岩版问答': 0, '展示&共享': 1404003, '我的世界：地球[逐步公测]': 662, '我的世界：故事模式': 1562, '搬运&鉴赏': 148759, '整合包发布': 390670, '新闻资讯': 118250, '服务器': 86074, '服务端插件': 413944, '服务端整合包': 102274, '材质资源': 168238, '游戏技巧': 266175, '皮肤分享': 359768, '矿工茶馆': 674127, '综合游戏讨论区': 27457, '编程开发': 46624, '翻译&Wiki': 56648, '联机教程': 55527, '联机问答': -5353, '视频实况': 177305, '软件资源':133107}, 'contribution': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 126, 'MCBBS擂台': 664, 'Mod发布': 476, 'Mod教程': 146, 'Mod讨论': 35, 'Mod问答': -75, 'Nukkit服务端专区': 15, 'PocketMine服务端专区': 17, '公告和反馈': 309, '匠人酒馆': 39, '原版问答': -155, '周边创作': 545, '周边问答': -20, '基岩版作品发布': 120, '基岩版多人联机': 22, '基岩版技巧教程': 87, '基岩版软件资源': 48, '基岩版问答': 0, '展示&共享': 2518, '我的世界：地球[逐步公测]': 5, '我的世界：故事模式': 1, '搬运&鉴赏': 71, '整合包发布': 196, '新闻资讯': 123, '服务器': 50, '服务端插件': 236, '服务端整合包': 30, '材质资源': 390, '游戏技巧': 520, '皮肤分享': 706, '矿工茶馆': 32957, '综合游戏讨论区': 45, '编程开发': 119, '翻译&Wiki': 301, '联机教程': 115, '联机问答': -347, '视频实况': 188, '软件资源': 286}, 'golden-ingot': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 0, 'MCBBS擂台': 0, 'Mod发布': 132, 'Mod教程': 21, 'Mod讨论': 4, 'Mod问答': -1, 'Nukkit服务端专区': 0, 'PocketMine服务端专区': 0, '公告和反馈': 140, '匠人酒馆': 13, '原版问答': -1, '周边创作': 96, '周边问答': 0, '基岩版作品发布': 5, '基岩版多人联机': 0, '基岩版技巧教程': 1, '基岩版软件资源': 0, '基岩版问答': 0, '展示&共享': 167, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 0, '搬运&鉴赏': 4, '整合包发布': 127, '新闻资讯': 19, '服务器': 0, '服务端插件': 11, '服务端整合包': 3, '材质资源': 62, '游戏技巧': 60, '皮肤分享': 113, '矿工茶馆': 510, '综合游戏讨论区': 0, '编程开发': 0, '翻译&Wiki': 19, '联机教程': 8, '联机问答': 2, '视频实况': 27, '软件资源': 11}, 'emerald': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 0, 'MCBBS擂台': 63, 'Mod发布': 0, 'Mod教程': 24, 'Mod讨论': 0, 'Mod问答': 0, 'Nukkit服务端专区': 0, 'PocketMine服务端专区': 0, '公告和反馈': 16, '匠人酒馆': 0, '原版问答': 0, '周边创作': 0, '周边问答': 0, '基岩版作品发布': 0, '基岩版多人联机': 0, '基岩版技巧教程': 0, '基岩版软件资源': 0, '基岩版问答': 0, '展示&共享': 0, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 0, '搬运&鉴赏': 0, '整合包发布': 0, '新闻资讯': 20, '服务器': 304, '服务端插件': 2353, '服务端整合包':-78, '材质资源': 0, '游戏技巧': 419, '皮肤分享': 0, '矿工茶馆': 0, '综合游戏讨论区': 0, '编程开发': 0, '翻译&Wiki': 1519, '联机教程': 411, '联机问答': 0, '视频实况': 0, '软件资源': 0}, 'nether-star': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 732, 'MCBBS擂台': 23, 'Mod发布': 0, 'Mod教程': 0, 'Mod讨论': 43, 'Mod问答': 0, 'Nukkit服务端专区': 0, 'PocketMine服务端专区': 0, '公告和反馈': 0, '匠人酒馆': 13, '原版问答': 0, '周边创作': 204, '周边问答': 0, '基岩版作品发布': 0, '基岩版多人联机': 0, '基岩版技巧教程': 0, '基岩版软件资源': 0, '基岩版问答': 0, '展示&共享': 114, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 0, '搬运&鉴赏': 0, '整合包发布': 0, '新闻资讯': 0, '服务器': 0, '服务端插件': 12, '服务端整合包': 9, '材质资源': 1, '游戏技巧': 6, '皮肤分享': 40, '矿工茶馆': 321, '综合游戏讨论区': 0, '编程开发': 0, '翻译&Wiki': 7, '联机教程': 0, '联机问答': 0, '视频实况': 3, '软件资源': 0}, 'heart': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 0, 'MCBBS擂台': 0, 'Mod发布': 0, 'Mod教程': 0, 'Mod讨论': 0, 'Mod问答': 0, 'Nukkit服务端专区': 0, 'PocketMine服务端专区': 0, '公告和反馈': 5, '匠人酒馆': 0, '原版问答': -1, '周边创作': 0, '周边问答': 0, '基岩版作品发布': 0, '基岩版多人联机': 0, '基岩版技巧教程': 0, '基岩版软件资源': 0, '基岩版问答': 0, '展示&共享': 1, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 0, '搬运&鉴赏': 0, '整合包发布': 0, '新闻资讯': 0, '服务器': 0, '服务端插件': 0, '服务端整合包': 0, '材质资源': 0, '游戏技巧': 0, '皮肤分享': 0, '矿工茶馆': 0, '综合游戏讨论区': 0, '编程开发': 0, '翻译&Wiki': 0, '联机教程': 0, '联机问答': -1, '视频实况': 0, '软件资源': 0}, 'profits': {'CubeWorld(魔方世界)': 459, 'Hytale[封测中]': 60, 'MCBBS创意馆（比赛结束）': 19389, 'MCBBS擂台': 29023, 'Mod发布': 330824, 'Mod教程': 26258, 'Mod讨论': 10580, 'Mod问答': -363, 'Nukkit服务端专区': 3231, 'PocketMine服务端专区': 2210, '公告和反馈': 89501, '匠人酒馆': 45243, '原版问答': 4353, '周边创作': 183887, '周边问答': 196, '基岩版作品发布': 23205, '基岩版多人联机': 1360, '基岩版技巧教程': 6789, '基岩版软件资源': 7713, '基岩版问答': 0, '展示&共享': 643841, '我的世界：地球[逐步公测]': 458, '我的世界：故事模式': 907, '搬运&鉴赏': 62120, '整合包发布': 213013, '新闻资讯': 67434, '服务器': 32180, '服务端插件': 201806, '服务端整合包': 51309, '材质资源': 90198, '游戏技巧': 128305, '皮肤分享': 167278, '矿工茶馆': 789959, '综合游戏讨论区': 11928, '编程开发': 22142, '翻译&Wiki': 32866, '联机教程': 27394, '联机问答': -2187, '视频实况': 72050, '软件资源': 66520}, 'appraisal': {'CubeWorld(魔方世界)': 48, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 666, 'MCBBS擂台': 2353, 'Mod发布': 81181, 'Mod教程': 2850, 'Mod讨论': 644, 'Mod问答': 793, 'Nukkit服务端专区': 0, 'PocketMine服务端专区': 2202, '公告和反馈': 12427, '匠人酒馆': 3236, '原版问答': 267, '周边创作': 6505, '周边问答': 0, '基岩版作品发布': 3306, '基岩版多人联机': 647, '基岩版技巧教程': 276, '基岩版软件资源': 1038, '基岩版问答': 0, '展示&共享': 53594, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 0, '搬运&鉴赏': 7251, '整合包发布': 64556, '新闻资讯': 5387, '服务器': 6388, '服务端插件': 21527, '服务端整合包': 12595, '材质资源': 29363, '游戏技巧': 19431, '皮肤分享': 20524, '矿工茶馆': 11734, '综合游戏讨论区': 1178, '编程开发': 1179, '翻译&Wiki': 774, '联机教程': 4728, '联机问答': 360, '视频实况': 6619, '软件资源': 13526}, 'heat': {'CubeWorld(魔方世界)': 627, 'Hytale[封测中]': 0, 'MCBBS创意馆（比赛结束）': 2247, 'MCBBS擂台': 21001, 'Mod发布': 1240216, 'Mod教程': 51832, 'Mod讨论': 22509, 'Mod问答': 3063, 'Nukkit服务端专区': 108, 'PocketMine服务端专区': 12470, '公告和反馈': 103066, '匠人酒馆': 59294, '原版问答': 17809, '周边创作': 82311, '周边问答': 0, '基岩版作品发布': 308986, '基岩版多人联机': 5510, '基岩版技巧教程': 16093, '基岩版软件资源': 83842, '基岩版问答': 0, '展示&共享': 2042010, '我的世界：地球[逐步公测]': 0, '我的世界：故事模式': 246, '搬运&鉴赏': 170642, '整合包发布': 1087629, '新闻资讯': 81821, '服务器': 23424, '服务端插件': 661858, '服务端整合包': 304718, '材质资源': 1946645, '游戏技巧': 242674, '皮肤分享': 1868949, '矿工茶馆': 1110770, '综合游戏讨论区': 9963, '编程开发': 47246, '翻译&Wiki': 21203, '联机教程': 96320, '联机问答': 3095, '视频实况': 45401, '软件资源': 603868}, 'image-amount': {'CubeWorld(魔方世界)': 376, 'Hytale[封测中]': 97, 'MCBBS创意馆（比赛结束）': 5671, 'MCBBS擂台': 6441, 'Mod发布': 75438, 'Mod教程': 21092, 'Mod讨论': 4347, 'Mod问答': 17609, 'Nukkit服务端专区': 1018, 'PocketMine服务端专区': 389,'公告和反馈': 13528, '匠人酒馆': 25040, '原版问答': 17262, '周边创作': 20526, '周边问答': 2125, '基岩版作品发布': 9360, '基岩版多人联机': 693, '基岩版技巧教程': 2536, '基岩版软件资源': 2944, '基岩版问答': 1, '展示&共享': 237848, '我的世界：地球[逐步公测]': 33, '我的世界：故事模式': 311, '搬运&鉴赏': 31642, '整合包发布': 32315, '新闻资讯': 6296, '服务器': 20311, '服务端插件': 46496, '服务端整合包': 13226, '材质资源': 18682, '游戏技巧': 62706, '皮肤分享': 60418, '矿工茶馆': 151430, '综合游戏讨论区': 9586, '编程开发': 4526, '翻译&Wiki': 8696, '联机教程': 6590, '联机问答': 33029, '视频实况': 7927, '软件资源': 9173}, 'iframe-amount': {'CubeWorld(魔方世界)': 0, 'Hytale[封测中]': 1, 'MCBBS创意馆（比赛结束）': 10, 'MCBBS擂台': 23, 'Mod发布': 300, 'Mod教程': 62, 'Mod讨论': 14, 'Mod问答': 2, 'Nukkit服务端专区': 4, 'PocketMine服务端专区': 0, '公告和反馈': 10, '匠人酒馆': 41, '原版问答': 5, '周边创作': 38, '周边问答': 1, '基岩版作品发布': 4, '基岩版多人联机': 0, '基岩版技巧教程': 7, '基岩版软件资源': 8, '基岩版问答': 0, '展示&共享': 637, '我的世界：地球[逐步公测]': 1, '我的世界：故事模式': 45, '搬运&鉴赏': 89, '整合包发布': 211, '新闻资讯': 67, '服务器': 67, '服务端插件': 150, '服务端整合包': 27, '材质资源': 46, '游戏技巧': 192, '皮肤分享': 57, '矿工茶馆': 900, '综合游戏讨论区': 51, '编程开发': 26, '翻译&Wiki': 47, '联机教程': 29, '联机问答': 2, '视频实况': 4455, '软件资源': 20}, 'table-amount': {'CubeWorld(魔方世界)': 59, 'Hytale[封测中]': 47, 'MCBBS创意馆（比赛结束）': 1054, 'MCBBS擂台': 1658, 'Mod发布': 26830, 'Mod教程': 4811, 'Mod讨论': 1241, 'Mod问答': 1551, 'Nukkit服务端专区': 1212, 'PocketMine服务端专区': 281, '公告和反馈': 1473, '匠人酒馆': 2644, '原版问答': 1148, '周边创作': 7937, '周边问答': 160, '基岩版作品发布': 700, '基岩版多人联机': 164, '基岩版技巧教程': 475, '基岩版软件资源': 749, '基岩版问答': 0, '展示&共享': 22601, '我的世界：地球[逐步公测]': 27, '我的世界：故事模式': 62, '搬运&鉴赏': 8094, '整合包发布': 15240, '新闻资讯': 5654, '服务器': 4173, '服务端插件': 47077, '服务端整合包': 7317, '材质资源': 3384, '游戏技巧': 5855, '皮肤分享': 6734, '矿工茶馆': 17122, '综合游戏讨论区': 1171, '编程开发': 2261, '翻译&Wiki': 3514, '联机教程': 3691, '联机问答': 3649, '视频实况': 5080, '软件资源': 2822}, 'redirect-amount': {'CubeWorld(魔方世界)': 75, 'Hytale[封测中]': 50, 'MCBBS创意馆（比赛结束）': 105, 'MCBBS擂台': 399, 'Mod发布':17652, 'Mod教程': 1910, 'Mod讨论': 614, 'Mod问答': 9101, 'Nukkit服务端专区': 371, 'PocketMine服务端专区': 115, '公告和反馈': 1924, '匠人酒馆': 580, '原版问答': 2748, '周边创作': 1783, '周边问答': 329, '基岩版作品发布': 447, '基岩版多人联机': 156, '基岩版技巧教程': 146, '基岩版软件资源': 817, '基岩版问答': 0, '展示&共享': 10332, '我的世界：地球[逐步公测]': 52, '我的世界：故事模式': 199, '搬运&鉴赏': 4989, '整合包发布': 9010, '新闻资讯': 15753, '服务器': 1283, '服务端插件': 9134, '服务端整合包': 888, '材质资源': 2219, '游戏技巧': 4943, '皮肤分享': 2349, '矿工茶馆': 13114, '综合游戏讨论区': 2327, '编程开发': 1615, '翻译&Wiki': 9377, '联机教程': 1625, '联机问答': 17289, '视频实况': 30595, '软件资源': 4247}, 'operation': {'CubeWorld(魔方世界)': 184, 'Hytale[封测中]': 11, 'MCBBS创意馆（比赛结束）': 418, 'MCBBS擂台': 69, 'Mod发布': 5054, 'Mod教程': 919, 'Mod讨论': 361, 'Mod问答': 1677, 'Nukkit服务端专区': 63, 'PocketMine服务端专区': 5, '公告和反馈': 1481, '匠人酒馆': 329, '原版问答': 1039, '周边创作': 283, '周边问答': 432, '基岩版作品发布': 81, '基岩版多人联机': 110, '基岩版技巧教程': 39, '基岩版软件资源': 64, '基岩版问答': 2, '展示&共享': 3457, '我的世界：地球[逐步公测]':52, '我的世界：故事模式': 50, '搬运&鉴赏': 151, '整合包发布': 4286, '新闻资讯': 1419, '服务器': 63650, '服务端插件': 3716, '服务端整合包': 540, '材质资源': 781, '游戏技巧': 593, '皮肤分享': 493, '矿工茶馆': 7176, '综合游戏讨论区': 322, '编程开发': 1499, '翻译&Wiki': 301, '联机教程': 1725, '联机问答': 4109, '视频实况': 517, '软件资源': 634}}
        md = ['''# 板块对比\n\n## 概况\n\n- #### 访问有效的帖子\n\n（注：指的是游客能进入、并看到内容的帖子）\n\n''']
        md.append(occupation_pie_figure(category_stats['valid_thread_count'], '访问有效的帖子'))
        md.append('''\n\n------------\n\n- #### 被回复的帖子\n\n''')
        md.append(occupation_pie_figure(category_stats['replied_thread'], '被回复的帖子'))
        md.append('''\n\n------------\n\n- #### 被评分的帖子\n\n''')
        md.append(occupation_pie_figure(category_stats['rewarded_thread'], '被评分的帖子'))
        md.append('''\n\n------------\n\n- #### 被关闭的帖子\n\n''')
        md.append(occupation_pie_figure(category_stats['closed_thread'], '被关闭的帖子'))
        md.append('''\n\n------------\n\n- #### 查看\n\n''')
        md.append(occupation_pie_figure(category_stats['view'], '查看量'))
        md.append('''\n\n------------\n\n- #### 回复\n\n''')
        md.append(occupation_pie_figure(category_stats['reply'], '回复量'))
        md.append('''\n\n------------\n\n- #### 评分\n\n''')
        md.append(occupation_pie_figure(category_stats['participation'], '参与评分人数'))
        md.append('''\n\n------------\n\n- #### 人气\n\n''')
        md.append(occupation_pie_figure(category_stats['popularity'], '人气'))
        md.append('''\n\n------------\n\n- #### 金粒\n\n''')
        md.append(occupation_pie_figure(category_stats['golden-nugget'], '金粒'))
        md.append('''\n\n------------\n\n- #### 贡献\n\n''')
        md.append(occupation_pie_figure(category_stats['contribution'], '贡献'))
        md.append('''\n\n------------\n\n- #### 金锭\n\n''')
        md.append(occupation_pie_figure(category_stats['golden-ingot'], '金锭'))
        md.append('''\n\n------------\n\n- #### 绿宝石\n\n''')
        md.append(occupation_pie_figure(category_stats['emerald'], '绿宝石'))
        md.append('''\n\n------------\n\n- #### 下界之星\n\n''')
        md.append(occupation_pie_figure(category_stats['nether-star'], '下界之星'))
        md.append('''\n\n------------\n\n- #### 爱心\n\n''')
        md.append(occupation_pie_figure(category_stats['heart'], '爱心'))
        md.append('''\n\n------------\n\n- #### 积分收益\n\n''')
        md.append(occupation_pie_figure(category_stats['profits'], '积分收益'))
        md.append('''\n\n------------\n\n- #### 好评度\n\n''')
        md.append(occupation_pie_figure(category_stats['appraisal'], '好评度'))
        md.append('''\n\n------------\n\n- #### 热度\n\n''')
        md.append(occupation_pie_figure(category_stats['heat'], '热度'))
        md.append('''\n\n------------\n\n- #### 图片\n\n''')
        md.append(occupation_pie_figure(category_stats['image-amount'], '图片数'))
        md.append('''\n\n------------\n\n- #### Iframe\n\n''')
        md.append(occupation_pie_figure(category_stats['iframe-amount'], 'iframe数'))
        md.append('''\n\n------------\n\n- #### 表格\n\n''')
        md.append(occupation_pie_figure(category_stats['table-amount'], '表格数'))
        md.append('''\n\n------------\n\n- #### 外链\n\n''')
        md.append(occupation_pie_figure(category_stats['redirect-amount'], '外链数'))
        md.append('''\n\n------------\n\n- #### 帖子\n\n''')
        md.append(occupation_pie_figure(category_stats['operation'], '帖子被操作次数'))
        with open(BASE_DIR + '/mds/&.md', 'w+', encoding='utf-8') as _f:
            _f.write(''.join(md))
        print('category', 'done.')
# time
def time_eachyear():
    for s in os.listdir(BASE_DIR + '/stats'):
        if not re.findall('^(\d+).txt', s) == []:
            year = re.findall('^(\d+).txt', s)[0]
            with open(os.path.join(BASE_DIR + '/stats', s), 'r', encoding='utf-8') as f:
                stats = json.loads(f.read())
                # private stats
                new_img_dir(year)
                md = ['''# 总览\n\n## 概况\n\n''']
                md.append('''\n\n- #### 被回复的帖子\n\n''')
                md.append(rate_pie_figure(stats['replied_thread'], stats['valid_thread_count'], '被回复的帖子'))
                md.append('\n\n- #### 被评分的帖子\n\n')
                md.append(rate_pie_figure(stats['rewarded_thread'], stats['valid_thread_count'], '被评分的帖子'))
                md.append('\n\n- #### 被关闭的帖子\n\n')
                md.append(rate_pie_figure(stats['closed_thread'], stats['valid_thread_count'], '被关闭的帖子', '状态正常的帖子'))
                md.append('\n\n- #### 查看与回帖\n\n')
                md.append(rate_pie_figure(sum(x[1] for x in stats['hists']['reply']['sum'].items()), sum(x[1] for x in stats['hists']['view']['sum'].items()), '查看并回帖', '查看无回帖'))
                md.append('\n\n- #### 有图章的帖子\n\n')
                md.append(rate_pie_figure(sum(x[1] for x in stats['seals'].items()), stats['valid_thread_count'], '有图章', '无图章'))
                md.append('''\n\n**（接下来的所有统计数据来源于访问有效的帖子，造成访问无效可能原因是帖子被删除、屏蔽、高权限隐藏等）**\n\n## 分段统计\n\n- #### 查看量\n\n''')
                md.append(rich_hist(occupy_cates['view'],hist_cates['view'],stats['hists']['view'],'查看',10))
                md.append('\n\n- #### 回复量\n\n')
                md.append(rich_hist(occupy_cates['reply'],hist_cates['reply'],stats['hists']['reply'],'回复'))
                md.append('\n\n- #### 评分参与人数\n\n')
                md.append(rich_hist(occupy_cates['participation'],hist_cates['participation'],stats['hists']['participation'],'参与人数'))
                md.append('\n\n- #### 人气\n\n')
                md.append(rich_hist(occupy_cates['popularity'],hist_cates['popularity'],stats['hists']['popularity'],'人气'))
                md.append('\n\n- #### 金粒\n\n')
                md.append(rich_hist(occupy_cates['golden-nugget'],hist_cates['golden-nugget'],stats['hists']['golden-nugget'],'金粒'))
                md.append('\n\n- #### 贡献\n\n')
                md.append(rich_hist(occupy_cates['contribution'],hist_cates['contribution'],stats['hists']['contribution'],'贡献'))
                md.append('\n\n- #### 金锭\n\n')
                md.append(rich_hist(occupy_cates['golden-ingot'],hist_cates['golden-ingot'],stats['hists']['golden-ingot'],'金锭'))
                md.append('\n\n- #### 绿宝石\n\n')
                md.append(rich_hist(occupy_cates['emerald'],hist_cates['emerald'],stats['hists']['emerald'],'绿宝石'))
                md.append('\n\n- #### 下界之星\n\n')
                md.append(rich_hist(occupy_cates['nether-star'],hist_cates['nether-star'],stats['hists']['nether-star'],'下界之星'))
                md.append('\n\n- #### 爱心\n\n')
                md.append(rich_hist(occupy_cates['heart'],hist_cates['heart'],stats['hists']['heart'],'爱心'))
                md.append('\n\n- #### 积分收益\n\n')
                md.append(rich_hist(occupy_cates['profits'],hist_cates['profits'],stats['hists']['profits'],'收益'))
                md.append('\n\n- #### 好评度\n\n')
                md.append(rich_hist(occupy_cates['appraisal'],hist_cates['appraisal'],stats['hists']['appraisal'],'好评度'))
                md.append('\n\n- #### 热度\n\n')
                md.append(rich_hist(occupy_cates['heat'],hist_cates['heat'],stats['hists']['heat'],'热度'))
                md.append('\n\n- #### 图片数\n\n')
                md.append(rich_hist(occupy_cates['image-amount'],hist_cates['image-amount'],stats['hists']['image-amount'],'图片数'))
                md.append('\n\n- #### iframe数\n\n')
                md.append(rich_hist(occupy_cates['iframe-amount'],hist_cates['iframe-amount'],stats['hists']['iframe-amount'],'iframe数'))
                md.append('\n\n- #### 表格数\n\n')
                md.append(rich_hist(occupy_cates['table-amount'],hist_cates['table-amount'],stats['hists']['table-amount'],'表格数'))
                md.append('\n\n- #### 外链数\n\n')
                md.append(rich_hist(occupy_cates['redirect-amount'],hist_cates['redirect-amount'],stats['hists']['redirect-amount'],'外链数'))
                md.append('\n\n- #### 帖子被操作次数\n\n')
                md.append(rich_hist(occupy_cates['operation'],hist_cates['operation'],stats['hists']['operation'],'被操作数'))
                if stats['seals'].__len__() > 0:
                    md.append('\n\n- #### 图章占比\n\n')
                    global seal_color
                    md.append(waffle_figure(stats['seals'],'图章占比',seal_color))
                md.append('\n\n----\n\n## 排名\n\n')
                md.append('- #### 查看最多的帖子\n\n')
                md.append(table_thread(stats['rank_view'],'查看数',rank_condition='>0'))
                md.append('\n\n- #### 回复最多的帖子\n\n')
                md.append(table_thread(stats['rank_reply'],'回复数',rank_condition='>0'))
                md.append('\n\n- #### 回帖率最高的帖子\n\n')
                md.append(table_thread(stats['rank_replyrate'],'回帖率',rank_condition='>0'))
                md.append('\n\n- #### 回帖率最低的帖子\n\n')
                md.append(table_thread(stats['rank_replyrate_negative'],'回帖率升序',rank_condition='>0'))
                md.append('\n\n- #### 参与评分人数最多的帖子\n\n')
                md.append(table_thread(stats['rank_participation'],'参与评分人数',rank_condition='>0'))
                md.append('\n\n- #### 获得人气最多的帖子\n\n')
                md.append(table_thread(stats['rank_popularity'],'人气',rank_condition='>0'))
                md.append('\n\n- #### 获得金粒最多的帖子\n\n')
                md.append(table_thread(stats['rank_golden_nugget'],'金粒',rank_condition='>0'))
                md.append('\n\n- #### 获得贡献最多的帖子\n\n')
                md.append(table_thread(stats['rank_contribution'],'贡献',rank_condition='>0'))
                md.append('\n\n- #### 获得金锭最多的帖子\n\n')
                md.append(table_thread(stats['rank_golden_ingot'],'金锭',rank_condition='>0'))
                md.append('\n\n- #### 获得绿宝石最多的帖子\n\n')
                md.append(table_thread(stats['rank_emerald'],'绿宝石',rank_condition='>0'))
                md.append('\n\n- #### 获得下界之星最多的帖子\n\n')
                md.append(table_thread(stats['rank_nether_star'],'下界之星',rank_condition='>0'))
                md.append('\n\n- #### 获得爱心最多的帖子\n\n')
                md.append(table_thread(stats['rank_heart'],'爱心',2,rank_condition='>0'))
                md.append('\n\n- #### 积分收益最高的帖子\n\n')
                md.append(table_thread(stats['rank_profits'],'积分收益',rank_condition='>0'))
                md.append('\n\n- #### 积分收益最低的帖子\n\n')
                md.append(table_thread(stats['rank_profits_negative'],'积分收益倒序',rank_condition='>0'))
                md.append('\n\n- #### 好评度最高的帖子\n\n')
                md.append(table_thread(stats['rank_appraisal'],'好评度',rank_condition='>0'))
                md.append('\n\n- #### 热度最高的帖子\n\n')
                md.append(table_thread(stats['rank_heat'],'热度',rank_condition='>0'))
                md.append('\n\n- #### 图片最多的帖子\n\n')
                md.append(table_thread(stats['rank_image'],'图片数',rank_condition='>0'))
                md.append('\n\n- #### iframe最多的帖子\n\n')
                md.append(table_thread(stats['rank_iframe'],'iframe数',rank_condition='>0'))
                md.append('\n\n- #### 表格最多的帖子\n\n')
                md.append(table_thread(stats['rank_table'],'表格数',rank_condition='>0'))
                md.append('\n\n- #### 外链最多的帖子\n\n')
                md.append(table_thread(stats['rank_url'],'外链数',rank_condition='>0'))
                md.append('\n\n- #### 被操作最多次的帖子\n\n')
                md.append(table_thread(stats['rank_operation'],'被操作数',rank_condition='>0'))
                md.append('\n\n----\n\n## 技术统计\n\n')
                md.append('\n\n- #### 标题关键词\n\n')
                md.append(table_counter(stats['title_keyword'],'标题关键词',100,rank_condition='>0'))
                md.append('\n\n- #### 内容关键词\n\n')
                md.append(table_counter(stats['content_keyword'],'内容关键词',100,rank_condition='>0'))
                md.append('\n\n- #### 评分评语\n\n')
                md.append(table_counter(stats['reasons'],'评语',100,rank_condition='>0'))
                md.append('\n\n- #### 有效发帖者\n\n')
                md.append(table_counter(stats['authors'],'有效发帖者',100,rank_condition='>0'))
                md.append('\n\n- #### 评分者\n\n')
                md.append(table_counter(stats['generous'],'评分者',100,rank_condition='>0'))
                md.append('\n\n- #### 精华帖作者\n\n')
                md.append(table_counter(stats['author_jh'],'精华帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 优秀贴作者\n\n')
                md.append(table_counter(stats['author_yx'],'优秀帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 置顶帖作者\n\n')
                md.append(table_counter(stats['author_zd'],'置顶帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 版主推荐帖作者\n\n')
                md.append(table_counter(stats['author_tj'],'版主推荐帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 原创帖作者\n\n')
                md.append(table_counter(stats['author_yc'],'原创帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 爆料贴作者\n\n')
                md.append(table_counter(stats['author_bl'],'爆料帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 授权搬运贴作者\n\n')
                md.append(table_counter(stats['author_by'],'授权搬运帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 过期贴作者\n\n')
                md.append(table_counter(stats['author_gq'],'过期帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 关闭贴作者\n\n')
                md.append(table_counter(stats['author_gb'],'关闭帖作者',100,rank_condition='>0'))
                md.append('\n\n- #### 发帖小组\n\n')
                md.append(table_counter(stats['group'],'发帖来自小组',20,rank_condition='>0'))
                md.append('\n\n----\n\n- ## 逼榜 / 2bindex\n\n- ### 最活跃发帖者\n\n```\n逼值 = 精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2 + 其他发帖数 * 0.1\n```\n\n')
                md.append(table_counter(most_active(stats),'用户',rank_condition='>0',value_name='逼值'))
                md.append('\n\n- ### 最有价值发帖者\n\n```\n逼度 = (精华帖数 + (优秀帖数 + 版主推荐帖数) * 0.5 + 置顶帖数 * 0.3 + 原创帖数 * 0.2) / 总发帖量\n```\n\n')
                md.append(table_counter(most_valuable(stats),'用户',rank_condition='>0',value_name='逼度'))
                with open(BASE_DIR + '/mds/' + year + '.md', 'w+', encoding='utf-8') as _f:
                    _f.write(''.join(md))
                print(year, 'done.')
def time_trend():
    month_stats = {
        'valid_thread_count' : {},
        'replied_thread' : {},
        'rewarded_thread' : {},
        'closed_thread' : {},
        'seals' : {},
    }
    for s in os.listdir(BASE_DIR + '/stats'):
        if not re.findall('^(\d+\-\d+).txt', s) == []:
            month = re.findall('^(\d+\-\d+).txt', s)[0]
            with open(os.path.join(BASE_DIR + '/stats', s), 'r', encoding='utf-8') as f:
                stats = json.loads(f.read())
                # month_stats
                month_stats['valid_thread_count'][month] = stats['valid_thread_count']
                month_stats['replied_thread'][month] = stats['replied_thread']
                month_stats['rewarded_thread'][month] = stats['rewarded_thread']
                month_stats['closed_thread'][month] = stats['closed_thread']
                if stats['seals'].__len__() > 0:
                    for i in stats['seals'].items():
                        if not i[0] in month_stats['seals']:
                            month_stats['seals'][i[0]] = {}
                        month_stats['seals'][i[0]][month] = i[1]
                for k,c in hist_cates.items():
                    if not k in month_stats:
                        month_stats[k] = {}
                    month_stats[k][month] = sum([x[1] for x in stats['hists'][k]['sum'].items()])
    md = ['''# 月度趋势\n\n## 概况\n\n- #### 访问有效的帖子\n\n（注：指的是游客能进入、并看到内容的帖子）\n\n''']
    md.append(trend_plot_month(month_stats['valid_thread_count'], '访问有效的帖子'))
    md.append('''\n\n------------\n\n- #### 被回复的帖子\n\n''')
    md.append(trend_plot_month(month_stats['replied_thread'], '被回复的帖子'))
    md.append('''\n\n------------\n\n- #### 被评分的帖子\n\n''')
    md.append(trend_plot_month(month_stats['rewarded_thread'], '被评分的帖子'))
    md.append('''\n\n------------\n\n- #### 被关闭的帖子\n\n''')
    md.append(trend_plot_month(month_stats['closed_thread'], '被关闭的帖子'))
    md.append('''\n\n------------\n\n- #### 查看\n\n''')
    md.append(trend_plot_month(month_stats['view'], '查看量'))
    md.append('''\n\n------------\n\n- #### 回复\n\n''')
    md.append(trend_plot_month(month_stats['reply'], '回复量'))
    md.append('''\n\n------------\n\n- #### 评分\n\n''')
    md.append(trend_plot_month(month_stats['participation'], '参与评分人数'))
    md.append('''\n\n------------\n\n- #### 人气\n\n''')
    md.append(trend_plot_month(month_stats['popularity'], '人气'))
    md.append('''\n\n------------\n\n- #### 金粒\n\n''')
    md.append(trend_plot_month(month_stats['golden-nugget'], '金粒'))
    md.append('''\n\n------------\n\n- #### 贡献\n\n''')
    md.append(trend_plot_month(month_stats['contribution'], '贡献'))
    md.append('''\n\n------------\n\n- #### 金锭\n\n''')
    md.append(trend_plot_month(month_stats['golden-ingot'], '金锭'))
    md.append('''\n\n------------\n\n- #### 绿宝石\n\n''')
    md.append(trend_plot_month(month_stats['emerald'], '绿宝石'))
    md.append('''\n\n------------\n\n- #### 下界之星\n\n''')
    md.append(trend_plot_month(month_stats['nether-star'], '下界之星'))
    md.append('''\n\n------------\n\n- #### 爱心\n\n''')
    md.append(trend_plot_month(month_stats['heart'], '爱心'))
    md.append('''\n\n------------\n\n- #### 积分收益\n\n''')
    md.append(trend_plot_month(month_stats['profits'], '积分收益'))
    md.append('''\n\n------------\n\n- #### 好评度\n\n''')
    md.append(trend_plot_month(month_stats['appraisal'], '好评度'))
    md.append('''\n\n------------\n\n- #### 热度\n\n''')
    md.append(trend_plot_month(month_stats['heat'], '热度'))
    md.append('''\n\n------------\n\n- #### 图片\n\n''')
    md.append(trend_plot_month(month_stats['image-amount'], '图片数'))
    md.append('''\n\n------------\n\n- #### Iframe\n\n''')
    md.append(trend_plot_month(month_stats['iframe-amount'], 'iframe数'))
    md.append('''\n\n------------\n\n- #### 表格\n\n''')
    md.append(trend_plot_month(month_stats['table-amount'], '表格数'))
    md.append('''\n\n------------\n\n- #### 外链\n\n''')
    md.append(trend_plot_month(month_stats['redirect-amount'], '外链数'))
    md.append('''\n\n------------\n\n- #### 帖子\n\n''')
    md.append(trend_plot_month(month_stats['operation'], '帖子被操作次数'))
    with open(BASE_DIR + '/mds/$.md', 'w+', encoding='utf-8') as _f:
        _f.write(''.join(md))
    ('trend', 'done.')
# html
def create_html():
    indexer = ['# 论坛帖子统计', '(统计至tid=923416, 11.3日统计)','----','## 索引']
    indexer.append('#### [全坛](@.html ' + '"全坛")')
    indexer.append('----')
    indexer.append('#### [各版](&.html ' + '"各版")')
    for s in os.listdir(BASE_DIR + '/mds'):
        if 'index' in s:
            continue
        if not re.findall('(^[^\d-]+).md', s) == [] and not '@' in s and not '$' in s and not s == '&.txt':
            indexer.append('#### [' + s.split('.')[0] + '](' + s.split('.')[0] + '.html ' + '"' + s.split('.')[0] + '")')
    indexer.append('----')
    indexer.append('#### [趋势]($.html ' + '"趋势")')
    for s in os.listdir(BASE_DIR + '/mds'):
        if 'index' in s:
            continue
        if not re.findall('^(\d+).md', s) == [] and not '@' in s and not '$' in s and not '&' in s:
            indexer.append('#### [' + s.split('.')[0] + '](' + s.split('.')[0] + '.html ' + '"' + s.split('.')[0] + '")')
    with open(BASE_DIR + '/mds/index.md', 'w+', encoding='utf-8') as _f:
        _f.write('\n\n'.join(indexer))
    for s in os.listdir(BASE_DIR + '/mds'):
        title = '全坛' if s.split('.')[0] == '@' else '各版' if s.split('.')[0] == '&' else '趋势' if s.split('.')[0] == '$' else s.split('.')[0]
        ht = '\n'.join(['<!DOCTYPE html>',
            '<html>',
            ' <head> ',
            '  <meta name="viewport" content="text/html; charset=utf-8" http-equiv="Content-Type" /> ',
            '  <title>'+ title +'</title> ',
            '  <script src="js/jquery.min.js"></script> ',
            '  <script src="js/marked.min.js"></script> ',
            '  <link rel="stylesheet" href="github-markdown.css" /> ',
            '  <style>',
            '	.markdown-body {',
            '		box-sizing: border-box;',
            '		min-width: 200px;',
            '		max-width: 980px;',
            '		margin: 0 auto;',
            '		padding: 45px;',
            '	}',
            '	@media (max-width: 767px) {',
            '		.markdown-body {',
            '			padding: 15px;',
            '		}',
            '	}',
            '</style> ',
            '  <script>',
            '$(document).ready(function(){',
            '    $(function(){',
            '		$.ajax({',
            '			url: \'mds/'+ s.split('.')[0] + '.md\',',
            '			dataType: \'text\',',
            '			scriptCharset: \'utf-8\',',
            '			success: function(data) {',
            '				document.getElementById(\'article\').innerHTML = marked(data);',
            '			}',
            '		});',
            '	});',
            '});',
            '</script> ',
            ' </head> ',
            ' <body> ',
            '  <article id="article" class="markdown-body"></article>  ',
            ' </body>',
            '</html>'])
        with open(BASE_DIR + '/html/' + s.split('.')[0] + '.html', 'w+', encoding='utf-8') as _f:
            _f.write(ht)
        print(s.split('.')[0], 'done.')

general()
category()
category_general()
time_eachyear()
time_trend()
create_html()