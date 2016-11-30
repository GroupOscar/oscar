#importing the libraries
import lxml.html
import requests
import urllib
import codecs
import re
import numpy as np

host = 'http://141.26.208.82'
file = codecs.open('WikiDump.txt','w','UTF-8')
website='http://141.26.208.82/articles/g/e/r/Germany.html'

def crawl(url):
        
        
        source = requests.get(url)
        html = source.text
        Page_viewed = lxml.html.document_fromstring(html)
        copier(Page_viewed) 

        links = Page_viewed.xpath('//div[@id="bodyContent"]//p/a/@href') #Collecting the links from first page
        counts = [0]*len(links)
        links_in_queue = dict(zip(links, counts))
        links_in_poped = 0 #Number of visited links
        page_nr=0
        internal=[]
        while True:
                if '../../../../articles/' in links[links_in_poped]:
                        
                        current = links[links_in_poped].replace('../../../..', host) #Replacing relative path to absolute
                        try:
                                source = requests.get(current)
                                html = source.text
                                status = source.status_code
                                if status == 200:
                                        page_nr+=1
                                
                                internal_links=0
                        
                        except Exception:
                                pass

                        page = lxml.html.document_fromstring(html)
                        Article_Name = page.xpath('//h1[@class="firstHeading"]/text()')
                        print(current) 

                        copier(page)
                        current_links = page.xpath('//p/a/@href') #Getting all the links from visited page


                        for i in range(len(current_links)): # for links in current page
                                if current_links[i] in links_in_queue: #Check whether link is already in queue,If yes we will not include it!
                                        pass
                                
                                elif '../../../../articles/' in current_links[i] and '.html' in current_links[i]:
                                        internal_links+=1
                                        links_in_queue[current_links[i]] = 0
                                        links.append(current_links[i])
                        internal.append(internal_links)
                       
                links_in_poped += 1
                if links_in_poped >= len(links):
                        break
                print("---",links_in_poped,"---")
                
       
        
        mean = np.mean(internal)
       
        print("Nr of visited links: " ,links_in_poped, "\nNr of pages: ",page_nr, " Mean: ", mean)


def copier(Page_viewed):
        try:
        
                Article_Name = Page_viewed.xpath('//h1[@class="firstHeading"]/text()')[0] #Read the Article name.

        except IndexError:
                return
        
        Body_Content = Page_viewed.xpath('//div[@id="bodyContent"]/p//text()') #crawling text from body of article.
        Article = ''.join(Body_Content)
        Article = Article_Name + '\t' + Article + '\n\n\n' #writing article name and body of article in the file.
        file.write(Article) #Writing it into the file


crawl(website)
