import requests
import re
import random
from lxml import etree
import json
import time
import sys


headers_pool = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1","Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
testurl = 'https://www.backpackers.com.tw/'
thisapi = 'http://api.xdaili.cn/xdaili-api//newExclusive/getIp?spiderId=5177a8eb71f64446a9e636777681b209&orderno=DX2019656398nzAtPT&returnType=1&count=1&machineArea='


def api(thisapi):
    resp = requests.get(thisapi)
    myip = resp.text
    print('get new ip')
    return myip


def use_ip(testurl, thisapi):
    for i in range(0,10):
        ip = api(thisapi)
        print(ip)
        check_data = requests.get(testurl,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
        print('status_code',check_data.status_code)
        return ip


def get_page(url,ip):
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
    html = resp.text
    time.sleep(1.5)
    pat = '共(.*?)頁</td>'
    page = int(re.compile(pat).findall(html)[0])
    #回傳一個int的數值，表示總頁數
    return page

def start_crawler(url,ip):
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
    html = resp.text
    time.sleep(1)
    pat_cat = '<a href="(.*?)"><strong>日本\w{2,4}</strong></a>'
    url_list = re.compile(pat_cat).findall(html)
    for ii in range(len(url_list)):
        url_list[ii] = 'https://www.backpackers.com.tw/forum/' + re.sub(r's=.*?;', '', url_list[ii])
    return url_list


def get_article(url,page,ip):
    myurl = url +'&order=desc&page='
    first = myurl+str(page)
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
    html = resp.text
    time.sleep(2)
    pat_url = '<a  href="(.*?)" id=".*">.*?</a>'
    pat_title = '<a  href=".*?" id=".*">(.*?)</a>'
    pat_category = '【(.*?)】'
    url_article = re.compile(pat_url).findall(html)
    category = re.compile(pat_category).findall(html)
    title = re.compile(pat_title).findall(html)
    for ii in range(len(url_article)):
        url_article[ii] = 'https://www.backpackers.com.tw/forum/' + re.sub(r's=.*?;', '', url_article[ii])
        title[ii] = category[ii] + '_' + title[ii]
    return [url_article,title]



def crawl(url,ip):
    content_list=[]
    result=[]
    dateresult=[]
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
    time.sleep(0.7)
    html = etree.HTML(resp.text)
    content = html.xpath('//div[@class="vb_postbit"]')
    mydate = html.xpath('//td[starts-with(@id,"td_post_")]/div[@class="smallfont"]/text()')

    for ii in content:
        string = ii.xpath("string(.)")
        content_list.append(string)
    for d in mydate:
        if re.search(r'(\d{4}-\d{2}-\d{2}, \d{2}:\d{2})',d):
            dateresult.append(d.strip())
    result.append(''.join(content_list))
    result.append(dateresult[0])
    return result

def get_filename(url,ip):
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                   'Accept-Encoding': 'gzip, deflate, br',
                                                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                                                   'Connection': 'keep-alive','DNT': '1',
                                                   'Host': 'www.backpackers.com.tw','Upgrade-Insecure-Requests': '1'},
                                  proxies={'http': 'http://' +ip })
    html = resp.text
    time.sleep(1.2)
    pat = '<a href=".*?"><strong>(日本\w{2,4})</strong></a>'
    filename = re.compile(pat).findall(html)
    return filename





# 獲得起始網頁
# ['https://www.backpackers.com.tw/forum/forumdisplay.php?f=57',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=139',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=43',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=141',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=55',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=138',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=140',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=67',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=282',
# 'https://www.backpackers.com.tw/forum/forumdisplay.php?f=19']

if __name__ == '__main__':
    ip = use_ip(testurl,thisapi)
    mystart = start_crawler('https://www.backpackers.com.tw/forum/forumdisplay.php?f=4',ip)
    filename = get_filename('https://www.backpackers.com.tw/forum/forumdisplay.php?f=4',ip)
    print('we start crawler!')
    print(mystart)
    print(filename)
    for index in range(3,len(mystart)):
        time.sleep(3)
        pages = get_page(mystart[index],ip)
        file = filename[index]
        print('website:',mystart[index],'total pages:',str(pages))
        with open('./'+file+'.txt','a',encoding='utf-8') as output:
            for page in range(56,pages+1):
                if page%5==0:
                    ip = use_ip(testurl,thisapi)
                    time.sleep(5)
                    print('website:', mystart[index],'page:',str(page))
                    article = get_article(mystart[index],page,ip)
                    if article==None:
                        print('we try next page!')
                        continue
                    article_url = article[0]
                    article_title = article[1]
                    print('total items:',str(len(article_url)))
                    for item in range(0,len(article_url)):
                        mydict = {}
                        time.sleep(2)
                        mycontent=crawl(article_url[item],ip)
                        time.sleep(3)
                        mydict['content'] = mycontent[0]
                        mydict['date'] = mycontent[1]
                        mydict['title'] = article_title[item]
                        output.write(json.dumps(mydict,ensure_ascii=False))
                        output.write('\n')
                        print('page',str(page+1),'item',str(item+1))
                else:
                    time.sleep(5)
                    print('website:', mystart[index], 'page:', str(page))
                    article = get_article(mystart[index], page, ip)
                    print(ip)
                    if article == None:
                        print('we try next page!')
                        continue
                    article_url = article[0]
                    article_title = article[1]
                    print('total items:', str(len(article_url)))
                    print(ip)
                    for item in range(0, len(article_url)):
                        print(ip)
                        mydict = {}
                        time.sleep(2)
                        mycontent = crawl(article_url[item],ip)
                        time.sleep(3)
                        mydict['content'] = mycontent[0]
                        mydict['date'] = mycontent[1]
                        mydict['title'] = article_title[item]
                        output.write(json.dumps(mydict, ensure_ascii=False))
                        output.write('\n')
                        print('page', str(page + 1), 'item', str(item + 1))
                        print(ip)

