import  requests
import urllib.request
thisip = '186.248.170.82:53281'

# proxy=urllib.request.ProxyHandler({"http":thisip})
# opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
# urllib.request.install_opener(opener)
# resp=urllib.request.urlopen("http://httpbin.org/ip").read().decode("utf-8","ignore")
resp = requests.get('http://httpbin.org/ip',proxies={'http://':'http://'+thisip})
print(resp.text)