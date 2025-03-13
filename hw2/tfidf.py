import re
from collections import Counter
import math

# Add all files to the queue
queue = []
with open("tfidf_docs.txt", "r") as file:
    for line in file:
        queue.append(line.strip())

#print(queue)

stopwords = []
with open("stopwords.txt", "r") as file:
    for line in file:
        stopwords.append(line.strip("\n"))

#print(True if 'it' in stopwords else False)

conglomerate = {}
for file in queue:
    with open(file, "r") as fi:
        contents = fi.read()
        words = re.split(r"[\s]+|https:\/\/[a-zA-Z0-9.\/-]*|http:\/\/.[a-zA-Z0-9.\/-]", contents)
        words = [re.sub(r"\W+", "", x) for x in words]
        # print(*words, sep=" ")

        words = [re.sub(r"(ly|ment|ing)$", "", x.lower()) for x in words if x != '' and x.lower() not in stopwords]
        # print(*words, sep=" ")

        with open(f'preproc_{file}', "w") as wr:
            wr.write(' '.join(words))
            

    # Q3 Pt.2 Actual TfIdf calc
    tfidf = {}
    with open(f'preproc_{file}', "r") as fi:
        contents = fi.read()
        total = len(contents.split())
        counts = Counter(contents.split())
       # print(total)
        for k,v in counts.items():
            # print(k,v)
            tfidf.setdefault(k, float(v/total))

    # print(tfidf)
    conglomerate[file] = tfidf
    
total_docs = len(queue)
for k,v in conglomerate.items():
    conglomerate[k] = {x:round(y * (math.log(total_docs / sum(1 for doc in queue if x in conglomerate[doc].keys())) + 1),2) for x,y in conglomerate[k].items()}
    sorted_data = [(k,v) for k,v in sorted(conglomerate[k].items(), key=lambda x: (-x[1], x[0]))]

    # print(sorted_data)
    with open(f'tfidf_{k}', "w") as wr:
        wr.write(str(sorted_data[:5]))
        
        