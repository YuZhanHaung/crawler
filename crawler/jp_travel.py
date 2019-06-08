from lxml import etree
import requests
import time
import json
import re
# def api(thisapi):
#     resp = requests.get(thisapi)
#     myip = resp.text
#     print('get new ip')
#     return myip
# headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
#                                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#                                                    'Accept-Encoding': 'gzip, deflate, br',
#                                                    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
#                                                    'Connection': 'keep-alive','DNT': '1',}
def my_get(url):
    resp = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'})
    time.sleep(3)
    print('Sataus Code: ',resp.status_code)
    if resp.status_code == 200:
        return resp.text
    else:
        return None
addr = 'https://www.ptt.cc'
count = 0
pat = '([a-zA-Z]{3}.[a-zA-Z]{3}..{1,2} \d{2}:\d{2}:\d{2} \d{4})'
for page in range(1,2):
    url = 'https://www.ptt.cc/bbs/Japan_Travel/index'+str(page)+'.html'
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'})
    resp.encoding='utf-8'
    if resp.status_code == 200:
        print('get web page,page number {}'.format(str(page)))
        print('sleep 3 seconds')
        time.sleep(3)
        print('wake up')
        text = resp.text
        html = etree.HTML(text)
        # 每頁都是20個內容，四個項目個數一致
        element_title = html.xpath("//div[@class='title']/a/text()")
        element_url = html.xpath("//div[@class='title']/a/@href")
        full_url = [addr + u for u in element_url]
        element_author = html.xpath("//div[@class='author']/text()")
        resp_cnt = [my_get(u) for u in full_url]
        element_content = [etree.HTML(u).xpath("//div[starts-with(@class,'bbs-screen')]")[0]
                                        .xpath('string(.)')
                           for u in resp_cnt if u]
        # 每頁的20文章內容寫入，完成後才會進行下一頁
        with open('./dataset/ptt', 'a', encoding='utf-8')as file:
            for i in range(0, len(element_content)):
                my_dict = {}
                my_dict['article_author'] = element_author[i]
                my_dict['article_content'] = element_content[i]
                my_dict['article_title'] = element_title[i]
                date = re.compile(pat, re.S).findall(element_content[i])
                if len(date) > 0:
                    date = date[0]
                else:
                    date = ''
                my_dict['article_date'] = date
                print('page {},item {}'.format(str(page), str(i + 1)))
                print(date)
                file.write(json.dumps(my_dict, ensure_ascii=False))
                file.write('\n')
        print('we sleep 3 seconds,and then we move to next step.')
        time.sleep(3)
        print('wake up')
        print('finish page')
























