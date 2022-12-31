from mido import MidiFile



class MIDI_EVENTS:
    on = "on"
    off = "off"

class MidiEvent:
    def __init__(self, event, note, velocity, tick):
        self.event = event
        self.note = note
        self.velocity = velocity
        self.tick = tick

    def __str__(self) -> str:
        return '{' + f'event: {self.event}, note: {self.note}, velocity: {self.velocity}, tick: {self.tick}' \
        + '}'


# mid = MidiFile('test.mid')
# midi_events = []
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         if msg.type == 'note_on':
#             event = MidiEvent(MIDI_EVENTS.on, msg.note, velocity=msg.velocity, tick=msg.time)
#             midi_events.append(event)
#         elif msg.type == 'note_off':
#             event = MidiEvent(MIDI_EVENTS.off, msg.note, velocity=msg.velocity, tick=msg.time)
#             midi_events.append(event)

# for e in midi_events:
#     print(e)

# def relative_2_abolute(events: list[MidiEvent]):
#     _midi_events = list(events)
#     current_tick = 0
#     for e in _midi_events:
#         tmp_tick = e.tick
#         e.tick = current_tick
#         current_tick += tmp_tick 
#     return _midi_events

# abs_ev = relative_2_abolute(midi_events)

# for e in abs_ev:
#     print(e)

def convert_midi_file(filename):
    mid = MidiFile(filename)
    midi_events = []

    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            if msg.type == 'note_on':
                event = MidiEvent(MIDI_EVENTS.on, msg.note, velocity=msg.velocity, tick=msg.time)
                midi_events.append(event)
            elif msg.type == 'note_off':
                event = MidiEvent(MIDI_EVENTS.off, msg.note, velocity=msg.velocity, tick=msg.time)
                midi_events.append(event)

    def relative_2_abolute(events: list[MidiEvent]):
        _midi_events = list(events)
        current_tick = 0
        for e in _midi_events:
            tmp_tick = e.tick
            e.tick = current_tick
            current_tick += tmp_tick 
        return _midi_events

    abs_ev = relative_2_abolute(midi_events)

    return abs_ev
