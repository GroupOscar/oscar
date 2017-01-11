#Solution for longest 100 articles
#This solution is also a special case solution
#where im considering my docs corpa to be the
#selected items + germany article 

import pandas as pd
import re
import numpy as np
import copy
from math import log
from math import sqrt

#Jaccard-Similarity on sets
store = pd.HDFStore('store.h5')
df1=store['df1']
df1['text']=df1['text'].str.lower()
df1.text.replace('', np.nan, inplace=True)
df1.dropna(subset=['text'], inplace=True)
df1.text=df1.text.apply(lambda x: re.findall(r'[0-9a-zA-Z]+', x))
df1.text=df1.text.apply(lambda x: ' '.join(map(str, x)))
df2=store['df2']


#functions 

def calcJaccardSimilarity(wordset1, wordset2):
      #length of intersection set
      JK1= len(wordset1 & wordset2)
      #length of union set
      JK2 = len(wordset1 | wordset2)
      #Jaccard Formula
      JK = JK1/float(JK2)
      return JK

def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
	tfIdfDict1_mag=0
	tfIdfDict2_mag=0
	vec_mult=0
	for key, value in tfIdfDict1.items():
		value2=tfIdfDict2[key] 
		type(value2)
		tfIdfDict1_mag+=(value*value)
		tfIdfDict2_mag+=(value2*value2)

		vec_mult+=(value*value2)
	tfIdfDict1_mag=sqrt(tfIdfDict1_mag)
	tfIdfDict2_mag=sqrt(tfIdfDict2_mag)
	return vec_mult/float(tfIdfDict1_mag*tfIdfDict2_mag)
	
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if(c1 == c2):
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

#I add a length column to the df1 to sort it
lengths=[]
for index,row in df1.iterrows():
	lengths.append(len(df1.text[index]))
df1['length']=lengths
df1=df1.sort_values(by=['length'], ascending=[False])
samples=df1.head(100)


target_doc_index= df1[df1.name=="Germany"].index
target_doc_index=target_doc_index[0]
target_doc_text = df1.text[target_doc_index]
target_doc_outlinks = df2.out_links[target_doc_index]

#cosine similarity pre processing
N=len(df1)
docfrq=dict()
target_doc_tfidf=dict()
docs_tfidf={}
for index,row in samples.iterrows():
	docs_tfidf[index]={}
	for word in row.text.split():
		docfrq[word]=0
		target_doc_tfidf[word]=0
		docs_tfidf[index][word]=0

for word in target_doc_text.split():
	if(word in docfrq):
		docfrq[word]+=1
	else:
		docfrq[word]=1
	if(word in target_doc_tfidf):
		target_doc_tfidf[word]+=1
	else:
		target_doc_tfidf[word]=1

for index,row in samples.iterrows():
	docs_tfidf[index]=copy.copy(docfrq)

for index,row in samples.iterrows():
	for word in row.text.split():
		if(index==target_doc_index):
			target_doc_tfidf[word]+=1
		else:
			docs_tfidf[index][word]+=1


for index, row in df1.iterrows():
	flag=False
	l=[]
	for word in row.text.split():
		if(word in docfrq  and word not in l):
			docfrq[word] +=1
			l.append(word)

print("Data preprocessing is over")

text_jacard=[]
graph_jacard=[]
cosine=[]


for index, row in samples.iterrows():
	#calculating text jacaard
	target_text_set=set(target_doc_text.split())
	current_text_set=set(df1.text[index].split())
	text_jacard.append((calcJaccardSimilarity(target_text_set,current_text_set),index))
	
	#calculating graph jacaard
	target_graph_set=set(target_doc_outlinks)
	current_graph_set=set(df2.out_links[index])
	graph_jacard.append((calcJaccardSimilarity(target_graph_set,current_graph_set),index))
	
	#calculating cosine sim
	tf_idf1=target_doc_tfidf
	tf_idf2=docs_tfidf[index]
	for key, value in docfrq.items():
		if(tf_idf1[key]!=0):
			tf_idf1[key]=tf_idf1[key]*log(N/float(value))
		if(tf_idf2[key]!=0):
			tf_idf2[key]=tf_idf2[key]*log(N/float(value))
	cosine.append((calculateCosineSimilarity(tf_idf1,tf_idf2),index))


text_jacard.sort(key=lambda tup: tup[0])
graph_jacard.sort(key=lambda tup: tup[0])
cosine.sort(key=lambda tup: tup[0])

#getting the docs ids ranked according to each sim measure
text_jacard = [int(i[1]) for i in text_jacard]
cosine = [int(i[1]) for i in cosine]
graph_jacard = [int(i[1]) for i in graph_jacard]

print(text_jacard)
print(graph_jacard)
print(cosine)


#grouping the output to calculate levenstein distance between each measure
#by using an function for levenstein distance i found online. I assign
#each doc with a letter and this way each ranked result will be like a word
#and at the end we calculate levenstein distance for all

grouped=list(set(text_jacard)|set(cosine)|set(graph_jacard))
reference=dict()
for i in range(len(grouped)):
	reference[grouped[i]]=chr(97+i)

text_jacard_string=''
cosine_string=''
graph_jacard_string=''
for i in range(len(text_jacard)):
	text_jacard_string+=reference[text_jacard[i]]
	cosine_string+=reference[cosine[i]]
	graph_jacard_string+=reference[graph_jacard[i]]


print(str(levenshteinDistance(text_jacard_string,cosine_string))+' levenstein distance between text jacard AND cosine') 
print(str(levenshteinDistance(text_jacard_string,graph_jacard))+' levenstein distance between text jacard AND graph jacard') 
print(str(levenshteinDistance(cosine_string,graph_jacard_string))+' levenstein distance between cosine And graph jacard') 
