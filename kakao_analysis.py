!pip install konlpy

###############################
 
import re
from collections import Counter
from google.colab import files
from konlpy.tag import Twitter 

# myfile = files.upload()
 
words = []

with open(r'/content/카카오톡 .txt', 'r', encoding='utf-8') as f:
    for line in f:
        # m = re.search(r"^.*?\[\d\d:\d\d\]\s*(.+)$", line)
        # print(m)
        matchOB = re.match("^\[(.+\]?)\[\w+.\d\d:\d\d\]" , line)
        if matchOB:
          # print(matchOB.group())
          m = re.sub("^\[(.+\]?)\[\w+.\d\d:\d\d\]","",line)
          # print(m)
 
        if m:
            # words.extend(re.split(r"\s+", m.group(1)))
            wanted_items = re.search('갖고 싶|갖고싶|사고 싶|사고싶|싶다|싶어|싶은|싶고', line)
            if wanted_items:
              # words.extend(m.split())
              wanted_items2 = re.search('갖고 싶|갖고싶|사고 싶|사고싶|싶다|싶어|싶은|싶고', m)

              if wanted_items2:
                nlpy = Twitter() 
                nouns = nlpy.nouns(m)
                print(nouns)

                print(wanted_items2.group())
                print(m)
                
                print("===========================================================================")
              # words.extend(wanted_items.group())
 
# for word, freq in Counter(words).most_common(10):
#     print("{0:10s} : {1:3d}".format(word, freq))

test = "방탄소년단 개좋아함"
nlpy = Twitter()
nouns = nlpy.nouns(test)
print(nouns)


######################################################################################################################


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import codecs
import binascii

item = u"선바"
print(item)
encode_item = item.encode('utf-8')
item = str(encode_item)
print(item)
item = re.sub('[^A-Za-z0-9]+x',"%",item)
item = item.strip("b")
item = item.strip("'")
print(item)

item_name = []
item_price = []
item_link = []

url = 'https://search.shopping.naver.com/search/all.nhn?query='+item+'&cat_id=&frm=NVSHATC'

with urlopen(url) as response:
  soup = BeautifulSoup(response, 'html.parser')
  print(url)
  i = 1
  j = 1
  for anchor in soup.select("div.basicList_title__3P9Q7"):
    item_name.append("상품명   : " + anchor.get_text())
    i = i + 1
  for anchor in soup.select("span.price_num__2WUXn"):
    item_price.append("가격   : " + anchor.get_text())
    j = j + 1
  
  for i in range(0, 5):
    print(item_name[i])
    print(item_price[i])
    print("=======================")
