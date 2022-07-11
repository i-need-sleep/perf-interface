import os
import json
import random
import threading
import webbrowser

import numpy as np

from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_cors import CORS, cross_origin
import jinja2

import pretty_midi
from pretty_midi import constants

SAMPLE_PATH = "static/samples_out"
SAMPLE_PATH_ANTHEM = "static/samples_out_anthem"
EXPRESSIVE_PATH = 'static/resolved_909'
SAMPLES = os.listdir(SAMPLE_PATH)
SAMPLES_ANTHEM = os.listdir(SAMPLE_PATH_ANTHEM)

# Server Setup ###################################################################################################################
app = Flask(__name__)
app.jinja_options['variable_start_string'] = '[['
app.jinja_options['variable_end_string'] = ']]'
CORS(app)
app.secret_key = str(random.random())
#  = jinja2.Environment(loader=loader, trim_blocks=True,block_start_string='@@',block_end_string='@@',variable_start_string='@=', variable_end_string='=@')

# Helpers ########################################################################################################################
def get_sample(sample_folder):
    original_midi_path_mixed = "{}/{}/mixed.mid".format(SAMPLE_PATH, sample_folder)
    original_midi_path_mel = "{}/{}/melody.mid".format(SAMPLE_PATH, sample_folder)
    # original_midi_path_acc = "{}/{}/accompaniment_track.mid".format(SAMPLE_PATH, sample_folder)
    # With expressive note length / velo
    original_midi_path_acc = "{}/{}.mid".format(EXPRESSIVE_PATH, sample_folder)
    notedic_path = "{}/{}/{}_mixed.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    notedic_mel_path = "{}/{}/{}_mel.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    notedic_acc_path = "{}/{}/{}_acc.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    chord_path = "{}/{}/chord.npy".format(SAMPLE_PATH, sample_folder)
    json_path = "{}/{}/songData.json".format(SAMPLE_PATH, sample_folder)
    notedic = np.load(notedic_path, allow_pickle=True).item()
    notedic_mel = np.load(notedic_mel_path, allow_pickle=True).item()
    notedic_acc = np.load(notedic_acc_path, allow_pickle=True).item()
    chord = np.load(chord_path)
    root = np.zeros((16,12))
    bass = np.zeros((16,12))
    root[[i for i in range(16)],chord[:,0].astype(int)] = 1
    bass[[i for i in range(16)],chord[:,-1].astype(int)] = 1
    chord = np.concatenate((root,chord[:,1:-1],bass),axis=1)

    sustain_path = "static/sustain.npy"
    sustain = np.load(sustain_path)


    with open(json_path, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
            name = jsonData['name']
            key = jsonData['key'][:-1]
            key = key.replace(':','')

    # Get horizontal and vertical densities
    onset_dict = {}
    v_ctr = 0
    v_ctr_offbeat = 0
    onset_down = []
    onset_up = []
    for val_ in notedic_acc.values():
        for notes in val_.values():
            for note in notes:
                if note[0] not in onset_dict.keys():
                    onset_dict[note[0]] = 1
                if note[0] % 1 == 0:
                    v_ctr += 1
                    if note[0] not in onset_down:
                        onset_down.append(note[0])
                elif note[0] % 1 == 0.5:
                    v_ctr_offbeat += 1
                    if note[0] not in onset_up:
                        onset_up.append(note[0])
            hd = len(onset_dict)
            # vd = len(notes) / hd
            vd = max(v_ctr/len(onset_down), v_ctr_offbeat/len(onset_up))
            break
        break

    return original_midi_path_mixed, original_midi_path_mel, original_midi_path_acc, notedic, notedic_mel, notedic_acc, chord, sustain, key, name, hd, vd

def chd_to_str(c_mat):
    out = []
    pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    for c in c_mat:
        root = np.argmax(c[:12])
        root_s = pitches[root]
        chroma = np.array([i for i in range(12)])[c[12:24]==1]
        chroma = (chroma - root) % 12
        bass = np.argmax(c[24:])
        if len(chroma) == 3:
            if 7 in chroma:
                if 4 in chroma:
                    c_type = ''
                if 3 in chroma:
                    c_type = 'm'
                if 1 in chroma or 2 in chroma:
                    c_type = 'sus2'
                if 5 in chroma or 6 in chroma:
                    c_type = 'sus4'
            else:
                c_type = '6'
        else:
            c_type = ''
        if bass == 0:
            bass_s = ''
        else:
            bass_s = '/' + pitches[(root + bass) % 12]
        out.append('{}{}{}'.format(root_s, c_type, bass_s))
    for i in range(len(out)-1, 0, -1):
        if out[i] == out[i-1]:
            out[i] = ''
    return out

def midi_to_noteseq(midi_path):
    midi = pretty_midi.PrettyMIDI(midi_path)
    note_seq = {'notes': [], 'totalTime':16}
    rescale = 4/3
    for note in midi.instruments[0].notes:
        note_seq['notes'].append({'pitch': note.pitch, 'startTime':note.start*rescale, 'endTime':note.end*rescale, 'velocity':note.velocity})
    return note_seq

def chd_to_deg(c_mat, key):
    out = []
    pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    pitches_flat  = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    deg = ['I', 'IIb', 'II', 'IIIb', 'III', 'IV', 'Vb', 'V', 'VIb', 'VI', 'VIIb', 'VI']

    key = key[:-3]
    if key in pitches:
        key = pitches.index(key)
    else:
        key = pitches_flat.index(key)

    for c in c_mat:
        root = np.argmax(c[:12])
        root_s = (root-key)%12
        chroma = np.array([i for i in range(12)])[c[12:24]==1]
        chroma = (chroma - root) % 12
        bass = np.argmax(c[24:])
        c_type = deg[root_s]
        if 3 in chroma:
            c_type = deg[root_s].lower()
        if 1 in chroma or 2 in chroma:
            c_type += 'sus2'
        if 5 in chroma or 6 in chroma:
            c_type += 'sus4'
        if bass != 0:
            c_type += '/' + deg[(root + bass - key) % 12]
        out.append(c_type)
    for i in range(len(out)-1, 0, -1):
        if out[i] == out[i-1]:
            out[i] = ''
    return out

def getSongData():
    # Progressions, keys, etc
    select_sample_folders = os.listdir(SAMPLE_PATH)
    songData = {}
    for folder in select_sample_folders:
        [song, segment] = folder.split("_")

        json_path = "{}/{}/songData.json".format(SAMPLE_PATH,folder)
        chord_path = "{}/{}/chord.npy".format(SAMPLE_PATH,folder)
        chord = np.load(chord_path)
        root = np.zeros((16,12))
        bass = np.zeros((16,12))
        root[[i for i in range(16)],chord[:,0].astype(int)] = 1
        bass[[i for i in range(16)],chord[:,-1].astype(int)] = 1
        chord = np.concatenate((root,chord[:,1:-1],bass),axis=1)

        with open(json_path, 'r') as jsonFile:
                jsonData = json.load(jsonFile)
                name = jsonData['name']
                key = jsonData['key'][:-1]
                key = key.replace(':','')

        songkey = "{}: {}".format(song, name)

        degs = chd_to_deg(chord, key)
        new_deg = []
        for deg in degs:
            if deg != '':
                new_deg.append(deg)

        if songkey not in songData.keys():
            songData[songkey] = {segment: '-'.join(new_deg), 'key': key}
        else:
            songData[songkey][segment] = '-'.join(new_deg)
    return songData

songData = getSongData()

def get_data_from_folder(folder):
    original_midi_path_mixed, original_midi_path_mel, original_midi_path_acc, notedic, notedic_mel, notedic_acc, chord, sustain, key, name, hd, vd = get_sample(folder)

    chord_str = chd_to_str(chord)
    chord_deg = chd_to_deg(chord, key)
    for idx, chd_str in enumerate(chord_str):
        if chord_deg[idx] != '':
            chord_str[idx] += " ({})".format(chord_deg[idx])

    out =  {'songID': folder,
            'original_chd_str': chord_str,
            'original_chd_mat': chord.tolist(),
            'original_noteseq_mixed': midi_to_noteseq(original_midi_path_mixed),
            'original_noteseq_mel': midi_to_noteseq(original_midi_path_mel),
            'original_noteseq_acc': midi_to_noteseq(original_midi_path_acc),
            'notedic_mixed': notedic,
            'notedic_mel': notedic_mel,
            'notedic_acc': notedic_acc,
            'sustain': sustain.tolist(),
            'key': key,
            'name': name,
            'hd': hd,
            'vd': vd}
    return out


# The Main Thing ##################################################################################################################
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", demo = '')

@app.route('/favicon.ico', methods=['GET'])
def serve_favicon():
    return app.send_static_file('favicon.ico')

@app.route('/js/<path>')
def serve_js(path):
    return app.send_static_file('js/'+path)

@app.route('/css/<path>')
def serve_css(path):
    return app.send_static_file('css/'+path)

@app.route('/accFilter_icons/<path>')
def serve_accFilter_icons(path):
    return app.send_static_file('accFilter_icons/'+path)

@app.route('/get_songdata', methods=['GET'])
def get_songdata():
    out = {'songData': songData}
    return json.dumps(out)

@app.route('/get_data', methods=['GET'])
def get_data():
    songID = request.args.get("song")
    if songID == "000":
        sample_folder = random.choice(SAMPLES)
    else:
        sample_folder = songID
    
    out = get_data_from_folder(sample_folder)
    return json.dumps(out)

@app.route('/get_data_all', methods=['GET'])
def get_data_all():
    out = [len(SAMPLES)]
    # Load AccoMontage edge weights
    with open('static/edge_weight_reduced.json', 'r') as f:
        out.append(['edge_weights', json.load(f)])
    return json.dumps(out)

@app.route('/get_data_all_idx', methods=['GET'])
def get_data_idx():
    idx = int(request.args.get("idx"))
    out = get_data_from_folder(SAMPLES[idx])
    return json.dumps([0,[SAMPLES[idx], out]])

@app.route('/get_data_anthem', methods=['GET'])
def get_data_anthem():
    out = [len(SAMPLES_ANTHEM)]
    out.append(['edge_weights', 'hi'])
    return json.dumps(out)

@app.route('/get_data_anthem_idx', methods=['GET'])
def get_data_anthem_idx():
    idx = int(request.args.get("idx"))
    out = get_data_from_folder(SAMPLES_ANTHEM[idx])
    return json.dumps([0,[SAMPLES_ANTHEM[idx], out]])

# Demos
@app.route('/uae_anthem', methods=['GET'])
def uae_anthem():
    return render_template("index.html", demo = 'anthem')

if __name__ == '__main__':
    # threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.1:5000/", new=0, autoraise=True) ).start()
    print(os.getenv('PORT',5000))
    app.run(debug=False,port=os.getenv('PORT',5000))
