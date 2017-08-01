import unittest

from textx.exceptions import TextXSyntaxError

from expremigen.io.constants import PhraseProperty as PP
from expremigen.mispel.mispel import Mispel
from expremigen.patterns.pchord import Pchord
from expremigen.patterns.pseq import Pseq


class TestPat2Midi(unittest.TestCase):
    def test_header1(self):
        m = Mispel()
        model = m.parse("with track 5 channel 2 time 0 notedriven :\n a3")
        for section in model.sections:
            self.assertEqual(section.headerspecs.track.id, 5)
            self.assertEqual(section.headerspecs.channel.id, 2)
            self.assertEqual(section.headerspecs.time.value, 0)
            self.assertEqual(section.headerspecs.driver, 'notedriven')

    def test_headershort(self):
        m = Mispel()
        model = m.parse("with channel 2 timedriven :\n a3")
        for section in model.sections:
            self.assertEqual(section.headerspecs.track, None)
            self.assertEqual(section.headerspecs.channel.id, 2)
            self.assertEqual(section.headerspecs.time, None)
            self.assertEqual(section.headerspecs.driver, 'timedriven')

    def test_headerbad(self):
        m = Mispel()
        try:
            m.parse("with chanel 2 buzzdriven :\n a3")
            self.assertTrue(False)  # will fail unless the above throws an exception
        except TextXSyntaxError:
            self.assertTrue(True)

    def test_events1(self):
        m = Mispel()
        model = m.parse("with channel 2 notedriven :\n a3_8. b-_16 c#3_16.5\\vol{100}\\tempo[vivace] ")
        for section in model.sections:
            event = section.events[0]
            self.assertEqual(event.cs, None)
            self.assertTrue(event.__class__.__name__, 'NoteSpec')
            self.assertEqual(event.ns.name, 'a')
            self.assertEqual(event.ns.octave, '3')
            self.assertEqual(event.ns.invdur.value, 8)
            self.assertListEqual(event.ns.invdur.dots, ['.'])
            self.assertEqual(event.ns.properties, [])
            event = section.events[1]
            self.assertEqual(event.ns.name, 'b-')
            self.assertEqual(event.ns.octave, None)
            self.assertEqual(event.ns.invdur.value, 16)
            self.assertListEqual(event.ns.invdur.dots, [])
            self.assertEqual(event.ns.properties, [])
            event = section.events[2]
            self.assertEqual(event.ns.name, 'c#')
            self.assertEqual(event.ns.octave, '3')
            self.assertEqual(event.ns.invdur.value, 16.5)
            for p in event.ns.properties:
                if p.avol:
                    self.assertEqual(p.avol.symval, None)
                    self.assertEqual(p.avol.value.value, 100)
                elif p.stempo:
                    self.assertEqual(p.stempo.symval.symval, 'vivace')
                    self.assertEqual(p.stempo.value, None)

        self.assertListEqual(m.notes_for_section(0), ["a3", "b-3", "c#3"])
        self.assertListEqual(m.durations_for_section(0), [1 / 8 + 1 / 16, 1 / 16, 1 / 16.5])

    def test_durationmultiplier(self):
        m = Mispel()
        m.parse(r"""
        with track 0 channel 0: cx4_4*2/3 d3 e-_4 g--_4.*2/3 r_1*10/1 a#2_1*5
        """)
        durs = [d for d in m.durations_for_section(0)]
        self.assertListEqual(durs, [0.16666666666666666, 0.16666666666666666, 0.25, 0.25, 10.0, 5.0])

    def test_sections(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            c4_8\vol{p}\pdur[legato] e g c5 b4 g f d c_2\vol{f}\pdur[staccato]
            
        with track 1:
            e3_8\vol{ff}\lag{0.5} g c4 e d b3 g f e_2\vol{p}\lag{0}
        """)
        self.assertEqual(m.get_no_of_sections(), 2)

    def test_dynamicsforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a3_8\vol[mf] b c4_4 d\vol{ff} e f\vol{30} e f-- r ax d\vol[20] c 
        """)
        self.assertListEqual(m.notes_for_section(0),
                             ["a3", "b3", "c4", "d4", "e4", "f4", "e4", "f--4", "r", "ax4", "d4", "c4"])
        self.assertListEqual(m.dynamics_for_section(0), [(('num', 'static', 70), ('sym', 'static', 'mf'), 0),
                                                         (('sym', 'static', 'mf'), ('sym', 'anim', 'ff'), 3),
                                                         (('sym', 'anim', 'ff'), ('num', 'anim', 30), 2),
                                                         (('num', 'anim', 30), ('num', 'static', 20), 5),
                                                         (('num', 'static', 20), ('num', 'static', 20), 2)]
                             )

    def test_dynamicsgeneratorforsection1(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a3_8\vol[mf] b c4_4 d\vol{10} e f\vol[30] e f-- r ax d\vol{90} c 
        """)
        vols = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols, [90, 90, 90, 10, 20, 30, 30, 30, 30, 30, 90, 90])

    def test_dynamicsgeneratorforsection_lastvolume_at_end(self):
        m = Mispel()
        m.parse(r"""
        
        with track 0:
            a3_8\vol[mf] b c4_4 d\vol{10} e f\vol[30] e f-- r ax d\vol{90} 

        """)
        vols = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols, [90, 90, 90, 10, 20, 30, 30, 30, 30, 30, 90])

    def test_lagforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a2_4 a3 a4_16\lag[0.9] b c5 d e f g a b a g f\lag{1} e d c b\lag{0.3}
        """)
        self.assertListEqual(m.notes_for_section(0),
                             "a2 a3 a4 b4 c5 d5 e5 f5 g5 a5 b5 a5 g5 f5 e5 d5 c5 b5".split(" "))
        self.assertListEqual(m.lag_for_section(0),
                             [(('num', 'static', 0), ('num', 'static', 0.9), 2),
                              (('num', 'static', 0.9), ('num', 'anim', 1.0), 11),
                              (('num', 'anim', 1.0), ('num', 'anim', 0.3), 4),
                              (('num', 'anim', 0.3), ('num', 'anim', 0.3), 1)]
                             )

    def test_laggeneratorforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a2_4 a3 a4_16\lag[0.9] b c5 d e f g a b a g f\lag{1} e d c b\lag{0.5}
        """)
        lags = [l for l in m.lag_generator_for_section(0)]
        self.assertListEqual(lags,
                             [0.0, 0.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 1.0, 0.875, 0.75, 0.625,
                              0.5])

    def test_pdurforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 1 channel 1 time 0:
            c4_4\pdur{staccato} d e f g a b c5\pdur[legato] d e d c_1\pdur[staccato]             
        """)
        self.assertListEqual(m.pdur_for_section(0),
                             [(('num', 'static', 0.9), ('sym', 'anim', 'staccato'), 0),
                              (('sym', 'anim', 'staccato'), ('sym', 'static', 'legato'), 7),
                              (('sym', 'static', 'legato'), ('sym', 'static', 'staccato'), 4),
                              (('sym', 'static', 'staccato'), ('sym', 'static', 'staccato'), 1)]
                             )

    def test_pdurgeneratorforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 1 channel 1 time 0:
            c4_4\pdur{staccato} d e f g a b c5\pdur[legato] d e d c_1\pdur[staccato]
        """)
        pdurs = [pd for pd in m.pdur_generator_for_section(0)]
        self.assertListEqual(pdurs,
                             [0.25, 0.35714285714285715, 0.4642857142857143, 0.5714285714285714, 0.6785714285714286,
                              0.7857142857142857,
                              0.8928571428571429, 1.0, 1.0, 1.0, 1.0, 0.25])

    def test_tempoforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 1 channel 1 time 0:
            c4_4\pdur{staccato}\tempo[allegretto] d e f g a b c5\pdur[legato] d e\tempo{120} d c_1\tempo[40]\pdur[staccato]             
        """)
        self.assertListEqual(m.tempo_for_section(0), [(('num', 'static', 100), ('sym', 'static', 'allegretto'), 0),
                                                      (('sym', 'static', 'allegretto'), ('num', 'anim', 120), 9),
                                                      (('num', 'anim', 120), ('num', 'static', 40), 2),
                                                      (('num', 'static', 40), ('num', 'static', 40), 1)]
                             )

    def test_tempogeneratorforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 1 channel 1 time 0:
            c4_4\pdur{staccato}\tempo[allegretto] d e f g a b c5\pdur[legato] d e\tempo{120} d c_1\tempo[40]\pdur[staccato]             
        """)

        tempos = [t for t in m.tempo_generator_for_section(0)]
        self.assertListEqual(tempos, [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 80, 40])

    def test_dot(self):
        m = Mispel()
        m.parse("with channel 2 notedriven :\n a3_8. b-16")
        durs = [d for d in m.duration_generator_for_section(0)]
        self.assertEqual(durs, [(1 / 8 + 1 / 16), (1 / 8 + 1 / 16)])

    def test_chord(self):
        m = Mispel()
        m.parse("with track 0 : a3_4\\vol[20] <c e g> a\\vol[30]")
        notes = [n for n in m.note_generator_for_section(0)]
        self.assertListEqual(notes, ['a3', Pchord(['c3', 'e3', 'g3']), 'a3'])
        vols = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols, [20.0, 20.0, 30.0])

    def test_ccpropertiesforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 0 : a3\pdur[legato]\cc[15,100] b <c\cc{16,23} d4> e\cc[15,90] f a g\cc[16,40] b
        """)
        self.assertDictEqual(m.cc_properties_for_section(0),
                             {15: [(None, ('num', 'static', 100), 0),
                                   (('num', 'static', 100), ('num', 'static', 90), 3),
                                   (('num', 'static', 90), ('num', 'static', 90), 5)],
                              16: [(None, ('num', 'anim', 23), 2),
                                   (('num', 'anim', 23), ('num', 'static', 40), 4),
                                   (('num', 'static', 40), ('num', 'static', 40), 2)]})

    def test_ccpropertiesgeneratorsforsection(self):
        m = Mispel()
        m.parse(r"""
        with track 0: a3\pdur[legato]\cc[15,100] b <c\cc{16,23} d4> e\cc[15,90] f a g\cc[16,40] b
        """)
        p = m.cc_properties_generators_for_section(0)

        dur15 = [d for d in Pseq(p[15][PP.ctrl_dur_key(15)], 1)]
        val15 = [v for v in Pseq(p[15][PP.ctrl_val_key(15)], 1)]

        dur16 = [d for d in Pseq(p[16][PP.ctrl_dur_key(16)], 1)]
        val16 = [v for v in Pseq(p[16][PP.ctrl_val_key(16)], 1)]

        self.assertListEqual(dur15, [0, 0.75, 1.25])
        self.assertListEqual(val15, [None, 100, 90])

        self.assertListEqual(dur16,
                             [0.5, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025,
                              0.025, 0.025, 0.025,
                              0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025,
                              0.025, 0.025, 0.025,
                              0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.5])
        self.assertListEqual(val16,
                             [None, 23.0, 23.425, 23.85, 24.275, 24.7, 25.125, 25.55, 25.975, 26.4, 26.825, 27.25,
                              27.675, 28.1, 28.525,
                              28.95, 29.375, 29.8, 30.225, 30.65, 31.075, 31.5, 31.925, 32.35, 32.775, 33.2, 33.625,
                              34.05, 34.475, 34.9,
                              35.325, 35.75, 36.175, 36.6, 37.025, 37.45, 37.875, 38.3, 38.725, 39.15, 39.575, 40])

    def test_animationtypes(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a4_4\vol{mp, easeOutQuad} b c d\vol{f, easeOutElastic, 2, 0.01}
        """)
        vols = [v for v in m.dynamics_for_section(0)]
        self.assertListEqual(vols,
                             [(('num', 'static', 70), ('sym', 'anim', 'mp', ['easeOutQuad']), 0),
                              (('sym', 'anim', 'mp', ['easeOutQuad']),
                               ('sym', 'anim', 'f', ['easeOutElastic', 2.0, 0.01]), 3),
                              (('sym', 'anim', 'f', ['easeOutElastic', 2.0, 0.01]),
                               ('sym', 'anim', 'f', ['easeOutElastic', 2.0, 0.01]), 1)])

    def test_animationtypes_generator(self):
        m = Mispel()
        m.parse(r"""
        with track 0:
            a4_4\vol{mp, easeOutQuad} b c d\vol{f, easeOutElastic, 50, 0.1} e f g a b c d e f g a b c d e f g a b c d e f g\vol[mp]
        """)
        vols2 = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols2,
                             [80.0, 91.11111111111111, 97.77777777777777, 100.0, 80, 100, 80, 100, 80, 80, 100, 80, 100,
                              80, 100, 80.62500000000003, 80, 95.3611067738703, 80, 88.42426702280262, 80, 80,
                              82.14053136466876, 80, 82.32220556599769, 80, 80.629068677026, 80.0])

    def test_drumnotes(self):
        m = Mispel()
        m.parse(r"""
        with track 0 channel 11:
            bassdrum_4 openhihat_8*2/3 openhihat ohh  
        """)
        notes = m.notes_for_section(0)
        self.assertListEqual(notes, ['bassdrum', 'openhihat', 'openhihat', 'ohh'])
        durs = m.durations_for_section(0)
        self.assertListEqual(durs, [0.25, 0.08333333333333333, 0.08333333333333333, 0.08333333333333333])


if __name__ == '__main__':
    unittest.main()
