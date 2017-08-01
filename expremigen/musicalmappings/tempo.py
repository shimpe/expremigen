class Tempo:
    """
    convert some italian tempo indications to bpm
    (in reality the names indicate a range of tempi;
     I just selected one at random)
    """
    larghissimo = 20
    grave = 40
    lento = 44
    largho = 50
    larghetto = 60
    adagissimo = 63
    adagio = 69
    adagietto = 72
    andante = 80
    andantino = 86
    moderato = 112
    allegretto = 120
    allegro = 132
    vivace = 144
    allegro_vivace = 152
    vivacissimo = 160
    allegro_assai = 176
    presto = 184
    prestissimo = 208

    @classmethod
    def from_string(cls, thestring):
        """

        :param thestring: symbolic tempo indication
        :return: number corresponding to symbolic tempo
        """
        lut = {
            'larghissimo': 20,
            'grave': 40,
            'lento': 44,
            'largho': 50,
            'larghetto': 60,
            'adagissimo': 63,
            'adagio': 69,
            'adagietto': 72,
            'andante': 80,
            'andantino': 86,
            'moderato': 112,
            'allegretto': 120,
            'allegro': 132,
            'vivace': 144,
            'allegro vivace': 152,
            'vivacissimo': 160,
            'allegro assai': 176,
            'presto': 184,
            'prestissimo': 208,
        }
        if thestring in lut:
            return lut[thestring]
        else:
            return 80
