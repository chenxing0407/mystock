#!/usr/bin/env python
# -*- coding: utf-8 -*-
import easyquotation
import candidate_code
import time
import threading
import datetime
import os
import easyutils

from db.util import get_session
from db.util import StockDaDantHistory

last_check = {}
NOW = datetime.datetime.now()
KP = NOW.replace(hour=9, minute=25)
LUNCH = NOW.replace(hour=11, minute=30)
KP2 = NOW.replace(hour=13, minute=0)
TEN = NOW.replace(hour=10, minute=15)
THREE = NOW.replace(hour=15, minute=1)
DATA_DIR = '/root/stock_data/'
# DATA_DIR = 'c:'
data_dir = DATA_DIR + os.sep + str(datetime.date.today())



'''

if now > last[now] B,

elif now < last[now]
  if now == buy:
     M
   else:
    S
else # now == buy
  if ask1 > last[ask1]:
    B

'''

'''
价格无变动
now == buy
  buy > last_buy
    B
  else:
    S

now == sell
  B



价格减少
   now == buy
     S
   now == sell:
     sell < last_sell
       S
     else：
       M


价格增加：
sell < last_sell
 M
else:
   B

'''

def add_to_db(dadan):
    print('over %s' % VALVE)
    sess = get_session()
    sess.begin()
    sess.add(dadan)
    sess.commit()

VALVE = 50*10000
def get_real(candi):
    sess = get_session()
    mydata = threading.local()
    mydata.BUY_COMMAND = {}
    mydata.SELL_COMMAND = {}
    sina = easyquotation.use('sina')
    while True:
        now = datetime.datetime.now()
        while now < KP:
            time.sleep(10)
            now = datetime.datetime.now()

        while now > LUNCH and now < KP2:
            time.sleep(10)
            now = datetime.datetime.now()
        if now > THREE:
            time.sleep(600)
        for code, st in sina.stocks(candi).items():
            try:
                if st['name'] not in last_check:
                    last_check[st['name']] = {}
                    last_check[st['name']]['turnover'] = st['turnover']
                    last_check[st['name']]['now'] = st['now']
                    last_check[st['name']]['buy'] = st['buy']
                    last_check[st['name']]['sell'] = st['sell']
                    last_check[st['name']]['rec'] = [] # 详细记录

                else:
                    if last_check[st['name']]['turnover'] == st['turnover']: # no change
                        pass
                    else:
                        diff = st['turnover'] - last_check[st['name']]['turnover']
                        if st['now'] == last_check[st['name']]['now']:
                            if st['now'] == st['buy']:
                                if st['buy'] > last_check[st['name']]['buy']:
                                    rec = 'B,%s,%s,%s\n' % (
                                    diff, st['now'], st['time'])
                                    if st['now'] * diff > VALVE:  # 发出买入指令

                                        dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'], name=st['name'],
                                                                   type='B', count=diff, price=st['now'], high=st['high'], low=st['low'])
                                        add_to_db(dadan)

                                        if code not in mydata.BUY_COMMAND:
                                            mydata.BUY_COMMAND[code] = []
                                            mydata.BUY_COMMAND[code].append(
                                                'buy %s at %s with price %s\n' % (
                                                code, time.ctime(), st['now']))
                                        else:
                                            mydata.BUY_COMMAND[code].append(
                                                'buy %s at %s with price %s\n' % (
                                                    code, time.ctime(),
                                                    st['now']))

                                        if len(mydata.BUY_COMMAND[
                                                   code]) > 10 or now > THREE:
                                            with open(
                                                                            data_dir + os.sep + 'buy_' + code,
                                                                            'a') as f:
                                                f.write(''.join(
                                                    mydata.BUY_COMMAND[code]))
                                else:
                                    rec = 'S,%s,%s,%s\n' % (
                                    diff, st['now'], st['time'])
                                    if st['now'] * diff > VALVE:  # 发出卖出指令
                                        dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'], name=st['name'],
                                                                   type='S', count=diff, price=st['now'], high=st['high'], low=st['low'])
                                        add_to_db(dadan)
                                        if code not in mydata.SELL_COMMAND:
                                            mydata.SELL_COMMAND[code] = []
                                            mydata.SELL_COMMAND[code].append(
                                                'sell %s at %s with price %s\n' % (
                                                    code, time.ctime(),
                                                    st['now']))
                                        else:
                                            mydata.SELL_COMMAND[code].append(
                                                'sell %s at %s with price %s\n' % (
                                                    code, time.ctime(),
                                                    st['now']))
                                        if len(mydata.SELL_COMMAND[
                                                   code]) > 10 or now > THREE:
                                            with open(
                                                                            data_dir + os.sep + 'sell_' + code,
                                                                            'a') as f:
                                                f.write(''.join(
                                                    mydata.SELL_COMMAND[code]))
                                            mydata.SELL_COMMAND[code] = []
                            if st['now'] == st['sell']:
                                rec = 'B,%s,%s,%s\n' % (diff, st['now'], st['time'])
                                if st['now'] * diff > VALVE:  # 发出买入指令
                                    dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'],
                                                               name=st['name'],
                                                               type='B', count=diff, price=st['now'], high=st['high'],
                                                               low=st['low'])
                                    add_to_db(dadan)
                                    if code not in mydata.BUY_COMMAND:
                                        mydata.BUY_COMMAND[code] = []
                                        mydata.BUY_COMMAND[code].append(
                                            'buy %s at %s with price %s\n' % (
                                                code, time.ctime(), st['now']))
                                    else:
                                        mydata.BUY_COMMAND[code].append(
                                            'buy %s at %s with price %s\n' % (
                                                code, time.ctime(),
                                                st['now']))

                                    if len(mydata.BUY_COMMAND[
                                               code]) > 10 or now > THREE:
                                        with open(
                                                                        data_dir + os.sep + 'buy_' + code,
                                                'a') as f:
                                            f.write(''.join(
                                                mydata.BUY_COMMAND[code]))
                            # else:
                            #     rec = 'B,%s,%s,%s\n' % (diff, st['now'], st['time'])
                            #     if st['now']*diff > VALVE:  # 发出买入指令
                            #         if code not in mydata.BUY_COMMAND:
                            #             mydata.BUY_COMMAND[code] = []
                            #             mydata.BUY_COMMAND[code].append('buy %s at %s with price %s\n' % (code, time.ctime(), st['now']))
                            #         else:
                            #             mydata.BUY_COMMAND[code].append(
                            #                 'buy %s at %s with price %s\n' % (
                            #                 code, time.ctime(), st['now']))
                            #
                            #         if len(mydata.BUY_COMMAND[code]) > 10 or now > THREE:
                            #             with open(data_dir + os.sep + 'buy_' + code, 'a') as f:
                            #                 f.write(''.join(mydata.BUY_COMMAND[code]))
                            #         mydata.BUY_COMMAND[code] = []
                        elif st['now'] < last_check[st['name']]['now']:
                            if st['now'] == st['sell']:
                                if st['sell'] < last_check[st['name']]['sell']:
                                    rec = 'S,%s,%s,%s\n' % (diff, st['buy'], st['time'])
                                    if st['now'] * diff > VALVE:  # 发出卖出指令
                                        dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'], name=st['name'],
                                                                   type='S', count=diff, price=st['now'], high=st['high'], low=st['low'])
                                        add_to_db(dadan)
                                        if code not in mydata.SELL_COMMAND:
                                            mydata.SELL_COMMAND[code] = []
                                            mydata.SELL_COMMAND[code].append(
                                                'sell %s at %s with price %s\n' % (
                                                    code, time.ctime(),
                                                    st['now']))
                                        else:
                                            mydata.SELL_COMMAND[code].append(
                                                'sell %s at %s with price %s\n' % (
                                                    code, time.ctime(),
                                                    st['now']))
                                        if len(mydata.SELL_COMMAND[
                                                   code]) > 10 or now > THREE:
                                            with open(
                                                                            data_dir + os.sep + 'sell_' + code,
                                                                            'a') as f:
                                                f.write(''.join(
                                                    mydata.SELL_COMMAND[code]))
                                            mydata.SELL_COMMAND[code] = []
                                else:
                                    rec = 'M,%s,%s,%s\n' % (diff, st['buy'], st['time'])
                            else:
                                rec = 'S,%s,%s,%s\n' % (diff, st['now'], st['time'])
                                if st['now'] * diff > VALVE:  # 发出卖出指令
                                    print('over %s' % VALVE)
                                    dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'],
                                                               name=st['name'],
                                                               type='S', count=diff, price=st['now'], high=st['high'],
                                                               low=st['low'])
                                    add_to_db(dadan)
                                    if code not in mydata.SELL_COMMAND:
                                        mydata.SELL_COMMAND[code] = []
                                        mydata.SELL_COMMAND[code].append(
                                            'sell %s at %s with price %s\n' % (
                                            code, time.ctime(), st['now']))
                                    else:
                                        mydata.SELL_COMMAND[code].append(
                                            'sell %s at %s with price %s\n' % (
                                                code, time.ctime(), st['now']))
                                    if len(mydata.SELL_COMMAND[code]) > 10 or now > THREE:
                                        with open(data_dir + os.sep + 'sell_' + code, 'a') as f:
                                            f.write(''.join(mydata.SELL_COMMAND[code]))
                                        mydata.SELL_COMMAND[code] = []
                        else:
                            if not (st['sell'] < last_check[st['name']]['sell']):
                                rec = 'B,%s,%s,%s\n' % (
                                diff, st['now'], st['time'])
                                if st['now'] * diff > VALVE:  # 发出买入指令
                                    dadan = StockDaDantHistory(code=code, time=st['time'], date=st['date'],
                                                               name=st['name'],
                                                               type='B', count=diff, price=st['now'], high=st['high'],
                                                               low=st['low'])
                                    add_to_db(dadan)
                                    if code not in mydata.BUY_COMMAND:
                                        mydata.BUY_COMMAND[code] = []
                                        mydata.BUY_COMMAND[code].append(
                                            'buy %s at %s with price %s\n' % (
                                            code, time.ctime(), st['now']))
                                    else:
                                        mydata.BUY_COMMAND[code].append(
                                            'buy %s at %s with price %s\n' % (
                                                code, time.ctime(), st['now']))

                                    if len(mydata.BUY_COMMAND[
                                               code]) > 10 or now > THREE:
                                        with open(
                                                                        data_dir + os.sep + 'buy_' + code,
                                                                        'a') as f:
                                            f.write(''.join(
                                                mydata.BUY_COMMAND[code]))
                                        mydata.BUY_COMMAND[code] = []
                            else:
                                rec = 'M,%s,%s,%s\n' % (
                                diff, st['buy'], st['time'])

                        last_check[st['name']]['rec'].append(rec)
                        if len(last_check[st['name']]['rec']) > 60 or now > THREE:
                            with open(data_dir + os.sep + code + '_' + st['date'], 'a') as f:
                                f.write(''.join(last_check[st['name']]['rec']))
                            last_check[st['name']]['rec'] = []

                        # 更新最新的数据
                        last_check[st['name']]['turnover'] = st['turnover']
                        last_check[st['name']]['now'] = st['now']
                        last_check[st['name']]['buy'] = st['buy']
                        last_check[st['name']]['sell'] = st['sell']
            except Exception as e:
                print(e)
                continue
        print('now is %s' % time.ctime())
        time.sleep(2)


if __name__ == '__main__':
    # candi = candidate_code.get_candidate_code()
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    sina = easyquotation.use('sina')
    stock_codes = sina.load_stock_codes()
    stock_with_exchange_list = [easyutils.stock.get_stock_type(code) + code[-6:]
                                for code in stock_codes]
    request_num = len(stock_with_exchange_list)
    max_num = 400
    t_count = int(request_num/max_num) + 1
    for range_start in range(t_count):
        num_start = max_num * range_start
        num_end = max_num * (range_start + 1)
        # request_list = ','.join(stock_with_exchange_list[num_start:num_end])
        th = threading.Thread(target=get_real, args=(stock_with_exchange_list[num_start:num_end],))
        print('starting one thread....')
        th.start()


