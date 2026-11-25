# RSA

**Studeerroute** · Notatie en oefenmappen → asymmetrische basis → RSA-bewijs en blokgrootte → modulaire exponentiatie en CRT → sleutelgeneratie → veiligheid en OAEP. De paginanummers verwijzen naar de PDF van Part 4.

Start hier voor de RSA-oefeningen van Computer and Network Security (UAntwerpen). De notatie en het rekenvoorbeeld volgen Part 4, *Asymmetric Encryption*, PDF-pagina's 16–22. PDF-pagina's 24–28 behandelen efficiënte modulaire exponentiatie.

## Symbolen in de cursus en in Python

| Cursus | Mogelijke Python-naam | Betekenis |
| --- | --- | --- |
| `p`, `q` | `p`, `q`, `prime1`, `prime2` | De twee priemfactoren van de modulus |
| `n = p*q` | `n`, `modulus` | RSA-modulus |
| `φ(n) = (p−1)(q−1)` | `phi`, `totient` | Totient van de modulus bij twee verschillende priemfactoren |
| `e` | `e`, `public_exponent` | Publieke exponent |
| `d` | `d`, `private_exponent` | Private exponent |
| `M` | `m`, `message_int` | Plaintext als geheel getal, met `0 <= m < n` |
| `C` | `c`, `ciphertext_int` | Ciphertext als geheel getal |

De namen `p` en `q` kunnen tussen cursus en code omgewisseld zijn. In het cursusvoorbeeld is `p = 17` en `q = 11`. Code die de priemfactoren oplopend benoemt, kan `p = 11` en `q = 17` gebruiken. Beide volgordes geven dezelfde `n` en `phi`.

## Van parameters naar een RSA-sleutelpaar

Met de voorbeeldparameters van de cursus (`p = 17`, `q = 11`, `e = 7`):

1. `n = 17 * 11 = 187`.
2. `phi = (17 - 1) * (11 - 1) = 16 * 10 = 160`.
3. `160 = 22 * 7 + 6` en `7 = 1 * 6 + 1`. Dus `gcd(7, 160) = 1`.
4. Terugsubstitutie geeft `1 = 7 - 6 = 7 - (160 - 22 * 7) = 23 * 7 - 160`.
5. Dus `7 * 23 ≡ 1 (mod 160)` en `d = 23`. In Python berekent `pow(e, -1, phi)` die inverse.
6. Een roundtrip met `m = 42` geeft `pow(42, 7, 187) = 15` en `pow(15, 23, 187) = 42`.

`pow(a, b, n)` berekent `a**b mod n` met modulaire reductie tijdens de berekening. Bij RSA-encryptie in productie gebruik je een cryptografische bibliotheek met RSA-OAEP of een geschikt hybride encryptieschema. Dat schema gebruikt RSA voor een sleutel en geauthenticeerde symmetrische encryptie voor het bericht.

## Oefeningen

| Oefening | Bestand |
| --- | --- |
| 1 — The group chat | [Oefenfiche](01-The-group-chat/README.md) |
| 2 — Sifting sand | [Oefenfiche](02-Sifting-sand/README.md) |
| 3 - Free keys | [Oefenfiche](03-Free-keys/README.md) |
| 4 — Sports car desire | [Oefenfiche](04-Sports-car-desire/README.md) |

## Lokale bronbestanden

Het bestaande overzicht staat in `Hacking session 1/README.md`. De Python-bron voor oefening 1 heet `(betterer) Group chat.py`. Het lokale `challenge.json` bevat ElGamal-velden (`p`, `g`, `y`, `cipher_known`, `cipher_flag`). Gebruik een oefenbestand pas nadat je hebt vastgesteld voor welke oefening het dient.

## Asymmetrische cryptografie begrijpen · pdf 4–12

Elke deelnemer genereert een samenhangend paar sleutels. Iedereen mag de publieke sleutel kennen. Generatie, encryptie en decryptie moeten efficiënt zijn voor de eigenaar. Uit alleen de publieke sleutel de private afleiden, of uit publieke sleutel en ciphertext het bericht achterhalen, moet praktisch onhaalbaar zijn. Dit zijn verschillende eisen: een moeilijk sleutelprobleem op zich maakt een willekeurige berichtcodering nog niet veilig.

| Doel | Wie gebruikt welke sleutel? | Wat ontvangt de andere partij? |
| --- | --- | --- |
| Vertrouwelijkheid | Alice versleutelt voor Bob met PU_B | Bob herstelt M met PR_B: D(PR_B, E(PU_B, M)) = M. |
| Authenticiteit en integriteit | Alice ondertekent met PR_A | Bob verifieert met PU_A op precies dezelfde berichtbytes. |
| Beide samen | Alice ondertekent M en versleutelt bericht en handtekening voor Bob | Bob ontsleutelt eerst en verifieert daarna. |
| Sleuteluitwisseling of -transport | Partijen spreken een geheim af of sturen een vers gekozen sessiesleutel naar de ontvanger | De sessiesleutel beschermt het dataverkeer met symmetrische cryptografie. |

De slides gebruiken private en publieke RSA-bewerkingen om de richting te illustreren. Bij echte handtekeningen horen een handtekeningschema, berichtcodering en verificatieregels. DH is een sleuteluitwisseling. RSA, de ElGamal-familie en elliptische-krommefamilies hebben verschillende constructies voor encryptie, handtekeningen en sleutelbeheer. De publieke sleutel moet bij de juiste identiteit horen. Asymmetrisch betekent op zichzelf geen hogere veiligheid. Voor grote berichten combineert men vaak asymmetrische sleutelverdeling met snelle symmetrische encryptie.

## Waarom RSA terugkeert naar M · pdf 15–22

RSA werd in 1977 gepubliceerd door Rivest, Shamir en Adleman. Clifford Cocks had in 1973 een verwante, destijds geheime constructie. De rekenstap steunt op **ed = 1 + tφ(n)**. Voor een M die relatief priem is met n zegt Euler dat M^φ(n) ≡ 1 mod n. Dus M^(ed) = M·(M^φ(n))^t ≡ M. Ook voor berichten die een factor met n delen geldt de roundtrip: redeneer apart modulo p en q. Een nulrest blijft nul; voor een niet-nulrest geldt Fermat. Gelijkheid modulo beide verschillende priemen geeft gelijkheid modulo n.

Een volledig blok van b bits moet voor *alle* waarden passen: 2^b − 1 < n. Voor n = 2 000 000 is b = 20. Een afzonderlijk getal van 21 bits kan nog passen, maar niet elk getal van 21 bits.

```python
from math import gcd

p, q, e = 17, 11, 7
n = p * q
phi = (p - 1) * (q - 1)
assert gcd(e, phi) == 1
d = pow(e, -1, phi)
assert (n, phi, d) == (187, 160, 23)
assert all(pow(pow(m, e, n), d, n) == m for m in range(n))
print(pow(88, e, n), pow(11, d, n))  # twee afzonderlijke slidevragen
print((2_000_000).bit_length() - 1)    # gegarandeerde bloklengte
```

## Efficiënt rekenen · pdf 23–30

**Square-and-multiply.** Lees de exponent van links naar rechts in binair. Na een prefix met waarde v bewaart de accumulator a^v mod n. Een nieuw bit b maakt de prefix 2v+b. Daarom kwadrateer je altijd en vermenigvuldig je nog met a als b=1. Modulo nemen na elke stap houdt de getallen klein. Voor e = 65537 = 2^16 + 1 zijn slechts twee bits 1. Ook 3 en 17 hebben die eigenschap. Een kleine exponent gecombineerd met deterministische berichtcodering kan informatie prijsgeven.

```python
def modmacht(a, exponent, modulus):
    if exponent < 0 or modulus <= 1:
        raise ValueError("Verwacht exponent >= 0 en modulus > 1.")
    waarde = 1
    for bit in bin(exponent)[2:]:
        waarde = waarde * waarde % modulus
        if bit == "1":
            waarde = waarde * a % modulus
    return waarde

for a, b, n in [(7, 21, 127), (7, 560, 561)]:
    print(modmacht(a, b, n))
    assert modmacht(a, b, n) == pow(a, b, n)
```

**CRT met de eigen private sleutel.** Voor een grote d voer je de private bewerking afzonderlijk uit modulo p en q. De projectie X₁ is 1 modulo p en 0 modulo q; voor X₂ is dat omgekeerd. Daardoor heeft de som precies de twee bedoelde resten. Men kan d mod (p−1), d mod (q−1) en de gewichten vooraf berekenen. Dit is de versnelling op slide 37.

```python
p, q, d, c = 17, 11, 23, 11
vp = pow(c, d % (p - 1), p)
vq = pow(c, d % (q - 1), q)
xp = q * pow(q, -1, p)
xq = p * pow(p, -1, q)
m = (vp * xp + vq * xq) % (p * q)
assert m == pow(c, d, p * q)
```

## Sleutelgeneratie · pdf 31–35

Kies twee verschillende, onafhankelijk gegenereerde grote priemen. De slides bespreken willekeurige oneven kandidaten, een probabilistische primaliteitstest en opnieuw proberen bij een composiet. Bij Miller–Rabin schrijf je n−1 = 2^s·t met t oneven. Een testronde met een geldige basis a controleert a^t mod n en opeenvolgende kwadraten op het patroon dat voor een priem verplicht is. Eén getuige volstaat om een kandidaat als composiet te verwerpen. Een passerende ronde geeft een waarschijnlijke priem. Bij onafhankelijke uniforme bases daalt de gebruikelijke foutgrens voor een oneven composiet tot 4^(−r) na r rondes.

```python
def passeert_ronde(n, a):
    """Een Miller–Rabin-ronde voor oneven n >= 5 en 2 <= a <= n-2."""
    if n < 5 or n % 2 == 0 or not 2 <= a <= n - 2:
        raise ValueError("Ongeldige kandidaat of basis.")
    t, s = n - 1, 0
    while t % 2 == 0:
        t //= 2
        s += 1
    x = pow(a, t, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False

assert passeert_ronde(17, 3)
assert not passeert_ronde(21, 2)
```

**Uitgebreide Euclides.** De gewone reststappen geven de ggd. Door voor elke rest ook de coëfficiënt van e te bewaren vind je bij rest 1 de inverse van e. Bij p=7 en q=11 is φ=60; het grootste toegelaten e onder 60 is 59, met d=59 omdat 59² ≡ 1 mod 60.

```python
def inverse(a, modulus):
    if modulus <= 1:
        raise ValueError("Modulus moet groter zijn dan 1.")
    oud, rest = modulus, a % modulus
    vorig, coef = 0, 1
    while rest:
        quotient, nieuw = divmod(oud, rest)
        oud, rest = rest, nieuw
        vorig, coef = coef, vorig - quotient * coef
    if oud != 1:
        raise ValueError("Geen inverse.")
    return vorig % modulus

assert inverse(7, 160) == 23
assert inverse(59, 60) == 59
```

## Wat beschermt welke RSA-bewerking? · pdf 36–48

| Onderwerp | Redenering uit de cursus |
| --- | --- |
| Sleutelruimte | Sleutellengtes van symmetrische en asymmetrische algoritmen zijn niet één op één vergelijkbaar. De figuur op pdf 38 vergelijkt geschatte rekeninspanning onder de aannames van het geciteerde rapport uit 2014. |
| Wiskundige veiligheid | Wie p en q kent, kent φ(n). Omgekeerd bepaalt kennis van n en φ(n) ook de som van de factoren. Een ongeschikte kleine private exponent ondermijnt de veiligheid. |
| Factorisatierecords | RSA-129 had 129 decimale cijfers en werd in 1994 gefactoriseerd. De overstap van quadratic sieve naar general number field sieve toont waarom zowel algoritmeverbeteringen als snellere hardware meetellen. De cursus noemt ook RSA-768 als historisch ijkpunt. |
| Keuze van priemen | De slides bespreken vergelijkbare bitlengtes, grote priemfactoren in p−1 en q−1 en een kleine ggd van die twee waarden. Vergelijkbare bitlengtes betekent niet dat de getallen dicht bij elkaar gekozen moeten worden. |
| Timing | De duur van private bewerkingen kan samenhangen met geheime bits. Constante-tijdimplementaties en blinding verminderen die koppeling. Willekeurige vertraging voegt ruis toe en kan bij herhaling worden uitgemiddeld. |
| Gekozen ciphertext | Textbook RSA heeft een multiplicatieve structuur: E(m₁)E(m₂) ≡ E(m₁m₂) mod n. Een dienst die ruwe private bewerkingen teruggeeft, mist bescherming tegen misbruik van die structuur. |
| OAEP | Een willekeurige seed en twee maskerstappen geven dezelfde plaintext bij herhaling verschillende coderingen. Encryptie gebruikt de publieke sleutel op de gecodeerde representatie. Ontsleuteling controleert de volledige codering. |

**Blinding met een eigen RSA-sleutel.** Kies r uit de inverteerbare resten. Voor c′ = c·r^e mod n geldt (c′)^d ≡ c^d·r mod n. Vermenigvuldigen met r⁻¹ verwijdert de willekeur. Alleen de interne berekening verandert.

```python
n, e, d, c, r = 187, 7, 23, 11, 3
geblindeerd = c * pow(r, e, n) % n
intern = pow(geblindeerd, d, n)
assert intern * pow(r, -1, n) % n == pow(c, d, n)
```

**OAEP op byteniveau.** Voor een modulus van k bytes en een hash van hLen bytes past maximaal k−2·hLen−2 bytes plaintext. DB = Hash(label) ∥ PS ∥ 01 ∥ M. PS bestaat uit nulbytes. maskedDB = DB XOR MGF(seed, lengte(DB)); maskedSeed = seed XOR MGF(maskedDB, hLen). De representatie is 00 ∥ maskedSeed ∥ maskedDB. Het label moet aan beide kanten hetzelfde zijn. Een uitvoerbare MGF1 staat in de [README over handtekeningen](../Digital%20Signatures/README.md).

```python
from hashlib import sha256

modulus_bytes = 256
max_message = modulus_bytes - 2 * sha256().digest_size - 2
assert max_message == 190
```

## De getallentabellen van slides 50 en 52

De historische vergelijking op slide 50 zet **geschatte equivalente sterkte** op één rij. L en N zijn hier bitlengtes. Deze tabel dient om de grafiek en de cursusterminologie te kunnen lezen.

| Symmetrische bits | DH/DSA L en N | RSA-modulus in bits | ECC in bits |
| ---: | ---: | ---: | ---: |
| 80 | 1024 / 160 | 1024 | 160–223 |
| 112 | 2048 / 224 | 2048 | 224–255 |
| 128 | 3072 / 256 | 3072 | 256–383 |
| 192 | 7680 / 384 | 7680 | 384–511 |
| 256 | 15360 / 512 | 15360 | 512 of meer |

De gemarkeerde zone begint bij 128 symmetrische bits. De historische factorisatietabel daarnaast meet iets anders: **welk concreet getal op welke datum daadwerkelijk is gefactoriseerd**.

| Decimale cijfers | Bits | Datum in de cursustabel |
| ---: | ---: | --- |
| 100 | 332 | april 1991 |
| 110 | 365 | april 1992 |
| 120 | 398 | juni 1993 |
| 129 | 428 | april 1994 |
| 130 | 431 | april 1996 |
| 140 | 465 | februari 1999 |
| 155 | 512 | augustus 1999 |
| 160 | 530 | april 2003 |
| 174 | 576 | december 2003 |
| 200 | 663 | mei 2005 |
| 193 | 640 | november 2005 |
| 232 | 768 | december 2009 |

**Verwacht aantal kandidaten bij priemgeneratie.** Nabij N is ongeveer één op ln(N) gehele getallen priem. Door alleen oneven kandidaten te proberen worden dat gemiddeld ln(N)/2 proeven. Nabij 2²⁰⁰ is dit ongeveer 69. De verwachting voorspelt niet hoeveel proeven één concrete sleutelgeneratie duurt.

```python
from math import log

for bits in (200, 512, 1024):
    print(bits, round(bits * log(2) / 2))
```

**Antwoorden bij de rekenvragen.** Met n=187 geeft 88⁷ mod 187 = 11 en 11²³ mod 187 = 88. Bij square-and-multiply voor exponent 21 (binair 10101) volgen de accumulatoren voor basis 7 modulo 127 de bitprefixen 1, 10, 101, 1010 en 10101. De eindwaarde is 108. Bij 7⁵⁶⁰ mod 561 is het antwoord 1. Het samengestelde getal 561 illustreert waarom één Fermat-test geen primaliteitsbewijs levert.

### OAEP uitvoeren met een eigen sleutelpaar

Het volgende blok gebruikt Python en de lokaal beschikbare OpenSSL-opdracht. Encryptie en decryptie spreken SHA-256 af voor zowel OAEP als MGF1. Twee encrypties van dezelfde bytes leveren elk een eigen willekeurige codering.

```python
from subprocess import run
from tempfile import TemporaryDirectory

with TemporaryDirectory() as mapnaam:
    def openssl(*args, invoer=None):
        return run(["openssl", *args], input=invoer, cwd=mapnaam,
                   capture_output=True, check=True).stdout

    openssl("genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048",
            "-out", "priv.pem")
    openssl("pkey", "-in", "priv.pem", "-pubout", "-out", "pub.pem")
    opties = ["-pkeyopt", "rsa_padding_mode:oaep", "-pkeyopt", "rsa_oaep_md:sha256",
              "-pkeyopt", "rsa_mgf1_md:sha256"]
    bericht = b"UAntwerpen"
    def versleutel(m):
        return openssl("pkeyutl", "-encrypt", "-pubin", "-inkey", "pub.pem",
                       *opties, invoer=m)

    c = versleutel(bericht)
    assert c != versleutel(bericht)
    assert openssl("pkeyutl", "-decrypt", "-inkey", "priv.pem",
                   *opties, invoer=c) == bericht
```

[Technische specificatie voor OAEP en RSA](https://www.rfc-editor.org/rfc/rfc8017)
