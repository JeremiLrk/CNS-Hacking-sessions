# Phone Book

Alice vertrouwt op een directory die namen aan publieke ElGamal-sleutels koppelt. Twee beslissingen spelen hier mee: wie mag een sleutel aan een naam koppelen, en welke geregistreerde ontvangers mogen het geheim krijgen?

## Wat toont je oorspronkelijke script?

Je registreert een publieke sleutel onder **james** en vraagt Alice een bericht voor **james** te versleutelen. Dit past bij de vermelde regel dat Alice naar iedere geregistreerde ontvanger wil sturen. De acties in het script tonen op zichzelf niet aan dat je een ciphertext voor **Bob** hebt gelezen of dat de directory wijzigingen aan Bobs registratie toestaat. Als Alice aan iedere naam dezelfde inhoud stuurt, kan een bericht voor James wel dezelfde plaintext bevatten.

De variabele `alice` bevat de HTTP-respons. Je print de respons, maar leest er geen waarden uit: `c1` en `c2` staan letterlijk in het script. Ook `p` en `g` zijn vaste waarden. Daardoor is er geen automatische controle dat de berekening bij de getoonde respons hoort.

## Notatie en berichtformaat

De directory bevat `name` en `y`; de publieke parameters heten `p` en `g`. Het script gebruikt `chosen_private` voor de eigen geheime exponent. De [algemene README](../README.md) zet de cursusformules naast deze namen.

De opgave codeert de bytes van het geheim als een big-endian geheel getal. Je laatste regels berekenen de minimale bytelengte en zetten het getal in dezelfde volgorde terug om. Eventuele nulbytes aan het begin zijn alleen exact te herstellen als de oorspronkelijke lengte bekend is.

`original_commented.py` bevat je oorspronkelijke script. De opgave beschrijft een HTTP-service en levert geen afzonderlijk challenge.json-bestand mee.
