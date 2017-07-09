from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.phrase import Phrase
from midiutil import MIDIFile

class Pat2Mid:
    def __init__(self, numTracks=1, removeDuplicates=True, deinterleave=True, file_format=1):
        self.midiFile = MIDIFile(numTracks=numTracks, removeDuplicates=removeDuplicates, deinterleave=deinterleave,
                                 adjust_origin=False, file_format=file_format)

    def setTempo(self, tempo=100, time=0):
        self.midiFile.addTempo(track=0, time=time, tempo=tempo)

    def addPhrase(self, phrase : Phrase, track = 0, channel = 0, start_time = 0):
        for event in phrase:
            self.midiFile.addNote(
                track = 0,
                channel = 0,
                pitch = event[PP.NOTE],
                time = start_time + phrase.generated_duration() + event[PP.LAG],
                duration = event[PP.DUR] * event[PP.PLAYEDDUR],
                volume = event[PP.VOL],
                annotation=None)
        return phrase.generated_duration()

    def write(self, filename):
        try:
            with open(filename, "wb") as f:
                self.midiFile.writeFile(fileHandle=f)
        except Exception:
            print("we hit a SNAFU while writing to {0}".format(filename))
