from expremigen.mispel.mispel import Mispel
from expremigen.io.pat2midi import Pat2Midi

outputfile = "output/tuplets.mid"


def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 0:
         r_1*4\tempo[160] |
         r_16 g#4\vol{p} a g# fx g# c#5 e\vol{mf} d# c# d# c# b#4 c#5 e g#\vol{p} |
         r_16 g#4\vol{p} a g# fx g# c#5 e\vol{mf} d# c# d# c# b#4 c#5 e g#\vol{p} |
         r_16 a4 c#5 d# f# a c#6 d# b a g# f# e d# f# c# |
         b#5 d#6 a5 g# f# a e d# f# c# b#4 d#5 a4 g# b a_8 |
         g#4_16\vol{p} a g# fx g# c#5 e\vol{mf} d# c# d# c# b#4 c#5 e g#\vol{p} |
        
    with track 1 channel 1:
        <g#2_1*2\vol{ff} g#3> | 
        <c#2_8*2/3\vol{f} c#3> g#3 c#4 e c# g#3 c# g# c#4 e c# g#3 |
        c# g# c#4 e c# g#3 c# g# c#4 e c# g#3\vol{p}  |
        c# g# c#4 e c# g#3 e g# c#4 e c# g#3 |
        c# g# c#4 e c# g#3 e g# c#4 e c# g#3 |
        d# a c#4 f# c# a3 f# c#4 d# a d# c# |
        g#2 d#3 f# b# f# d# g#2 d#3 f# b# f# d# |  
        
    """)
    p2m = Pat2Midi(m.get_no_of_tracks())
    m.add_to_pattern2midi(p2m)
    p2m.write(outputfile)


if __name__ == "__main__":
    make_midi()
