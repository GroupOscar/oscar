#This is the most elegant form for all other questions
#in terms of modeling similarity as i do it here for
#all documents given each similarity. In cosine sim
#i followed a different and more realistic approach
#by using only non zero entries in tfidf vectors thus
#you will see that my calculateCosineSimilarity function
#is different from here and for me it's the most generic
#one that can apply on any case
import pandas as pd
import re
import numpy as np
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
	tfIdfDict1_mag=tfIdfDict1.values()
	tfIdfDict1_mag=[x**2 for x in tfIdfDict1_mag]
	tfIdfDict1_mag= sqrt(sum(tfIdfDict1_mag))

	tfIdfDict2_mag=tfIdfDict2.values()
	tfIdfDict2_mag=[x**2 for x in tfIdfDict2_mag]
	tfIdfDict2_mag= sqrt(sum(tfIdfDict2_mag))

	vec_mult=0

	set1=set(tfIdfDict1.keys())
	set2=set(tfIdfDict2.keys())
	common_words=list(set1&set2)

	for i in range(len(common_words)):
		vec_mult+=tfIdfDict1[common_words[i]]*tfIdfDict2[common_words[i]]

	return vec_mult/float(tfIdfDict1_mag*tfIdfDict2_mag)

def smart_push(l,item,n):
	if(len(l)<n):
		l.append(item)
	else:
		if(item[0]>l[0][0]):
			l.remove(l[0])
			l.append(item)	
	l=sorted(l, key=lambda x: x[0])
	return l

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


target_doc_index= df1[df1.name=="Germany"].index
target_doc_index=target_doc_index[0]
target_doc_text = df1.text[target_doc_index]
target_doc_outlinks = df2.out_links[target_doc_index]

#cosine similarity pre processing
N=len(df1)

docfrq=dict()
target_doc_tfidf=dict()
docs_tfidf={}

print('started preprocessing')
#filled docfrqs and target_tfidt
for index,row in df1.iterrows():
	docs_tfidf[index]=dict()
	l=[]
	for word in row.text.split():
		if(word in docfrq and word not in l):
			docfrq[word]+=1
		else:
			if(word not in docfrq):
				docfrq[word]=1
		l.append(word)


		if(index==target_doc_index):
			if(word in target_doc_tfidf):
				target_doc_tfidf[word]+=1
			else:
				target_doc_tfidf[word]=1

		if(word in docs_tfidf[index]):
			docs_tfidf[index][word]+=1
		else:
			docs_tfidf[index][word]=1
	if(index%10000==0):
		print(index)

for key,value in target_doc_tfidf.items():
	target_doc_tfidf[key]=value*log(N/float(docfrq[key]))


text_jacard=[]
graph_jacard=[]
cosine=[]
print('preprocessing ended ... calculating similarity')
for index,row in df1.iterrows():
	#calculating cosine
	for key,value in docs_tfidf[index].items():
		docs_tfidf[index][key]=value*log(N/float(docfrq[key]))
	cosine=smart_push(cosine,(calculateCosineSimilarity(target_doc_tfidf,docs_tfidf[index]),index),10)

	#calculating text jacaard
	target_text_set=set(target_doc_text.split())
	current_text_set=set(df1.text[index].split())
	text_jacard= smart_push(text_jacard,(calcJaccardSimilarity(target_text_set,current_text_set),index),10)
	#calculating graph jacaard
	target_graph_set=set(target_doc_outlinks)
	current_graph_set=set(df2.out_links[index])
	graph_jacard=smart_push(graph_jacard,(calcJaccardSimilarity(target_graph_set,current_graph_set),index),10) 
	if(index %10000==0):
		print(index)

#getting the docs ids ranked according to each sim measure
text_jacard = [int(i[1]) for i in text_jacard]
cosine = [int(i[1]) for i in cosine]
graph_jacard = [int(i[1]) for i in graph_jacard]

print(text_jacard)
print(cosine)
print(graph_jacard)

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


print(str(levenshteinDistance(text_jacard_string,cosine_string))+' levenstein distance between text jacard AND cosine') #9
print(str(levenshteinDistance(text_jacard_string,graph_jacard))+' levenstein distance between text jacard AND graph jacard') #10
print(str(levenshteinDistance(cosine_string,graph_jacard_string))+' levenstein distance between cosine And graph jacard') #9
