from midi2audio import FluidSynth
import mido
import moteaf as mt

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
fs = FluidSynth(sound_font='Nice-Steinway-Lite-v3.0.sf2')

def change_track_bmp(filename, bpm):
    mid = mido.MidiFile(filename)
    tempo = mido.bpm2tempo(bpm) 
    
    for i, track in enumerate(mid.tracks):
        found = False
        for msg in track:
            if msg.type == 'set_tempo':
                msg.tempo = tempo
                found = True
        if found == False:
            track.insert(0, mido.MetaMessage('set_tempo', tempo=tempo))
    return mid

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

def play_motif(motif_string: str, bpm: float = 120, transpose: int = 0):
    temp_name = 'temp_motif.mid'
    motif_tree = mt.motif_parse(motif_string)
    midi = mt.motif_2_midi(motif_tree)
    mt.save_midi(midi, temp_name)

    play_track_with_bpm(temp_name, bpm, transpose)

# motif ="""
#     Am9[0 1 2 3 4 :: 4]-(3/2), 
#     Bm7[3 4 5 6 :: 3]-(3/2), 
#     Cmaj9[0 1 2 3 4 :: 5]-(2), 
#     Em7<[3 5]-(3/4), [6]-(1/4), [7 9]-(1/4), [8]-(1/4), [6]-(1/4) :: 4>, 
#     Em7<[3]-(1/4), [2]-(1/4), [3]-(1/4), [4]-(1/4), [1]-(1/4) :: 4>
#     """
# play_motif(motif, bpm=140)
# read_midi_file('temp.mid')
# print()
# # read_midi_file('temp_mof.mid')
# play_track_with_bpm('temp.mid', 60)
# read_midi_file('temp.mid')