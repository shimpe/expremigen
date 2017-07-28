from expremigen.io.pat2midi import Pat2Midi
from expremigen.mispel.mispel import Mispel

outputfile = "output/example_drumpattern.mid"


def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 10:
        bassdrum r4 bassdrum r4 bassdrum r4
        
    with track 0 channel 10:
        r4 closedhihat r4 closedhihat   
    """)
    p2m = Pat2Midi(m.get_no_of_tracks())
    m.add_to_pattern2midi(p2m)
    p2m.write(outputfile)


if __name__ == "__main__":
    make_midi()
