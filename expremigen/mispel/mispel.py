from textx.metamodel import metamodel_from_str
from vectortween.NumberAnimation import NumberAnimation

from expremigen.io.constants import Defaults
from expremigen.mispel.exception import ValidationException
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween


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
            (ns=NoteSpec | cs=CcSpec)
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
            '#' | 'bb' | 'b' | 'x'
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
            '_' value=FLOAT
        ;
        NoteProperties:
            (avol=AnimatedVol|svol=StaticVol|apdur=AnimatedPDur|spdur=StaticPDur|alag=AnimatedLag|slag=StaticLag|
             atempo=AnimatedTempo|stempo=StaticTempo|acc=AnimatedControlChange|scc=StaticControlChange)
        ;
        StaticControlChange:
            '\cc' '[' id=INT ',' value=INT ']'
        ;                                
        AnimatedControlChange:
            '\cc' '{' id=INT ',' value=INT '}'
        ;
        StaticTempo:
            '\tempo' '[' (symval=SymTempo|value=NumTempo) ']'
        ;
        AnimatedTempo:
            '\tempo' '{' (symval=SymTempo|value=NumTempo) '}' 
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
            '\lag' '{' value=NumLag '}'
        ;
        NumLag:
            value=FLOAT
        ;
        StaticPDur:
            '\pdur' '[' (symval=SymPDur | value=NumPDur) ']'
        ;
        AnimatedPDur:
            '\pdur' '{' (symval=SymPDur | value=NumPDur) '}'
        ;
        NumPDur:
            value=FLOAT
        ;                                                        
        SymPDur:
            'staccato' | 'legato' | 'normal'
        ;                                        
        StaticVol:
            '\vol' '[' (symval=SymVol|value=NumVol) ']'
        ;                                        
        AnimatedVol:
            '\vol' '{' (symval=SymVol|value=NumVol) '}'
        ;                                        
        NumVol:
            value=INT
        ;
        SymVol:
            symval='ppppp' | symval='pppp' | symval='ppp' | symval='pp' | symval='p' | symval='mp' | symval='mf' | 
            symval='ffff' | symval='fff' | symval='ff' | symval='f'  
        ;
        Comment:
            /\/\/.*$/ |
            /\/\*(.|\n)*?\*\//
        ;
        """
        self.mm = metamodel_from_str(self.grammar)
        self.last_octave = Defaults.octave
        self.last_duration = 1 / Defaults.dur
        self.last_dynamic = ('num', 'static', Defaults.vol)
        self.last_lag = Defaults.lag
        self.last_pdur = Defaults.playeddur

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
        return section.headerspecs.track

    def channel_for_section(self, section_id):
        section = self.section(section_id)
        if section.headerspecs.channel is None:
            return 0
        return section.headerspecs.channel

    def time_for_section(self, section_id):
        section = self.section(section_id)
        if section.headerspecs.time is None:
            return 0
        return section.headerspecs.time

    def driver_for_section(self, section_id):
        section = self.section(section_id)
        if not section.headerspecs.driver:
            return 'notedriven'
        return section.headerspecs.driver

    def events_for_section(self, section_id):
        section = self.section(section_id)
        return section.events

    def name_for_noteevent(self, event):
        if event.ns is None:
            raise ValidationException("Fatal Error! Asking name only makes sense for note events.")
        if event.ns.name is None:
            raise ValidationException("Fatal Error! Note needs a name.")
        return event.ns.name

    def octave_for_noteevent(self, event):
        if event.ns.octave is None:
            return self.last_octave
        if event.ns.name != "r":
            self.last_octave = event.ns.octave
        return self.last_octave

    def duration_for_noteevent(self, event):
        if event.ns.invdur is None:
            return self.last_duration
        if event.ns.invdur.value is None:
            return self.last_duration
        self.last_duration = event.ns.invdur.value
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
            if event.ns is None:
                raise ValidationException("Fatal Error! Expected a NoteSpec.")
            name = self.name_for_noteevent(event)
            octave = self.octave_for_noteevent(event)
            if name == "r":
                notes.append(f"{name}")
            else:
                notes.append(f"{name}{octave}")
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
            if event.ns is None:
                raise ValidationException("Fatal Error! Expected a NoteSpec.")
            duration = self.duration_for_noteevent(event)
            durations.append(duration)
        return durations

    def duration_generator_for_section(self, section_id):
        return Pseq(self.durations_for_section(section_id), 1)

    def extract_dynamics(self, event):
        for p in event.ns.properties:
            if p.avol is not None:
                if p.avol.symval is not None:
                    return "sym", "anim", p.avol.symval.symval
                elif p.avol.value is not None:
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

    def dynamics_for_section(self, section_id):
        """
        :param section_id:
        :return: list of (fromdynamic, todynamic, distance)
                    where fromdynamic and todynamic correspond to ('num' or 'sym', 'anim' or 'static', distance)
        """
        section = self.section(section_id)
        driver = self.driver_for_section(section_id)
        dynamics = []
        count_since_previous_event = 0
        for event in self.events_for_section(section_id):
            if event.ns:
                dynamic = self.extract_dynamics(event)
                if dynamic is not None:
                    dynamics.append((self.last_dynamic, dynamic, count_since_previous_event))
                    self.last_dynamic = dynamic
                    count_since_previous_event = 0
            else:
                # TODO
                pass
            count_since_previous_event += 1
        dynamics.append((self.last_dynamic, self.last_dynamic, count_since_previous_event))
        return dynamics

    def dynamics_generator_for_section(self, section_id):
        dynamics = self.dynamics_for_section(section_id)
        patterns = []
        for d in dynamics:
            frm_dyn = d[0]
            to_dyn = d[1]
            distance = d[2]
            if distance:
                from_value_type = frm_dyn[0]
                if from_value_type == 'sym':
                    from_value = Dyn.from_string(frm_dyn[2])
                else:
                    from_value = frm_dyn[2]
                to_value_type = to_dyn[0]
                if to_value_type == 'sym':
                    to_value = Dyn.from_string(to_dyn[2])
                else:
                    to_value = to_dyn[2]
                animation_type = frm_dyn[1]
                if animation_type == 'anim':
                    n = Ptween(NumberAnimation(frm=from_value, to=to_value, tween=['linear']), 0, 0, distance, distance,
                               None)
                elif animation_type == 'static':
                    n = Ptween(NumberAnimation(frm=from_value, to=from_value, tween=['linear']), 0, 0, distance,
                               distance, None)
                else:
                    print(animation_type)
                    assert False
                patterns.append(n)
        return Pseq(patterns, 1)
