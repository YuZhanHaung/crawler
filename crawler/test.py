import re
teststring ='作者: gyoko (gyoko) 看板: Japan_Travel 標題: [遊記] 08夏末JR PASS日本趴趴走（8天夜車的瘋狂之旅XD）\n 時間: Mon Sep  2 22:51:36 2008'
pat = '時間: ([a-zA-Z]{3}.[a-zA-Z]{3}..{1,2} \d{2}:\d{2}:\d{2} \d{4})'
# result = re.compile(pat,re.S).findall()

a = [1,2,3,4,5,None]

result2 = [i + 1 for i in a if i]
print(result2)