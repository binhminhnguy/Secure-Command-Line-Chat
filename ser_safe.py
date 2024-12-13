import socket
import threading

class SecureChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def broadcast(self, message, client_socket):
        encrypted_message = self.encrypt_message(message.decode())
        print(f"Encrypted Message: {encrypted_message.decode()}")
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(encrypted_message)
                except:
                    self.remove(client)

    def remove(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                decrypted_message = self.decrypt_message(message.decode())
                print(f"Received: {decrypted_message}")
                self.broadcast(message, client_socket)
            except:
                self.remove(client_socket)
                break

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connection established with {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def encrypt_message(self, message):
        key = "UMASS"  # desired keyword
        encrypted_message = ""
        key_index = 0

        for char in message:
            if char.isalpha():
                shift = ord(key[key_index % len(key)].upper()) - ord('A')
                key_index += 1

                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26

                encrypted_message += chr(shifted)
            else:
                encrypted_message += char

        return encrypted_message.encode()

    def decrypt_message(self, message):
        key = "UMASS"  # desired keyword
        decrypted_message = ""
        key_index = 0

        for char in message:
            if char.isalpha():
                shift = ord(key[key_index % len(key)].upper()) - ord('A')
                key_index += 1

                shifted = ord(char) - shift
                if char.islower():
                    if shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted < ord('A'):
                        shifted += 26

                decrypted_message += chr(shifted)
            else:
                decrypted_message += char

        return decrypted_message

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    server = SecureChatServer(HOST, PORT)
    print(f"Server listening on {HOST}:{PORT}")
    server.accept_clients()