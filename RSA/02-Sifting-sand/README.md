# RSA 2 — Sifting sand

## Wat doet jouw oplossing?

De opgave vraagt meerdere factorisatiemethoden te testen. Je Python-script roept één keer SymPy’s `factorint` aan. Daarna berekent het de private exponent. Je gebruikt de meegeleverde `decryptor.py` voor het verwerken van de ciphertext. Het script bevat geen tijdmetingen of afzonderlijke proeven met verschillende zeven. Uit de code kun je dus geen snelste zeef afleiden.

## Van code naar cursusnotatie

| Variabele | Betekenis in deze oefening |
| --- | --- |
| `n` | De publieke modulus, 34664911185892166593 |
| `e` | De publieke exponent, 65537 |
| `factors` | Dictionary met priemfactoren als sleutels en multipliciteiten als waarden |
| `p`, `q` | De eerste twee sleutels van die dictionary |
| `euler` | φ(n), het aantal gehele getallen van 1 tot en met n die onderling ondeelbaar zijn met n |
| `d` | De modulaire inverse van e modulo φ(n) |

## Controle van de redenering

Bij twee **verschillende** priemfactoren die elk één keer voorkomen, geldt n = pq. Van de n getallen zijn er q deelbaar door p en p deelbaar door q. Het getal pq werd dubbel geteld. Dat geeft φ(n) = n − q − p + 1 = pq − p − q + 1 = (p − 1)(q − 1). Dit verklaart de regel die `euler` berekent.

De inverse bestaat wanneer gcd(e, φ(n)) = 1. De cursusrelatie voor deze parameters is 65537 · d ≡ 1 (mod φ(n)). Dat is de betekenis van `pow(e, -1, euler)`.

Je algebra klopt onder die voorwaarden. `list(factors)` gebruikt alleen de sleutels en controleert de multipliciteiten niet. De variabelenaam `list` overschrijft bovendien de ingebouwde naam. Bij een tweede uitvoering in dezelfde interactieve Python-sessie kan daardoor een fout ontstaan.

## Bestanden

- `original_commented.py` is jouw oplossing met verklarende opmerkingen.
- `challenge.json` bevat de publieke parameters en 14 ciphertextblokken. Bij 8 bytes per blok is de totale bloklengte 14 × 8 = 112 bytes, gelijk aan `original_length`.
- `decryptor.py` is de meegeleverde helper. Hij gebruikt een ingevoerde private exponent en zet de blokken om naar bytes in big-endianvolgorde. Hij bewaart de eerste 112 bytes en leest ze als UTF-8.