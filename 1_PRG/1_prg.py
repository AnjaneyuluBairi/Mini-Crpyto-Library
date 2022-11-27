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

if __name__ == "__main__":
	print("Enter seed for PRG")
	x=input()
	print(PRG(x))


