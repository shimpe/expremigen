class Defaults:
    note = "a4"
    dur = 1 / 4
    playeddur = 0.9
    lag = 0
    vol = 70


from enum import Enum


class PhraseProperty(Enum):
    NOTE = 0
    DUR = 1
    PLAYEDDUR = 2
    VOL = 3
    LAG = 4
