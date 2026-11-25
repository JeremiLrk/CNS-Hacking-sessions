# Digital Signatures

**Studeerroute** · Notatie en formules → eigenschappen van handtekeningen → DSA-bewijs en code → RSA-PSS, MGF1 en volledige verificatie. Behandelt Part 4, pdf-pagina’s 58–73, ook de stof zonder bijbehorende oefening.

De afzender ondertekent een bericht met een private sleutel. De ontvanger controleert het bericht en de handtekening met de publieke sleutel van de afzender. De cursus behandelt **DSA** en **RSA-PSS**. Bron: *Part 4 — Asymmetric Encryption*, slides 71–81 (pdf-pagina’s 59–73).

## DSA — cursus naast Double Entry

Slides 74–76 (pdf-pagina’s 63–65). Bij DSA komen de namen **p, q, g en y letterlijk overeen met de JSON**. p is de priemmodulus van de groep. q is de orde van de subgroep en deelt p − 1. De vertaling van ElGamal waarbij cursus-q overeenkwam met JSON-p geldt hier dus niet.

Neem één record `sig = signatures[i]`. Hieronder is `z` de hash van zijn bericht als geheel getal modulo q, volgens de regel van deze opgave. x en k zijn geheime rekenvariabelen. Het zijn geen invoervelden. Een superscript −1 betekent de modulaire inverse.

| Stap | Cursusformule | Met de namen van de JSON |
| --- | --- | --- |
| Generator kiezen | g = h^((p−1)/q) mod p | De JSON geeft de berekende waarde `g`. De hulpwaarde h staat niet in het bestand. |
| Publieke sleutel | y = g^x mod p | `y = pow(g, x, p)` |
| Berichthash | H(M) | `z = int.from_bytes(sha256(sig["message"].encode()).digest(), "big") % q` |
| Ondertekenen, eerste component | r = (g^k mod p) mod q | `sig["r"] = pow(g, k, p) % q` |
| Ondertekenen, tweede component | s = k⁻¹(H(M) + xr) mod q | `sig["s"] = (pow(k, -1, q) * (z + x * sig["r"])) % q` |
| Verificatie voorbereiden | w = (s′)⁻¹ mod q | `w = pow(sig["s"], -1, q)` |
| Twee exponenten berekenen | u₁ = H(M′)w mod q, u₂ = r′w mod q | `u1 = z*w % q`, `u2 = sig["r"]*w % q` |
| Verificatie afronden | v = ((g^u₁ · y^u₂) mod p) mod q | `v = ((pow(g,u1,p) * pow(y,u2,p)) % p) % q` |

Bij verificatie controleer je eerst 0 < r′, s′ < q. Daarna accepteer je als v = r′. De accenten op de slides duiden de **ontvangen** waarden aan. In de JSON zijn dat gewoon `message`, `r` en `s`. Bij ondertekening krijgt elk bericht een eigen geheime k en moeten r en s beide ongelijk aan nul zijn.

## RSA-PSS — dezelfde taak met een RSA-sleutel

Slides 77–80 (pdf-pagina’s 66–72). Deze opgave bevat uitsluitend DSA-velden. Voor RSA-PSS staat hieronder de cursusnotatie met de gebruikelijke betekenis van elke variabele.

| Stap | Cursusformule | Wat gebeurt er? |
| --- | --- | --- |
| Bericht coderen | mHash = Hash(M), H = Hash(acht nulbytes ∥ mHash ∥ salt) | De afzender kiest een salt en bouwt een datablok uit nulbytes, een scheidingsbyte en de salt. |
| Maskeren | maskedDB = DB ⊕ MGF(H), EM = maskedDB ∥ H ∥ 0xbc | Het masker heeft de lengte van DB. De ongebruikte hoogste bits worden gewist zoals voorgeschreven door de gekozen sleutellengte. |
| Ondertekenen | s = em^d mod n | em is de gehele-getalrepresentatie van EM. d is de private RSA-exponent. |
| Verifiëren | em = s^e mod n | De ontvanger reconstrueert EM, controleert lengte, bits, scheidingsbyte en eindbyte, herstelt de salt en controleert de hash tegen het ontvangen bericht. |

DSA levert een paar (r, s). RSA-PSS levert één handtekening s. De DSA-nonce k blijft geheim. De PSS-salt mag de verificateur uit de codering terughalen.

[Oefening 1 — Double Entry](01-Double-Entry/README.md)

## Wat bewijst een handtekening? · pdf 58–62

Alice ondertekent een welbepaalde bytevolgorde met haar private sleutel. De verificateur heeft diezelfde bytes, de handtekening en een authentieke publieke sleutel nodig. Een geldige verificatie bindt de inhoud aan die sleutel. De binding van de sleutel aan de naam ‘Alice’ volgt bijvoorbeeld uit een certificaat. Bewijs van het tijdstip vereist een betrouwbare tijdsbron of een vertrouwd tijdstempel. Een datum die de ondertekenaar zelf in het bericht schrijft is alleen een ondertekende bewering over die datum.

| Begrip | Gevolg voor een betwiste overschrijving |
| --- | --- |
| Integriteit | Een andere omschrijving, spatie of bedrag wijzigt het te verifiëren bericht. |
| Authenticiteit | De handtekening wordt gecontroleerd onder de publieke sleutel van de vermeende afzender. |
| Verificatie door derden | Een derde kan met de publieke sleutel hetzelfde bewijs controleren. Bij een gedeelde MAC-sleutel kunnen beide houders een geldige tag maken. |
| Onweerlegbaarheid | Publiek controleerbare handtekeningen kunnen bewijs ondersteunen. Bewaring van sleutel, certificaatstatus en tijdstip bepalen hoe sterk dat bewijs is. |
| Vertrouwelijkheid | Een ondertekend bericht kan volledig leesbaar blijven. Voor geheimhouding is afzonderlijke versleuteling nodig. |

In het schema op slide 71 produceren ondertekenaar en ontvanger de hash elk zelf. Wie een nieuw bericht met dezelfde hash kan construeren, kan die binding ondermijnen. Een hash alleen vertelt niet wie hem berekende. Het hoofdstuk behandelt de historische DSA-standaard en onderscheidt de algoritmen in de bredere DSS-standaardenfamilie, waaronder RSA en elliptische-krommevarianten.

## Waarom v gelijk is aan r bij DSA · pdf 63–65

De generator ligt in een subgroep van orde q. Kies een geschikte h en bereken g = h^((p−1)/q) mod p. Bij g=1 wordt opnieuw gekozen. Omdat g^q = 1 mod p, kunnen de exponenten in die subgroep modulo q worden behandeld. **Mod p** gebruik je bij groepsbewerkingen. **Mod q** gebruik je bij de scalairen x, k, r, s en hun inversen. Het veld `hash` in Double Entry beschrijft expliciet een integer uit SHA-256 modulo q. In standaardspecificaties kan de omzetting van digest naar z ook een bitafkapping voorschrijven; volg de definitie van het schema dat je verifieert.

Uit s ≡ k⁻¹(z+xr) mod q volgt ks ≡ z+xr. Voor geldige s bestaat w=s⁻¹. Dan k ≡ zw+xrw ≡ u₁+xu₂ mod q. Daaruit volgt g^u₁·y^u₂ ≡ g^(u₁+xu₂) ≡ g^k mod p. Na de laatste reductie modulo q krijgt de ontvanger r terug. Het bericht beïnvloedt u₁ via z, ook al bestaat de eindtest uit een vergelijking met r.

```python
from hashlib import sha256
from secrets import randbelow

def berichtwaarde(bericht, q):
    return int.from_bytes(sha256(bericht).digest(), "big") % q

def onderteken(bericht, p, q, g, x):
    z = berichtwaarde(bericht, q)
    while True:
        k = 1 + randbelow(q - 1)
        r = pow(g, k, p) % q
        s = pow(k, -1, q) * (z + x * r) % q
        if r and s:
            return r, s

def verifieer(bericht, handtekening, p, q, g, y):
    r, s = handtekening
    if not (0 < r < q and 0 < s < q):
        return False
    w = pow(s, -1, q)
    u1 = berichtwaarde(bericht, q) * w % q
    u2 = r * w % q
    element = pow(g, u1, p) * pow(y, u2, p) % p
    return element % q == r

# Kleine, vooraf gekozen cursusgroep en eigen ondertekenaar.
p, q, h, x = 23, 11, 2, 3
g = pow(h, (p - 1) // q, p)
assert g != 1 and pow(g, q, p) == 1
y = pow(g, x, p)
m = b"Ontvangen op dinsdag"
sig = onderteken(m, p, q, g, x)
assert verifieer(m, sig, p, q, g, y)
assert not verifieer(m, (0, 0), p, q, g, y)
```

## RSA-PSS stap voor stap · pdf 66–72

RSA-PSS geeft een bericht een gerandomiseerde codering EM. Neem emBits = bitlengte(n)−1 en emLen = ⌈emBits/8⌉. Met hashgrootte hLen en saltgrootte sLen is de lengte van de nulreeks PS precies emLen−sLen−hLen−2 bytes. Een negatieve lengte betekent dat de parameters niet passen. De acht nulbytes vóór mHash en de nulreeks PS hebben verschillende functies.

1. Bereken mHash = Hash(M). Kies de salt, vorm M′ = acht nulbytes ∥ mHash ∥ salt en bereken H = Hash(M′).
2. Vorm DB = PS ∥ 01 ∥ salt. MGF1 produceert uit H een masker met precies de lengte van DB. XOR geeft maskedDB. Wis bovenaan de 8·emLen−emBits ongebruikte bits.
3. Vorm EM = maskedDB ∥ H ∥ BC. De RSA-private bewerking levert de handtekeninginteger s = em^d mod n. De laatste byte BC en de scheidingsbyte 01 zijn hexadecimale waarden.
4. Verificatie herstelt em = s^e mod n en zet dat om naar emLen bytes. Controleer bereik, lengte, eindbyte en ongebruikte bits, verwijder het masker, wis de ongebruikte bits in DB en controleer PS en 01. Lees de salt uit en bereken H′ uit het ontvangen bericht. Accepteer alleen als alle structuurcontroles slagen en H′ gelijk is aan H.

**MGF1 en de PSS-codering in Python.** MGF1 hasht de seed telkens met een vierbyte big-endian teller die bij nul start. De laatste digest wordt op de gevraagde lengte afgekapt. De vaste salt hieronder maakt het tussenresultaat reproduceerbaar; bij een gewone PSS-ondertekening kiest de ondertekenaar een verse salt.

```python
from hashlib import sha256

def mgf1(seed, lengte):
    if not 0 <= lengte <= (2**32) * sha256().digest_size:
        raise ValueError("Ongeldige maskerlengte.")
    masker = bytearray()
    for teller in range((lengte + 31) // 32):
        masker.extend(sha256(seed + teller.to_bytes(4, "big")).digest())
    return bytes(masker[:lengte])

def pss_codering(bericht, salt, em_bits):
    em_len = (em_bits + 7) // 8
    ps_len = em_len - len(salt) - 32 - 2
    if ps_len < 0:
        raise ValueError("Codering past niet.")
    m_hash = sha256(bericht).digest()
    h = sha256(bytes(8) + m_hash + salt).digest()
    db = bytes(ps_len) + b"\x01" + salt
    masker = mgf1(h, len(db))
    gemaskeerd = bytearray(a ^ b for a, b in zip(db, masker))
    gemaskeerd[0] &= 255 >> (8 * em_len - em_bits)
    return bytes(gemaskeerd) + h + b"\xbc"

assert mgf1(b"abc", 12) == sha256(b"abc" + bytes(4)).digest()[:12]
em = pss_codering(b"college", bytes(range(32)), 2047)
assert len(em) == 256 and em[-1] == 0xBC and em[0] < 128

def controleer_pss_codering(bericht, em, em_bits, salt_lengte):
    if em_bits <= 0 or salt_lengte < 0:
        return False
    em_len = (em_bits + 7) // 8
    ps_len = em_len - salt_lengte - 32 - 2
    if len(em) != em_len or ps_len < 0 or em[-1] != 0xbc:
        return False
    gemaskeerd, h = em[:-33], em[-33:-1]
    toegelaten_bits = 255 >> (8 * em_len - em_bits)
    if gemaskeerd[0] & ~toegelaten_bits:
        return False
    db = bytearray(a ^ b for a, b in zip(gemaskeerd, mgf1(h, len(gemaskeerd))))
    db[0] &= toegelaten_bits
    if db[:ps_len] != bytes(ps_len) or db[ps_len] != 1:
        return False
    salt = db[ps_len + 1:]
    controlehash = sha256(bytes(8) + sha256(bericht).digest() + salt).digest()
    return h == controlehash

assert controleer_pss_codering(b"college", em, 2047, 32)
assert not controleer_pss_codering(b"ander bericht", em, 2047, 32)
assert not controleer_pss_codering(b"college", em[:-1] + bytes(1), 2047, 32)
```

**Volledige PSS-handtekening met verificatie.** Dit zelfstandige Python-blok gebruikt de lokaal geïnstalleerde OpenSSL-opdracht. Het maakt de sleutel in een tijdelijke map. Zowel de ondertekenaar als de verificateur gebruikt SHA-256 en een salt van 32 bytes. De tweede verificatie laat zien waarom de berichtbytes ertoe doen.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run

with TemporaryDirectory() as mapnaam:
    map_pad = Path(mapnaam)
    def openssl(*args, vereist=True):
        return run(["openssl", *args], cwd=map_pad, capture_output=True, check=vereist)

    openssl("genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048",
            "-out", "priv.pem")
    openssl("pkey", "-in", "priv.pem", "-pubout", "-out", "pub.pem")
    bericht = map_pad / "bericht.txt"
    bericht.write_bytes(b"College om 10 uur")
    pss = ["-sigopt", "rsa_padding_mode:pss", "-sigopt", "rsa_pss_saltlen:32"]
    openssl("dgst", "-sha256", "-sign", "priv.pem", *pss, "-out", "sig.bin", "bericht.txt")
    controle = ["dgst", "-sha256", "-verify", "pub.pem", *pss,
                "-signature", "sig.bin", "bericht.txt"]
    assert openssl(*controle).returncode == 0
    bericht.write_bytes(b"College om 11 uur")
    assert openssl(*controle, vereist=False).returncode != 0
```

**Examenvraag.** Waarom kan de salt uit een RSA-PSS-handtekening worden teruggevonden terwijl de DSA-nonce geheim moet blijven? Bij PSS maakt de salt deel uit van de gecodeerde gegevens die de verificateur opnieuw controleert. Bij DSA komt de nonce voor in de geheime berekening met de private ondertekeningssleutel. Hetzelfde woord ‘willekeur’ beschrijft twee verschillende rollen.

[Specificatie van EMSA-PSS en MGF1 (RFC 8017)](https://www.rfc-editor.org/rfc/rfc8017)
