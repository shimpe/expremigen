from midiutil import MIDIFile

from expremigen.io.constants import Defaults, NO_OF_CONTROLLERS, NO_OF_OFFICIAL_CONTROLLERS, NO_OF_TRACKS
from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.midicontrolchanges import MidiControlChanges
from expremigen.io.phrase import Phrase
from expremigen.patterns.pchord import Pchord


class Pat2Midi:
    """
    class to convert Pattern to Midi
    """

    def __init__(self, num_tracks: int = 1, remove_duplicates: bool = True, deinterleave: bool = True,
                 file_format: int = 1):
        """

        :param num_tracks: number of tracks (default: 1)
        :param remove_duplicates: remove notes if they start at the same time on the same channel if they have the same pitch  (default: True)
        :param deinterleave: clean up two note-ons with no note-off in between (default: True)
        :param file_format: 1 or 2 (default: 1)
        """
        self.midiFile = MIDIFile(numTracks=num_tracks, removeDuplicates=remove_duplicates, deinterleave=deinterleave,
                                 adjust_origin=False, file_format=file_format)
        self.last_set_tempo = [Defaults.tempo for _ in range(16)]  # set every track to default tempo
        self.set_tempo(Defaults.tempo, 0)
        self.last_set_cc = [[None for _ in range(NO_OF_CONTROLLERS)] for _ in range(NO_OF_TRACKS)]

    def set_tempo(self, tempo=100, time=0):
        """

        :param tempo: bpm (default: 100)
        :param time: time at which the tempo change should be inserted in the midi stream (default: 0)
        """
        self.midiFile.addTempo(track=0, time=time, tempo=tempo)
        self.last_set_tempo[0] = tempo
        self.last_set_cc = [[None for _ in range(NO_OF_CONTROLLERS)] for _ in range(NO_OF_TRACKS)]

    def add_phrase(self, phrase: Phrase, track=0, channel=0, start_time=0):
        """

        :param phrase: a Phrase containing patterns and animations
        :param track: default: 0
        :param channel: default: 0
        :param start_time: time at which the phrase should be inserted default: 0
        :return: total duration of the inserted phrase
        """
        for event in phrase:
            # set tempo events only if they changed since last time
            # handle note events
            if PP.NOTE in event:
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
            # handle controller events (only if they changed since last time)
            else:
                for cc in range(NO_OF_OFFICIAL_CONTROLLERS):
                    if PP.CtrlDurKey(cc) in event:
                        time = start_time + phrase.generated_ctrl_duration(cc)
                        value = event[PP.CtrlValKey(cc)]
                        self.midiFile.addControllerEvent(track=track,
                                                         channel=channel,
                                                         time=time,
                                                         controller_number=cc,
                                                         parameter=value)
                for cc in [MidiControlChanges.PitchWheel]:
                    if PP.CtrlDurKey(cc) in event:
                        time = start_time + phrase.generated_ctrl_duration(cc)
                        pwvalue = event[PP.CtrlValKey(cc)]
                        self.midiFile.addPitchWheelEvent(track=track,
                                                         channel=channel,
                                                         time=time,
                                                         pitchWheelValue=pwvalue)

        return phrase.generated_duration()

    def add_phrases(self, list_of_phrase, track=0, channel=0, start_time=0):
        """

        :param list_of_phrase: a list of Phrase
        :param track: default: 0
        :param channel: midi channel, deafult: 0
        :param start_time: default: 0
        :return: total duration of piece from begin until end of list of phrases
        """
        time_delta = 0
        for phrase in list_of_phrase:
            duration = self.add_phrase(phrase, track, channel, start_time + time_delta)
            time_delta += duration
        return start_time + time_delta

    def write(self, filename):
        """
        write to midi file
        :param filename: filename
        """
        try:
            with open(filename, "wb") as f:
                self.midiFile.writeFile(fileHandle=f)
        except Exception as e:
            print("we hit a SNAFU while writing to {0}: {1}".format(filename, e))
