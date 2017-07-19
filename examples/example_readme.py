from expremigen.io.pat2midi import Pat2Midi
from expremigen.mispel.mispel import Mispel

outputfile = "output/example_readme.mid"


def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 0:
        c4_16\vol{p} e g c5 b4 g f d c_4\vol{ff}

    with track 1 channel 1:
        <c3_4\vol{mf} e3 g3> <b2 d3 g3> <c3 e3 g3 c4>
    """)
    p2m = Pat2Midi(m.get_of_tracks())
    m.add_to_pattern2midi(p2m)
    p2m.write(outputfile)


if __name__ == "__main__":
    make_midi()
