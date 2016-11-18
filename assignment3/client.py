#Stela Nebiaj
#Fiorela Ciroku
#Abdullah Elkindy

#Import socket module
import socket              
#Create a socket objectki
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Get local machine name
host = 'localhost'
port = 8080            

sock.connect((host, port))
message="http://www.example.com/path/to/myfile.html?key1=value1&key2=value2#InTheDocument"
sock.send(message.encode('utf-8'))
data = sock.recv(1024)
sock.close     
print('Sent data: ',data)
