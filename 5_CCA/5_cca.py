
SEED_SIZE  = 16
GENERATOR  = 2462 #primitive root
MODULUS    = 18443
N=16
BLOCK_SIZE=16
import random

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

def gen(n):
    key1=""
    for i in range(n):
        temp=str(random.randint(0,1))
        key1=key1+temp
    return key1


def CBC_MAC(msg,key,N):
    #N is block length and r is IV(Initialization vector)
    len_msg=len(msg)
    bin_value_len_msg=bin(len_msg).replace('0b','')
    msg_blocks=int(len(msg)/N)
    rem=len(msg)%N

    if rem!=0:
        temp=msg[-1*rem:].zfill(N) # padding last block with 0s and storing into temp
        msg=msg[:-1*rem] #deleting last block ,which is not having perfect length 'N'
        msg=msg+temp #adding that last block to msg
    new_msg=bin_value_len_msg+msg #adding msg length to msg 

    xor_vec='0'*N  # for xoring with message length block
    #here we need to divide msg into blocks of length 'N'

    for i in range(0,len(new_msg),N):
        msg_bits=new_msg[i:i+N]
        f_ip=bin(int(msg_bits,2)^int(xor_vec,2)).replace('0b','')
        f=PRF(key,f_ip)
        xor_vec=f # this PRF's output is input for next XOR opearation with next msg_block
    mac_tag=f #output of PRF's contains final mac tag
    return mac_tag

def verification_CBC_MAC(msg,key,N,tag):
    re_tag=CBC_MAC(msg,key,N)
    return re_tag==tag

def Encr_cca(msg,key1,r1,key2,N):
    cipher_msg=Encr_cpa(msg,key1,r1)
    len_cipher=len(cipher_msg)
    mac_tag=CBC_MAC(cipher_msg,key2,N)
    return [cipher_msg,mac_tag]

def Decr_cca(msg,key1,key2,r1,tag,N):
    plain_msg=Decr_cpa(msg,key1,r1)

    isTagMatched=verification_CBC_MAC(msg,key2,N,tag)
    if isTagMatched:
        print("decrypted successfully and tag is matching")
        return plain_msg
    else:
        print("Error in MAC")
        return ""

def CCA_CBC():
    print("Enter message")
    msg=input()
    key1=gen(N)
    key2=gen(N)
    r1=gen(N) #for Encrypion ( CPA in PRF)
    enc_text=Encr_cca(msg,key1,r1,key2,N)
    mac_tag=enc_text[1]
    cipher_msg=enc_text[0]
    plain_text=Decr_cca(cipher_msg,key1,key2,r1,mac_tag,N)
    print("decrypted message = ",plain_text)


if __name__ == "__main__":
   # CCA_MAC()
   CCA_CBC()
    
