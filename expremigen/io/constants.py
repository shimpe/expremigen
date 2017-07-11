from enum import Enum


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


class PhraseProperty(Enum):
    """
    list of animatable properties
    """
    NOTE = 0
    DUR = 1
    PLAYEDDUR = 2
    VOL = 3
    LAG = 4
    TEMPO = 5
