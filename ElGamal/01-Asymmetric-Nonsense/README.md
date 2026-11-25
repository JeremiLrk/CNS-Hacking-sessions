# Oefening 1 — Asymmetric Nonsense

**Waarom moet k vers zijn?** Bij dezelfde publieke sleutel en dezelfde k ontstaan dezelfde eerste ciphertextcomponent en dezelfde vermenigvuldigingsfactor K. Daardoor ontstaat een algebraïsch verband tussen de twee tweede componenten. Dat is het probleem dat slide 66 over sleutelhergebruik bespreekt (pdf-pagina 55).

## Je code lezen

- `cipher_known[0]` en `cipher_flag[0]` zijn de eerste componenten van twee verschillende berichten. De vergelijking bovenaan je script controleert of die waarden gelijk zijn. De tweede print wordt altijd uitgevoerd, ongeacht de uitkomst van de vergelijking.
- `M1` is de bekende tekst als getal. Je code zet de tekst eerst om naar UTF-8-bytes en leest die bytes dan in big-endianvolgorde. De eerste byte is dus de meest significante.
- `Message` is een geheel getal en `answer` is de byteweergave. `bit_length()` geeft het aantal benodigde bits. De berekening `(bits + 7) // 8` rondt naar boven af tot een geheel aantal bytes.

Zie de [algemene README](../README.md) voor de formules in cursus- en JSON-notatie. De map bevat je oorspronkelijke Python-oplossing met extra commentaar en de bijbehorende challengegegevens.