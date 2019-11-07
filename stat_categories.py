from stat_util import value_conditional, value_multi_conditional, binary_insert
import os, json, re
BASE_DIR = os.path.dirname(__file__)
class stats_category:
# COUNT
    # thread
    def __init__(self):
        self.stats = {
            'thread_count' : 0,
            'valid_thread_count' : 0,
            'replied_thread' : 0,
            'rewarded_thread' : 0,
            'closed_thread' : 0,
            'blocked_thread' : 0,
            # basic
            'view_sum' : 0,
            'reply_sum' : 0,
            'seals' : {},
            'hists' : {
                "view" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "reply" : { 'occupy': {}, 'count': {}, 'sum': {}},
                # reward
                "participation" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "popularity" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "golden-nugget" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "contribution" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "golden-ingot" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "emerald" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "nether-star" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "heart" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "profits" : { 'occupy': {}, 'count': {}, 'sum': {}},
                # tag
                "appraisal" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "heat" : { 'occupy': {}, 'count': {}, 'sum': {}},
                # tech
                "image-amount" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "iframe-amount" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "table-amount" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "redirect-amount" : { 'occupy': {}, 'count': {}, 'sum': {}},
                "operation" : { 'occupy': {}, 'count': {}, 'sum': {}}
            },
            
            # RANK
            # basic
            'rank_view' : [],
            'rank_reply' : [],
            'rank_replyrate' : [],
            'rank_replyrate_negative' : [],
            # reward
            'rank_participation' : [],
            'rank_popularity' : [],
            'rank_golden_nugget' : [],
            'rank_contribution' : [],
            'rank_golden_ingot' : [],
            'rank_emerald' : [],
            'rank_nether_star' : [],
            'rank_heart' : [],
            'rank_profits' : [],
            'rank_profits_negative' : [],
            # tag
            'rank_appraisal' : [], #proved invalid
            'rank_appraisal_negative' : [],
            'rank_heat' : [],
            # tech
            'rank_image' : [],
            'rank_iframe' : [],
            'rank_table' : [],
            'rank_url' : [],
            'rank_operation' : [],

            # Rank_by_Count
            'title_keyword' : {},
            'content_keyword' : {},
            'reasons' : {},
            'authors' : {},
            'generous' : {},
            'author_jh' : {},
            'author_yx' : {},
            'author_zd' : {},
            'author_tj' : {},
            'author_yc' : {},
            'author_bl' : {},
            'author_by' : {},
            'author_gq' : {},
            'author_gb' : {},
            'group' : {}
        }

def get_keys(objective):
    date = objective['time'].split(' ')[0]
    ymd = date.split('-')
    return [ymd[0], ymd[0]+'-'+ymd[1], objective['category'], objective['category']+'-'+objective['subcategory']]

categories = {'': stats_category()}

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

def hist_op(v, store, cates, mode='sum'):
    for cate in cates:
        if not cate[0] in store:
            store[cate[0]] = 0
        if value_multi_conditional(v, cate[1]):
            if mode == 'sum':
                store[cate[0]] += v
            elif mode == 'count':
                store[cate[0]] += 1
def rank_op(v, container: list, attached_info, order='descend'):
    binary_insert(container, (v, attached_info), 50, order)
def rank_count_op(key, rank, allowRepeat = True):
    if type(key) == list:
        if not allowRepeat:
            key = list(set(key))
        for i in key:
            if not i in rank:
                rank[i] = 1
            else:
                rank[i] += 1
    else:
        if not key in rank:
            rank[key] = 1
        else:
            rank[key] += 1

def writein_stat(data, stat, tid):
    global hist_cates, occupy_cates
    stat['thread_count'] += 1
    stat['valid_thread_count'] += 1
    stat['view_sum'] += data['view']
    stat['reply_sum'] += data['reply']
    if data['reply'] > 0:
        stat['replied_thread'] += 1
    if data['participation'] > 0:
        stat['rewarded_thread'] += 1
    if not [x for x in data['state'] if '关闭' in x] == []:
        stat['closed_thread'] += 1
    if not data['seal'] == "": # occupy
        if not data['seal'] in stat['seals']:
            stat['seals'][data['seal']] = 0
        stat['seals'][data['seal']] += 1
    # 精华帖数X45+人气X3+贡献X10+爱心X4
    data['profits'] = data['popularity'] * 3 + data['contribution'] * 10 + data['heart'] * 4 + (45 if "精华" in data['seal'] else 0)
    # hist
    for i in stat['hists']:
        hist_op(data[i], stat['hists'][i]['count'], hist_cates[i], 'count')
        hist_op(data[i], stat['hists'][i]['sum'], hist_cates[i], 'sum')
        hist_op(data[i], stat['hists'][i]['occupy'], occupy_cates[i], 'count')
    # rank
    rank_op(data['view'], stat['rank_view'], tid)
    rank_op(data['reply'], stat['rank_reply'], tid)
    if data['view'] > 0:
        rank_op(data['reply']/data['view'], stat['rank_replyrate'], tid)
    if data['reply'] == 0:
        rank_op(data['view'], stat['rank_replyrate_negative'], tid)
    rank_op(data['participation'], stat['rank_participation'], tid)
    rank_op(data['popularity'], stat['rank_popularity'], tid)
    rank_op(data['golden-nugget'], stat['rank_golden_nugget'], tid)
    rank_op(data['contribution'], stat['rank_contribution'], tid)
    rank_op(data['golden-ingot'], stat['rank_golden_ingot'], tid)
    rank_op(data['emerald'], stat['rank_emerald'], tid)
    rank_op(data['nether-star'], stat['rank_nether_star'], tid)
    rank_op(data['heart'], stat['rank_heart'], tid)
    rank_op(data['profits'], stat['rank_profits'], tid)
    rank_op(data['profits'], stat['rank_profits_negative'], tid, order='ascend')
    rank_op(data['appraisal'], stat['rank_appraisal'], tid)
    rank_op(data['appraisal'], stat['rank_appraisal_negative'], tid, order='ascend')
    rank_op(data['heat'], stat['rank_heat'], tid)
    rank_op(data['image-amount'], stat['rank_image'], tid)
    rank_op(data['iframe-amount'], stat['rank_iframe'], tid)
    rank_op(data['table-amount'], stat['rank_table'], tid)
    rank_op(data['redirect-amount'], stat['rank_url'], tid)
    rank_op(data['operation'], stat['rank_operation'], tid)
    rank_count_op(data['title-keywords'], stat['title_keyword'])
    rank_count_op(data['content-keywords'], stat['content_keyword'])
    rank_count_op(data['reasons'], stat['reasons'])
    rank_count_op(data['participants'], stat['generous'], False)
    rank_count_op(data['author'], stat['authors'])
    if "精华" in data['seal']:
        rank_count_op(data['author'], stat['author_jh'])
    if "优秀" in data['seal']:
        rank_count_op(data['author'], stat['author_yx'])
    if "原创" in data['seal']:
        rank_count_op(data['author'], stat['author_yc'])
    if "爆料" in data['seal']:
        rank_count_op(data['author'], stat['author_bl'])
    if "推荐" in data['seal']:
        rank_count_op(data['author'], stat['author_tj'])
    if "置顶" in data['seal']:
        rank_count_op(data['author'], stat['author_zd'])
    if "过期" in data['seal']:
        rank_count_op(data['author'], stat['author_gq'])
    if "搬运" in data['seal']:
        rank_count_op(data['author'], stat['author_by'])
    if not [x for x in data['state'] if '关闭' in x] == []:
        rank_count_op(data['author'], stat['author_gb'])
    if not data['group'] == '':
        rank_count_op(data['group'] , stat['group'])
for i in os.listdir(BASE_DIR + '/database/'):
    if i[-4:] == '.txt':
        with open(os.path.join(BASE_DIR + '/database/', i), 'r') as f: # for each small-pack
            threads = json.loads(f.read())
            for t in threads: # for each thread
                if not type(t['data']) == dict:
                    categories[''].stats['thread_count'] += 1
                    if t['data'] == 'unknown-error': # blocked thread
                        categories[''].stats['blocked_thread'] += 1
                    continue
                ks = get_keys(t['data']) + [''] # split
                for k in ks:
                    if not k in categories:
                        categories[k] = stats_category()
                    writein_stat(t['data'], categories[k].stats, t['tid']) # writeIn
                print(t['tid'], 'got')
c = 0
for cate in categories:
    c += 1
    print(c, '/', categories.keys().__len__(), '-', cate)
    with open(BASE_DIR + '/stats/' + ('@' if cate == '' else cate.replace('/','-')) + '.txt', 'w+') as f:
        f.write(json.dumps(categories[cate].stats, indent=4))