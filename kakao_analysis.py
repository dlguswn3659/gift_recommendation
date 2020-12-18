!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

# 한글 깨짐 해결을 위한 폰트 설치
###############################

!pip install konlpy

###############################
 
# Most Frequently Used Words
 
import re
import zipfile
import os
from collections import Counter
from google.colab import files
from konlpy.tag import Twitter 

# myfile = files.upload()
# print("========================")

zip_file_name = ""

for fn in myfile.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(myfile[fn])))
  zip_file_name = fn


print(zip_file_name)

# 파일명에서 선물하고 싶은 상대방의 이름 추출
contact_name = zip_file_name.split("님과")
contact_name = contact_name[0]
print("선물해주고 싶은 사람 : " + contact_name)

################################# 압축 해제하는 구간 ###################################
# path_to_zip_file = '/content/' + zip_file_name
# directory_to_extract_to = '/content'

# with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
#     zip_ref.extractall(directory_to_extract_to)

# print("압축 해제 완료")
########################################################################################

# my_zip = zipfile.ZipFile("/content/MuSE 18 전전 윤종원님과 카카오톡 대화.zip", 'w')  # zip파일 쓰기모드
# zipfile.ZipFile(zip_file_name).extractall()

path = "/content" # 검색하고자하는 폴더 경로
file_names = os.listdir(path)
print(file_names)

context_files = []

for num in file_names:
  m = re.search("Talk", num)
  if m:
    context_files.append(num)

context_files.sort()
print(context_files)



words = []

from collections import namedtuple
GiftData = namedtuple("GiftData", ["Date", "Context", "WishList"])

TotalGiftList = []  # 대화에서 추출한 선물 리스트, 해당 대화, 해당 대화 일자를 모두 담음
GiftList = [] # 오로지 선물(상품, 좋아하는 것) 리스트만 담기

m = 0

for txt_files in context_files:
  with open(r'/content/' + txt_files, 'r', encoding='utf-8') as f:
      print(txt_files)
      for line in f:
          # m = re.search(r"^.*?\[\d\d:\d\d\]\s*(.+)$", line) -> pc버전 내보내기
          # print(m)
          ############아이폰 모바일버전 내보내기 정규표현식 추정###################
          # m = re.search(r"^\d\d\d\d.+.\d\d.+.\d\d.+.\w+.\d\d:\d\d,+.(.+?)+.:+.", line)
          # matchOB = re.match("^\d\d\d\d.+.\d\d.+.\d\d.+.\w+.\d\d:\d\d,+.(.+?)+.:+." , line)
          ##########################################################################
          # m = re.search(":", line)
          # print(line)

          matchOB = re.search(" : ", line)
          is_not_me = re.search(contact_name, line) # 상대방의 말만 고려하도록
          
          # matchOB = re.match("^\[(.+\]?)\[\w+.\d\d:\d\d\]" , line) -> pc버전 내보내기 날짜 정규표현식
          if matchOB and is_not_me:
            # print(matchOB.group())
            # m = re.sub("^\d\d\d\d.+.\d\d.+.\d\d.+.\w+.\d\d:\d\d,+.(.+?)+.:+.","",line) -> 아이폰 모바일버전 내보내기 정규표현식 부분 자르기
            m = line.split(" : ")
            del m[0]
            # print(''.join(m))
            m = m[0]
            # print(m)
  
            if m:
                # words.extend(re.split(r"\s+", m.group(1)))
                wanted_items = re.search('갖고 싶|갖고싶|사고 싶|사고싶|싶다|싶어|싶은|싶고', line)
                if wanted_items:
                  # words.extend(m.split())
                  # print(m)
                  wanted_items2 = re.search('갖고 싶|갖고싶|사고 싶|사고싶|싶다|싶어|싶은|싶고', m)

                  if wanted_items2:
                    #####~~~ 갖고 싶다 앞에 나오는 명사들만 취급#####
                    m = m.split("갖고 싶|갖고싶|사고 싶|사고싶|싶다|싶어|싶은|싶고")
                    m = m[0]
                    ##################
                    nlpy = Twitter() 
                    nouns = nlpy.nouns(m)
                    # print(nouns)
                    if nouns:
                      TotalGiftList.append(GiftData("", m, nouns))  # 선물리스트 관련 튜플에 추가
                      GiftList.append(nouns) # 상품들만 하나의 리스트로 정리

                    # print(wanted_items2.group())
                    # print(m)
                    
                    # print("===========================================================================")
                  # words.extend(wanted_items.group())
    
# for word, freq in Counter(words).most_common(10):
#     print("{0:10s} : {1:3d}".format(word, freq))

test = "방탄소년단 개좋아함"
nlpy = Twitter()
nouns = nlpy.nouns(test)
print(nouns)


# p1 = GiftData("2020. 1. 17. 오전 7:12","나도 무언가에 꽂혀서 뭔가를 해보고싶은데 말이지", ['무언가', '뭔가', '말'])
# p2 = GiftData("2020. 1. 17. 오전 7:18", "그럼 떡볶이를 먹고 싶은 사람들은", ['떡볶이', '사람'])
# list_of_pairs = [p1,p2]
# print(list_of_pairs)
# print(list_of_pairs[0].WishList)


for list_ in TotalGiftList:
  print(list_.WishList)

print("==============================")
GiftList = sum(GiftList, [])  # 다중 리스트 형태의 선물 상품 리스트를 1차원으로 만들기
print(GiftList)
GiftList2 = GiftList[0:50]

cnt = Counter(GiftList2)
print(cnt)

######################################################################################################################

from matplotlib import pyplot as plt #시각화 모듈 작동
import pandas as pd # 통계,분석등을 위한 pandas의 모듈을 불러옵니다.

plt.rc('font', family='NanumBarunGothic') 

data = pd.Series(cnt) # pandas의 Series를 사용해 인덱스와 값을 자동으로 만들어줍니다.
k_lotto=data.sort_index() # 보기좋게 인덱스를 정렬합니다.
k_lotto.plot(figsize=(10,15),kind='barh',grid=True, title='What gift do I want?')

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
    print("======================") 
