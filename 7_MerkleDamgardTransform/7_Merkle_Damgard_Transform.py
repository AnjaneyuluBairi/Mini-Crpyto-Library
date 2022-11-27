import random
import math
N = 16  # this is one of input length of hash function 
GENERATOR = 6 #primitive roots for 60271
H_VAL = 7 #primitive roots for 60271


MODULUS = 60271 #this is 16 bit prime number

def gen(n):
    key1 = ""
    for i in range(n):
        temp = str(random.randint(0, 1))
        key1 = key1+temp
    return key1


def FLHF(x1, x2):
    num1 = pow(GENERATOR, int(x1, 2), MODULUS)
    num2 = pow(H_VAL, int(x2, 2), MODULUS)
    ans = (num1*num2) % MODULUS
    ans = bin(ans).replace('0b', '').zfill(N)
    return ans


def CRHF(msg, IV):
    L = len(msg)
    rem = L % N
    if rem != 0:
        temp = msg[-1:rem:].zfill(N)
        msg = msg[:-1*rem]
        msg = msg+temp
    bin_len=bin(math.ceil(math.log2(L))).replace('0b','').zfill(N)

    L = len(msg)
    hash_list = list()
    Z = IV  # inital second input is Z which is IV
    B = L//N  # each block length is N=512 and output length will be 512
    msg=msg+bin_len
    L=len(msg)
    for i in range(0, L, N):
        x = msg[i:i+N]  # taking msg part
        Z = FLHF(x, Z)  # passing msg and Z
    return Z



def call_hash_func():
    #print("Enter message")
    msg = gen(pow(2,6))
    print("Input message is")
    print(msg)
    IV = gen(N)
    compressed_msg = CRHF(msg, IV)
    print("MAC using Merkle-damgard transform is")
    print(compressed_msg)
    
if __name__ == "__main__":
    call_hash_func()
