class MidiControlChanges:
    """
    list of midi control change messages
    """
    BankSelect = 0  # Bank Select Allows user to switch bank for patch selection.Program change used with
    # Bank Select. MIDI can access 16384 patches per MIDI channel.

    Modulation = 1  # Generally this CC controls a vibrato effect(pitch, loudness, brighness).What is modulated is
    # based n the patch.

    BreathController = 2  # Often times associated with aftertouch messages.It was originally intended for use with a
    # breath MIDI controller in which blowing harder produced higher MIDI control values.
    # It can be used for modulation as well.

    FootController = 4  # Often used with aftertouch messages.It can send a continuous stream of values based on how
    # the pedal is used.

    PortamentoTime = 5  # Controls portamento rate to slide between 2 notes played subsequently

    DataEntry = 6  # Data Entry Most Significant Bit(MSB) Controls Value for NRPN or RPN parameters.

    Volume = 7  # the volume of the channel

    Balance = 8  # Balance Controls the left and right balance, generally for stereo patches.
    # 0 = hard left, 64 = center, 127 = hard right

    Pan = 10  # Pan Controls the left and right balance, generally for mono patches.
    # 0 = hard left, 64 = center, 127 = hard right

    Expression = 11  # Expression is a percentage of volume(CC7).

    EffectController1 = 12  # Effect Controller. Usually used to control a parameter of an effect within the
    # synth / workstation.
    EffectController2 = 13  # Usually used to control a parameter of an effect within the synth / workstation.

    GeneralPurpose1 = 16  # General purpose MIDI CC

    GeneralPurpose2 = 17  # General purpose MIDI CC

    GeneralPurpose3 = 18  # General purpose MIDI CC

    GeneralPurpose4 = 19  # General purpose MIDI CC

    Controller0LSb = 32  # Least Significant Bit (LSB)
    Controller1LSb = 33  # Least Significant Bit (LSB)
    Controller2LSb = 34  # Least Significant Bit (LSB)
    Controller3LSb = 35  # Least Significant Bit (LSB)
    Controller4LSb = 36  # Least Significant Bit (LSB)
    Controller5LSb = 37  # Least Significant Bit (LSB)
    Controller6LSb = 38  # Least Significant Bit (LSB)
    Controller7LSb = 39  # Least Significant Bit (LSB)
    Controller8LSb = 40  # Least Significant Bit (LSB)
    Controller9LSb = 41  # Least Significant Bit (LSB)
    Controller10LSb = 42  # Least Significant Bit (LSB)
    Controller11LSb = 43  # Least Significant Bit (LSB)
    Controller12LSb = 44  # Least Significant Bit (LSB)
    Controller13LSb = 45  # Least Significant Bit (LSB)
    Controller14LSb = 46  # Least Significant Bit (LSB)
    Controller15LSb = 47  # Least Significant Bit (LSB)
    Controller16LSb = 48  # Least Significant Bit (LSB)
    Controller17LSb = 49  # Least Significant Bit (LSB)
    Controller18LSb = 50  # Least Significant Bit (LSB)
    Controller19LSb = 51  # Least Significant Bit (LSB)
    Controller20LSb = 52  # Least Significant Bit (LSB)
    Controller21LSb = 53  # Least Significant Bit (LSB)
    Controller22LSb = 54  # Least Significant Bit (LSB)
    Controller23LSb = 55  # Least Significant Bit (LSB)
    Controller24LSb = 56  # Least Significant Bit (LSB)
    Controller25LSb = 57  # Least Significant Bit (LSB)
    Controller26LSb = 58  # Least Significant Bit (LSB)
    Controller27LSb = 59  # Least Significant Bit (LSB)
    Controller28LSb = 60  # Least Significant Bit (LSB)
    Controller29LSb = 61  # Least Significant Bit (LSB)
    Controller30LSb = 62  # Least Significant Bit (LSB)
    Controller31LSb = 63  # Least Significant Bit (LSB)

    Damper = 64  # Damper Pedal / Sustain Pedal On / Off switch that controls sustain.(See also Sostenuto CC 66)
    # 0 to 63 = Off, 64 to 127 = On

    Portamento = 65  # Portamento On / Off Switch On / Off switch 0 to 63 = Off, 64 to 127 = On

    Sostenuto = 66  # Sostenuto On / Off Switch On / Off switch – Like the Sustain controller(CC 64), However it
    # only holds notes that were “On” when the pedal was pressed.People use it to “hold” chords”
    # and play melodies over the held chord. 0 to 63 = Off, 64 to 127 = On

    SoftPedal = 67  # Soft Pedal On / Off Switch On / Off switch - Lowers the volume of notes played.
    # 0 to 63 = Off, 64 to 127 = On

    Legato = 68  # Legato FootSwitch On / Off switch - Turns Legato effect between 2 subsequent notes
    # On or Off. 0 to 63 = Off, 64 to 127 = On

    Hold = 69  # Hold 2 Another way to “hold notes” (see MIDI CC 64 and MIDI CC 66).However notes fade out
    # according to their release parameter rather than when the pedal is released.

    SoundController1 = 70  # Sound Controller 1 Usually controls the way a sound is produced.Default = Sound Variation.

    SoundController2 = 71  # Sound Controller 2 Allows shaping the Voltage Controlled Filter(VCF).
    # Default = Resonance - also(Timbre or Harmonics)
    SoundController3 = 72  # Sound Controller 3 Controls release time of the Voltage controlled Amplifier(VCA).
    # Default = Release Time.
    SoundController4 = 73  # Sound Controller 4 Controls the “Attack’ of a sound.The attack is the amount of time it
    # takes forthe sound to reach maximum amplitude.
    SoundController5 = 74  # Sound Controller 5 Controls VCFs cutoff frequency of the filter.

    SoundController6 = 75  # Sound Controller 6 Generic – Some manufacturers may use to further shave their sounds.

    SoundController7 = 76  # Sound Controller 7 - Generic – Some manufacturers may use to further shave their sounds.

    SoundController8 = 77  # Sound Controller 8 - Generic – Some manufacturers may use to further shave their sounds.

    SoundController9 = 78  # Sound Controller 9 -  Generic – Some manufacturers may use to further shave their sounds.

    SoundController10 = 79  # Sound Controller 10 - Generic – Some manufacturers may use to further shave their sounds.

    GeneralPurpose5 = 80  # General Purpose MIDI CC Controller Generic On / Off switch 0 to 63 = Off, 64 to     127 = On

    GeneralPurpose6 = 81  # General Purpose MIDI CC Controller Generic On / Off switch 0 to 63 = Off, 64 to 127 = On

    GeneralPurpose7 = 82  # General Purpose MIDI CC Controller Generic On / Off switch 0 to 63 = Off, 64 to 127 = On

    GeneralPurpose8 = 83  # General Purpose MIDI CC Controller Generic On / Off switch 0 to 63 = Off, 64 to 127 = On

    PortamentoCCControl = 84  # Controls the amount of Portamento.

    Effect1 = 91  # Effect 1 Depth Usually controls reverb send amount
    Effect2 = 92  # Effect 2 Depth Usually controls tremolo
    Effect3 = 93  # Effect 3 Depth Usually controls chorus amount
    Effect4 = 94  # Depth Usually controls detune amount MIDI CC 95
    Effect5 = 95  # Effect 5 Depth Usually controls phaser amount

    DataIncrement = 97  # Data Increment Usually tested to increment data for RPN and NRPN messages.
    DataDecrement = 96  # Usually used to decrement data for RPN and NRPN messages.

    NRNNoneRegParamLSB = 98  # Non - Registered Parameter Number LSB(NRPN) For controllers 6, 38, 96, and 97,
    # it selects the NRPN parameter.
    NRPNNonRegParamMSB = 99  # Non - Registered Parameter Number MSB(NRPN) For controllers 6, 38, 96, and 97,
    # it selects the NRPN parameter.

    ReParameterNumberLSBR = 100  # For controllers 6, 38, 96, and 97, it selects     the RPN parameter.

    ReParameterNumberMSB = 101  # Registered Parameter Number MSB(RPN) For controllers

    ChannelModeMessage1 = 120  # 120 to 127 are “Channel Mode Messages.”
    AllSoundOff = 120  # All Sound Off Mutes all sounding notes.It does so regardless of release
    # time or sustain.(See MIDI CC 123)
    ResetAllControllers = 121  # reset all controllers. It will reset all controllers to their default.
    LocalOnOffSwitch = 122  # Local On / Off Switch Turns internal connection of a MIDI keyboard / workstation, etc.On
    # or if you use a computer, you will most likely want local control off to avoid notes
    #  being played twice.Once locally and twice whent the note is sent back from the computer
    # to your keyboard.
    AllNotes = 123  # Off Mutes all sounding notes.Release time will still be maintained, and notes held sustain
    # will not turn off until sustain pedal is depressed.
    OmniMode = 124  # 1Omni Mode Off Sets to “Omni Off” mode. MIDI CC
    OmonModeOnSets = 125  # 125 Omni Mode On Sets to “Omni On” mode
    MonoModeMode = 126  # Mono Mode Sets device mode to Monophonic.
    PolyMode = 127  # Poly Mode Sets device mode to Polyphonic.

    PitchWheel = 128  # Own addition...
