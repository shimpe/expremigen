from expremigen.io.pat2midi import Pat2Midi
from expremigen.mispel.mispel import Mispel

outputfile = "output/mispelpitchbend.mid"


def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0:
        c4_16\cc{128,-8000} c c c c c c c c c\cc[128,3000] c c\cc{128,8000} c c c c\cc{128,0}

    with track 1:
        <c3_4 e3 g3> <b2 d3 g3> <c3 e3 g3 c4>
    """)
    p2m = Pat2Midi(num_tracks=2)
    for s in range(m.get_no_of_sections()):
        p2m.add_phrase(m.phrase_for_section(s), m.track_for_section(s), m.channel_for_section(s), m.time_for_section(s))

    p2m.write(outputfile)


if __name__ == "__main__":
    make_midi()
