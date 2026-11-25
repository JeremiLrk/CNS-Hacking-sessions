n = 122669927411406727028788626411679443825688776964989352296475427773238194525648382371552761821855169263312605721407880877201759835810127064710476447051953689721330492645804679815792399036086826175563763597773587160877571184108516088814876030806480091013658263418131474441195440823023139298901952911255011539271
e = 93570199767358024291201010969804528185370907625457279260926085845016814204197871528076645182086290233543797522608794365343079838239595866737414231665735577696295318454369964329852287041541654159409978529168799334787687422979841162861038975098731934708646455041406657882224493351947655156228657436753078459681
c = 63190008952747037070429205997813552737461029227687467209185847535467974587640762563475064539913916079017028949672905146132754696181065925175268042787315140973476806461302280659042070005545642451857859868819928731084766790121697292805285631884013218055705384394531201778850069464339792949444208423036622974887


from math import isqrt


def wiener_attack(n, e):
    """
    Probeert de geheime RSA-sleutel d te vinden.

    Werkt wanneer d uitzonderlijk klein is.
    Je hebt alleen de publieke sleutel (n, e) nodig.

    Geeft d terug als de aanval lukt.
    Geeft None terug als er niets gevonden wordt.
    """

    # STAP 1: Begin met de publieke getallen e en n.
    # We gaan deze herhaaldelijk delen door elkaar.
    a, b = e, n

    # STAP 2: Startwaarden voor het kettingbreukalgoritme.
    # Dit algoritme maakt slimme kandidaten voor d.
    # Deze vier waarden zijn vaste beginwaarden.
    k_prev2, k_prev1 = 0, 1
    d_prev2, d_prev1 = 1, 0

    while b != 0:

        # STAP 3: Deel a door b.
        # q = hoeveel keer b in a past
        # r = wat overblijft
        q, r = divmod(a, b)

        # STAP 4: Bereken een nieuwe kandidaat.
        # k = een hulpgetal
        # d = mogelijke geheime RSA-sleutel
        #
        # Dit zijn standaardformules voor kettingbreuken.
        # Je hoeft ze niet zelf uit te vinden.
        k = q * k_prev1 + k_prev2
        d = q * d_prev1 + d_prev2

        # STAP 5: We weten uit RSA:
        #
        # e*d - 1 = k * phi(n)
        #
        # Dus:
        # phi(n) = (e*d - 1) / k
        #
        # We testen of dit een geheel getal oplevert.
        if k != 0 and (e * d - 1) % k == 0:

            phi = (e * d - 1) // k

            # STAP 6: Controleren of phi echt klopt.
            #
            # RSA gebruikt:
            # n = p*q
            # phi = (p-1)*(q-1)
            #
            # Daaruit volgt:
            # p + q = n - phi + 1
            #
            # We noemen die som s.
            s = n - phi + 1

            # STAP 7: Als p en q bestaan, dan geldt:
            #
            # (p-q)^2 = (p+q)^2 - 4*p*q
            #
            # Omdat p+q = s en p*q = n:
            #
            # (p-q)^2 = s^2 - 4*n
            #
            # We berekenen dus het verschil.
            discriminant = s * s - 4 * n

            if discriminant >= 0:

                # isqrt berekent de gehele vierkantswortel.
                # Bijvoorbeeld: isqrt(81) = 9.
                root = isqrt(discriminant)

                # Als root^2 gelijk is aan discriminant,
                # hebben we een exacte vierkantswortel.
                if root * root == discriminant:

                    # Bereken de twee mogelijke priemfactoren.
                    if (s + root) % 2 == 0:
                        p = (s + root) // 2
                        q_factor = (s - root) // 2

                        # Laatste controle:
                        # Vermenigvuldigen p en q echt tot n?
                        if p > 1 and q_factor > 1 and p * q_factor == n:

                            # Ja! We hebben een geldige d.
                            return d

        # STAP 8: Bewaar de vorige kandidaten.
        # Die zijn nodig om de volgende te berekenen.
        k_prev2, k_prev1 = k_prev1, k
        d_prev2, d_prev1 = d_prev1, d

        # STAP 9: Ga verder met de volgende deling.
        a, b = b, r

    # Geen geschikte private sleutel gevonden.
    return None

d = wiener_attack(n,e)
M = pow(c, d, n)
length = (M.bit_length() + 7) // 8
answer = M.to_bytes(length, byteorder="big")
print(answer)