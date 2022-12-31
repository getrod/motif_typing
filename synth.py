import fluidsynth
import math
import time
import asyncio
from mido import MidiFile
import numpy
import pyaudio

fs = fluidsynth.Synth()
lock = asyncio.Lock()
reset = False
ppq = 98
secondsPerMinute = 60
MAX_TICKS = ppq * 100

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

def print_midi_events(events: list[MidiEvent]):
        for event in events:
            print(event)

def activate_midi_event(midi_event):
        if midi_event.event == MIDI_EVENTS.on:
            fs.noteon(0, midi_event.note, midi_event.velocity)
        else:
            fs.noteoff(0, midi_event.note)

def start_synth():
    fs.start()
    sfid = fs.sfload(f'Nice-Steinway-Lite-v3.0.sf2')
    fs.program_select(0, sfid, 0, 0)

def find_same_tick_events(midi_events: list[MidiEvent], tick: int):
    same_tick_events = []
    while len(midi_events) != 0:
        if midi_events[0].tick == tick:
            same_tick_events.append(midi_events.pop(0))
        else: break
    return same_tick_events

def play_track(midi_events: list[MidiEvent], bpm):
    secondsPerBeat = (secondsPerMinute) / (bpm)
    seconds_per_tick = secondsPerBeat / ppq
    current_tick = 0

    # sort by tick time
    _midi_e = list(midi_events)
    _midi_e.sort(key=lambda midi_event : midi_event.tick)

    # for each tick
    while current_tick < MAX_TICKS:
        # if no more events, break
        if len(_midi_e) == 0: break

        # find ticks with same event
        same_tick_events = find_same_tick_events(_midi_e, current_tick)

        # activate midi events of current tick
        for midi_event in same_tick_events:
            activate_midi_event(midi_event)

        current_tick += 1
        print(current_tick)
        # time.sleep(seconds_per_tick)

def render_audio(midi_events: list[MidiEvent], bpm, sample_rate = 44100, ppq = 98):
    secondsPerBeat = (secondsPerMinute) / (bpm)
    seconds_per_tick = secondsPerBeat / ppq
    pa = pyaudio.PyAudio()
    strm = pa.open(
        format = pyaudio.paInt16,
        channels = 2, 
        rate = sample_rate, 
        output = True
    )
    s = []

    prev_tick = -1
    current_tick = 0

    # sort by tick
    midi_events.sort(key=lambda midi_event : midi_event.tick)

    while len(midi_events) != 0:
        # find the first tick value that is greater than prev_tick 
        for i in range(0, len(midi_events)):
            if midi_events[i].tick > prev_tick:
                current_tick = midi_events[i].tick 
                break
        if prev_tick < 0: prev_tick = 0
        
        # find all events in the current_tick
        same_tick_events = []
        while len(midi_events) != 0:
            if midi_events[0].tick == current_tick:
                same_tick_events.append(midi_events.pop(0))
            else: break

        # render audio
        s = numpy.append(s, fs.get_samples(math.floor(sample_rate * seconds_per_tick * (current_tick - prev_tick))))

        # activate midi events of current tick
        for midi_event in same_tick_events:
            activate_midi_event(midi_event)

        prev_tick = current_tick
    
    # End with silence 1 second
    s = numpy.append(s, fs.get_samples(sample_rate * 1))
    samps = fluidsynth.raw_audio_string(s)
    strm.write(samps)
        

async def set_reset(val: bool):
    global reset
    async with lock:
        reset = val

async def get_reset():
    async with lock:
        return reset

async def play_track_async(midi_events: list[MidiEvent], bpm):
    secondsPerBeat = (secondsPerMinute) / (bpm)
    seconds_per_tick = secondsPerBeat / ppq
    current_tick = 0

    # sort by tick time
    _midi_e = list(midi_events)
    _midi_e.sort(key=lambda midi_event : midi_event.tick)

    # for each tick
    while current_tick < MAX_TICKS:
        # if no more events, break
        if len(_midi_e) == 0: break

        # if user resets, break loop
        async with lock:
            if reset == True:
                break

        # find ticks with same event
        same_tick_events = find_same_tick_events(_midi_e, current_tick)

        # activate midi events of current tick
        for midi_event in same_tick_events:
            activate_midi_event(midi_event)

        current_tick += 1
        await asyncio.sleep(seconds_per_tick)
    
    await set_reset(False)


def tick_2_beat(mid: MidiFile, tick: int):
    if tick == 0: return 0
    print(mid.ticks_per_beat)
    return tick / mid.ticks_per_beat

def convert_midi_file(filename):
    mid = MidiFile(filename)
    midi_events = []

    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                event = MidiEvent(MIDI_EVENTS.on, msg.note, velocity=msg.velocity, tick=msg.time)
                midi_events.append(event)
            elif msg.type == 'note_off':
                event = MidiEvent(MIDI_EVENTS.off, msg.note, velocity=msg.velocity, tick=msg.time)
                midi_events.append(event)
    print_midi_events(midi_events)

    def relative_2_abolute(events: list[MidiEvent]):
        _midi_events = list(events)
        current_tick = 0
        for e in _midi_events:
            current_tick += e.tick 
            e.tick = current_tick
            
        return _midi_events

    print()
    
    abs_ev = relative_2_abolute(midi_events)
    print_midi_events(midi_events)
    # convert tick to beat
    for e in abs_ev:
        e.tick = tick_2_beat(mid, e.tick) * ppq

    return abs_ev



midi_events = [
    MidiEvent(MIDI_EVENTS.on, 70, 127, 0),
    MidiEvent(MIDI_EVENTS.on, 74, 127, 0),
    MidiEvent(MIDI_EVENTS.off, 74, 127, ppq),
    MidiEvent(MIDI_EVENTS.on, 77, 127, 0),
    
    MidiEvent(MIDI_EVENTS.off, 70, 127, ppq),
    
    MidiEvent(MIDI_EVENTS.off, 77, 127, ppq),
]

start_synth()


midi_events = convert_midi_file('test.mid')
# print()
# print_midi_events(midi_events)

render_audio(midi_events, 140)


# start_synth()
# play_track(midi_events, 60)
# print('terminate')

# # asyncio.run(play_track_async(midi_events, 128))

# keep script alive
async def loop():
    try:
        while True:
            x = input()
            if x == 's': 
                await set_reset(True)
                print('reset is now true')
            elif x == 'p':
                print('reset: ' + str(await get_reset()))
            time.sleep(1)
    except KeyboardInterrupt:
        print('')

asyncio.run(loop())