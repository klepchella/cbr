#!/usr/bin/python
#coding: utf-8

import lxml.html as html
import requests
from datetime import datetime

today = datetime.now().strftime('%d.%m.%Y')

cbr_url = 'http://www.cbr.ru/currency_base/daily.aspx?date_req=' + today

sheet = requests.get(cbr_url)
with open('/home/sentra/PycharmProjects/cbr_parser/test.html', 'w') as output_file:
  output_file.write(sheet.text.encode('utf-8'))

tree = html.fromstring(sheet.text)
table = tree.xpath('//table[@class="data"]')
tr = table[0].xpath('.//tr')  # список всех строк

col = []
for u in tr[1:]:
    try:
        str_table = u.xpath('.//td')
        if str_table[1].text in ['USD', 'EUR', 'GBP']:
            col.append((today, [i.text for i in str_table[1:4]], float(str_table[-1].text.replace(',', '.'))))
    except IndexError:
        continue

with open('/home/sentra/PycharmProjects/cbr_parser/statistics.txt', 'a') as result_file:
    for val in col:
        result_file.write(''.join([val[0], '\t', val[1][0].encode('utf-8'), '\t', val[1][1], '\t', val[1][2].encode(
            'utf-8'), '\t', str(val[2]), '\n']))

