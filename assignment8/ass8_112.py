#This is also a special case solution designed for finding
#cosine similarity between germany and europe where im 
#considering my text corpa as only the words involved,
#which are words in the texts of germany and europe article.
#I know it's not theoritcally correct as im supposed to cal-
#culate it for all df1 but it works here because it's too
#many zeros that we don't need. However, in 1.3 I've provided
#a full solution covering all pd1 docs
import pandas as pd
import numpy as np
import re
from collections import defaultdict
from math import log
from math import sqrt
store = pd.HDFStore('store.h5')
df1=store['df1']
df1['text']=df1['text'].str.lower()
df1.text.replace('', np.nan, inplace=True)
df1.dropna(subset=['text'], inplace=True)
df1.text=df1.text.apply(lambda x: re.findall(r'[0-9a-zA-Z]+', x))
df1.text=df1.text.apply(lambda x: ' '.join(map(str, x)))


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

#get id-s for articles named Germany and Europe
index1= df1[df1.name=="Germany"].index
index1=index1[0]

index2= df1[df1.name=="Europe"].index
index2=index2[0]

tf_idf1 = defaultdict(int)
tf_idf2 = defaultdict(int)

docfrq=defaultdict(int)

#preprocesing both tfidf docs data
for word in df1.text[index1].split():
	docfrq[word] = 0
	tf_idf1[word] =0
	tf_idf2[word] =0


for word in df1.text[index2].split():
	docfrq[word] = 0
	tf_idf1[word] =0
	tf_idf2[word] =0


#calculating tf and idf
for index, row in df1.iterrows():
	flag=False
	l=[]
	for word in row.text.split():
		if(word in docfrq  and word not in l):
			docfrq[word] +=1
			l.append(word)

N =len(df1)

for word in df1.text[index1].split():
	tf_idf1[word] +=1

for word in df1.text[index2].split():
	tf_idf2[word] +=1

for key, value in docfrq.items():
	if(tf_idf1[key]!=0):
		tf_idf1[key]=tf_idf1[key]*log(N/float(value))
	if(tf_idf2[key]!=0):
		tf_idf2[key]=tf_idf2[key]*log(N/float(value))

print(calculateCosineSimilarity(tf_idf1,tf_idf2))