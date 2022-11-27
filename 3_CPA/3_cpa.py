import random
from unittest import result



SEED_SIZE = 16
GENERATOR = 2462  # primitive root
MODULUS = 18443
BLOCK_SIZE = 16



def L(x):
	return 2*x;

def OWF(x,r):
	mod_exp = bin(pow(GENERATOR, int(x,2), MODULUS)).replace('0b', '').zfill(SEED_SIZE)
	hc=0
	for i in range(len(x)):
		hc=(hc^(int(x[i])&int(r[i])))%2
	return mod_exp+r+str(hc)
	
def PRG(SEED):
	result=""
	SEED_LEN=len(SEED)
	output_len=L(SEED_SIZE)
	for i in range(output_len):
		x=SEED[:len(SEED)//2]
		r=SEED[len(SEED)//2:]
		g=OWF(x,r)
		result=result+str(g[-1])
		SEED=g[:-1]
	return result

def PRF(k,x): #key and tree number Fk(x)
	
	for i in x: # for every bit in x make a tree
		g=PRG(k)
		n=len(g)
		if i==0: #g0
			k=g[:int(n/2)]
		else:	 #g1
			k=g[int(n/2):]
	return k


def gen(n):
    key1 = ""
    for i in range(n):
        temp = str(random.randint(0, 1))
        key1 = key1+temp
    return key1


def Encr_cpa(m, k, r):
    f = PRF(k, r)  # Fk(r)
    msg_len = len(m)
    rem = msg_len % BLOCK_SIZE
    total_blocks = msg_len//BLOCK_SIZE
    cipher_blocks = list()
    for block in range(0, msg_len-rem, BLOCK_SIZE):
        msg_bits = m[block:block+BLOCK_SIZE]
        cipher_text = ""
        for i in range(len(msg_bits)):
            xor_val = int(msg_bits[i]) ^ int(f[i])
            cipher_text += str(xor_val)
        cipher_blocks.append(cipher_text)
        f = PRF(k, f)

    if rem != 0:
        cipher_text = ""
        msg_bits = m[-1*rem:]
        for i in range(rem):
            xor_val = int(msg_bits[i]) ^ int(f[i])
            cipher_text += str(xor_val)
        cipher_blocks.append(cipher_text)
    final_cipher = ""
    for text in cipher_blocks:
        final_cipher += text
    return final_cipher


def Decr_cpa(m, k, r):
    # sending cipher to text same algo instead of plain text
    plain_text = Encr_cpa(m, k, r)
    return plain_text


if __name__ == "__main__":
    key = gen(BLOCK_SIZE)
    print("Enter message")
    message = input()
    print("Original Text: ", message)

    r = gen(BLOCK_SIZE)  # IV uniform vector INITIALIZATION VECTOR
    cipher_text = Encr_cpa(message, key, r)
    print("Encrypted Text: ", cipher_text)
   
    plain_text = Decr_cpa(cipher_text, key, r)
   
    print(plain_text == message)
    print("Decrypted Text: ", plain_text)
