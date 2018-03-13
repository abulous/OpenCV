import io
import sys
import socket
import struct
import time
import numpy as np
import cv2

#video capture
cap = cv2.VideoCapture(0)
cap.set(3,640) #change width to 640
cap.set(4, 480) #change height to 480

myint = 4

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
#client_socket.connect(('my_server', 8000)) 
client_socket.connect(('192.168.0.100', 8000)) 

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
time.sleep(2) #some time to set up

try:
    stream = io.BytesIO()
    #for foo in camera.capture_continuous(stream, 'jpeg'):
    while(True):
        #capture frame by frame
        ret, stream = cap.read()
        
        #stream=list_benefits()
        #print ( stream[0] )
        #print ( stream[1] )
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        #connection.write(struct.pack('<L', stream.length()))
        connection.write(struct.pack('<L', sys.getsizeof(myint) ))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        #stream.seek(0)
        #connection.write(stream.read())
        connection.write(stream[1])
        #connection.write(stream)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Reset the stream for the next capture
        #stream.seek(0)
        #stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    cap.release()
    connection.close()
    client_socket.close()
    
    
    
