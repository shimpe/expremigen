# Expremigen
Expremigen is an **expre**ssive **mi**di **gen**eration library

For quite a while I've been searching for a library that allows 
generation of expressive midi information. With expressive I mean that 
it should allow generating midi that doesn't sound like a mechanic 
robot. My current attempt is to make this possible by incorporating a 
way of animating midi properties over time. 

Expremigen models music as a collection of phrases. Within such a 
phrase you can specify and/or animate:
 * note values (melody, harmony)
 * durations (rhythm)
 * played durations (legato versus staccato) 
 * lag (rubato), 
 * volume (pppp to fffff, crescendo, decrescendo)
 * tempo (rallentando, accelerando)
 * midi control changes and pitchbend
 
Specification of properties like note values or durations is done 
using a library of patterns. Each pattern can generate numbers
according to its specifications. Patterns internallly use python 
generators to avoid memory and time explosion when you specify 
patterns with very large repeat values. These patterns are modeled 
after the more or less equivalent concept in [supercollider](http://supercollider.github.io/) and [isobar](https://github.com/ideoforms/isobar). Compared to isobar in particular, the patterns in expremigen are written in python 3, and heavily based on generators, which allows things like expressing patterns of very long lengths without blowing up the required time and memory space. 

Animations of properties are implemented by leveraging an
animation library [pyvectortween](https://github.com/shimpe/pyvectortween) which has ample possibilities for 
specifying and combining advanced animations, and enrich them with 
all kinds of tweening and noise functions for maximum expressive 
results. A special pattern called Ptween applies the animations 
calculated by pyvectortween to the midi properties generated by 
patterns.

# Dependencies
To get the most out of this library you will need to install [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil) (pip), [textX](https://github.com/igordejanovic/textX) (pip) and [pyvectortween](https://github.com/shimpe/pyvectortween) (available on github only for now).

# Getting started: MISPEL
Probably the easiest way to get started with expremigen is to use its domain specific **MI**di **SPE**cification **L**anguage, mispel. Mispel syntax reuses ideas from [lilypond](http://lilypond.org/), [abc notation](http://abcnotation.com/) and [music21](http://web.mit.edu/music21/)'s [tinynotation](http://web.mit.edu/music21/doc/moduleReference/moduleTinyNotation.html). A mispel based program could look as follows:
 
 ```python
from expremigen.io.pat2midi import Pat2Midi
from expremigen.mispel.mispel import Mispel

outputfile = "output/example_readme.mid"

def make_midi():
    m = Mispel()
    m.parse(r"""
    with track 0 channel 0:
        c4_16\vol{p} e g c5 b4 g f d c_4 r\vol{ff}

    with track 1 channel 1:
        <c3_4\vol[mp] e3 g> <b2\vol[f] d3 g> <c3_2\vol[mf] e g c4>
    """)
    p2m = Pat2Midi(m.get_no_of_tracks())
    m.add_to_pattern2midi(p2m)
    p2m.write(outputfile)

if __name__ == "__main__":
    make_midi()
```

This program generates a midi file containing two tracks on two different midi channels. The first track plays a crescendo arpeggio and the second track specifies three chords.

## Specifying notes and rhythms
* As you can see you specify events in the form of notenames with octave numbers, e.g. a4 is a "la" in octave 4 (typically 440Hz). Acceptable note names are a, b, c, d, e, f, g, and r for a rest.
 
* Sharps are indicated with #, e.g. ```a#```, double sharps with x, e.g. ```cx```, flats with -, e.g. ```e-``` and double flats with --, e.g. ```g--```.

* To make chords, put notes in angular brackets: ```<a4_8 c# e>```. The properties of the first note in the chord are used for the whole chord. Properties other than note name and octave attached to the second and later notes are discarded.

* Rhythm is indicated by using underscore and an (inverse) duration in beats, e.g. _16 means a sixteenth note. You can add one or more dots to indicate a dotted rhythm, e.g. ```d#3_8.``` is a "d sharp" in octave 3 with a length of one eighth plus one sixteenth. 
 
 ## Adding expressivity
 * To the notes you can add properties. The main difference between mispel and other midi domain specific languages (like [skini](https://ccrma.stanford.edu/software/stk/skini.html), [alda](https://github.com/alda-lang/alda), [semitone](https://github.com/benwbooth/semitone), [micromidi](https://github.com/arirusso/micromidi)) is the combination of a fairly concise syntax with an easy to use built-in property animation system. 
 
 * Properties in *curly braces* ```\property{}``` are *animated* from this occurrence of the property to the next. In track 0 in the example above, the volume will be animated from p to ff (*crescendo*). 
 
 * Properties in *square braces* ```\property[]``` keep a *constant* value until the next property of the same kind is encountered. 
 
 * The properties you can specify are:
   * **vol** for volume - can be ppppp to ffff or an integer between 0-127
   * **pdur** for played duration - can be staccatissimo, staccato, normal, legato or legatissimo, or a number. The number is interpreted as a multiplier with which to multiply the specified duration. E.g. number 0.1 would specify staccatissimo and number 1 would specify legato.
   * **lag** for lag. Lag is a numeric value (where 1 stands for a full beat). By animating lag you can create a convincing rubato.
   * **tempo** by animating tempo you can speed up or slow down (accelerando and ritardando)
   * **cc** midi control changes. These are specified using two parameters, e.g. \cc{15, 100} specifies that midi control change for controller 15 should be set to 100 and this value will be animated until the next midi control change for controller 15 is encountered. Midi control changes are animated with a higher time resolution than individual notes meaning you can perfectly animate control message values between one long note and the next note.
     * *NOTE:* **pitchbend** in midi is not specified using a control change message, but in mispel it is. Just use controller value 128.
 * Vectortween also allows to specifying tweening options and noise function options. Only the tweening options are exposed in mispel, so if you wanted to get fancy you could write an animation like 
 ```
 with track 0 channel 0:
        c4_16\vol{p, easeOutElastic, 30, 0.1} e g c5 b4 g f d c_4 r\vol{ff}
  ```
 * The supported tweening options are (see [this picture](http://easings.net/nl)) for a graphical display of what these mean:
   * linear, 
   * easeInQuad, easeOutQuad,easeInOutQuad,
   * easeInCubic,easeOutCubic,easeInOutCubic,
   * easeInQuart,easeOutQuart,easeInOutQuart,
   * easeInQuint,easeOutQuint,easeInOutQuint,
   * easeInSine,easeOutSine,easeInOutSine,
   * easeInExpo,easeOutExpo,easeInOutExpo,
   * easeInCirc,easeOutCirc,easeInOutCirc,
   * easeInBounce,easeOutBounce,easeInOutBounce,
   * easeInElastic,easeOutElastic,easeInOutElastic (these require two extra float parameters: amplitude and damping)
   * easeInBack,easeOutBack,easeInOutBack (these require one extra float parameter: damping)
## Reducing duplication
If two successive notes share the same octave you can leave out the octave in the second note. If two successive notes share the same duration, you can leave out the duration in the second notes. The following fragments are equivalent:
```python
'a4_4 b4_4 c#4_4 d#4_4 e4_1'
```
and
```python
'a4_4 b c# d# e_1'
```

# Going deeper
If you don't like mispel, or you need more power than mispel exposes, you can of course tap into the raw power of patterns. Although a typical pattern-based expremigen program may look a bit daunting at first, it's actually quite simple. In a typical use case, you will concatenate phrases into a piece. Phrases are dictionaries containing patterns that specify the notes, the volumes, the durations, the played durations, the lag and the tempo.

The following example shows off some of the possibilities for creating
a phrase using tweened animations.

The examples folder has more things to examine. The tests folder has unit tests for a substantial part of the library.

```python
from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween
from vectortween.NumberAnimation import NumberAnimation
from vectortween.SequentialAnimation import SequentialAnimation

outputfile = "output/singlephrase.mid"

def create_phrase():
    # we will add a single phrase into a music piece
    
    # Note2Midi converts from music notation to midi numbers
    n = Note2Midi()
    # notes is a list of music notes
    notes = "c4 e4 g4 c5 b4 g4 f4 d4 c4".split(" ")
    # specify a (volume) animation that increases linearly from mp to f
    crescendo = NumberAnimation(frm=Dyn.mp, to=Dyn.f, tween=['linear'])
    # specify a (volume) animation that decreases using an easOutQuad
    # tween function from f to ppp
    decrescendo = NumberAnimation(frm=Dyn.f, to=Dyn.ppp, 
                                  tween=['easeOutQuad'])                                
    # Combine both animations into one swell_dim animation.
    # Note that animations do not specify start and stop times
    # as these are specified in Ptween.
    # Animations are abstract descriptions of behavior,
    # not bound to time and can easily be reused in different 
    # contexts or easily combined into SequentialAnimations.
    # Animations automatically stretch over the 
    # number of events they encompass as specified in Ptween
    swell_dim = SequentialAnimation([crescendo, decrescendo])
    # specify an animation that will animate the playeddur
    increasing_staccato = NumberAnimation(frm=1, to=0.5)
    # specify the phrase properties
    properties = {
        # convert from note names to midi numbers
        # Pseq is a pattern that generates notes one by one from a list
        PP.NOTE: Pseq(n.convert2(notes)),
        # last note is longer than the rest
        # Pconst is a pattern that repeats its constant the requested number of times
        PP.DUR: Pseq([Pconst(Dur.quarter, len(notes) - 1), Pconst(Dur.whole, 1)]),
        # animate staccato
        # Ptween is a pattern that animates values over time as specified
        # in the animation argument
        PP.PLAYEDDUR: Ptween(increasing_staccato, 0, 0, len(notes), len(notes)),
        # volume should linearly go up from mp to f, then go down from f to ppp as the phrase progresses
        PP.VOL: Ptween(swell_dim, 0, 0, len(notes), len(notes), None),
        # tempo: constant at 100 bpm
        PP.TEMPO: Pconst(100)
    }
    # with the above animated properties, build a phrase
    p = Phrase(properties)
    # take a pattern to midi object
    p2m = Pat2Midi()
    # add the phrase into the pattern to midi object
    total_dur = p2m.add_phrase(p)
    print(total_dur)
    # and write the result to midi file
    p2m.write(outputfile)


if __name__ == "__main__":
    create_phrase()
```