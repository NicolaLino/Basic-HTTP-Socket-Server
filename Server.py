import socket
import os


FORMAT = 'utf-8'
PORT = 9000
HEADER = 1024
SERVER_HOST = socket.gethostbyname(socket.gethostname())  # get the server IP
# SERVER_HOST = '0.0.0.0'
ADDR = (SERVER_HOST, PORT)  # tuple with the IP and PORT

# creating socket socket.AF_INET is the type, socket.SOCK_STREAM protocol method
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)  # bind the socket with to the address
server.listen(1)
print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(f'[PORT]  Listening on port {PORT} ...')
print(f'[HOST]  Hosting on {SERVER_HOST} ...')


def read_file(myfile):
    # open file , r => read , b => byte format
    cwd = os.getcwd()
    # print(cwd)
    file = open(
        f"{cwd}\\templates\\{myfile}", 'rb')
    response = file.read()
    file.close()
    return response


while True:
    # Wait for client connections
    conn, addr = server.accept()
    print(f"[CLIENT IP]  {addr[0]}")
    print(f"[CLIENT PORT]  {addr[1]}")
    # Get the client request
    req = conn.recv(HEADER).decode(FORMAT)
    msg = req.split(' ')
    method, req_file = msg[0], msg[1]
    # Get the content
    print("[CLIENT IS REQUESTING]")
    print(f'[METHOD]    {method}')
    requested_file = req_file.lstrip('/')
    print(f"[REQUESTED FILE]    {requested_file}")
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    if(requested_file == '' or requested_file.lower() == 'en'):
        requested_file = 'index.html'
    elif(requested_file.lower() == 'ar'):
        requested_file = 'indexAR.html'

    try:

        header = 'HTTP/1.1 200 OK\n' #The HTTP 200 OK success status response code indicates that the request has succeeded
        Temporary_Redirect_Header = "HTTP/1.1 307 Temporary Redirect\n".encode(
            FORMAT) #307 Temporary Redirect redirect status response code
        if(requested_file.endswith(".jpg")):
            response = read_file(requested_file)
            mimetype = 'image/jpeg'
        elif(requested_file.endswith(".png")):
            response = read_file(requested_file)
            mimetype = 'image/png'
        elif(requested_file.endswith(".css")):
            cwd = os.getcwd()
            file = open(
                f"{cwd}\\{requested_file}", 'rb')
            response = file.read()
            file.close()
            mimetype = 'text/css'
        elif(requested_file.lower() == 'go'):
            conn.send(Temporary_Redirect_Header)
            conn.send("Location : https://www.google.com\n\n".encode(FORMAT))
        elif(requested_file.lower() == 'bzu'):
            conn.send(Temporary_Redirect_Header)
            conn.send("Location : https://www.birzeit.edu\n\n".encode(FORMAT))
        elif(requested_file.lower() == 'cnn'):
            conn.send(Temporary_Redirect_Header)
            conn.send("Location : https://edition.cnn.com/\n\n".encode(FORMAT))
        else:
            response = read_file(requested_file)
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        #404 Not Found response status code indicates that the server cannot find the requested resource
        header = 'HTTP/1.1 404 Not Found\n\n'
        # HTML FILE FOR HANDLING ERROR 
        response = '''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            p {
                font-size: 17px;
                text-align: center;
                font-weight: bold;
                font-family: Arial;
            }

            h1 {
                font-size: 60px;
                text-align: center;
                color: red;
                font-family: Arial;
            }
            </style>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Error</title>
        </head>
        <title>Error</title>

        <body>
            <header>
            <h1>The file is not found</h1>
            <h1>404</h1>
            <p>Client IP : %s &nbsp;&nbsp;Client Port: %s</p>
            </header>
        </body>
        </html>
        '''

        response = response % (addr[0], addr[1]) # placing ip and port in html error file
        response = response.encode(FORMAT)# encode the html   


    final_response = header.encode(FORMAT)# encode the https header
    final_response += response # add the response to the header
    conn.sendall(final_response) # Send HTTP response to the client
    conn.close() # close the connection
