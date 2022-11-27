import random
N=16


SEED_SIZE  = 16
GENERATOR  = 2462 #primitive root
MODULUS    = 18443

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



def CBC_MAC_input():
    print("Enter message")
    msg=input()
    key=gen(N) #key for PRF
    r=gen(N)  # i think we dont need it ,check it later anyway
    tag=CBC_MAC(msg,key,N)
    print("tags: ",tag)
    ver_tags=verification_CBC_MAC(msg,key,N,tag)
    if ver_tags:
        print("tag is matching at the receiver side")
    else:
        print("tag is not matching at the receiver side")


if __name__== "__main__":
    CBC_MAC_input()
    