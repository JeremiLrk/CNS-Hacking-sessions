# RSA 3 — Free keys

De opgave toont twee versleutelingen van dezelfde boodschap met dezelfde modulus. De publieke exponent verschilt. Verschillende ciphertexts zijn hier geen bewijs van vertrouwelijkheid. Dit is het common-modulusprobleem bij textbook RSA.

| Variabele | Betekenis |
| --- | --- |
| `n` | De gedeelde modulus |
| `e1`, `c1` | Publieke exponent 65537 en de bijbehorende ciphertext |
| `e2`, `c2` | Publieke exponent 17 en de bijbehorende ciphertext |
| `a`, `b` | Bezout-coefficienten voor de twee exponenten |
| `M` | Gehele-getalrepresentatie van de boodschap |

## De algebra achter de controle

De uitgebreide Euclidische methode levert coefficienten voor de identiteit van Bezout. Met de exponenten uit deze oefening geldt:

1. `65537 = 3855 * 17 + 2`
2. `17 = 8 * 2 + 1`
3. `1 = 17 - 8 * 2`
4. `1 = 17 - 8 * (65537 - 3855 * 17)`
5. `1 = -8 * 65537 + 30841 * 17`

De controle in je Python-script test dus precies de relatie die je verwacht. In een van je oorspronkelijke commentaarregels wisselen de labels c1 en c2 om. De JSON en de toewijzingen bovenaan het script zijn consistent: index 1 hoort bij 65537 en index 2 bij 17.

## Representatie van de boodschap

De hint `bytes_to_long(FLAG)` beschrijft een big-endian omzetting van bytes naar een geheel getal. Je laatste regels bepalen hoeveel bytes het getal inneemt en gebruiken dezelfde bytevolgorde voor de terugweg. Eventuele nulbytes aan het begin kun je alleen exact reconstrueren als ook de oorspronkelijke lengte bekend is.

## Bestanden

- `original_commented.py` bevat je oplossing met extra commentaar.
- `challenge.json` is een kopie van het lokale `challenge2.json`. Alle vijf de parameters komen overeen met je Python-bestand.
