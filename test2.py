import requests
import re
import json
from lxml import etree
URL='http://www.xiladaili.com/https/'
resp = requests.get(URL)
text = resp.text
html = etree.HTML(text)
#
# pat = '<td>([0-9]*.[0-9]*.[0-9]*.[0-9]*:[0-9]*)</td>'
# ip = re.compile(pat).findall(html)
ip = html.xpath('//tbody/tr/td[1]')

with open('./ip.txt','w',encoding='utf-8') as file:
    for item in ip:
        file.write("%s\n" % item.text)

