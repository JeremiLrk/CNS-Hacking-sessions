# ElGamal 2 — Fresh Every Time

Bij *Asymmetric Nonsense* waren de eerste ciphertextcomponenten gelijk. Hier zijn ze verschillend. De vraag verschuift daarmee van ‘zijn de nonces identiek?’ naar ‘zijn ze onafhankelijk gekozen?’.

## Wat laten de publieke gegevens zien?

Volgens slide 61 is C₁ = α^k mod q. In deze JSON heet α `g`, heet q `p` en is g = 2. De eerste componenten voldoen aan de volgende relatie, gecontroleerd op de meegeleverde getallen:

`cipher_flag[0] = (2 × cipher_known[0]) mod p`

Hoe past dit bij de cursusformule? Vermenigvuldig α^k met α. Volgens de machtsregel geeft dat α^(k+1). Na reductie modulo q ontstaat precies het waargenomen verband. De waarden passen dus bij opeenvolgende exponenten modulo de orde van de generator. Uit twee ciphertexts alleen volgt geen uitspraak over alle andere berichten van de dienst.

## Je script lezen

| In het script | In de JSON of cursus | Betekenis |
| --- | --- | --- |
| `q`, `alpha`, `Ya` | `p`, `g`, `y` | Modulus, generator en publieke sleutelwaarde |
| `cipher_known[0]`, `cipher_flag[0]` | C₁ per bericht | De twee publieke waarden die je bovenaan vergelijkt |
| `M1` | M van het bekende bericht | UTF-8-tekst gelezen als een big-endian geheel getal |
| `K1`, `K2` | K per bericht | De twee berichtgebonden factoren |
| `Message`, `answer` | M en de bijbehorende bytes | Twee representaties van hetzelfde resultaat |

Je oorspronkelijke commentaar formuleert de relatie tussen de eerste componenten. Het script veronderstelt die relatie zonder een controle uit te voeren. De concrete invoer voldoet eraan. Daarom is ‘elke nonce is uniek’ hier een onvoldoende argument voor vertrouwelijkheid.

## Bestanden

- `ElGamal_challenge.json` bevat beide ciphertextparen en de bekende tekst.
- `original_commented.py` bevat je oorspronkelijke berekening met opmerkingen bij de notatie en byteconversie.

[Algemene ElGamal-formules in cursus- en JSON-notatie](../README.md)
