# ElGamal — cursusnotatie naast de JSON

**Studeerroute** · Cursus ↔ JSON → bewijs → cursusvoorbeeld en huiswerk → bytecodering → noncekeuze en discrete logaritmen. De bron is Part 4, pdf-pagina’s 49–57.

In *Security, Part 4: Asymmetric Encryption* staan de sleutelgeneratie op slide 60, encryptie en decryptie op slide 61 en het bewijs op slide 62 (pdf-pagina's 50–52). Hieronder staat elke cursusformule naast dezelfde berekening met de namen uit de oefening.

| Cursus | Oefening | Betekenis |
| --- | --- | --- |
| q | `p` | Priemgetal waarmee je modulo rekent |
| α | `g` | Generator |
| Y_A | `y` | Publieke sleutelwaarde van de ontvanger |
| X_A | x | Geheime exponent van de ontvanger |
| k | k | Verse geheime exponent die de afzender voor één encryptie kiest |
| K | K | Eenmalige vermenigvuldigingsfactor voor het bericht |
| M | m | Bericht als geheel getal |
| (C₁, C₂) | `cipher_known` of `cipher_flag` | Eén ciphertextpaar, met C₁ op index 0 en C₂ op index 1 |

De namen x, k, K en m in de formules hieronder zijn rekenvariabelen. De JSON bevat de bekende tekst als string in `known_plaintext`.

| Stap | Originele cursusformule | Dezelfde formule met oefennotatie |
| --- | --- | --- |
| Publieke sleutel berekenen | Y_A = α^(X_A) mod q | y = g^x mod p |
| Eenmalige factor bij encryptie | K = Y_A^k mod q | K = y^k mod p |
| Eerste ciphertextcomponent | C₁ = α^k mod q | cipher[0] = g^k mod p |
| Tweede ciphertextcomponent | C₂ = K·M mod q | cipher[1] = K·m mod p |
| Ontvanger berekent K | K = C₁^(X_A) mod q | K = cipher[0]^x mod p |
| Ontvanger ontsleutelt | M = C₂·K⁻¹ mod q | m = cipher[1]·K⁻¹ mod p |

Hier staat `cipher` voor één van de twee arrays. Het teken ^ betekent machtsverheffing in deze tabel. K⁻¹ is de modulaire inverse: K·K⁻¹ ≡ 1 (mod p).

**Waarom vinden beide partijen dezelfde K?** De afzender berekent y^k ≡ (g^x)^k ≡ g^(xk). De ontvanger berekent cipher[0]^x ≡ (g^k)^x ≡ g^(kx). Omdat xk = kx zijn beide uitkomsten gelijk modulo p.

[Oefening 1 — Asymmetric Nonsense](01-Asymmetric-Nonsense/README.md)

[Oefening 2 — Fresh Every Time](02-Fresh-Every-Time/README.md)

## Van discrete logaritme naar encryptie · pdf 49–52

We rekenen met de niet-nulresten modulo de priem q (JSON: p). Een primitieve wortel α (JSON: g) is een generator: zijn machten doorlopen alle q−1 elementen. Exponenten die een veelvoud van q−1 verschillen, geven dezelfde groepswaarde. De discrete logaritme van Y met basis α is een exponent X waarvoor α^X ≡ Y mod q. De publieke waarde berekenen is snel met modulaire exponentiatie. Het omgekeerde probleem vormt de veiligheidsbasis voor geschikt gekozen groepen.

De publieke sleutel bestaat uit **(q, α, Y_A)**. Alleen X_A blijft bij de ontvanger. Bij de afzender is k tijdelijk en geheim. De cursus neemt 1 ≤ M ≤ q−1. Voor het algebraïsche voorbeeld op de slide is de getoonde range voor k inclusief q−1; bij k=q−1 zouden C₁ en K beide 1 zijn. Bij encryptie kies je een verse geheime exponent uit de geldige niet-triviale exponenten van de gekozen groep. Het bericht wordt hier als groepselement behandeld.

**Volledig bewijs.** Schrijf eerst K zoals Bob het ziet: C₁^X_A ≡ (α^k)^X_A ≡ α^(kX_A). De afzender kreeg Y_A^k ≡ (α^X_A)^k ≡ α^(X_Ak). Beide zijn dus dezelfde niet-nulrest. Omdat q priem is, heeft K een inverse. Dan geldt C₂K⁻¹ ≡ (KM)K⁻¹ ≡ M(KK⁻¹) ≡ M mod q. Het toegelaten bereik van M maakt die rest eenduidig.

## Cursusvoorbeeld · pdf 53–54

Slide 63 geeft q=19, α=10, X_A=5, M=17 en k=6. Hieronder staan de namen uit de JSON. In de huiswerkvraag op pdf-pagina 54 staat bij X_A het label ‘public key’; uit de sleuteldefinitie en C₁^X_A blijkt dat X_A de **private** exponent is.

```python
# Cursus q, α, X_A en M heten hier p, g, x en m.
p, g, x, m, k = 19, 10, 5, 17, 6
y = pow(g, x, p)
c1 = pow(g, k, p)
shared_sender = pow(y, k, p)
c2 = (shared_sender * m) % p
shared_receiver = pow(c1, x, p)
recovered = c2 * pow(shared_receiver, -1, p) % p
print("y, K, (c1,c2), m =", y, shared_sender, (c1, c2), recovered)
assert shared_sender == shared_receiver and recovered == 17

# Afzonderlijke huiswerkvraag: hetzelfde eigen x, gegeven paar (11, 5).
c1, c2 = 11, 5
shared_receiver = pow(c1, x, p)
print("Huiswerk:", c2 * pow(shared_receiver, -1, p) % p)
```

Een modulaire inverse is een geheel getal. In het voorbeeld 5⁻¹ mod 19 = 4, want 5·4 = 20 ≡ 1. Python schrijft dit als `pow(5, -1, 19)`. Gewone deling met `/` produceert een kommagetal en beantwoordt een andere vraag.

## Bytes, getallen en lengte

Een bericht dat meerdere bytes telt wordt in big-endian gelezen: voor bytes b₀, …, bₜ is de gehele waarde de som van bᵢ·256^(t−i). De lengte behoort bij de codering. Als de eerste byte nul is, heb je de oorspronkelijke lengte nodig om precies dezelfde bytes terug te krijgen.

```python
bericht = b"\x00UA"
m = int.from_bytes(bericht, "big")
assert m == 0x5541
assert m.to_bytes(len(bericht), "big") == bericht
assert (m.bit_length() + 7) // 8 == 2  # minimale lengte; origineel had 3 bytes
```

## Waarom telkens verse willekeur? · pdf 55–57

Bij hergebruik van k met dezelfde ontvanger worden C₁ en K herhaald. Dan worden verschillende M-waarden telkens met dezelfde factor gemaskeerd en is hun onderlinge algebraïsche verhouding zichtbaar. Zelfs verschillende k-waarden kunnen samenhang vertonen als de generator van de nonces voorspelbaar is. Voor elke encryptie moet de tijdelijke exponent geheim en onafhankelijk gekozen zijn. De langetermijnsleutel X_A heeft een andere levensduur.

De slides beschrijven twee discrete-logaritmeproblemen: Y_A hoort bij X_A en C₁ bij k. Hun moeilijkheid hangt af van de groep, inclusief de factorisatie van haar orde. De vuistregel op slide 68 noemt een priem met minstens 300 decimale cijfers en een grote priemfactor van q−1; lees dit als de historische cursuswaarde. Een tweede eigenschap van textbook ElGamal is dat vermenigvuldigen van C₂ ook een factor in het ontsleutelde bericht aanbrengt. Vertrouwelijkheid alleen geeft dus geen berichtintegriteit.

**Zelfcontrole.** Wie kent K vóór verzending? De afzender kan het uit y en k berekenen. Hoe krijgt de ontvanger het? Uit c1 en x. Waarom mag de ontvanger x lang bewaren terwijl k vers moet zijn? x hoort bij de identiteit van de ontvanger; k randomiseert één afzonderlijke encryptie.

## Het slidevoorbeeld met alle tussenwaarden

| Stap | Invulling modulo 19 | Uitkomst |
| --- | --- | ---: |
| Publieke sleutel | y = 10⁵. Eerst 10² ≡ 5, dan 10⁴ ≡ 6, dus 10⁵ ≡ 6·10 | 3 |
| Eerste component | c1 = 10⁶ ≡ 10⁵·10 ≡ 3·10 | 11 |
| Eenmalige factor | K = 3⁶ = 729 ≡ 729−38·19 | 7 |
| Tweede component | c2 = 7·17 = 119 ≡ 119−6·19 | 5 |
| Zelfde factor bij de ontvanger | 11² ≡ 7, 11⁴ ≡ 11, dus 11⁵ ≡ 11·11 | 7 |
| Modulaire inverse | 7·11 = 77 = 4·19+1 | 11 |
| Bericht | 5·11 = 55 ≡ 55−2·19 | 17 |

**Verband met andere hoofdstukken.** Bij DH maken twee deelnemers uit elkaars publieke factoren hetzelfde geheim. ElGamal gebruikt dat idee per bericht en vermenigvuldigt het bericht met de afgeleide factor. DSA gebruikt eveneens exponenten in een eindige groep, maar bewijst authenticiteit met een handtekening. Let vooral op **q**: hier is q in de cursus de groepsmodulus; in het DSA-hoofdstuk is q de orde van een subgroep modulo p. Bij ElGamal is slide **67** (pdf-pagina 55) de slide over hergebruik.

**Kopieerbare functies voor het cursusmodel.** Geef de functie zelf een oefenbericht en een eigen geheime ontvangersleutel. De uitvoer gebruikt dezelfde indexering als de JSON-arrays.

```python
from secrets import randbelow

def versleutel_getal(p, g, y, bericht):
    """Textbook ElGamal in de volledige groep bij een gegeven priem en generator."""
    if p < 5 or not 1 <= bericht < p:
        raise ValueError("Bericht of modulus valt buiten het oefenbereik.")
    k = 1 + randbelow(p - 2)
    return pow(g, k, p), bericht * pow(y, k, p) % p

def ontsleutel_eigen_bericht(p, x, paar):
    c1, c2 = paar
    factor = pow(c1, x, p)
    return c2 * pow(factor, -1, p) % p

p, g, x = 19, 10, 5
y = pow(g, x, p)
for bericht in range(1, p):
    paar = versleutel_getal(p, g, y, bericht)
    assert ontsleutel_eigen_bericht(p, x, paar) == bericht
```
