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

sock.connect((host, port))
name= input("Give your name.")
age= input("Give your age.")
matrikelnummer = input("Give your matrikelnummer.")
message = "Name: "+name+"\n Age: "+age+"\n Matrikelnummer: "+matrikelnummer

sock.send(message.encode('utf-8'))
data = sock.recv(1024)
sock.close     
print('Received data: ',data)
