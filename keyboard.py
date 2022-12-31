from rtmidi import (midiutil, MidiIn, midiconstants)
import sys
import time
import pyautogui


''' open midi input '''
def midi_callback(event, data=None):
    message, deltatime = event
    if message[0] == midiconstants.NOTE_ON \
    and message[2] != 0:
        midi_event = 'note_on'
        pyautogui.write('note ', interval=0)
    else:
        midi_event = 'note_off'
    print(midi_event)

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
