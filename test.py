import json
result=json.loads('{"bar":["baz", null, 1.0, 2]}')

# with open('C:/Users/user/Desktop/yuchan/tip.json','r',encoding='utf-8') as file:
#     lines = file.readlines()
#     with open('./tip.json', 'w', encoding='utf-8') as outputfile:
#         for line in lines:
#             mydict = {}
#             result=json.loads(line)
#             mydict['business_id'] = result['business_id']
#             mydict['text'] =  result['text']
#             outputfile.write(json.dumps(mydict)+'\n')
# with open('./tip_filter.json','r',encoding='utf-8') as file:
#     lines = file.readlines()
#     for line in lines:
#         print(line)ed to convert it into string or serialize it.

import json

# as requested in comment
exDict = {'exDict': 12}
for i in range(0,20):
    with open('./file.txt', 'a') as file:
         file.write('----------' + str(i) + '-------------')
         file.write(json.dumps(exDict)) # use `json.loads` to do the reverse
         file.write('\n')
