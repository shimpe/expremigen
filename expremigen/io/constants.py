REST = 128

class Defaults:
    note = "a4"
    dur = 1/4
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

class Dynamics:
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

class Dur:
    onehundredtwentyeighth = 1/128
    sixtyfourth = 1/64
    thirtysecond = 1/32
    sixteenth = 1/16
    eighth = 1/8
    quarter = 1/4
    half = 1/2
    whole = 1
    doublewhole = 2