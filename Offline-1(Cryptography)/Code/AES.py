import random
import time
import BitVector as BitVector
from BitVector import *

roundsMap = {128: 10, 192: 12, 256: 14}
AES_modulus = BitVector(bitstring='100011011')


key_scheduling_time = 0.0
encryption_time = 0.0
decryption_time = 0.0

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]


def transpose(array):
    '''
    Transposes a 2D array
    '''
    for i in range(0, len(array)):
        for j in range(i + 1, len(array)):
            array[i][j], array[j][i] = (array[j][i]), (array[i][j])
    return array


def convert_to_2D_array(array):
    '''
    Converts a 1D array to a 2D array
    '''
    temp_array = []
    for i in range(0, len(array), 4):
        temp_array.append(array[i:i + 4])


    # Transpose the array
    array = transpose(temp_array)
    # array = temp_array
    # Convert the array elements to BitVector
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            array[i][j] = BitVector(hexstring=array[i][j])
    return array


def convert_to_2D_array_key(array):
    '''
    Converts a 1D hex array to a 2D array
    '''
    temp_array = []
    for i in range(0, len(array), 4):
        temp_array.append(array[i:i + 4])

    array = temp_array

    # Convert the array elements to BitVector
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            array[i][j] = BitVector(hexstring=array[i][j])
    return array

def string_to_hex_array(s):
    '''
    Converts a string to a hex array
    '''
    tmp = []
    for c in s:
        t = hex(ord(c))[2:].upper()
        tmp.append(t)
    return tmp


def print_2D_bitVector_array(array):
    '''
    Prints a 2D array of BitVector in HEX format
    '''
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            print(array[i][j].getHexStringFromBitVector(), end=" ")
        print()


def print_1D_bitVector_array(array):
    '''
    Prints a 1D array of BitVector in HEX format
    '''
    for i in range(0, len(array)):
        print(array[i].getHexStringFromBitVector(), end=" ")
    print()


def circular_byte_left_shift(column):
    '''
    Performs a circular byte left shift on a column or row
    '''
    temp = column[0]
    for i in range(0, len(column) - 1):
        column[i] = column[i + 1]
    column[len(column) - 1] = temp
    return column


def circular_byte_right_shift(column):
    '''
    Performs a circular byte right shift on a column or row
    '''
    temp = column[len(column) - 1]
    for i in range(len(column) - 1, 0, -1):
        column[i] = column[i - 1]
    column[0] = temp
    return column

def SBox_substitution(element):
    '''
    Performs S-Box substitution on an element
    '''
    index = element.intValue()
    return BitVector(intVal=Sbox[index], size=8)


def inverse_SBox_substitution(element):
    '''
    Performs inverse S-Box substitution on an element
    '''
    index = element.intValue()
    return BitVector(intVal=InvSbox[index], size=8)


def g_operation(last_column, round_constant):
    '''
    1.Circular byte left shift
    2.S-Box substitution
    3.XOR with round constant
    '''

    # 1. Circular byte left shift
    last_column = circular_byte_left_shift(last_column)

    # 2. S-Box substitution
    for i in range(0, len(last_column)):
        last_column[i] = SBox_substitution(last_column[i])

    # 3. XOR with round constant
    last_column[0] = last_column[0] ^ round_constant
    # debug
    # print_1D_bitVector_array(last_column)

    return last_column


def print_all_round_keys(keys):
    '''
    Prints all the round keys in column major order
    '''
    for i in range(0, len(keys)):
        print("Round Key " + str(i) + ":", end=" ")
        for j in range(0, len(keys[0])):
            for k in range(0, len(keys[0][0])):
                print(keys[i][k][j].getHexStringFromBitVector(), end=" ")
        print()



def key_expansion(key, AES_length):
    '''
        Takes in a padded/trimmed key and
        Generates all the round keys
    '''
    n = len(key)
    key = string_to_hex_array(key)
    key = convert_to_2D_array_key(key)

    keys = []

    # print_2D_bitVector_array(keys)

    # Round constant initialization
    round_constant_array = []
    round_constant = BitVector(hexstring="01")
    round_constant_array.append(round_constant)

    for i in range(1, roundsMap[AES_length] + 1):
        round_constant = round_constant.gf_multiply_modular(BitVector(hexstring="02"), AES_modulus, 8)
        round_constant_array.append(round_constant)

    N = AES_length // 32

    #print_1D_bitVector_array(round_constant_array)
    for i in range(0, 4 * (roundsMap[AES_length]+1)):
        '''
        Perform g operation
        '''
        if i < N:
            keys.append(key[i])

        elif i >= N and i % N == 0:
            temp_last_word = []
            for j in range(0, len(keys[i-1])):
                temp_last_word.append(keys[i-1][j])
            temp_last_word = g_operation(temp_last_word, round_constant_array[(i-1)//N])
            for j in range(0, len(temp_last_word)):
                temp_last_word[j] = temp_last_word[j] ^ keys[i - N][j]
            keys.append(temp_last_word)

        elif i >= N and N > 6 and i % N == 4:
            temp_last_word = []
            for j in range(0, len(keys[i-1])):
                temp_last_word.append(SBox_substitution(keys[i-1][j]))
            for j in range(0, len(temp_last_word)):
                temp_last_word[j] = temp_last_word[j] ^ keys[i - N][j]
            keys.append(temp_last_word)

        else:
            temp_last_word = []
            for j in range(0, len(keys[i-1])):
                temp_last_word.append(keys[i-1][j] ^ keys[i - N][j])
            keys.append(temp_last_word)

    return keys


def key_generation(key):
    '''
    Takes in a padded/trimmed key and
    Generates all the round keys
    '''
    n = len(key)
    key = string_to_hex_array(key)
    key = convert_to_2D_array(key)

    # debug
    # print_2D_bitVector_array(key)
    keys = []
    keys.append(key)

    # Round constant initialization
    round_constant = BitVector(hexstring="01")
    for i in range(1, roundsMap[n * 8] + 1):
        '''
        Perform g function on the last column of the previous key
        '''
        temp_last_column = []
        for j in range(len(keys[i - 1])):
            temp_last_column.append(keys[i - 1][j][3])

        temp_last_column = g_operation(temp_last_column, round_constant)

        # Calculate the first column of the new key by XORing the first column of the previous key
        # with the g(last column) of the previous key
        temp = []
        for j in range(len(temp_last_column)):
            temp.append(keys[i - 1][j][0] ^ temp_last_column[j])
        temp2 = []
        temp2.append(temp)

        # Calculate the remaining columns of the new key by XORing the previous column of the new key
        for j in range(1, len(keys[i - 1])):
            temp = []
            for k in range(len(keys[i - 1][j])):
                temp.append(keys[i - 1][k][j] ^ temp2[j - 1][k])
            temp2.append(temp)

        # Transpose the 2D array to make it column major
        temp2 = transpose(temp2)
        keys.append(temp2)

        # update the round constant
        round_constant = round_constant.gf_multiply_modular(BitVector(hexstring="02"), AES_modulus, 8)

    return keys


def add_padding_to_plaintext(plaintext, AES_length):
    '''
    Adds padding to the plaintext with space if needed
    '''
    if len(plaintext) % (16) == 0:
        return plaintext
    else:
        while len(plaintext) % (16) != 0:
            plaintext += " "
        return plaintext


def trims_or_pads_key(key, AES_length):
    '''
    Trims or pads the key to make it of the required length
    '''
    if len(key) == (AES_length // 8):
        return key
    elif len(key) > (AES_length // 8):
        return key[:(AES_length // 8)]
    else:
        while len(key) < (AES_length // 8):
            key += "0"
        return key


def add_round_key(text, roundKey):
    '''
    XORs the text with the round key
    '''
    for i in range(0, len(text)):
        for j in range(0, len(text[0])):
            text[i][j] = text[i][j] ^ roundKey[i][j]
    return text


def shift_rows(text):
    '''
    Shifts the rows(circular byte left shift) of the text
    '''
    for i in range(0, len(text)):
        for j in range(0, i):
            text[i] = circular_byte_left_shift(text[i])
    return text


def inverse_shift_rows(text):
    '''
    Shifts the rows(circular byte right shift) of the text
    '''
    for i in range(0, len(text)):
        for j in range(0, i):
            text[i] = circular_byte_right_shift(text[i])
    return text


def mix_columns(text, isEncryption):
    '''
    Mixes the columns of the text
    '''
    if isEncryption:
        mat = Mixer
    else:
        mat = InvMixer

    # initialize return matrix
    return_matrix = []
    for i in range(0, len(text)):
        return_matrix.append([])
        for j in range(0, len(text[0])):
            return_matrix[i].append(BitVector(intVal=0, size=8))

    # start mix column operation
    for i in range(0, len(text)):
        for j in range(0, len(text[0])):
            for k in range(0, len(text)):
                   return_matrix[i][j] = (return_matrix[i][j] ^ (mat[i][k].gf_multiply_modular(text[k][j], AES_modulus, 8)))
    return return_matrix


def convert_2D_to_1D_array(text):
    '''
    Converts the 2D array to a 1D array in column major order
    '''
    temp = []
    for i in range(0, len(text)):
        for j in range(0, len(text[0])):
            temp.append(text[j][i])
    return temp


def AES_encrypt_helper(text, roundKeys, AES_length):
    '''
    :param text: 1D array of hex values
    :param roundKeys: all the round keys
    :param AES_length: 128/192/256
    :return: ciphertext as a 1D array of hex values
    '''
    # First convert the hex 1D array to a 2D array of bitvectors in column major order
    text = convert_to_2D_array(text)

    # Round 0 : Add round key 0
    temp_round_key = []
    for i in range(0, 4):
        temp_round_key.append(roundKeys[i])

    temp_round_key = transpose(temp_round_key)

    # Round 0: XOR the text with the round key
    text = add_round_key(text, temp_round_key)

    for i in range(1, roundsMap[AES_length] + 1):
        # Round i.1 : SubBytes
        for j in range(0, len(text)):
            for k in range(0, len(text[0])):
                text[j][k] = SBox_substitution(text[j][k])

        # Round i.2 : Shift Rows
        text = shift_rows(text)

        # Round i.3 : Mix Columns
        if i != roundsMap[AES_length]:
            text = mix_columns(text, True)

        # Round i.4 : Add round key i
        temp_round_key = []
        for j in range(4*i, 4*(i+1)):
            temp_round_key.append(roundKeys[j])
        temp_round_key = transpose(temp_round_key)
        text = add_round_key(text, temp_round_key)

    # Convert the 2D array to a 1D array in column major order
    text = convert_2D_to_1D_array(text)
    return text



def AES_encrypt(plaintext, keytext, AES_length, IV):
    '''
    Encrypts the plaintext using the key
    '''
    global key_scheduling_time
    global encryption_time

    # Add padding to the plaintext if needed
    # text = add_padding_to_plaintext(plaintext, AES_length)
    # Convert the plaintext to hex array
    text = string_to_hex_array(plaintext)
    # add padding to the text
    text = generalized_Padding(text)

    # Handle variable length key
    key = trims_or_pads_key(keytext, AES_length)
    # Generate all the round keys
    key_scheduling_time = time.time()
    roundKeys = key_expansion(key, AES_length)
    key_scheduling_time = (time.time() - key_scheduling_time) * 1000

    # Encrypt the plaintext
    blocksize = 16
    ciphertext = []

    # Preperaing IV
    tem_IV= []
    for i in range(0, len(IV)):
        tem_IV.append(IV[i])

    encryption_time = time.time()
    for i in range(0, len(text), blocksize):
        text_to_send = text[i:i + blocksize]

        # CBC
        # XOR with IV
        for j in range(0, len(text_to_send)):
            text_to_send[j] = (BitVector(hexstring=text_to_send[j]) ^ tem_IV[j]).getHexStringFromBitVector()

        tmp = (AES_encrypt_helper(text_to_send, roundKeys, AES_length))
        for j in range(0, len(tmp)):
            ciphertext.append(tmp[j].get_hex_string_from_bitvector())

        # Update IV
        tem_IV = tmp

    encryption_time = (time.time() - encryption_time) * 1000
    return ciphertext


def AES_decrypt_helper(ciphertext, roundKeys, AES_length):
    '''
    :param ciphertext: 1D array of hex values of ciohertext
    :param roundKeys: all the round keys
    :param AES_length:  128/192/256
    :return: 1D array of decrypted hex values
    '''
    # First convert the hex 1D array to a 2D array of bitvectors in column major order
    ciphertext = convert_to_2D_array(ciphertext)

    temp_round_key = []

    for i in range(roundsMap[AES_length], 0, -1):
        # Round i.1 : Add round key i
        temp_round_key = []
        for j in range(4 * i, 4 * (i + 1)):
            temp_round_key.append(roundKeys[j])
        temp_round_key = transpose(temp_round_key)
        ciphertext = add_round_key(ciphertext, temp_round_key)

        # Round i.2 : Inverse Mix Columns
        if i != roundsMap[AES_length]:
            ciphertext = mix_columns(ciphertext, False)

        # Round i.3 : Inverse SubBytes
        for j in range(0, len(ciphertext)):
            for k in range(0, len(ciphertext[0])):
                ciphertext[j][k] = inverse_SBox_substitution(ciphertext[j][k])

        # Round i.3 : Shift Rows
        ciphertext = inverse_shift_rows(ciphertext)


    temp_round_key = []
    for i in range(0, 4):
        temp_round_key.append(roundKeys[i])

    temp_round_key = transpose(temp_round_key)
    # Round 0 : Add round key 0
    ciphertext = add_round_key(ciphertext, temp_round_key)

    # Convert the 2D array to a 1D array in column major order
    plaintext = convert_2D_to_1D_array(ciphertext)
    return plaintext



def AES_decrypt(ciphertext, keytext, AES_length, IV):
    '''
    Decrypts the ciphertext using the key
    '''
    global decryption_time

    # Handle variable length key
    key = trims_or_pads_key(keytext, AES_length)
    # Generate all the round keys
    roundKeys = key_expansion(key,AES_length)

    # Decrypt the ciphertext
    blocksize = 16
    plaintext = []

    temp_IV= []
    for i in range(0, len(IV)):
        temp_IV.append(IV[i])

    decryption_time = time.time()
    for i in range(0, len(ciphertext), blocksize):
        next_IV = []
        for j in range(0, len(ciphertext[i:i + blocksize])):
            next_IV.append(BitVector(hexstring=ciphertext[i:i + blocksize][j]))


        tmp = (AES_decrypt_helper(ciphertext[i:i + blocksize], roundKeys, AES_length))

        # CBC
        # XOR with IV
        for j in range(0, len(tmp)):
            tmp[j] = tmp[j] ^ temp_IV[j]

        # Update IV
        temp_IV = []
        for j in range(0, len(next_IV)):
            temp_IV.append(next_IV[j])

        for j in range(0, len(tmp)):
            plaintext.append(tmp[j].get_hex_string_from_bitvector())

    decryption_time = (time.time() - decryption_time) * 1000
    # # Remove padding
    # plaintext = generalized_unPadding(plaintext)
    #
    # # Convert the hex array to a string
    # plaintext = hex_array_to_string(plaintext)
    return plaintext


def hex_array_to_string(hex_array):
    '''
    First converts the hex array to a ASCII array
    then concerts the ASCII array to a string
    '''
    ascii_array = []
    for i in range(0, len(hex_array)):
        ascii_array.append(chr(int(hex_array[i], 16)))
    return "".join(ascii_array)



def IV_generator():
    '''
    Generates a random IV
    '''
    IV = []
    for i in range(0, 16):
        IV.append(BitVector(intVal=random.randint(0, 255), size=8))
    return IV


def generalized_Padding(hexArray):
    '''
    :param hexArray: hexarray of plaintext
    :return:
    '''
    blocksize = 16
    padding_size = 16 - (len(hexArray) % blocksize)
    for i in range(0, padding_size):
        hexArray.append(hex(padding_size)[2:])
    return hexArray


def generalized_unPadding(hexArray):
    '''
    :param hexArray: hexarray of plaintext
    :return:
    '''
    blocksize = 16
    padding_size = int(hexArray[-1], 16)
    for i in range(0, padding_size):
        hexArray.pop()
    return hexArray


def print_hex_array(hexArray):
    '''
    Prints the hex array
    '''
    for i in range(0, len(hexArray)):
        print(hexArray[i], end=" ")
    print()


def main():
    # key = string_to_hex_array("Thats my Kung Fu")
    # print(key)
    # t = convert_to_2D_array(key)
    # for i in range(0, len(t)):
    #     for j in range(0, len(t[0])):
    #         print(t[i][j].getHexStringFromBitVector(), end=" ")
    # keys = key_generation("Thats my Kung Fu")
    # print_all_round_keys(keys)
    # print(len(keys))
    # print(trims_or_pads_key("Thats my Kung Fuck", 128))
    # print(add_padding_to_plaintext("Two One Nine Two", 128))

    # IV = IV_generator()
    # ciphertext = AES_encrypt("Two One Nine twoo", "Thats my Kung Fuuuu", 192, IV)
    # print(ciphertext)
    # plaintext = AES_decrypt(ciphertext, "Thats my Kung Fuuuu", 192, IV)
    # print(plaintext)


    # hexArray = string_to_hex_array("Two One Tine Two1")
    # hexArray = generalized_Padding(hexArray)
    # print(hexArray)
    # hexArray = generalized_unPadding(hexArray)
    # print(hexArray)

    # key = trims_or_pads_key("Thats my Kung Fu",128)
    # key_expansion(key,128)

    AES_length = 192

    key = "BUET CSE19 Batch"
    print("Key:")
    print("In ASCII:", end=" ")
    print(key)
    padded_key = trims_or_pads_key(key, AES_length)
    hexKey = string_to_hex_array(key)
    print("In HEX", end=" ")
    print_hex_array(hexKey)
    print()

    text = "Never Gonna Give you up"
    print("Plain Text:")
    print("In ASCII:", end=" ")
    print(text)
    hexText = string_to_hex_array(text)
    hexTextWithPadding = generalized_Padding(hexText)
    print("In HEX:", end=" ")
    print_hex_array(hexTextWithPadding)
    print()


    IV = IV_generator()
    ciphered_hex_array = AES_encrypt(text, key, AES_length, IV)
    print("Ciphered Text:")
    print("In HEX:", end=" ")
    print_hex_array(ciphered_hex_array)
    print("In ASCII:", end=" ")
    print(hex_array_to_string(ciphered_hex_array))
    print()


    deciphered_hex_array = AES_decrypt(ciphered_hex_array, key, AES_length, IV)
    print("Deciphered Text:")
    print("In HEX:", end=" ")
    print_hex_array(deciphered_hex_array)
    deciphered_hex_array = generalized_unPadding(deciphered_hex_array)
    print("In ASCII:", end=" ")
    print(hex_array_to_string(deciphered_hex_array))
    print()

    print("Execution Time Details:")
    print(f"Key Generation Time: {key_scheduling_time:.4f} ms")
    print(f"Encryption Time: {encryption_time:.4f} ms")
    print(f"Decryption Time: {decryption_time:.4f} ms")




if __name__ == "__main__":
    main()
