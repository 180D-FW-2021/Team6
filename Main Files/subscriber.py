import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()  # Get local machine name
host_ip = socket.gethostbyname(host)
port = 12345                 # Reserve a port for your service.
s.bind((host_ip, port))        # Bind to the port
f = open('torecv.jpg', 'wb')
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from'), addr
    print("Receiving...")
    l = c.recv(4096)
    while (l):
        print("Receiving...")
        f.write(l)
        l = c.recv(4096)
    # f.close()
    print("Done Receiving")
    #c.send('Thank you for connecting')
    c.close()  