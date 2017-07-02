

f = r'C:\Users\Administrator\Desktop\select_sum_count_price__as_s__type_code_.csv'
content=None

with open(f) as of:
    content = of.read()

res = {}
for line in content.split('\n'):
    if len(line) > 0:
        amount, t, code = line.split(',')
        amount = float(amount)
        if code not in res:
            res[code] = {}
            res[code]['diff'] = 0
            if t == 'B':
                res[code]['diff'] += amount
            else:
                res[code]['diff'] -= amount
            res[code][t] = amount
        else:
            if t == 'B':
                res[code]['diff'] += amount
            else:
                res[code]['diff'] -= amount
            res[code][t] = amount

print(res)
final_res = {}
for x in res:
    if res[x]['diff'] > 0:
        final_res[x] = res[x]['diff']


print (sorted(final_res.items(), key=lambda d: -d[1]))
# diff_great = [x['diff'] > 10*0000 for x in res ]
# print(diff_great)
