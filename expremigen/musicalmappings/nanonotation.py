import re

from expremigen.musicalmappings.note2midi import Note2Midi


class NanoNotation:
    """
    simple text-based note entry
    each note consists of at least the note name, and then some optional parts:
    note name is one of a, b, c, d, e, f, g
    note name optionally can be followed by one of #, x, b, bb modifiers (note: modifiers are not remembered from previous notes)
    modifier is optionally followed by _[inverseduration (e.g. _8 for an eighth note)]
    inverse duration is optionally followed by one of \pdur{s} \pdur{l} \pdur{n} \pdur[s] \pdur[l] \pdur[n] for
                                                      (staccato, legato, normal), or -\pdur{1.2} or -\pdur[0.3]
       note: parameters in {} will animate from this value to the next value
             parameters in [] will remain constant until the next value
    staccato/legato is optionally followed by dynamics: one of \dyn{ppppp}, ..., \dyn{ffff} or \dyn[ppppp] ... \dyn[ffff],
                                                        or \dyn{43} or \dyn[23]
       note: parameters in {} will animate from this value to the next value
             parameters in [] will remain constant until the next value
    dynamics is optionally followed by \lag{0.125} or \lag[0.125] to specify a lag of 0.125
       note: parameters in {} will animate from this value to the next value
             parameters in [] will remain constant until the next value
    lag is optionally followed by \tempo{80} or \tempo[80] to indicate tempo of 80 bpm
       note: parameters in {} will animate from this value to the next value
             parameters in [] will remain constant until the next value
    """

    def __init__(self):
        self.note2midi = Note2Midi()
        self.note = re.compile("[a-g]")
        self.note_octave = re.compile("[a-g](?P<octave>\d+)")
        self.last_dur = 1
        self.last_octave = 4

    def notes(self, a_phrase):
        """
        return the list of midi note numbers in a_string
        :param a_phrase: consisting of "[notename][octave]_[inverseduration] ..."
        e.g. "a5_8 e5_8 d4 c4 a3_2"
        :returns list of midi note numbers
        """
        note_durs = a_phrase.split(" ")
        notes = []
        for notedur in note_durs:
            if "_" in notedur:
                note = notedur.split("_")[0].lower()
            else:
                note = notedur.lower()

            m = re.match(self.note_octave, note)
            if m:
                self.last_octave = int(m.group("octave"))
            else:
                m2 = re.match(self.note, note)
                if m2:
                    note = f"{note}{self.last_octave}"
                else:
                    pass  # note = note ;)
            notes.append(note)
        return notes

    def midinumbers(self, a_phrase):
        """
        :param a_phrase: a nanonotaion string "[notename][octave]_[inverseduration]..."
        :return: list of midi note numbers
        """
        return self.note2midi.convert2(self.notes(a_phrase))

    def dur(self, a_phrase):
        """
        :param a_phrase:
        :return: list of durations
        """
        note_durs = a_phrase.split(" ")
        durs = []
        for notedur in note_durs:
            if "_" in notedur:
                dur = notedur.split("_")[1]
                cnt = 0
                while dur.endswith("."):
                    dur = dur[:-1]
                    cnt += 1
                float_dur = 1 / int(dur)
                for c in range(cnt):
                    pointed_dur = (float_dur / (2 * (c + 1)))
                    float_dur = float_dur + pointed_dur

                durs.append(float_dur)
                self.last_dur = float_dur
            else:
                durs.append(self.last_dur)
        return durs
