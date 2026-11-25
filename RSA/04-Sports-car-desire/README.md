# RSA 4 — Sports car desire

De ingenieur wilde de decryptie versnellen door een kleine private exponent te kiezen. In de cursus is `d` de private exponent en `e` de publieke exponent. Je script onderzoekt met de methode van Wiener of de gekozen `d` uitzonderlijk klein is. De methode gebruikt kettingbreuken. De grootte van `n` alleen vertelt je dus niet of deze sleutelkeuze veilig is.

## Notatie in jouw code

| Variabele | Betekenis |
| --- | --- |
| `n`, `e`, `c` | Modulus, publieke exponent en ciphertext uit de opgave |
| `q` in `divmod(a, b)` | Quotiënt van een deling |
| `q_factor` | De tweede factor van de modulus, in de cursus meestal geschreven als q |
| `phi`, `s` | Kandidaat voor φ(n) en bijbehorende som van de twee factoren |
| `M`, `answer` | Het bericht als geheel getal en vervolgens als bytes |

## Waarom klopt de algebra van de controle?

Voor twee verschillende priemfactoren geldt φ(n) = (p − 1)(q − 1). Werk de haakjes uit: φ(n) = pq − p − q + 1. Vul pq = n in en verplaats de termen. Dan volgt p + q = n + 1 − φ(n). Dat is de betekenis van `s` in de code.

De discriminantcontrole berust op (p + q)² − 4pq = p² + 2pq + q² − 4pq = (p − q)². Een echte factorisatie geeft dus een exact kwadraat. Python geeft met `isqrt` de naar beneden afgeronde wortel. De gelijkheid `root * root == discriminant` controleert of de wortel exact is.

## Beoordeling van jouw oplossing

De algebra achter beide controles klopt. De functie kan ook `None` teruggeven. De code onderaan gebruikt de teruggegeven waarde onmiddellijk als exponent en zou in dat geval een `TypeError` geven. De opdracht gebruikt big-endian bytevolgorde. Je laatste regels volgen die conventie en tonen de Python-weergave van de bytes.

## Bestanden

- `original_commented.py` bevat je eigen oplossing en de oorspronkelijke stapsgewijze opmerkingen.
- `challenge.json` bevat de drie waarden uit de opgave. Ze komen alle drie overeen met de constanten bovenaan het script.