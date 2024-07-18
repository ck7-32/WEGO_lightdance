import socket
UDP_IP = "192.168.111,222" # The IP that is printed in the serial monitor from the ESP32
SHARED_UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.connect((UDP_IP, SHARED_UDP_PORT))
def loop():
    while True:
        data = sock.recv(255)
        print(data)
if __name__ == "__main__":
    sock.send('Hello ESP32'.encode())
    loop()