#Stela Nebiaj
#Fiorela Ciroku 
#Abdullah Elkindy



import socket
import sys
import os
from urllib.parse import urlparse
import requests
import struct
import time
import errno

# a function to create a directory
def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
#main function
def http_req(url):
#get file name     
    url_array=url.split("/")
    file_name=url_array[len(url_array)-1]

    is_image=False;

    if "." not in file_name: 
        file_name = file_name+".php"
    else:
        is_image = True


#checking the response if 200 we continue
    if requests.get(url).status_code !=200:
        print("ERROR: HTTP status code ",requests.get(url).status_code," is not allowed")
        sys.exit()
#creating the download path in the local machine 
    download_path="data/"
    if is_image:
        download_path=download_path+"images/"

    create_dir(download_path)

    #creating the files on the local machine
    o = urlparse(url)
    file_path_header=download_path+file_name+".header"
    file_header=open(file_path_header,"w")
    file_path_body=download_path+file_name
    if is_image:
        file_body=open(file_path_body,"wb")
    else:
        file_body=open(file_path_body,"w")
    #defining the socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket')
        sys.exit()
    print('socket created')

    host = o.netloc
    port = 80           


    sock.connect((host, port))

    message="GET "+o.path+" HTTP/1.0\r\n\r\n"
        
    #we send the GET message req encoded. It has to be bytes on the socket.    
    try :
        sock.send(message.encode('utf-8'))
    except socket.error:
        print("send failed")
        sys.exit()

        
    print ("Message send successfully")

    #recv_timeout is a function where the data are received. We receive all as undecoded bytes and we decode when writing in header files
    #and body of php files. As for images we keep them unencoded to be able to save them on the machine

    def recv_timeout(the_socket,timeout=2):
        #make socket non blocking
        the_socket.setblocking(0)
         
        
        total_data=[];
        data='';
         
        
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
             
            #if you got no data at all, wait a little longer
            elif time.time()-begin > timeout*2:
                break
             
           
            try:
                data = the_socket.recv(8192)
                
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
         
        
        return b''.join(total_data)
     


    header,body = recv_timeout(sock).split(b'\r\n\r\n',1)
        

    #here we decide to decode the body of php files and leave the body of images as is
    print(header.decode('utf-8'))
    file_header.write(header.decode('utf-8'))
    if is_image:
        file_body.write(body)
    else:
        file_body.write(body.decode('utf-8'))
    sock.close()
#for terminal invocation
if len(sys.argv) == 2:
    http_req(sys.argv[1])
else:
    print('Invalid invocation of the function: python httpclient.py url')


