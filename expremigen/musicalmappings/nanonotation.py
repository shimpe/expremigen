import re
from expremigen.musicalmappings.note2midi import Note2Midi


class NanoNotation:
    def __init__(self):
        self.note2midi = Note2Midi()
        self.note = re.compile("[a-g]")
        self.note_octave = re.compile("[a-g](?P<octave>\d+)")
        self.last_dur = 1
        self.last_octave = 4

    def notes(self, a_string):
        """
        return the list of midi note numbers in a_string
        :param a_string: consisting of "[notename][octave]_[inverseduration] ..."
        e.g. "a5_8 e5_8 d4 c4 a3_2"
        :returns list of midi note numbers
        """
        note_durs = a_string.split(" ")
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
                    pass # note = note ;)
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
        :return:
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
