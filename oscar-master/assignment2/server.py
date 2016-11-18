#Stela Nebiaj
#Fiorela Ciroku 
#Abdullah Elkindy

#Import socket module
import socket               
#Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Get local machine name
host = socket.gethostname() 
port = 8080

#Bind to the port
sock.bind((host, port))        

#Now wait for client connection.
sock.listen(5)                 

#Establish connection with client.
connection, client_addr = sock.accept()

print ('Got connection from', client_addr)
while 1: 
       data= connection.recv(1024)
       if not data: break
       print('Received data: ',data)
       connection.send(data)
   
connection.close()              
