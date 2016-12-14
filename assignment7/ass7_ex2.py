import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import operator

zipf = open('zipf.txt', 'w')
uniform = open('uniform.txt','w')

#function for retreiving a character from a dictionary with a random flip
def retreive_char( dict ):
    random_number=random.random()
    output=' '
    for key, value in dict.items():
        if(value>=random_number):
            output=key
            break
    return output
#function to calculate the cdf just like the one in the lecture
def getFileCDF(file):
    c = Counter(file.read().split())
    words,frequencies = zip(*c.most_common())
    cumsum= np.cumsum(frequencies)
    normedcumsum = [x/float(cumsum[-1]) for x in cumsum]
    wrank = {words[i]:i+1 for i in range(0,len(words))}
    return wrank,normedcumsum



with open('simple-20160801-1-article-per-line','rb') as file:
    content=file.readlines()
file.close()


zipf_probabilities = {' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643, '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454, '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295, '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05, 'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115, 'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856, 'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837, 'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945, 'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105, 'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755, 'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219, 'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391, 'x': 0.0014600810295164054, 'z': 0.001048859288348506}
uniform_probabilities = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125, 'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125, 'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125, 's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125, 'y': 0.03125, 'x': 0.03125, 'z': 0.03125}

# we transform the probabilities into commulative ones. 
old_val=0.0
for key, value in zipf_probabilities.items():
    zipf_probabilities[key]=old_val+value
    old_val=zipf_probabilities[key]

old_val=0.0
for key, value in uniform_probabilities.items():
    uniform_probabilities[key]=old_val+value
    old_val=uniform_probabilities[key]

# we start the sampling here by looping on each doc and each letter in in each line, the same as 
# looping on N. The i generate 2 characters each using its own probability dist. Then i write
# into the corresponding files every 1000 characters
print("Sampling started")
string=""
loop_index=0
zipf_probabilities_generated=[]
string=list(" "*1000)
string_index=0
string2=list(" "*1000)
while loop_index<len(content):
    loop_index_2=0
    line=content[loop_index].decode().lower()
    while loop_index_2<len(line):
        char=retreive_char(zipf_probabilities)
        char2=retreive_char(uniform_probabilities)
        string[string_index]=char
        string2[string_index]=char2
        string_index=string_index+1
        if(string_index==1000):
            zipf.write("".join(string))
            uniform.write("".join(string2))
            string_index=0

        loop_index_2=loop_index_2+1
    loop_index=loop_index+1
    if(loop_index%5000==0):
        print("Sampling index:"+str(loop_index))
zipf.close()
uniform.close()
print("Done sampling")

#we calculate CDF for simple english wiki, generated zipf and uniform dists

with open('simple-20160801-1-article-per-line','r') as file:
    wrank,normedcumsum = getFileCDF(file)
file.close()
print("simple english wiki CDF calculation done")

with open('zipf.txt','r') as zipf_file:
    zipf_wrank, zipf_normedcumsum = getFileCDF(zipf_file)
zipf_file.close()
print("zipf CDF calculation done")


with open('uniform.txt','r') as uniform_file:
    uniform_wrank, uniform_normedcumsum = getFileCDF(uniform_file)
uniform_file.close()
print("uniform CDF calculation done")

#here i calculate the maximum point wise distance for both 2 generated corpuses
print("calculating the maximum point wise distance for zipf")
print("zipf max point= "+str(max(list(map(operator.sub, normedcumsum, zipf_normedcumsum)))))#0.411679964745
print("calculating the maximum point wise distance for uniform")
print("uniform max point= "+str(max(list(map(operator.sub, normedcumsum, uniform_normedcumsum)))))#0.436318188857


print("plotting now")


plt.title("Exercise 2")
plt.xlabel('Word Rrank')
plt.ylabel('CDF')
plt.loglog(list(range(len(wrank))), normedcumsum)
plt.loglog(list(range(len(zipf_wrank))), zipf_normedcumsum)
plt.loglog(list(range(len(uniform_wrank))), uniform_normedcumsum)
plt.show()

