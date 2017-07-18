from expremigen.io.pat2midi import Pat2Midi
from expremigen.mispel.mispel import Mispel

outputfile = "output/bwv784_2voice_invention_13.mid"


def create_bach():
    m = Mispel()
    m.parse(r"""
    with track 0:
        r_16\pdur[legato]\vol{f} e4 a c5 b4 e b d5 c_8\pdur[staccato]\vol{ff} e g#4 e5
        a4_16\vol{f} e4_16\pdur[legato] a c5 b4 e b d5 c_8\vol{ff}\pdur[staccato] a4 r_4\vol{f}
        r_16 e5\vol{p}\pdur[legato] c e a4 c5 e4 g f_8\vol{ff}\pdur[staccato] a\vol{f} d5 f_8.\vol{p}
        d_16\pdur[legato] b4 d5 g4 b d f e_8\vol{ff}\pdur[staccato] g\vol{f} c5 e_8.\vol{p}
        c5_16\pdur[legato] a4 c5 f4_8\vol{ff}\pdur[staccato] d5_8.\vol{p}\pdur[legato] b4_16 g b 
        e_8\vol{ff}\pdur[staccato] c5_8.\vol{p}\pdur[legato] 
        a4_16 f a d_8\vol{ff}\pdur[staccato] b_8 c5_8 r_8 r_4
        
    with track 1:
        a2_8\vol{mf}\pdur[staccato] a3_4\pdur[legato]\vol{f} g#_8\vol{mf} a_16\pdur[staccato]\vol{f} e3\pdur[legato] a c4 b3 e b d4 
        c_8\pdur[staccato]\vol{ff} a3 g# e a_16\vol{f} e\pdur[legato] a c4 b3 e b d4 
        c_8\pdur[staccato]\vol{ff} a3 c4 a3 
        d4_16\vol{f} a3\pdur[legato] f a d f a2 c3 
        b2_8\vol{p}\pdur[staccato] d3 g b_8.\vol{f}\pdur[legato] g3_16 e g c e g2 b 
        a_8\vol{p}\pdur[staccato] c3\vol{mf} d_16\pdur[legato] f b2 d3 g2_8\vol[f]\pdur[staccato] b c3_16\vol{f}\pdur[legato] e a2 c3
        f2_8\vol{p}\pdur[staccato] d g_16\vol{mp} g3\pdur[legato] f g c\vol{mf}\pdur[staccato] g\pdur[legato] 
        c4 e d g3 d4 f e_8\vol{f}\pdur[staccato] c

    """)
    p2m = Pat2Midi(num_tracks=2)
    for s in range(m.get_no_of_sections()):
        p2m.add_phrase(m.phrase_for_section(s), m.track_for_section(s), m.channel_for_section(s), m.time_for_section(s))

    p2m.write(outputfile)


if __name__ == "__main__":
    create_bach()
