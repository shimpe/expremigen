from expremigen.mispel.mispel import Mispel
from expremigen.io.pat2midi import Pat2Midi

outputfile = "output/chopin.mid"

def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 0:
         r_1*4 |
         r_16 g#4\vol{p} a g# fx g# c#5 e\vol{mf} d# c# d# c# b#4 c# e g#\vol{p} |
         r_16 g#4\vol{p} a g# fx g# c#5 e\vol{mf} d# c# d# c# b#4 c# e g#\vol{p} |
        
    with track 1 channel 1:
        <g#2_1*2/1\vol{ff} g#3> | 
        <c#2_8*2/3\vol{f} c#3> g#3 c#4 e c# g#3 c# g# c#4 e c# g#3 |
        c# g# c#4 e c# g#3 c# g# c#4 e c# g#3\vol{p}  |
        c# g# c#4 e c# g#3 e g# c#4 e c# g#3 |
        
    """)
    p2m = Pat2Midi(m.get_no_of_tracks())
    m.add_to_pattern2midi(p2m)
    p2m.write(outputfile)

if __name__=="__main__":
    make_midi()