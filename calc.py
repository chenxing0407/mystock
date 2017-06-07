import easyquotation
import operator

sina = easyquotation.use('sina')

earn = {}
sell_earn = {}
buy = open('/root/sort_buy').read().split('\n')
sell = open('/root/sort_sell').read().split('\n')
# sorted_all = sorted()
for stcode, st in sina.all_market.items():
    for line in buy[:]:
        if len(line) > 0:
            code = line[4:10]
            price = float(line.split(' ')[-1])
            if stcode[2:] == code:
                if stcode not in earn:
                    earn[stcode] = st['now'] - price
                else:
                    earn[stcode] += (st['now'] - price)
                buy.remove(line)
    line = ''
    for line in sell[:]:
        if len(line) > 0:
            code = line[5:11]
            price = float(line.split(' ')[-1])
            if stcode[2:] == code:
                if stcode not in sell_earn:
                    sell_earn[stcode] = price - st['now']
                else:
                    sell_earn[stcode] += ( price - st['now'] )
                    sell.remove(line)

print (earn)
buy_sum = 0.0
for s in earn:
    buy_sum+=earn[s]

sorted_x = sorted(earn.items(), key=operator.itemgetter(1))
print(sorted_x)
print('##############')

print (sell_earn)
sell_sum = 0.0
for s in sell_earn:
    sell_sum +=sell_earn[s]

sorted_y = sorted(sell_earn.items(), key=operator.itemgetter(1))
print(sorted_y)
print('##############')
print('buy %s, sell %s' % (buy_sum, sell_sum))