#Stela Nebiaj
#Fiorela Ciroku 
#Abdullah Elkindy

import sys
import re
from httpclient import http_req
def downloadImages(file_name,url):
	#We download the php file using http_req from task 1
	http_req(url)
	#read the php file into the variable data
	with open('data/'+file_name, 'r') as myfile:
	    data=myfile.read().replace('\n', ' ')
	#use regex to get the source of each image tag and save it in images array
	images = re.findall(r'<img[^>]*\ssrc="(.*?)"', data)
	i=0
	#We loop on each img to clean its url and then use http_req from task 1 to download it on the local machine
	while i<len(images):
		if "?" in images[i]:
			images[i]=images[i].split("?")[0]
		
		if "http" not in images[i]:
		#Im adding the url to these tags because they're relative to the domain. They're also not downloadable so
		#i discarded them from http_req use
			images[i]=url+images[i]
		else:
			http_req(images[i])
		i=i+1
	#last we print all urls. 
	j=0
	while j<len(images):
		print(images[j])
		j=j+1

if len(sys.argv) == 3:
    downloadImages(sys.argv[1],sys.argv[2])
else:
    print('Invalid invocation of the function: python downloadEverything.py file_name url')

