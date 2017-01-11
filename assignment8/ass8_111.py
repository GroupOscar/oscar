#This is a special case where im calculating jacaard sim for 
#only Germany and Europe. I know it says in the assignmnt to
#build the wordset for all documents, but i dont need it here.
#So i haven't built it. However, I put it in 1.3 because it's
#required.

import pandas as pd
import re
import numpy as np
#Jaccard-Similarity on sets
store = pd.HDFStore('store.h5')
df1=store['df1']
df1['text']=df1['text'].str.lower()
df1.text.replace('', np.nan, inplace=True)
df1.dropna(subset=['text'], inplace=True)
df1.text=df1.text.apply(lambda x: re.findall(r'[0-9a-zA-Z]+', x))
df1.text=df1.text.apply(lambda x: ' '.join(map(str, x)))

def calcJaccardSimilarity(wordset1, wordset2):
      #length of intersection set
      JK1= len(wordset1 & wordset2)
      #length of union set
      JK2 = len(wordset1 | wordset2)
      #Jaccard Formula
      JK = JK1/float(JK2)
      return JK

#get id-s for articles named Germany and Europe
index1= df1[df1.name=="Germany"].index
index1=index1[0]

index2= df1[df1.name=="Europe"].index
index2=index2[0]

#building sets for each article
set1= set(df1.text[index1].split())
set2=set(df1.text[index2].split())

print(calcJaccardSimilarity(set1,set2),"\n")

