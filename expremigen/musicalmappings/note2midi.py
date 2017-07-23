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

    corner_case_octave_lower = set(["b#", "bx"])
    corner_case_octave_higher= set(["cb", "c-", "cbb", "c--"])

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
