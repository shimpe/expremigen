from expremigen.musicalmappings.constants import REST
from expremigen.patterns.pchord import Pchord


class Note2Midi:
    """
    class to convert note names to midi numbers

    a note name consists of
    [note name][modifier][octave]
    where
    note name: one of a, b, c, d, e, f, g
    modifier: one of #, b, x, bb
    octave: 0-10

    anything not recognized as a note becomes a rest
    """
    chromatic_scale = [['c', 'b#', 'dbb', 'd--'],  # one row contains all synonyms (i.e. synonym for our purpose)
                       ['c#', 'bx', 'db', 'd-'],
                       ['d', 'cx', 'ebb', 'e--'],
                       ['d#', 'eb', 'e-', 'fbb', 'f--'],
                       ['e', 'dx', 'fb', 'f-'],
                       ['f', 'e#', 'gbb', 'g--'],
                       ['f#', 'ex', 'gb', 'g-'],
                       ['g', 'fx', 'abb', 'a--'],
                       ['g#', 'ab', 'a-'],
                       ['a', 'gx', 'bbb', 'b--'],
                       ['a#', 'bb', 'b-', 'cbb', 'c--'],
                       ['b', 'ax', 'cb', 'c-']]

    corner_case_octave_lower = {"b#", "bx"}
    corner_case_octave_higher = {"cb", "c-", "cbb", "c--"}

    drummap = {
        ('acousticbassdrum', 'abd'): 35,
        ('bassdrum', 'bad'): 36,
        ('sidestick', 'sis'): 37,
        ('acousticsnare', 'acs'): 38,
        ('brushtap', 'brt'): 38,  # brush kit instead of drum kit
        ('handclap', 'hac'): 39,
        ('brushslap', 'brs'): 39,  # brush kit instead of drum kit
        ('electricsnare', 'els'): 40,
        ('brushswirl', 'brw'): 40,  # brush kit instead of drum kit
        ('lowfloortom', 'lft'): 41,
        ('closedhihat', 'chh'): 42,
        ('highfloortom', 'hft'): 43,
        ('pedalhihat', 'phh'): 44,
        ('lowtom', 'lot'): 45,
        ('openhihat', 'ohh'): 46,
        ('lowmidtom', 'lmt'): 47,
        ('highmidtom', 'hmt'): 48,
        ('crashsymbal1', 'cs1'): 49,
        ('hightom', 'hit'): 50,
        ('ridecymbal1', 'rc1'): 51,
        ('chinesecymbal', 'chc'): 52,
        ('ridebell', 'rib'): 53,
        ('tambourine', 'tam'): 54,
        ('splashcymbal', 'spc'): 55,
        ('cowbell', 'cob'): 56,
        ('crashsymbal2', 'cc2'): 57,
        ('vibraslap', 'vis'): 58,
        ('ridecymbal2', 'rc2'): 59,
        ('highbongo', 'hib'): 60,
        ('lowbongo', 'lob'): 61,
        ('mutehiconga', 'mhc'): 62,
        ('openhiconga', 'ohc'): 63,
        ('lowconga', 'loc'): 64,
        ('hightimbale', 'him'): 65,
        ('lowtimbale', 'lom'): 66,
        ('highagogo', 'hag'): 67,
        ('lowagogo', 'lag'): 68,
        ('cabasa', 'cab'): 69,
        ('maracas', 'mar'): 70,
        ('shortwhistle', 'swh'): 71,
        ('longwhistle', 'lwh'): 72,
        ('shortguiro', 'shg'): 73,
        ('longguiro', 'log'): 74,
        ('claves', 'cla'): 75,
        ('hiwoodblock', 'hwb'): 76,
        ('lowoodblock', 'lwb'): 77,
        ('mutecuica', 'muc'): 78,
        ('opencuica', 'opc'): 79,
        ('mutetriangle', 'mut'): 80,
        ('opentriangle', 'opt'): 81,
        ('shaker', 'shk'): 82
    }

    def __init__(self):
        # '#' denotes a sharp, 'b' denotes a flat, x denotes a double sharp, bb denotes a double flat
        self.note_to_midi = {}
        notenum = 0
        for octave in range(10):
            for note_synonyms in self.chromatic_scale:
                if notenum <= 127:
                    for note in note_synonyms:

                        o = octave - 1
                        if note in self.corner_case_octave_lower:
                            o = o - 1
                        elif note in self.corner_case_octave_higher:
                            o = o + 1
                        self.note_to_midi["{0}{1}".format(note, o)] = notenum
                    notenum += 1

        self.all_drum_notes = set([])
        for d in self.drummap:
            self.note_to_midi["{0}".format(d[0])] = self.drummap[d]
            self.note_to_midi["{0}".format(d[1])] = self.drummap[d]
            # check that we didn't use the same acronym twice...
            assert d[0] not in self.all_drum_notes
            assert d[1] not in self.all_drum_notes
            self.all_drum_notes.add(d[0])
            self.all_drum_notes.add(d[1])

    def get_drumnotes_for_grammar(self):
        """
        internal helper function
        :return: list of drumnotes for inclusion in the textX grammar
        """
        from functools import cmp_to_key
        def mycmp(s1, s2):
            if len(s1) < len(s2):
                return 1
            if len(s1) > len(s2):
                return -1
            if s1 < s2:
                return 1
            if s1 > s2:
                return -1
            return 0

        strng = "|".join(sorted(["'" + d.strip() + "'" for d in self.all_drum_notes], key=cmp_to_key(mycmp)))
        return strng

    def lookup(self, note):
        """

        :param note: lookup simple note or Pchord
        :return: midi number corresponding to the note name or the notes in the Pchord
        """
        try:
            if isinstance(note, Pchord):
                return Pchord([self.note_to_midi[n.lower()] for n in note.notes])
            else:
                return self.note_to_midi[note.lower()]
        except KeyError:
            return REST

    def convert(self, notelist):
        """

        :param notelist: list of music notes
        :return: iterator iterating over the converted list of notes
        """
        for n in notelist:
            yield self.lookup(n)

    def convert2(self, notelist):
        """

        :param notelist:  listof music notes and/or Pchords
        :return: list of midi numbers and Pchords of midi numbers
        """
        return [self.lookup(note) for note in notelist]
