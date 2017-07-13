NO_OF_OFFICIAL_CONTROLLERS = 128
NO_OF_CONTROLLERS = 129
NO_OF_TRACKS = 16


class Defaults:
    """
    some default values used to fill in missing data
    """
    note = "a4"
    dur = 1 / 4
    playeddur = 0.9
    lag = 0
    vol = 70
    tempo = 100


class PhraseProperty:
    """
    list of animatable properties
    """
    NOTE = "0"
    DUR = "1"
    PLAYEDDUR = "2"
    VOL = "3"
    LAG = "4"
    TEMPO = "5"

    @classmethod
    def CtrlDurKey(cls, CCNumber):
        return f"D{CCNumber}"

    @classmethod
    def CtrlValKey(cls, CCNumber):
        return f"V{CCNumber}"
