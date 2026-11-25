p = 6746884642898045158586100770737756293393842294217621284683764334092675665317142415412395870329547530242099335486421376675198692609457054882379293678037631
q = 828501186989456969634087545115821181461968049491
g = 4771346124025851787008537691957768340119708194592789003251318422138883835679180113071550689720819538734622694321320763375269264613538770908685537501076695
y = 51421953478148373341502434435209534945979140302697738580686333856428250387931563065532531018805972910300248283132473420251649607983785126255366520848710
hash = "H(m) = int(sha256(m)) mod q",
signatures =  [
        {
            "message": "Transfer 10 EUR to Alice",
            "r": 259424547497814479088341768889640828593313868574,
            "s": 434602912726934846699458227108070269471546402108
        },
        {
            "message": "Transfer 25 EUR to Bob",
            "r": 259424547497814479088341768889640828593313868574,
            "s": 410136646881530712205473169074431276894954478027
        }
    ]

encrypted_flag = "59ac8f6ac4e5b3832ed05eea9b6abeb654b3bbf446a01dbe6b833be38968fc0cb9"
flag_encryption = "flag XOR keystream, keystream = sha256(f'{x}:0') || sha256(f'{x}:1') || ..., x = private key"


import hashlib
M1 = signatures[0]["message"]
M2 = signatures[1]["message"]

H1 = int.from_bytes(hashlib.sha256(M1.encode()).digest(), "big")
hash1 = pow(H1,1,q)

H2 = int.from_bytes(hashlib.sha256(M2.encode()).digest(), "big")
hash2 = pow(H2,1,q)

r = signatures[0]["r"]
s1 = signatures[0]["s"]
s2 = signatures[1]["s"]

temp = pow(s1 - s2, -1, q)
k = pow((hash1 - hash2)*temp, 1, q)
print(k)

r_inverse = pow(r, -1, q)
x = pow((k*s1 - hash1)*r_inverse, 1, q)



keystream_temp = hashlib.sha256(f'{x}:0'.encode()).hexdigest() + hashlib.sha256(f'{x}:1'.encode()).hexdigest()
size = len(encrypted_flag)
keystream = keystream_temp[:size]
print(keystream_temp)
print(keystream)
print(encrypted_flag)

keystream_bytes = bytes.fromhex(keystream)
encrypted_bytes = bytes.fromhex(encrypted_flag)

answer = bytes(a ^ b for a, b in zip(keystream_bytes, encrypted_bytes))
print(answer)

