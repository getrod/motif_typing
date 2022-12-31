from midi2audio import FluidSynth
import mido

def read_midi_file(filename):
    mid = mido.MidiFile(filename)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)


# ''' SECION 1 '''
# filename = 'test.mid'
# mid = mido.MidiFile(filename)
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         if msg.type == 'set_tempo':
#             msg.tempo = mido.bpm2tempo(240) 
#         print(msg)


# read_midi_file('test1.mid')
# mid.save('test1.mid')

# # using the default sound font in 44100 Hz sample rate
# fs = FluidSynth(sound_font='Nice-Steinway-Lite-v3.0.sf2')
# # fs.midi_to_audio('test.mid', 'output.wav')


# fs.play_midi(filename)
# fs.play_midi('test1.mid')
# fs.midi_to_audio('test1.mid', 'output.wav')



''' SECION 2 '''
read_midi_file('test1.mid')
print()
read_midi_file('test.mid')

def change_track_bmp(filename, bpm):
    mid = mido.MidiFile(filename)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'set_tempo':
                msg.tempo = mido.bpm2tempo(bpm) 
    return mid

fs = FluidSynth(sound_font='Nice-Steinway-Lite-v3.0.sf2')

def play_midi_file(filename):
    fs.play_midi(filename)

def play_track_with_bpm(midi_filename, bpm, transpose = 0):
    mid = change_track_bmp(midi_filename, bpm)

    # transpose midi file
    if transpose != 0:
        for i, track in enumerate(mid.tracks):
            for msg in track:
                if msg.type == 'note_on' or msg.type == 'note_off':
                    msg.note += transpose

    temp_filename = 'temp.mid'
    mid.save(temp_filename)
    play_midi_file(temp_filename)

play_track_with_bpm("test.mid", 60, transpose=1)