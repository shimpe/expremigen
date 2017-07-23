from collections import defaultdict

from textx.metamodel import metamodel_from_str
from vectortween.NumberAnimation import NumberAnimation

from expremigen.io.constants import Defaults, NO_OF_CONTROLLERS
from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.phrase import Phrase
from expremigen.mispel.exception import ValidationException
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.playeddurations import PlayedDurations as PDur
from expremigen.musicalmappings.tempo import Tempo
from expremigen.patterns.pchord import Pchord
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween
from expremigen.patterns.utils import take


class Mispel:
    """
    Mispel = MIdi SPEcification Language
    """

    def __init__(self):
        self.grammar = r"""
        SectionModel:
            sections+=Section
        ;
        Section:
            'with' headerspecs=HeaderSpec ':' events+=Event
        ;
        HeaderSpec:
             (TimeDrivenHeaderSpec | NoteDrivenHeaderSpec)
        ;
        TimeDrivenHeaderSpec:
            (track=TrackSpec)? (channel=ChannelSpec)? (time=TimeSpec)? (driver='timedriven')
        ;
        NoteDrivenHeaderSpec:
            (track=TrackSpec)? (channel=ChannelSpec)? (time=TimeSpec)? (driver='notedriven')?
        ;        
        TimeSpec:
            'time' value=FLOAT
        ;        
        ChannelSpec:
            'channel' id=INT
        ;
        TrackSpec:
            'track' id=INT
        ;
        Event:
            (ks=ChordSpec | ns=NoteSpec | cs=CcSpec)
        ;
        ChordSpec:
            '<' notes+=NoteSpec '>'
        ;
        CcSpec:
            (acc=AnimatedControlChange|scc=StaticControlChange)
        ;
        Note:
            NoteName NoteModifier?
        ;
        NoteName:
            'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'r'
        ;
        NoteModifier:
            '#' | '--' | '-' | 'x'
        ;
        OneOrTwoDigits:
            Digit Digit?
        ;
        Digit:
            '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        ;
        NoteSpec:
            name=Note (octave=OneOrTwoDigits)? (invdur=UnderScoreInt)? properties*=NoteProperties  
        ;
        UnderScoreInt:
            '_' value=MyFloat dots*='.' ('*' num=INT '/' den=INT)?
        ;
        NoteProperties:
            (avol=AnimatedVol|svol=StaticVol|apdur=AnimatedPDur|spdur=StaticPDur|alag=AnimatedLag|slag=StaticLag|
             atempo=AnimatedTempo|stempo=StaticTempo|acc=AnimatedControlChange|scc=StaticControlChange)
        ;
        StaticControlChange:
            '\cc' '[' id=INT ',' value=INT ']'
        ;                                
        AnimatedControlChange:
            '\cc' '{' id=INT ',' value=INT (tweenoptions=TweenOptions)? '}'
        ;
        StaticTempo:
            '\tempo' '[' (symval=SymTempo|value=NumTempo) ']'
        ;
        AnimatedTempo:
            '\tempo' '{' (symval=SymTempo|value=NumTempo) (tweenoptions=TweenOptions)? '}' 
        ;
        NumTempo:
            value=INT
        ;                
        SymTempo:
            (symval='larghissimo' | symval='grave' | symval='lento' | symval='largho' | symval='larghetto' | 
             symval='adagissimo' | symval='adagio' | symval='adagietto' | symval='andante' | symval='andantino' | 
             symval='moderato' | symval='allegretto' | symval='allegro' | symval='vivace' | symval='allegro_vivace' | 
             symval='vivacissimo' | symval='allegro_assai' | symval='presto' | symval='prestissimo')
        ;
        StaticLag:
            '\lag' '[' value=NumLag ']'
        ;
        AnimatedLag:
            '\lag' '{' value=NumLag (tweenoptions=TweenOptions)? '}'
        ;
        NumLag:
            value=FLOAT
        ;
        StaticPDur:
            '\pdur' '[' (symval=SymPDur | value=NumPDur) ']'
        ;
        AnimatedPDur:
            '\pdur' '{' (symval=SymPDur | value=NumPDur) (tweenoptions=TweenOptions)? '}'
        ;
        NumPDur:
            value=FLOAT
        ;                                                        
        SymPDur:
            symval='staccatissimo' | symval='staccato' | symval='legatissimo' | symval='legato' | symval='normal'
        ;                                        
        StaticVol:
            '\vol' '[' (symval=SymVol|value=NumVol) ']'
        ;                                        
        AnimatedVol:
            '\vol' '{' (symval=SymVol|value=NumVol) (tweenoptions=TweenOptions)? '}'
        ;       
        TweenOptions:
            ',' (tweentype=TweenType) ','? extra_options*=MyFloat[',']
        ;
        TweenType:
            'linear' | 'easeInQuad' | 'easeOutQuad'| 'easeInOutQuad'| 'easeInCubic'| 'easeOutCubic'| 'easeInOutCubic'|
            'easeInQuart'| 'easeOutQuart'| 'easeInOutQuart'| 'easeInQuint'| 'easeOutQuint'| 'easeInOutQuint'|
            'easeInSine'| 'easeOutSine'| 'easeInOutSine'| 'easeInExpo'| 'easeOutExpo'| 'easeInOutExpo'|
            'easeInCirc'| 'easeOutCirc'| 'easeInOutCirc'| 'easeInBounce'| 'easeOutBounce'| 'easeInOutBounce'|
            'easeInElastic'| 'easeOutElastic'| 'easeInOutElastic'| 'easeInBack'| 'easeOutBack'| 'easeInOutBack'
        ;
        NumVol:
            value=INT
        ;
        SymVol:
            symval='ppppp' | symval='pppp' | symval='ppp' | symval='pp' | symval='p' | symval='mp' | symval='mf' | 
            symval='ffff' | symval='fff' | symval='ff' | symval='f'  
        ;
        MyFloat:
            /\d+(\.\d+)?/
        ;
        Comment:
            /\/\/.*$/ |
            /\/\*(.|\n)*?\*\//
        ;
        """
        self.mm = metamodel_from_str(self.grammar, match_filters={'MyFloat': lambda x: float(x)}, ws="' '\n\t'|'")
        self.last_octave = Defaults.octave
        self.last_duration = 1 / Defaults.dur
        self.last_dynamic = ('num', 'static', Defaults.vol)
        self.last_lag = ('num', 'static', Defaults.lag)
        self.last_pdur = ('num', 'static', Defaults.playeddur)
        self.last_tempo = ('num', 'static', Defaults.tempo)
        self.last_cc = defaultdict(lambda: None)

    def parse(self, thestring):
        self.model = self.mm.model_from_str(thestring)
        return self.model

    def get_no_of_sections(self):
        if self.model.sections:
            return len(self.model.sections)
        return 0

    def section(self, section_id):
        if self.model.sections is None:
            raise ValidationException("Fatal Error! Expected sections to be defined.")
        if (len(self.model.sections) <= section_id):
            raise ValidationException(f"Fatal Error! Trying to access non-existing section {section_id}")
        return self.model.sections[section_id]

    def track_for_section(self, section_id):
        section = self.section(section_id)
        if section.headerspecs.track is None:
            return 0
        return int(section.headerspecs.track.id)

    def channel_for_section(self, section_id):
        section = self.section(section_id)
        if section.headerspecs.channel is None:
            return 0
        return int(section.headerspecs.channel.id)

    def time_for_section(self, section_id):
        section = self.section(section_id)
        if section.headerspecs.time is None:
            return 0
        return section.headerspecs.time.value

    def driver_for_section(self, section_id):
        section = self.section(section_id)
        if not section.headerspecs.driver:
            return 'notedriven'
        return section.headerspecs.driver

    def events_for_section(self, section_id):
        section = self.section(section_id)
        return section.events

    def name_for_notespec(self, notespec):
        if notespec is None:
            raise ValidationException("Fatal Error! Asking name only makes sense for note events.")
        if notespec.name is None:
            raise ValidationException("Fatal Error! Note needs a name.")
        return notespec.name

    def octave_for_notespec(self, notespec):
        if notespec.octave is None:
            return self.last_octave
        if notespec.name != "r":
            self.last_octave = notespec.octave
        return self.last_octave

    def duration_for_notespec(self, notespec):
        if notespec.invdur is None:
            return self.last_duration
        if notespec.invdur.value is None:
            return self.last_duration
        duration = notespec.invdur.value
        if notespec.invdur.dots:
            numdots = len(notespec.invdur.dots)
            duration = 1 / ((1 / duration) * (2 - 1 / pow(2, numdots)))
        multiplier = 1
        if notespec.invdur.num and notespec.invdur.den:
            multiplier = notespec.invdur.num / notespec.invdur.den
        self.last_duration = duration * multiplier
        return self.last_duration

    def notes_for_section(self, section_id):
        section = self.section(section_id)
        driver = self.driver_for_section(section_id)
        if driver != 'notedriven':
            raise ValidationException("Fatal Error! notes can only be specified in notedriven track")
        notes = []
        for event in self.events_for_section(section_id):
            if event.cs is not None:
                raise ValidationException(
                    "Fatal Error! in note driven sections, control changes must be attached to notes")
            if event.ns is None and event.ks is None:
                raise ValidationException("Fatal Error! Expected a NoteSpec or a ChordSpec.")
            if event.ns:
                name = self.name_for_notespec(event.ns)
                octave = self.octave_for_notespec(event.ns)
                if name == "r":
                    notes.append(f"{name}")
                else:
                    notes.append(f"{name}{octave}")
            elif event.ks:
                chordnotes = []
                for note in event.ks.notes:
                    name = self.name_for_notespec(note)
                    octave = self.octave_for_notespec(note)
                    if name == "r":
                        assert ValidationException("Fatal Error! No rests allowed inside chords.")
                    else:
                        chordnotes.append(f"{name}{octave}")
                notes.append(Pchord(chordnotes))
        return notes

    def note_generator_for_section(self, section_id):
        return Pseq(self.notes_for_section(section_id), 1)

    def durations_for_section(self, section_id):
        section = self.section(section_id)
        driver = self.driver_for_section(section_id)
        if driver != 'notedriven':
            raise ValidationException("Fatal Error! durations can only be specified in notedriven track")
        durations = []
        for event in self.events_for_section(section_id):
            if event.cs is not None:
                raise ValidationException(
                    "Fatal Error! in note driven sections, control changes must be attached to notes")
            if event.ns is None and event.ks is None:
                raise ValidationException(f"Fatal Error! Expected a NoteSpec/ChordSpec {event}")

            if event.ns:
                notespec = event.ns
            elif event.ks:
                notespec = event.ks.notes[0]
            duration = self.duration_for_notespec(notespec)
            durations.append(1 / duration)

        return durations

    def duration_generator_for_section(self, section_id):
        return Pseq(self.durations_for_section(section_id), 1)

    def cc_properties_for_section(self, section_id):
        section = self.section(section_id)
        driver = self.driver_for_section(section_id)
        if driver != 'notedriven':
            raise ValidationException("Fatal Error! cc_properties_for_section only makes sense in notedriven track")
        cc_properties = defaultdict(list)
        cc_count_since_previous_event = defaultdict(lambda: 0)
        for event in self.events_for_section(section_id):
            if event.cs is not None:
                raise ValidationException(
                    f"Fatal Error! cc_properties_for_section extracts from note and chordspecs only {event}")
            if event.ns is None and event.ks is None:
                raise ValidationException(f"Fatal Error! Expected a NoteSpec/ChordSpec {event}")
            if event.ns:
                notespec = event.ns
            elif event.ks:
                notespec = event.ks.notes[0]
            else:
                continue
            for p in notespec.properties:
                if p.acc is not None:
                    ccid = p.acc.id
                    ccval = p.acc.value
                    prop = ('num', 'anim', ccval)
                    cc_properties[ccid].append((self.last_cc[ccid], prop, cc_count_since_previous_event[ccid]))
                    self.last_cc[ccid] = prop
                    cc_count_since_previous_event[ccid] = 0
                elif p.scc is not None:
                    ccid = p.scc.id
                    ccval = p.scc.value
                    prop = ('num', 'static', ccval)
                    cc_properties[ccid].append((self.last_cc[ccid], prop, cc_count_since_previous_event[ccid]))
                    self.last_cc[ccid] = prop
                    cc_count_since_previous_event[ccid] = 0
            for i in range(NO_OF_CONTROLLERS):
                cc_count_since_previous_event[i] += 1
        for key in cc_properties:
            cc_properties[key].append((self.last_cc[key], self.last_cc[key], cc_count_since_previous_event[key]))

        return cc_properties

    def cc_properties_generators_for_section(self, section_id):
        cc_properties = self.cc_properties_for_section(section_id)
        patterns = defaultdict(lambda: defaultdict(list))
        for cc in cc_properties:
            delay = 0
            note_durations = self.duration_generator_for_section(section_id)
            for segment in cc_properties[cc]:
                frm = segment[0]
                to = segment[1]
                durkey = PP.CtrlDurKey(cc)
                valkey = PP.CtrlValKey(cc)
                if segment[0] is None:
                    no_of_notes = int(segment[2])
                    dur = sum(take(no_of_notes, note_durations))
                    patterns[cc][durkey].append(Pconst(dur, 1))
                    patterns[cc][valkey].append(Pconst(None, 1))
                else:
                    no_of_notes = int(segment[2])
                    dur = sum(take(no_of_notes, note_durations))
                    if frm[1] == "anim":
                        n = NumberAnimation(frm=int(frm[2]), to=int(to[2]))
                        patterns[cc][durkey].append(Pconst(0.1 * dur / no_of_notes, int(no_of_notes / 0.1)))
                        patterns[cc][valkey].append(Ptween(n, 0, 0, int(no_of_notes / 0.1), int(no_of_notes / 0.1)))
                    elif frm[1] == "static":
                        patterns[cc][durkey].append(Pconst(dur, 1))
                        patterns[cc][valkey].append(Pconst(int(frm[2]), 1))
                    else:
                        raise ValidationException(f"Fatal Error. Unknown animation type {frm}")
        return patterns

    def extract_extra_tween_options(self, animatedproperty):
        if animatedproperty.tweenoptions is not None:
            tweentype = [animatedproperty.tweenoptions.tweentype]
            if animatedproperty.tweenoptions.extra_options:
                tweentype.extend(animatedproperty.tweenoptions.extra_options)
            return tweentype
        return None

    def extract_dynamics(self, notespec):
        for p in notespec.properties:
            if p.avol is not None:
                tweenoptions = self.extract_extra_tween_options(p.avol)
                if p.avol.symval is not None:
                    if tweenoptions is not None:
                        return "sym", "anim", p.avol.symval.symval, tweenoptions
                    else:
                        return "sym", "anim", p.avol.symval.symval
                elif p.avol.value is not None:
                    if tweenoptions is not None:
                        return "num", "anim", p.avol.value.value, tweenoptions
                    else:
                        return "num", "anim", p.avol.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand animated dynamics specification {p.avol}")
            elif p.svol is not None:
                if p.svol.symval is not None:
                    return "sym", "static", p.svol.symval.symval
                elif p.svol.value is not None:
                    return "num", "static", p.svol.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand static dynamics specification {p.svol}")
        return None

    def extract_pdur(self, notespec):
        for p in notespec.properties:
            if p.apdur is not None:
                tweenoptions = self.extract_extra_tween_options(p.apdur)
                if p.apdur.symval is not None:
                    if tweenoptions is not None:
                        return "sym", "anim", p.apdur.symval.symval, tweenoptions
                    else:
                        return "sym", "anim", p.apdur.symval.symval
                elif p.apdur.value is not None:
                    if tweenoptions is not None:
                        return "num", "anim", p.apdur.value.value, tweenoptions
                    else:
                        return "num", "anim", p.apdur.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand animated pdur specification {p.apdur}")
            elif p.spdur is not None:
                if p.spdur.symval is not None:
                    return "sym", "static", p.spdur.symval.symval
                elif p.spdur.value is not None:
                    return "num", "static", p.spdur.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand static pdur specification {p.spdur}")
        return None

    def extract_tempo(self, notespec):
        for p in notespec.properties:
            if p.atempo is not None:
                tweenoptions = self.extract_extra_tween_options(p.atempo)
                if p.atempo.symval is not None:
                    if tweenoptions is not None:
                        return "sym", "anim", p.atempo.symval.symval, tweenoptions
                    else:
                        return "sym", "anim", p.atempo.symval.symval
                elif p.atempo.value is not None:
                    if tweenoptions is not None:
                        return "num", "anim", p.atempo.value.value, tweenoptions
                    else:
                        return "num", "anim", p.atempo.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand animated pdur specification {p.atempo}")
            elif p.stempo is not None:
                if p.stempo.symval is not None:
                    return "sym", "static", p.stempo.symval.symval
                elif p.stempo.value is not None:
                    return "num", "static", p.stempo.value.value
                else:
                    raise ValidationException(f"Fatal! Couldn't understand static pdur specification {p.stempo}")
        return None

    def extract_lag(self, notespec):
        for p in notespec.properties:
            if p.alag is not None:
                tweenoptions = self.extract_extra_tween_options(p.alag)
                if p.alag.value is not None:
                    if tweenoptions is not None:
                        return "num", "anim", p.alag.value.value, tweenoptions
                    else:
                        return "num", "anim", p.alag.value.value
            elif p.slag is not None:
                if p.slag.value is not None:
                    return "num", "static", p.slag.value.value
        return None

    def property_for_section(self, section_id, property_from_notespec_fn, default_value):
        """
        :param section_id:
        :return: list of (from_property, to_property, distance)
                    where from_property and to_property correspond to ('num' or 'sym', 'anim' or 'static', distance)
        """
        section = self.section(section_id)
        driver = self.driver_for_section(section_id)
        properties = []
        count_since_previous_event = 0
        for event in self.events_for_section(section_id):
            if event.ns:
                notespec = event.ns
            elif event.ks:
                notespec = event.ks.notes[0]
            else:
                continue
            prop = property_from_notespec_fn(notespec)
            if prop is not None:
                properties.append((default_value, prop, count_since_previous_event))
                default_value = prop
                count_since_previous_event = 0
            count_since_previous_event += 1
        properties.append((default_value, default_value, count_since_previous_event))
        return properties

    def property_generator_for_section(self, section_id, symvalue_from_string_fn, property_from_notespec_fn,
                                       default_value):
        dynamics = self.property_for_section(section_id, property_from_notespec_fn, default_value)
        patterns = []
        for d in dynamics:
            frm_dyn = d[0]
            to_dyn = d[1]
            distance = d[2]
            try:
                tweenoptions = d[0][3]
            except IndexError:
                tweenoptions = ['linear']
            if distance:
                from_value_type = frm_dyn[0]
                if from_value_type == 'sym':
                    from_value = symvalue_from_string_fn(frm_dyn[2])
                else:
                    from_value = frm_dyn[2]
                to_value_type = to_dyn[0]
                if to_value_type == 'sym':
                    to_value = symvalue_from_string_fn(to_dyn[2])
                else:
                    to_value = to_dyn[2]
                animation_type = frm_dyn[1]
                if animation_type == 'anim':
                    n = Ptween(NumberAnimation(frm=from_value, to=to_value, tween=tweenoptions), 0, 0, distance,
                               distance,
                               None)
                elif animation_type == 'static':
                    n = Ptween(NumberAnimation(frm=from_value, to=from_value, tween=['linear']), 0, 0, distance,
                               distance, None)
                else:
                    print(animation_type)
                    assert False
                patterns.append(n)
        return Pseq(patterns, 1)

    def dynamics_for_section(self, section_id):
        """
        :param section_id:
        :return: list of (fromdynamic, todynamic, distance)
                    where fromdynamic and todynamic correspond to ('num' or 'sym', 'anim' or 'static', distance)
        """
        return self.property_for_section(section_id, self.extract_dynamics, self.last_dynamic)

    def dynamics_generator_for_section(self, section_id):
        return self.property_generator_for_section(section_id, Dyn.from_string, self.extract_dynamics,
                                                   self.last_dynamic)

    def lag_for_section(self, section_id):
        """
        :param section_id:
        :return: list of (fromlag, tolag, distance)
                    where fromlag and tolag correspond to ('num' or 'sym', 'anim' or 'static', distance)
        """
        return self.property_for_section(section_id, self.extract_lag, self.last_lag)

    def lag_generator_for_section(self, section_id):
        return self.property_generator_for_section(section_id, None, self.extract_lag, self.last_lag)

    def pdur_for_section(self, section_id):
        return self.property_for_section(section_id, self.extract_pdur, self.last_pdur)

    def pdur_generator_for_section(self, section_id):
        return self.property_generator_for_section(section_id, PDur.from_string, self.extract_pdur, self.last_pdur)

    def tempo_for_section(self, section_id):
        return self.property_for_section(section_id, self.extract_tempo, self.last_tempo)

    def tempo_generator_for_section(self, section_id):
        return self.property_generator_for_section(section_id, Tempo.from_string, self.extract_tempo, self.last_tempo)

    def phrase_properties_for_section(self, section_id):
        pp = {
            PP.NOTE: self.note_generator_for_section(section_id),
            PP.VOL: self.dynamics_generator_for_section(section_id),
            PP.DUR: self.duration_generator_for_section(section_id),
            PP.PLAYEDDUR: self.pdur_generator_for_section(section_id),
            PP.LAG: self.lag_generator_for_section(section_id),
            PP.TEMPO: self.tempo_generator_for_section(section_id)
        }

        ccs = self.cc_properties_generators_for_section(section_id)
        for key in ccs:
            pp[PP.CtrlDurKey(key)] = Pseq(ccs[key][PP.CtrlDurKey(key)], 1)
            pp[PP.CtrlValKey(key)] = Pseq(ccs[key][PP.CtrlValKey(key)], 1)

        return pp

    def phrase_for_section(self, section_id):
        return Phrase(self.phrase_properties_for_section(section_id))

    def get_of_tracks(self):
        no_of_sections = self.get_no_of_sections()
        tracks = set([])
        for section_id in range(no_of_sections):
            tracks.add(self.track_for_section(section_id))
        return len(tracks)

    def add_to_pattern2midi(self, pattern2midi):
        for s in range(self.get_no_of_sections()):
            pattern2midi.add_phrase(self.phrase_for_section(s), self.track_for_section(s), self.channel_for_section(s),
                                    self.time_for_section(s))
