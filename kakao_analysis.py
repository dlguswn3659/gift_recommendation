import re
from collections import Counter
from google.colab import files

# myfile = files.upload()
 
words = []

with open(r'/content/파일이름.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # m = re.search(r"^.*?\[\d\d:\d\d\]\s*(.+)$", line)
        # print(m)
        matchOB = re.match("^\[(.+\]?)\[\w+.\d\d:\d\d\]" , line)
        if matchOB:
          # print(matchOB.group())
          m = re.sub("^\[(.+\]?)\[\w+.\d\d:\d\d\]","",line)
          print(m)
 
        if m:
            # words.extend(re.split(r"\s+", m.group(1)))
            words.extend(m.split())
 
for word, freq in Counter(words).most_common(10):
    print("{0:10s} : {1:3d}".format(word, freq))
