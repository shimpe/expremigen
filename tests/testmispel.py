import unittest

from textx.exceptions import TextXSyntaxError

from expremigen.mispel.mispel import Mispel


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
            model = m.parse("with chanel 2 buzzdriven :\n a3")
            self.assertTrue(False)  # will fail unless the above throws an exception
        except TextXSyntaxError as e:
            self.assertTrue(True)

    def test_events1(self):
        m = Mispel()
        model = m.parse("with channel 2 notedriven :\n a3_8 b- c#3_16.5\\vol{100}\\tempo[vivace] ")
        for section in model.sections:
            event = section.events[0]
            self.assertEqual(event.cs, None)
            self.assertTrue(event.__class__.__name__, 'NoteSpec')
            self.assertEqual(event.ns.name, 'a')
            self.assertEqual(event.ns.octave, '3')
            self.assertEqual(event.ns.invdur.value, 8)
            self.assertEqual(event.ns.properties, [])
            event = section.events[1]
            self.assertEqual(event.ns.name, 'b-')
            self.assertEqual(event.ns.octave, None)
            self.assertEqual(event.ns.invdur, None)
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
        self.assertListEqual(m.durations_for_section(0), [8, 8, 16.5])

    def test_sections(self):
        m = Mispel()
        model = m.parse(r"""
        with track 0:
            c4_8\vol{p}\pdur[legato] e g c5 b4 g f d c_2\vol{f}\pdur[staccato]
            
        with track 1:
            e3_8\vol{ff}\lag{0.5} g c4 e d b3 g f e_2\vol{p}\lag{0}
        """)
        self.assertEqual(m.get_no_of_sections(), 2)

    def test_dynamicsforsection(self):
        m = Mispel()
        model = m.parse(r"""
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
        model = m.parse(r"""
        with track 0:
            a3_8\vol[mf] b c4_4 d\vol{10} e f\vol[30] e f-- r ax d\vol{90} c 
        """)
        vols = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols, [90, 90, 90, 10, 20, 30, 30, 30, 30, 30, 90, 90])

    def test_dynamicsgeneratorforsection_lastvolume_at_end(self):
        m = Mispel()
        model = m.parse(r"""
        
        with track 0:
            a3_8\vol[mf] b c4_4 d\vol{10} e f\vol[30] e f-- r ax d\vol{90} 

        """)
        vols = [v for v in m.dynamics_generator_for_section(0)]
        self.assertListEqual(vols, [90, 90, 90, 10, 20, 30, 30, 30, 30, 30, 90])

    def test_lagforsection(self):
        m = Mispel()
        model = m.parse(r"""
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
        model = m.parse(r"""
        with track 0:
            a2_4 a3 a4_16\lag[0.9] b c5 d e f g a b a g f\lag{1} e d c b\lag{0.5}
        """)
        lags = [l for l in m.lag_generator_for_section(0)]
        print(lags)
        self.assertListEqual(lags,
                             [0.0, 0.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 1.0, 0.875, 0.75, 0.625,
                              0.5])


if __name__ == '__main__':
    unittest.main()
