import re
import matplotlib.pyplot as plt
import statistics
words_per_article_high=list()
words_per_article_low=list()
average_high=list()
average_low=list()
with open('simple-20160801-1-article-per-line','rb') as file:
    content=file.readlines()
index=0
while index<len(content):
    line=content[index].decode()
    count =0
    wordlist= re.findall(r"\b([a-zA-Z]+-*[a-zA-Z]*)\b",line, re.I)
    av=0
    for w in wordlist:
        count = count +len(w)
    if(len(wordlist))==0 :
        av=0
    else:
        av=count/float(len(wordlist))
#value we precalculated to the median of the averages so that we seperated into avg high and low, to plot the 2 catogories in different colors.   
    if(av>=4.68075117370892):
        average_high.append(av)
        words_per_article_high.append(len(wordlist))
    else:
        average_low.append(av)
        words_per_article_low.append(len(wordlist))
    index=index+1
file.close()
perc=len(words_per_article_high)/(len(words_per_article_high)+len(words_per_article_low))
perc=int(perc*100)
print("The hypothesis holds for around "+str(perc)+"% of the data")
#print(statistics.median(average))
plt.title("Exercise 3")
plt.xlabel('words per document')
plt.ylabel('average')
plt.scatter(words_per_article_high, average_high)
plt.scatter(words_per_article_low, average_low,c=[2000]*len(average_low))
plt.ylim(0,max(average_high))
plt.xlim(0,max(words_per_article_high))
plt.show()
