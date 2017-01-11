#same as jacaard in 1.111 but for outlinks

import pandas as pd
import re
import numpy as np

#Jaccard-Similarity on sets
store = pd.HDFStore('store.h5')
df2=store['df2']

def calcJaccardSimilarity(wordset1, wordset2):
      #length of intersection set
      JK1= len(wordset1 & wordset2)
      #length of union set
      JK2 = len(wordset1 | wordset2)
      #Jaccard Formula
      JK = JK1/float(JK2)
      return JK

#get id-s for articles named Germany and Europe
index1= df2[df2.name=="Germany"].index
index1=index1[0]

index2= df2[df2.name=="Europe"].index
index2=index2[0]

#building sets for each article
set1= set(df2.out_links[index1])
set2=set(df2.out_links[index2])

print(calcJaccardSimilarity(set1,set2),"\n")

