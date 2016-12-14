import random
import numpy as np
import matplotlib.pyplot as plt
import operator

def roll( dict ):
    random_number=random.random()
    output=' '
    for key, value in dict.items():
        if(value>=random_number):
            output=key
            break
    return output

def getFileCDF(dict):
	words=[]
	frequencies=[]
	for key, value in dict.items():
		words.append(key)
		frequencies.append(value)
	cumsum = np.cumsum(frequencies)
	normedcumsum = [x/float(cumsum[-1]) for x in cumsum]
	wrank = {words[i]:i+1 for i in range(0,len(words))}
	return wrank,normedcumsum
prob_dist = {'1': 1/6, '2': 1/6, '3': 1/6, '4': 1/6, '5': 1/6, '6': 1/6}

old_val=0.0
old_val=0.0
for key, value in prob_dist.items():
    prob_dist[key]=old_val+value
    old_val=prob_dist[key]

output_dict={'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0}

loop_index=0
while loop_index<=100:
	n1=roll(prob_dist)
	n2=roll(prob_dist)
	sum_of=int(n1)+int(n2)
	sum_of=str(sum_of)
	output_dict[sum_of]=output_dict[sum_of]+1
	loop_index=loop_index+1

a,cdf=getFileCDF(output_dict)

print("sum count= ")
print(a)
l=[0]*11
for key, value in output_dict.items():
	l[int(key)-2]=value

plt.title("Exercise 3")
plt.xlabel('Dice outcome')
plt.ylabel('Frequency')
plt.scatter([2,3,4,5,6,7,8,9,10,11,12],l)
plt.show()

plt.title("Exercise 3")
plt.xlabel('Sum Rank')
plt.ylabel('CDF')
plt.plot([1,2,3,4,5,6,7,8,9,10,11],cdf)
plt.show()

output_dict={'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0}

loop_index=0
while loop_index<=100:
	n1=roll(prob_dist)
	n2=roll(prob_dist)
	sum_of=int(n1)+int(n2)
	sum_of=str(sum_of)
	output_dict[sum_of]=output_dict[sum_of]+1
	loop_index=loop_index+1

a2,cdf2=getFileCDF(output_dict)

plt.title("Exercise 3")
plt.xlabel('Sum Rank')
plt.ylabel('CDF')
plt.plot([1,2,3,4,5,6,7,8,9,10,11],cdf)
plt.plot([1,2,3,4,5,6,7,8,9,10,11],cdf2)
plt.show()
print("point wise distance= "+str(max(list(map(operator.sub, cdf, cdf2)))))#
