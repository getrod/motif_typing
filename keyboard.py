from rtmidi import (midiutil, MidiIn, midiconstants)
import sys
import time
import pyautogui
import json
from moteaf import motif_2_midi, motif_parse

# get words
json_f = open('dictionary.json')
dictionary = json.loads(json_f.read())
json_f.close()

# create dictionary entries
entries = []
for entry in dictionary[1:]:
    # make intervals
    tree = motif_parse(entry[1])
    midi = motif_2_midi(tree)
    _notes = []
    for note in midi:
        if note.event == 'note_on':
            _notes.append(note.note)
    intervals = []
    if len(_notes) > 1:
        for i in range(len(_notes) - 1):
            interval = _notes[i + 1] - _notes[i]
            intervals.append(interval)
    print(_notes)
    print(intervals)

    entries.append({'word': entry[0], 'motif': entry[1], 'bpm': int(entry[2]), 'intervals': intervals})

''' check if motif_interals is a sublist of keyboard_intervals '''
def interval_check(keyboard_intervals: list[int], motif_interals: list[int]):
    # find first interval
    first_interval = motif_interals[0]

    def find_starting_index(offset):
        start_idx = -1
        for i in range(offset, len(keyboard_intervals)):
            if keyboard_intervals[i] == first_interval:
                start_idx = i
                break
        return start_idx

    start_idx = find_starting_index(0)
        
    if start_idx == -1: 
        return False

    
    while True:
        failed = False

        # check motif intervals
        for i in range(len(motif_interals)):
            keyboard_idx = i + start_idx

            # if end of keyboard_intervals is reached before end of motif_interals
            # return false
            if keyboard_idx >= len(keyboard_intervals):
                return False

            # if interval order doesn't match, return false
            if motif_interals[i] != keyboard_intervals[keyboard_idx]: 
                failed = True

        if failed:
            # try another starting index
            start_idx = find_starting_index(start_idx + 1)
            if start_idx == -1: return False
            
        else: return True
                
def make_intervals(_notes):
    intervals = []
    if len(_notes) > 1:
        for i in range(len(_notes) - 1):
            interval = _notes[i] - _notes[i + 1]
            intervals.append(interval)
    return intervals

def find_word(keyboard_intervals):
    for entry in entries:
        intervals_match = interval_check(keyboard_intervals, entry['intervals'])
        if intervals_match:
            return entry['word']
    return None

# # print(find_word([0, 2, 1, 3, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
# # print(find_word([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
# print(interval_check([0, 2, 1, 3, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
# print(find_word([0, 2, 1, 3, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

''' open midi input '''
MAX_NOTES = 50
notes = []
def midi_callback(event, data=None):
    message, deltatime = event
    if message[0] == midiconstants.NOTE_ON \
    and message[2] != 0:
        midi_event = 'note_on'
        
        notes.insert(0, message[1])
        if len(notes) >= MAX_NOTES: notes.pop()

        intervals = make_intervals(notes)
        word = find_word(intervals)
        if word != None: 
            # reset the intervals
            notes.clear()
            pyautogui.write(f'{word} ', interval=0)
        print(word)
    else:
        midi_event = 'note_off'
    # print(midi_event)

midiin = MidiIn()
try:
    midiin, port_name = midiutil.open_midiinput()
except (EOFError, KeyboardInterrupt):
    sys.exit()
midiin.set_callback(midi_callback) 

''' loop '''
print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
