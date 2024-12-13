import socket
import threading

class SecureChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.key = key

    def send_message(self):
        while True:
            message = input("Enter your message: ")
            encrypted_message = self.encrypt_message(message)
            self.client_socket.send(encrypted_message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                decrypted_message = self.decrypt_message(message.decode())
                print(f"Received: {decrypted_message}")
            except:
                print("Connection closed.")
                break

    def encrypt_message(self, message):
        key ="UMASS"  # desired keyword
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
        if self.key != "UMASS":
            print("Invalid key! Decryption is only allowed with the key 'UMASS'.")
            return None  # Return None for invalid key
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

    
'''if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    client = SecureChatClient(HOST, PORT)

    # Starts a thread for sending messages
    send_thread = threading.Thread(target=client.send_message)
    send_thread.start()

    # Starts a thread for receiving messages
    receive_thread = threading.Thread(target=client.receive_messages)
    receive_thread.start()

    encrypted_message = input("Enter the encrypted message: ")
    client = SecureChatClient("127.0.0.1", 12345)
    decrypted_message = client.decrypt_message(encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")'''
from ser_safe import SecureChatServer  # or from cli_safe import SecureChatClient'''

if __name__ == "__main__":
    key = input("Enter the encryption key: ")
    plaintext = input("Enter the plaintext to encrypt: ")

    # Initialize server or client class
    server = SecureChatClient("127.0.0.1", 12345)

    # Encrypt the plaintext
    encrypted_message = server.encrypt_message(plaintext)
    print(f"Encrypted Message: {encrypted_message.decode()}")

    # Decrypt the message
    decrypted_message = server.decrypt_message(encrypted_message.decode())
    if decrypted_message is not None:
        print(f"Decrypted Message: {decrypted_message}")
    else:
        print("Decryption failed due to an incorrect key.")
