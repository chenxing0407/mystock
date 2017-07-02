# mystock

表结构
cjmx: code,price,count,amount,zd,time,type(B,S,M)
stock_info: code,liutong,total,pe,pb
history:id,buy_at,buy_price,buy_count,buy_amount,sell_at,sell_price,sell_count,
        sell_amount,sy(收益)



思路：
根据cjmx 来判断，如果一段时间diff 超过一定值A，查看当时的macd rsi等指标
发出buy 指令，记录buy记录，模拟买

成交明细
http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sh600926&date=2017-06-01&page=53

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



    

{'000401': {'name': '冀东水泥', 'open': 16.09, 'close': 16.12, 'now': 16.25, 'high': 16.27, 
'low': 15.86, 'buy': 16.24, 'sell': 16.25, 'turnover': 50434699, 'volume': 813348476.35,
 'bid1_volume': 158400, 'bid1': 16.24, 'bid2_volume': 62266, 'bid2': 16.23, 
 'bid3_volume': 34500, 'bid3': 16.22, 'bid4_volume': 63100, 'bid4': 16.21, 'bid5_volume': 78400, 
 'bid5': 16.2, 'ask1_volume': 311008, 'ask1': 16.25, 'ask2_volume': 536588, 'ask2': 16.26, 
 'ask3_volume': 292100, 'ask3': 16.27, 'ask4_volume': 255500, 'ask4': 16.28, 
 'ask5_volume': 269900, 'ask5': 16.29, 
 'date': '2017-06-21', 'time': '15:05:03'}}

