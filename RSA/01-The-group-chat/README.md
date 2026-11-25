# RSA 1 — The group chat

**10 punten.** De afzender versleutelt dezelfde groepsboodschap voor drie ontvangers, elk met hun eigen publieke RSA-sleutel. De oefening vraagt of alleen de ontvangers hun bericht kunnen lezen.

## Methode en wiskunde

Bij textbook RSA wordt het bericht voorgesteld als hetzelfde gehele getal `m` voor elke ontvanger. In deze opgave is de publieke exponent bij alle drie de sleutels gelijk aan 3. De drie ciphertexts voldoen dus aan:

- `c1 ≡ m³ (mod n1)`
- `c2 ≡ m³ (mod n2)`
- `c3 ≡ m³ (mod n3)`

`n1`, `n2` en `n3` zijn drie verschillende moduli. De letters `p` en `q` uit de cursus duiden de twee priemfactoren van één modulus aan.

Je oplossing gebruikt de Chinese reststelling en een gehele derdemachtswortel. De reststelling is hier relevant omdat de drie ciphertexts resten van dezelfde macht zijn. Het gebruik van textbook RSA met meerdere sleutels biedt in deze opzet onvoldoende vertrouwelijkheid. RSA-OAEP gebruikt verse willekeur bij het coderen van elk bericht.

## Controle van je redenering

In je eerdere chat *Theorie asymmetrische encryptie* rapporteerde je drie resultaten: alle drie de paarsgewijze GGD's waren 1, alle drie de congruentiecontroles gaven `True`, en SymPy meldde `exact=True`. Die resultaten zijn consistent met de methode die je voor deze oefening koos. De eerdere bespreking wees ook op de haakjes rond de volledige som. In de huidige lokale bron staan die haakjes correct.

| Diagnose | Betekenis |
| --- | --- |
| Drie GGD's gelijk aan 1 | De drie moduli zijn paarsgewijs onderling ondeelbaar. |
| Drie congruentiecontroles gelijk aan `True` | Het berekende gehele getal heeft de verwachte rest onder elke modulus. |
| `exact=True` | De wortel die SymPy teruggaf is exact, zonder afronding. |

De scriptlog toont deze voorwaarden als diagnostiek. Een ongunstige uitkomst van een congruentiecontrole of `exact=False` stopt het script niet. Het blijft dan bytes afdrukken. De conclusie hierboven steunt op de waarden die je in de eerdere chat rapporteerde.

## Bestanden

| Bestand | Inhoud |
| --- | --- |
| `original_commented.py` | Je oorspronkelijke oplossing met commentaar bij de invoer, notatie en diagnostiek |
| `public_keys_active.txt`, `ciphertexts_active.txt` | Invoer die overeenkomt met de actieve toewijzingen in je script |
| `public_keys_commented.txt`, `ciphertexts_commented.txt` | Invoer die overeenkomt met het uitgecommentarieerde blok bovenaan |

Zie de [algemene RSA-README](../README.md) voor sleutelnotatie en een uitgeschreven voorbeeld van de modulaire inverse.
