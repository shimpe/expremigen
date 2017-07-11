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
    chromatic_scale = [['c', 'b#', 'dbb'],  # one row contains all synonyms (i.e. synonym for our purpose)
                       ['c#', 'bx', 'db'],
                       ['d', 'cx', 'ebb'],
                       ['d#', 'eb', 'fbb'],
                       ['e', 'dx', 'fb'],
                       ['f', 'e#', 'gbb'],
                       ['f#', 'ex', 'gb'],
                       ['g', 'fx', 'abb'],
                       ['g#', 'ab'],
                       ['a', 'gx', 'bbb'],
                       ['a#', 'bb', 'cbb'],
                       ['b', 'ax', 'cb']]

    def __init__(self):
        # '#' denotes a sharp, 'b' denotes a flat, x denotes a double sharp, bb denotes a double flat
        self.note_to_midi = {}
        notenum = 0
        for octave in range(10):
            for note_synonyms in self.chromatic_scale:
                if notenum <= 127:
                    for note in note_synonyms:
                        self.note_to_midi["{0}{1}".format(note, octave - 1)] = notenum
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
