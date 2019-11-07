import os,json

DATABASE = os.path.dirname(__file__) + '/database/'

def value_conditional(value, condition='') -> bool:
    if condition == '' or condition == None:
        return True
    elif condition[0:4] == 'has:':
        return value.count(condition[4:]) > 0
    elif condition[0:2] == '>=':
        return value >= int(condition[2:])
    elif condition[0:2] == '<=':
        return value <= int(condition[2:])
    elif condition[0] == '>':
        return value > int(condition[1:])
    elif condition[0] == '<':
        return value < int(condition[1:])
    elif condition[0] == '=':
        return str(value) == condition[1:].strip() if not type(value) == str else value.strip() == condition[1:].strip()
    elif condition[0] == '!':
        return not str(value) == condition[1:].strip() if not type(value) == str else not value.strip() == condition[1:].strip()
    else:
        return False

def value_multi_conditional(value, conditions = '', logic = 'and'):
    condition_list = conditions.split(',')
    if conditions == '' or conditions == None:
        return True
    if logic == 'and':
        for i in condition_list:
            if not value_conditional(value, i):
                return False
        return True
    elif logic == 'or':
        for i in condition_list:
            if value_conditional(value, i):
                return True
        return False
    elif logic == 'not and':
        for i in condition_list:
            if not value_conditional(value, i):
                return True
        return False
    elif logic == 'not or':
        for i in condition_list:
            if value_conditional(value, i):
                return False
        return True
    else:
        print('Unknown logic. And return False.')
        return False

def splited_key(objective, split=''):
    if not type(objective) == str:
        if split == '':
            return ''
        date = objective['time'].split(' ')[0]
        ymd = date.split('-')
        if split == 'y' :
            return ymd[0]
        elif split == 'm' :
            return ymd[0]+'-'+ymd[1]
        elif split == 'd' :
            return date
        elif split == 'c':
            return objective['category']
        elif split == 'cs':
            return objective['category']+'-'+objective['subcategory']
    return ''

def foreach_pack(container, function, temp_value=None, splitted=True):
    for i in os.listdir(DATABASE):
        if i[-4:] == '.txt':
            with open(os.path.join(DATABASE, i), 'r') as f: # for each small-pack
                threads = json.loads(f.read())
                for t in threads: # for each thread
                    if temp_value == None:
                        function(container, t)
                    else:
                        function(container, t, temp_value)
    if splitted:
        return container
    else:
        return container['']

def binary_insert(container: list, data, max_length=None, order='descend', sort_value_index=0):
    if container.__len__() == 0:
        container.append(data)
        return
    left, right = 0, container.__len__() - 1
    d, c = data, container
    if data == list or data == dict or data == tuple:
        d = data[sort_value_index]
        c = [x[sort_value_index] for x in container]
    if not max_length == None and max_length == container.__len__():
        if (order == 'descend' and d < c[-1]) or (order == 'ascend' and d > c[-1]):
            return
    while (left <= right):
        mid = (int)((left + right) / 2)
        if (order == 'descend' and d > c[mid]) or (order == 'ascend' and d < c[mid]):
            right = mid - 1
        elif (order == 'descend' and d < c[mid]) or (order == 'ascend' and d > c[mid]):
            left = mid + 1
        else:
            container.insert(mid, data)
            break
        if (left > right):
            container.insert(left, data)
    if not max_length == None and max_length < container.__len__():
        container.pop()


def data_count(target: str, conditions = '', logic = 'and', split = '', conditional_sections:list = None):
    '''
    Data count.

    :param target: target property. ('@' means the thread itself)\n
    :param conditions: conditions of properties. (support '>', '<', '>=', '<=', '=', '!', 'has:' at beginning) ('' or None or Null means no condition) \n
    :param logic: logic between conditions. ('and', 'or', 'not and', 'not or')\n
    :param split: split by time(y,m,d) or category(c) or category+subcategory(cs). ('', None means no split)\n
    :param conditional_sections: further split by sections via conditions. (None means no section)\n
    '''
    splitted = not (split == '' or split == None) or not conditional_sections == None 
    if conditional_sections == None:
        conditional_sections = ['']
    def function(container, thread, conditional_sections):
        k = splited_key(thread['data'], split=split if not split == None else '')
        if target == '@' and value_multi_conditional(str(thread['data']), conditions, logic):
            for c in conditional_sections:
                if value_multi_conditional(str(thread['data']), c):
                    kc = k + ('' if c == '' else ' ' + c if not k == '' else c)
                    if not kc in container:
                        container[kc] = 1
                    else:
                        container[kc] += 1
        elif not target == '@' and not type(thread['data']) == str and value_multi_conditional(thread['data'][target], conditions, logic):
            for c in conditional_sections:
                if value_multi_conditional(thread['data'][target], c):
                    kc = k + ('' if c == '' else ' ' + c if not k == '' else c)
                    if not kc in container:
                        container[kc] = 1
                    else:
                        container[kc] += 1
    return foreach_pack({}, function, splitted=splitted, temp_value=conditional_sections)

def data_sum(target: str, conditions = '', logic = 'and', split = '', conditional_sections:list = None):
    '''
    Data sum.

    :param target: target property. (type int only)\n
    :param conditions: conditions of properties. (support '>', '<', '>=', '<=', '=', '!', 'has:' at beginning) ('' or None or Null means no condition) \n
    :param logic: logic between conditions. ('and', 'or', 'not and', 'not or')\n
    :param split: split by time(y,m,d) or category(c) or category+subcategory(cs). ('', None means no split)\n
    :param conditional_sections: further split by sections via conditions. (None means no section)\n
    '''
    splitted = not (split == '' or split == None) or not conditional_sections == None 
    if conditional_sections == None:
        conditional_sections = ['']
    def function(container, thread, conditional_sections):
        k = splited_key(thread['data'], split=split if not split == None else '')
        if not target == '@' and not type(thread['data']) == str and type(thread['data'][target]) == int and value_multi_conditional(thread['data'][target], conditions, logic):
            for c in conditional_sections:
                if value_multi_conditional(thread['data'][target], c):
                    kc = k + ('' if c == '' else ' ' + c if not k == '' else c)
                    if not kc in container:
                        container[kc] = thread['data'][target]
                    else:
                        container[kc] += thread['data'][target]
    return foreach_pack({}, function, splitted=splitted, temp_value=conditional_sections)

def rank_value(target: str, conditional_target: str = None, conditions = '', logic = 'and', split = '', limit=50, order='descend'):
    '''
    Rank by a certain property value in a thread.

    :param target: target property. (type int only)\n
    :param conditional_target: conditional property.\n
    :param conditions: conditions of conditional properties. (support '>', '<', '>=', '<=', '=', '!', 'has:' at beginning) ('' or None or Null means no condition) \n
    :param logic: logic between conditions. ('and', 'or', 'not and', 'not or')\n
    :param split: split by time(y,m,d) or category(c) or category+subcategory(cs). ('', None means no split)\n
    :param limit: max length of the rank.\n
    :param order: 'ascend' or 'descend'.\n
    '''
    def function(container, thread, mark):
        k = splited_key(thread['data'], split=split if not split == None else '')
        if not target == '@' and not type(thread['data']) == str and type(thread['data'][target]) == int and (value_multi_conditional(thread['data'][conditional_target], conditions, logic) if not conditional_target == None else True):
            if not k in container:
                container[k] = [(thread['data'][target], thread['tid'])]
            else:
                binary_insert(container[k], (thread['data'][target], thread['tid']), max_length=limit, order=order, sort_value_index=0)
    return foreach_pack({}, function, temp_value=0, splitted=not (split == '' or split == None))

def rank_times(target: str, repeatable = True, conditional_target: str = None, conditions = '', logic = 'and', split = '', limit=50, order='descend'):
    '''
    Rank by times of presence.

    :param target: target property. (include list)\n
    :param target: if items in a target list can appear more than twice.\n
    :param conditional_target: conditional property.\n
    :param conditions: conditions of conditional properties. (support '>', '<', '>=', '<=', '=', '!', 'has:' at beginning) ('' or None or Null means no condition) \n
    :param logic: logic between conditions. ('and', 'or', 'not and', 'not or')\n
    :param split: split by time(y,m,d) or category(c) or category+subcategory(cs). ('', None means no split)\n
    :param limit: max length of the rank. None means no limit.\n
    :param order: 'ascend' or 'descend'.\n
    '''
    def function(container, thread):
        k = splited_key(thread['data'], split=split if not split == None else '')
        if not target == '@' and not type(thread['data']) == str and (value_multi_conditional(thread['data'][conditional_target], conditions, logic) if not conditional_target == None else True):
            if not k in container:
                container[k] = {}
            if type(thread['data'][target]) == list:
                if not repeatable:
                    thread['data'][target] = list(set(thread['data'][target]))
                for v in thread['data'][target]:
                    if not v in container[k]:
                        container[k][v] = 1
                    else:
                        container[k][v] += 1
            else:
                if not thread['data'][target] in container[k]:
                    container[k][thread['data'][target]] = 1
                else:
                    container[k][thread['data'][target]] += 1
    r = foreach_pack({}, function, splitted=not (split == '' or split == None))
    if split == '' or split == None:
        p = [(x,y) for x,y in r.items()]
        return sorted(p, key = lambda x:x[1], reverse=order=='descend') if limit == None else sorted(p, key = lambda x:x[1], reverse=order=='descend')[:limit]
    else:
        t = {}
        for z,w in r.items():
            p = [(x,y) for x,y in w.items()]
            t[z] = sorted(p, key = lambda x:x[1], reverse=order=='descend') if limit == None else sorted(p, key = lambda x:x[1], reverse=order=='descend')[:limit]
        return t