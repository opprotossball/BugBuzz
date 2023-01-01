import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = "10.0.20.100"
        self.port = 5555
        self.address = (self.server_ip, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


if __name__ == "__main__":
    n = Network()
    n.send("Hello")
    n.send("There")
