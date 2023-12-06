import socket
import pickle
import importlib

from BitVector import BitVector

AES = importlib.import_module("1905101_AES")
ECDH = importlib.import_module("1905101_ECDH")



PORT = 5002
message = "Never gonna give you up, never gonna let you down"

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

# reserve a port (e.g: 5000)
serversocket.bind(('', PORT))
print(f"socket binded to {PORT}")

# put the socket into listening mode
serversocket.listen()
print("listening...")

# an infinity loop until we interrupt it or an error occurs
while True:
    # Establish connection with client.
    clientsocket, addr = serversocket.accept()
    print(f"Got a connection from {addr}")
    print()


    clientsocket.send(b"Send AES length")
    AES_length = int(clientsocket.recv(1024).decode())
    print(f" received AES length: {AES_length}")
    print()



    clientsocket.send(b"Send p")
    p = int(clientsocket.recv(1024).decode())
    print(f"p: {p}")
    ECDH.set_p(p)

    # ask for a and b
    clientsocket.send(b"Send a")
    tmp_a = int(clientsocket.recv(1024).decode())
    print(f"received a: {tmp_a}")
    clientsocket.send(b"Send b")
    tmp_b = int(clientsocket.recv(1024).decode())
    print(f"received b: {tmp_b}")
    print()
    ECDH.set_a_b(tmp_a, tmp_b)


    clientsocket.send(b"Send G_x")
    G_x = int(clientsocket.recv(1024).decode())
    print(f"G_x: {G_x}")

    clientsocket.send(b"Send G_y")
    G_y = int(clientsocket.recv(1024).decode())
    print(f"G_y: {G_y}")
    print()

    # calculate the private key
    private_key_self = ECDH.calculate_private_key()
    print(f"private_key_self: {private_key_self}")
    print()

    # send public key to the client
    public_key_self = ECDH.calculate_public_key((G_x, G_y),private_key_self)
    clientsocket.send(str(public_key_self).encode())
    print(f"sent public_key_self: {public_key_self}")
    print()

    # receive public key from the client
    data = clientsocket.recv(1024).decode()
    public_key_client = []
    public_key_client.append(int(data[1:data.find(',')]))
    public_key_client.append(int(data[data.find(',')+1:-1]))
    print(f"received public_key_client: {public_key_client}")
    print()

    # calculate the shared key
    shared_key = ECDH.calculate_public_key(public_key_client, private_key_self)
    print(f"shared_key: {shared_key}")
    print()

    # send IV to the client
    IV = AES.IV_generator()
    temp_IV = AES.convert_1D_bitvector_to_1D_hexarray(IV)
    print(f"sent IV: {temp_IV}")
    temp_IV = pickle.dumps(temp_IV)
    clientsocket.sendall(temp_IV)
    print()

    # send encrypted message to the client
    print(f"sent message: {message}")

    temp_bitvector = BitVector(intVal=shared_key[0], size=AES_length)

    encrypted_message = AES.AES_encrypt_ECDH(message, shared_key[0], AES_length, IV)
    print(f"sent encrypted_message: {encrypted_message}")
    encrypted_message = pickle.dumps(encrypted_message)
    clientsocket.sendall(encrypted_message)