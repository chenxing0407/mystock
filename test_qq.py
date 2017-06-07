import easyquotation

qq = easyquotation.use('sina')

print(qq.stocks('gb_$dji'))

# curl 'http://hq.sinajs.cn/rn=1497019696583&list=gb_$dji,gb_ixic,gb_$inx,hf_GC,hf_CL,DINIW,s_sh000001,rt_hkHSI,b_NKY' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Host: hq.sinajs.cn' -H 'Referer: http://stock.finance.sina.com.cn/usstock/quotes/CCCL.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
'''
{'600926': {'name': '杭州银行', 'code': '600926', 'now': 21.6, 'close': 21.35,
'open': 21.24, 'volume': 16328600.0, 'bid_volume': 8190000, 'ask_volume': 8138600.0,
'bid1': 21.6, 'bid1_volume': 5000, 'bid2': 21.59, 'bid2_volume': 10400, 'bid3': 21.58,
'bid3_volume': 19100, 'bid4': 21.57, 'bid4_volume': 13200, 'bid5': 21.56, 'bid5_volume': 14000,
'ask1': 21.61, 'ask1_volume': 16200, 'ask2': 21.62, 'ask2_volume': 8600, 'ask3': 21.63,
'ask3_volume': 10400, 'ask4': 21.64, 'ask4_volume': 13300, 'ask5': 21.65, 'ask5_volume': 17600,
'最近逐笔成交': '
15:00:01/21.61/27/B/58322/30927|
14:59:58/21.61/7/B/15127/30919|
14:59:55/21.60/26/S/56166/30913|
14:59:52/21.61/15/B/32405/30905|
14:59:49/21.59/49/S/105848/30900|
14:59:46/21.59/45/S/97163/30895',
'datetime': datetime.datetime(2017, 6, 1, 15, 5, 52), '涨跌': 0.25, '涨跌(%)': 1.17,
'high': 21.94, 'low': 21.22, '价格/成交量(手)/成交额': '21.61/163259/353905551',
'成交量(手)': 16328600, '成交额(万)': 353960000.0, 'turnover': 6.24, 'PE': 14.06,
'unknown': '', 'high_2': 21.94, 'low_2': 21.22, '振幅': 3.37, '流通市值': 56.54,
'总市值': 565.37, 'PB': 1.42, '涨停价': 23.49, '跌停价': 19.22}}
'''


'''
{'600926': {'name': '杭州银行', 'open': 15.6, 'close': 15.69, 'now': 15.6, 'high': 15.6, 'low': 15.6, 'buy': 15.58,
'sell': 15.6, 'turnover': 116600, 'volume': 1818960.0,
'bid1_volume': 14400, 'bid1': 15.58, 'bid2_volume': 27800, 'bid2': 15.57, 'bid3_volume': 5000, 'bid3': 15.56,
'bid4_volume': 13100, 'bid4': 15.55, 'bid5_volume': 200, 'bid5': 15.54,
'ask1_volume': 11300, 'ask1': 15.6, 'ask2_volume': 8100, 'ask2': 15.61, 'ask3_volume': 23280, 'ask3': 15.62,
'ask4_volume': 3100, 'ask4': 15.63, 'ask5_volume': 3100, 'ask5': 15.65, 'date': '2017-06-08', 'time': '09:26:25'}}


'''