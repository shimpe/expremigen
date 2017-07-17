class PlayedDurations:
    staccatissimo = 0.1
    staccato = 0.25
    normal = 0.9
    legato = 1
    super_legato = 1.1

    @classmethod
    def from_string(cls, thestring):
        lut = {
            'staccatissimo': 0.1,
            'staccato': 0.25,
            'normal': 0.9,
            'legato': 1,
            'legatissimo': 1.1
        }

        if thestring in lut:
            return lut[thestring]
        else:
            return 0.9