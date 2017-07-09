from expremigen.musicalmappings.constants import REST


class Note2Midi:
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
                for note in note_synonyms:
                    self.note_to_midi["{0}{1}".format(note, octave - 1)] = notenum
                notenum += 1

    def lookup(self, note):
        try:
            return self.note_to_midi[note.lower()]
        except KeyError:
            return REST

    def convert(self, notelist):
        for n in notelist:
            yield self.lookup(n)

    def convert2(self, notelist):
        return [self.lookup(note) for note in notelist]
