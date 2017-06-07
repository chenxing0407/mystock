#!/usr/bin/env python
# -*- coding: utf-8 -*-
import easyquotation


def get_candidate_code():
    qq = easyquotation.use('qq')
    candi = []
    for code, st in qq.all_market.items():
        try:
            if st['流通市值'] < 200: #市值小于
                candi.append(st['code'])
        except Exception as e:
            print(e)
            continue
    return candi

