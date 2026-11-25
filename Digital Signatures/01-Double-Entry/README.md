# Double Entry — twee ondertekende overschrijvingen

De twee records bevatten verschillende berichten: ‘Transfer 10 EUR to Alice’ en ‘Transfer 25 EUR to Bob’. Beide handtekeningen doorstaan afzonderlijk de publieke DSA-verificatie met y. Hun r-waarden zijn gelijk. Dat is opvallend omdat DSA voor iedere ondertekening een verse geheime k gebruikt. Een gelijke r is een signaal van mogelijk noncehergebruik. Alleen de gelijkheid bewijst niet dat de nonces identiek waren.

## Je script lezen

| Variabelen | Betekenis |
| --- | --- |
| M1, M2 | De twee exacte berichtteksten. Spaties en hoofdletters tellen mee bij het hashen. |
| H1, H2 | SHA-256-digests, als big-endian getallen gelezen. |
| hash1, hash2 | De digests modulo q. In je code betekent pow(H1, 1, q) precies H1 % q. |
| r, s1, s2 | De gemeenschappelijke eerste component en de twee afzonderlijke tweede componenten. |
| encrypted_flag | Hextekst met de versleutelde flag. Dit veld hoort bij de afzonderlijke versleutelingsstap van de opgave. |

De variabele `hash` bovenaan is door de afsluitende komma een tuple met één string. De hashberekeningen gebruiken rechtstreeks hashlib en hangen dus niet af van deze variabele. De code neemt r uit het eerste record. Bij controle van het bestand bleek de tweede r inderdaad gelijk.

De [algemene README](../README.md) geeft de ondertekenings- en verificatieformules naast de JSON-notatie. De publieke verificatie controleert of elke handtekening past bij het bijbehorende bericht en de publieke sleutel. Ze controleert niet hoe de ondertekenaar k heeft gekozen.

## Bestanden

- `original_commented.py` bevat je eigen oplossing met toelichting bij de Python-notatie.
- `dsa1_challenge.json` is de oorspronkelijke invoer.
