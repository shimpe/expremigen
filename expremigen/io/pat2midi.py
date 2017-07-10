from midiutil import MIDIFile

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.constants import Defaults
from expremigen.io.phrase import Phrase
from expremigen.patterns.pchord import Pchord


class Pat2Midi:
    def __init__(self, num_tracks: int = 1, remove_duplicates: bool = True, deinterleave: bool = True,
                 file_format: int = 1):
        self.midiFile = MIDIFile(numTracks=num_tracks, removeDuplicates=remove_duplicates, deinterleave=deinterleave,
                                 adjust_origin=False, file_format=file_format)
        self.last_set_tempo = [Defaults.tempo for _ in range(16)] # set every track to default tempo
        self.set_tempo(Defaults.tempo, 0)

    def set_tempo(self, tempo=100, time=0):
        self.midiFile.addTempo(track=0, time=time, tempo=tempo)
        self.last_set_tempo[0] = tempo

    def add_phrase(self, phrase: Phrase, track=0, channel=0, start_time=0):
        for event in phrase:
            # set tempo events only if they changed since last time
            if event[PP.TEMPO] != self.last_set_tempo[track]:
                self.midiFile.addTempo(track, start_time + phrase.generated_duration(), event[PP.TEMPO])
                self.last_set_tempo[track] = event[PP.TEMPO]
            # set notes always
            if isinstance(event[PP.NOTE], Pchord):
                for n in event[PP.NOTE].notes:
                    self.midiFile.addNote(
                        track=track,
                        channel=channel,
                        pitch=n,
                        time=start_time + phrase.generated_duration() + event[PP.LAG],
                        duration=event[PP.DUR] * event[PP.PLAYEDDUR],
                        volume=event[PP.VOL],
                        annotation=None)
            else:
                self.midiFile.addNote(
                    track=track,
                    channel=channel,
                    pitch=event[PP.NOTE],
                    time=start_time + phrase.generated_duration() + event[PP.LAG],
                    duration=event[PP.DUR] * event[PP.PLAYEDDUR],
                    volume=event[PP.VOL],
                    annotation=None)
        return phrase.generated_duration()

    def add_phrases(self, list_of_phrase, track=0, channel=0, start_time=0):
        time_delta = 0
        for phrase in list_of_phrase:
            duration = self.add_phrase(phrase, track, channel, start_time + time_delta)
            time_delta += duration
        return start_time + time_delta

    def write(self, filename):
        try:
            with open(filename, "wb") as f:
                self.midiFile.writeFile(fileHandle=f)
        except Exception as e:
            print("we hit a SNAFU while writing to {0}: {1}".format(filename, e))
