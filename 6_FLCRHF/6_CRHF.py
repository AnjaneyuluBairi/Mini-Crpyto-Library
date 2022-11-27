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

def call_hash_func():
    x1=gen(N)
    x2=gen(N)
    print("Fixed length inputs are x1 = ",x1," ,x2= ",x2)
    compressed_msg = FLHF(x1, x2)
    print("o/p using FLHF")
    print(compressed_msg)
   

if __name__ == "__main__":
    call_hash_func()
