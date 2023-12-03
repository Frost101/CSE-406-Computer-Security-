import math

from sympy import nextprime
import random

a = 2
b = 2
p = 17



def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inverse(a):
    if (a < 0):
        a = (a % p + p) % p
    m = p
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"The modular inverse does not exist for {a} (mod {m}).")
    else:
        return x % m


def caluculate_G():
    '''
    calculate the G based on a, b, p
    '''
    global p
    while True:
        x = random.randint(1, p - 1)
        tmp = (x ** 3 + a * x + b) % p
        y = math.sqrt(tmp)
        if y.is_integer():
            return x, int(y)


def calculate_private_key():
    '''
    calculate the private key based on p
    '''
    global p
    return random.randint(1, p - 1)


def calculate_p(AES_length):
    '''
    calculate the p based on AES_length 128/192/256
    '''
    global p
    str1 = "1"
    for i in range(2,AES_length,1):
        str1 = str1 + "0"
    str1 += "1"
    num1 = int(str1, 2)

    # nextprime(num1) is the prime number which is larger than num1
    p = nextprime(num1)
    # print(p)
    return p

def set_p(new_p):
    global p
    p = new_p



def addition(point1, point2):
    '''
    elliptic curve addition
    :param point1: array or tuple 0=>x and 1=>y
    :param point2: array or tuple 0=>x and 1=>y
    :return: tuple
    '''
    global p

    if point1 == (0, 0):
        return point2
    elif point2 == (0, 0):
        return point1
    elif point1[0] == point2[0] and point1[1] == point2[1]:
        s = (((3 * point1[0] ** 2 + a) % p) * ((mod_inverse(2 * point1[1]))%p)) % p
    else:
        s = (((point2[1] - point1[1])%p) * ((mod_inverse(point2[0] - point1[0]))%p)) % p

    x = (s ** 2 - point1[0] - point2[0]) % p
    y = (s * (point1[0] - x) - point1[1]) % p
    return int(x), int(y)


def calculate_public_key(G, k):

    tmp = G
    res = (0,0)
    while(k > 0):
        if(k & 1 == 1):
            res = addition(res, tmp)
        k = k >> 1
        tmp = addition(tmp, tmp)
    return res



def main():
    global p
    # calculate_p(128)
    # x,y = caluculate_G()
    # print(x," ",y)
    # x,y  = addition((6,3), (9,16))
    # res = calculate_public_key((5,1), 19)
    # print(res)

    calculate_p(256)
    x,y = caluculate_G()

    private_key_1 = calculate_private_key()
    private_key_2 = calculate_private_key()

    public_key_1 = calculate_public_key((x,y), private_key_1)
    print("Public key 1: ", public_key_1)
    public_key_2 = calculate_public_key((x,y), private_key_2)
    print("Public key 2: ", public_key_2)

    shared_key_1 = calculate_public_key(public_key_2, private_key_1)
    shared_key_2 = calculate_public_key(public_key_1, private_key_2)

    print("Shared key 1: ", shared_key_1)
    print("Shared key 2: ", shared_key_2)



if __name__ == "__main__":
    main()