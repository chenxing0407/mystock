#!/usr/bin/env python
# -*- coding: utf-8 -*-
import easyquotation
import candidate_code
import time
import threading
import datetime
import os
import easyutils

last_check = {}
NOW = datetime.datetime.now()
KP = NOW.replace(hour=9, minute=25)
LUNCH = NOW.replace(hour=11, minute=30)
KP2 = NOW.replace(hour=13, minute=0)
TEN = NOW.replace(hour=10, minute=15)
THREE = NOW.replace(hour=15, minute=1)
DATA_DIR = '/root/stock_data_count/'
# DATA_DIR = 'c:'
data_dir = DATA_DIR + os.sep + str(datetime.date.today())


def get_real(candi):
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
            time.sleep(36000)
        for code, st in sina.stocks(candi).items():
            try:
                if st['name'] not in last_check:
                    last_check[st['name']] = {}
                    last_check[st['name']]['turnover'] = st['turnover']
                    last_check[st['name']]['buy'] = st['buy']
                    last_check[st['name']]['rec'] = []
                    last_check[st['name']]['buy_count'] = 0
                    last_check[st['name']]['sell_count'] = 0

                else:
                    if last_check[st['name']]['turnover'] == st['turnover']: # no change
                        pass
                    else:
                        diff = st['turnover'] - last_check[st['name']]['turnover']
                        if st['bid1'] > last_check[st['name']]['buy']:
                            rec = 'B,%s,%s,%s\n' % (diff, st['buy'], st['time'])
                            if st['buy']*diff > 1000000: # 发出买入指令
                                last_check[st['name']]['buy_count'] += 1
                                if last_check[st['name']]['sell_count'] % 3 == 0:
                                    if code not in mydata.BUY_COMMAND:
                                        mydata.BUY_COMMAND[code] = []
                                        mydata.BUY_COMMAND[code].append('buy %s at %s with price %s\n' % (code, time.ctime(), st['now']))
                                    else:
                                        mydata.BUY_COMMAND[code].append(
                                            'buy %s at %s with price %s\n' % (
                                            code, time.ctime(), st['now']))

                                if len(mydata.BUY_COMMAND[code]) > 10 or now > THREE:
                                    with open(data_dir + os.sep + 'buy_' + code, 'a') as f:
                                        f.write(''.join(mydata.BUY_COMMAND[code]))
                                    mydata.BUY_COMMAND[code] = []
                        elif st['bid1'] < last_check[st['name']]['buy']:
                            rec = 'S,%s,%s,%s\n' % (diff, st['buy'], st['time'])

                            if st['buy'] * diff > 1000000:  # 发出卖出指令
                                last_check[st['name']]['sell_count'] += 1
                                if last_check[st['name']]['sell_count'] % 3 == 0:
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
                            rec = 'M,%s,%s,%s\n' % (diff, st['buy'], st['time'])

                        last_check[st['name']]['rec'].append(rec)
                        if len(last_check[st['name']]['rec']) > 60 or now > THREE:
                            with open(data_dir + os.sep + code + '_' + st['date'], 'a') as f:
                                f.write(''.join(last_check[st['name']]['rec']))
                            last_check[st['name']]['rec'] = []

                        last_check[st['name']]['turnover'] = st['turnover']
                        last_check[st['name']]['buy'] = st['buy']
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


