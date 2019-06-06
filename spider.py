import requests
from lxml import etree
import random
import csv
import re
import time
import json
import certifi

with open('region_id.json','r',encoding='utf-8') as file:
    data = json.load(file)

def region(id):
    name=data[id]
    return name

proxies = ['51.15.227.220:3128', '81117.191.11.75:8080', '117.191.11.110:80', '1.162.56.154:8081', '117.191.11.76:80',
           '117.191.11.78:8080',
           '117.191.11.77:8080', '17.191.11.79:8080',
           '117.191.11.71:8080', '117h.191.11.73:8080', '39.137.107.98:8080', '39.137.69.6:8080'
           ]
headers = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1","Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

food_dict = {'5':'美食_回教','12':'美食_居酒屋','16':'美食_素食','17':'美食_咖啡廳','70':'美食_餐廳'}
hotel_dict = {'79':'住宿_豪華','80':'住宿_中等價位','81':'住宿_經濟實惠'}
tour_dict = {'28':'觀光_博物館與美術館','30':'觀光_溫泉','31':'觀光_主題公園','72':'觀光_景點與地標','73':'觀光_自然與四季','74':'觀光_公園與庭園','75':'觀光_戶外活動','76':'觀光_導覽','77':'觀光_推薦行程','78':'觀光_懶人包',
             '85':'觀光_活動','86':'觀光_課程活動及工作訪'}
dicts = {}
for d in [food_dict, hotel_dict, tour_dict]:
    dicts.update(d)

def start_atricle(url):

    resp = requests.get(url, headers={"User-Agent": random.choice(headers)},proxies={'http': 'http://' + random.choice(proxies)},
                        verify=True)
    html = etree.HTML(resp.text)
    articles=[]

    article_url = html.xpath("//div[@class='c-section']/ul[@class='c-horizontalList']/li/div[@class='content']/h3/a/@href")
    for article in article_url:
        articles.append("https://matcha-jp.com"+article)
    return articles



def next_page(url):
    resp = requests.get(url, headers={"User-Agent": random.choice(headers)},proxies={'http': 'http://' + random.choice(proxies)},
                        verify=True)
    html = etree.HTML(resp.text)
    next = []
    next_one = html.xpath("//div[@class='c-pagination']/a[@class='paginationNextBtn']/@href")
    if next_one == []:
        print("This is the final page.")
    else:
        for str in next_one:
            next.append("https://matcha-jp.com" + str)
    return next

def next_list(url):
    mylist = []
    mylist.append(url)
    next_pages = next_page(url)

    while next_pages!=[]:
        mylist.append(next_pages[0])
        next_pages = next_page(next_pages[0])

    return mylist


def crawl(url,category):
    result={}
    resp = requests.get(url, headers={"User-Agent": random.choice(headers)},proxies={'http': 'http://' + random.choice(proxies)},
                        verify=True)
    html = etree.HTML(resp.text)
    article_title = html.xpath("//h1[@class='title']/text()")
    article_date = html.xpath("//p[@class='meta']/span/text()")
    article_area = html.xpath("//p[@class='meta']/a/span/text()")  # 取index=0
    article_author = html.xpath("//p[@class='name']/a/text()")
    content = html.xpath("//div[@class='article_content tw']")
    content_list = []
    for cnt in content:
        string = cnt.xpath("string(.)")
        string.replace("\n", "")
        content_list.append(string.strip())
    article_content = "".join(content_list)
    result['article_title'] = article_title[0]
    result['article_date'] = article_date[0]
    result['article_area'] = article_area[0]
    result['article_category'] = dicts[category]
    result['article_author'] = article_author[0]
    result['article_content'] = article_content
    return result

def readcsv(file):
    with open(file,"r") as csvfile:
        myurl=[]
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            for url in row:
                myurl.append(url)
        return myurl
#
if __name__=="__main__":
    myurl = readcsv("./food_url.csv")
    # myurl = ['https://matcha-jp.com/tw/list/?region=32&category=17','https://matcha-jp.com/tw/list/?region=41&category=73']
    filename = 'food_result.json'
    print('start our crawling.')
    for url in myurl:
        ranking = []
        latest = []
        category_number = url.split("&")[1].split('=')[1]
        region_id = url.split("&")[0].split('=')[1]
        print('start:',url)
        myarticle = start_atricle(url)
        if myarticle == []:
            print('There is no article.')
            continue
        #將文章分成熱門文章與最新文章
        article_ranking=myarticle[0:int((len(myarticle)/2))]
        article_latest = myarticle[int(len(myarticle)/2):int(len(myarticle))]
        #完成首頁的爬取，裡面有分熱門文章與最新文章
        #若是使用list comprehesive
        #ranking_list = [crawl(ar,category) for ar in article_ranking];rank+=ranking_list
        for ar in article_ranking:
            print('start:',ar)
            ranking.append(crawl(ar,category_number))

        print('Finished the first page ranking article')
        for al in article_latest:
            print('start: ', al)
            latest.append(crawl(al,category_number))
        print('Finished the first page latest article')
        #有兩個下一頁按鈕，分別獲得
        print('start to get next page button.')
        next_button = next_page(url)
        if len(next_button)==0:
            print('There is no next page button')
            tmp = ranking + latest
            with open('./'+filename, 'a', encoding='utf-8') as file:
                json.dump(tmp, file, ensure_ascii=False)
            continue
        ranking_button = next_button[0]
        latest_button = next_button[1]
        print('Get all next page button.')
        #獲得熱門文章有幾頁，最新文章有幾頁
        print('start to get next page list.')
        ranking_list = next_list(ranking_button)
        latest_list = next_list(latest_button)
        print('Get all next page url.')
        #先獲得文章的網址，在獲取文章的內容
        for rl in ranking_list:
            art_rkg = start_atricle(rl)
            print('start:',rl)
            for ar in art_rkg:
                print('start:', ar)
                ranking.append(crawl(ar,category_number))
        print('Finisged all ranking article.')
        for ll in latest_list:
            art_lat = start_atricle(ll)
            print('start:', ll)
            for arl in art_lat:
                print('start:', arl)
                latest.append(crawl(arl,category_number))
        print('Finished all latest article.')
        output = ranking + latest
        with open('./'+filename,'a',encoding='utf-8') as file:
            json.dump(output, file,ensure_ascii=False)

    with open('./'+filename,'r',encoding='utf-8') as file:
        with open('./output_food.json', 'w+', encoding='utf-8') as files:
            line = file.read()
            content = line.replace('][',',')
            files.write(content)