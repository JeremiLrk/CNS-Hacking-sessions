import requests
from sympy import public

URL = "http://cns-test.idlab.uantwerpen.be:50011"
params = requests.get(URL + "/params")
directory = requests.get(URL + "/directory")

print(params.text)
print(directory.text)

directory = requests.get(URL + "/directory")
print(directory.text)

p = 7307846879904189030929679948466541795201493576644000827516745178921657491638900092075124066074860350245731460646064790947916261089076564811441840899544337
g = 2

chosen_private = 67

public_key = pow(g, chosen_private, p)

data = {
    "name" : "james",
    "y" : str(public_key)
}
person = requests.post(URL + "/directory", json=data)
print(person.text)


alice = requests.get(URL + "/send?to=james")
print(alice.text)
c1 = 6650307962615851677499833107994869194424764163641477556364085759107236592635664599215457722468775428446993689850965433275791404491787599932426879711536249
c2 = 1697046910264470721175517743700633324650469373949341032828687289450888724018777679556226974866198240043841351011196071344796377844242365351419507074728264

K = pow(c1, chosen_private, p)
K_inverse = pow(K, -1, p)
Message = pow(c2*K_inverse, 1, p)

length = (Message.bit_length() + 7) // 8
answer = Message.to_bytes(length, byteorder="big")
print(answer)