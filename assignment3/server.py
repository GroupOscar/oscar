#Stela Nebiaj
#Fiorela Ciroku 
#Abdullah Elkindy

#Import socket module
import socket               
#Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Get local machine name
host = 'localhost'
port = 8080
print(host)
#Bind to the port
sock.bind((host, port))        

#Now wait for client connection.
sock.listen(5)                 

#Establish connection with client.
connection, client_addr = sock.accept()

print ('Got connection from', client_addr)
print("url info:")
print("")

while 1: 
       data= connection.recv(1024)
       if not data: break
       dns_link=str(data).split('\'')
       dns_link=str(dns_link[1])
       dns_link=dns_link.split('/')
       print("Protocol: ",dns_link[0].rsplit(':',1)[0])
       dom_str=dns_link[2]
       dom_str=str(dom_str).split('.')
       print("Domain: ",str(dom_str[1])+"."+str(dom_str[2]))
       print("Subdomain: ",dom_str[0])
       path_str=str(dns_link[5])
       print("File path: ",path_str.rsplit('?', 1)[0])
       remaining_path_str=path_str.rsplit('?', 1)[1]

       parameters_str=remaining_path_str.rsplit('#', 1)[0]
       parameters_str_array=parameters_str.split('&')
       index=0
       while index<len(parameters_str_array):
           print("Parameter"+str(index)+": "+parameters_str_array[index])
           index=index+1

       fragment=remaining_path_str.rsplit('#', 1)[1]
       print("Fragment: ",fragment)
       connection.send(data)
   
connection.close()              
