from expremigen.mispel.mispel import Mispel
from expremigen.io.pat2midi import Pat2Midi

def create_bach():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 0 time 0:
        r_16\pdur[legato]\vol{f} e4 a c5 b4 e b d5 c_8\pdur[staccato]\vol{ff} e g#4 e5 
        a4_16\vol{f} e4_16\pdur[legato] a c5 b4 e b d5 c_8\vol{ff}\pdur[staccato] a4 r_4\vol{f}
        r_16 e5\vol{p}\pdur[legato] c e a4 c5 e4 g f_8\vol{ff}\pdur[staccato] a\vol{f} d5 f_8.\vol{p}
        d_16\pdur[legato] b4 d5 g4 b d f e_8\vol{ff}\pdur[staccato] g\vol{f} c5 e_8.\vol{p}
        c5_16\pdur[legato] a4 c5 f4_8\vol{ff}\dur[staccato] d5_8.\vol{p}\pdur[legato] b4_16 g b e_8\vol{ff}\pdur[staccato] c5_8.\vol{p}\pdur[legato] 
        a4_16 f a d_8\vol{ff}\pdur[staccato] b_8 c5_8 r_8 r_4
    """)
    p2m = Pat2Midi()


if __name__=="__main__":
    create_bach()

