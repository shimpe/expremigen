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
    octave = "4"


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
    def ctrl_dur_key(cls, cc_number):
        """
        calculates a key for specifying control change duration value (internal usage)
        :param cc_number: control change number
        :return: cc key
        """
        return f"D{cc_number}"

    @classmethod
    def ctrl_val_key(cls, cc_number):
        """
        calculates a key for specifying control change value (internal usage)
        :param cc_number: control change number
        :return: cc key
        """
        return f"V{cc_number}"
