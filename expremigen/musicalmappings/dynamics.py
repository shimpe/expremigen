class Dynamics:
    """
    a convenience class containing some dynamics
    """
    ppppp = 10
    pppp = 20
    ppp = 30
    pp = 40
    p = 60
    mp = 80
    mf = 90
    f = 100
    ff = 110
    fff = 120
    ffff = 127

    @classmethod
    def from_string(cls, thestring):
        """

        :param thestring: a string containing a symbolic volume indication
        :return: the string mapped to a number
        """
        lut = {
            'ppppp': Dynamics.ppppp,
            'pppp': Dynamics.pppp,
            'ppp': Dynamics.ppp,
            'pp': Dynamics.pp,
            'p': Dynamics.p,
            'mp': Dynamics.mp,
            'mf': Dynamics.mf,
            'f': Dynamics.f,
            'ff': Dynamics.ff,
            'fff': Dynamics.fff,
            'ffff': Dynamics.ffff
        }
        if thestring in lut:
            return lut[thestring]
        else:
            return 0
