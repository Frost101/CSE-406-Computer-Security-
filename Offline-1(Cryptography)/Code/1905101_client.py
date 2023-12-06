import socket
import pickle
import importlib

AES = importlib.import_module("1905101_AES")
ECDH = importlib.import_module("1905101_ECDH")



PORT = 5002
AES_length = 128

# create a socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server on local computer
clientsocket.connect(('127.0.0.1', PORT))

# receive "send AES length message" from the server
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
# send AES length to the server
clientsocket.send(str(AES_length).encode())
print(f"sent AES length: {AES_length}")
print()


# send p to the server
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
p = ECDH.calculate_p(AES_length)
clientsocket.send(str(p).encode())
print(f"sent p: {p}")
print()



# send a and b to the server
ECDH.calculate_a_b()
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
tmp_a = ECDH.get_a()
clientsocket.send(str(tmp_a).encode())
print(f"sent a: {tmp_a}")
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
tmp_b = ECDH.get_b()
clientsocket.send(str(tmp_b).encode())
print(f"sent b: {tmp_b}")
print()



# send G_x to the server
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
G_x , G_y = ECDH.caluculate_G()
clientsocket.send(str(G_x).encode())
print(f"sent G_x: {G_x}")
print()

# send G_y to the server
data = clientsocket.recv(1024).decode()
print(f"received data: {data}")
clientsocket.send(str(G_y).encode())
print(f"sent G_y: {G_y}")
print()

# receive public key from the server
data = clientsocket.recv(1024).decode()
public_key_server = []
public_key_server.append(int(data[1:data.find(',')]))
public_key_server.append(int(data[data.find(',')+1:-1]))
print(f"received public_key_server: {public_key_server}")
print()

# calculate the private key
private_key_self = ECDH.calculate_private_key()
print(f"private_key_self: {private_key_self}")
print()

# send public key to the server
public_key_self = ECDH.calculate_public_key((G_x, G_y),private_key_self)
clientsocket.send(str(public_key_self).encode())
print(f"sent public_key_self: {public_key_self}")
print()


# calculate the shared key
shared_key = ECDH.calculate_public_key(public_key_server, private_key_self)
print(f"shared_key: {shared_key}")
print()

# receive IV from the server
data = clientsocket.recv(1024)
data = pickle.loads(data)
print(f"received IV: {data}")
IV = AES.convert_1D_hexarray_to_1D_bitvector(data)
print()

# receive encrypted message from the server
data = clientsocket.recv(1024)
data = pickle.loads(data)
print(f"received encrypted message: {data}")
encrypted_message = data
print()

# decrypt the message
decrypted_message = AES.AES_decrypt_ECDH(encrypted_message, shared_key[0], AES_length, IV)
decrypted_message = AES.generalized_unPadding(decrypted_message)
decrypted_message = AES.hex_array_to_string(decrypted_message)
print(f"decrypted message: {decrypted_message}")
