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


def CRHF(msg, IV): #merkle-damgard transformation
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
    B = L//N  # each block length is N=16 and output length will be 16
    msg=msg+bin_len
    L=len(msg)
    for i in range(0, L, N):
        x = msg[i:i+N]  # taking msg part
        Z = FLHF(x, Z)  # passing msg and Z
    return Z

def HMAC(msg,IV,key,ipad,opad):
    #key is also length of N =16
    #IV also length of N=16
    ipad_len=len(ipad)
    opad_len=len(opad)
    while(ipad_len!=N):
        ipad=ipad+ipad
        opad=opad+opad
        ipad_len=2*ipad_len

    kxoripad=bin(int(key,2)^int(ipad,2)).replace('0b','').zfill(N)
    kxoropad=bin(int(key,2)^int(opad,2)).replace('0b','').zfill(N)
    Z0=FLHF(kxoripad,IV)
    Z=CRHF(msg,Z0)
    Zn=FLHF(kxoropad,IV)
    HMAC_TAG=FLHF(Z,Zn)
    return HMAC_TAG


def call_hash_func():
    #print("Enter message")
    msg = gen(pow(2, 6))
    print(msg)
    IV = gen(N)
    print("o/p using HMAC")
    ipad='00110110'
    opad='01011100'
    key=gen(N)
    HMAC_TAG=HMAC(msg,IV,key,ipad,opad)
    print(HMAC_TAG)



if __name__ == "__main__":
    call_hash_func()
