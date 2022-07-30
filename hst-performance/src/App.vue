<template>
<div>

<!-- Nav Bar -->
<nav class="navbar navbar-expand-sm bg-light navbar-hover">
  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mr-auto">   
          <li class="nav-item dropdown">
              <button class="dropdown-toggle btn" id="browse_samples" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Browse Samples
              </button>
              <ul class="dropdown-menu">
                <li id="resample" v-on:click="get_data">Random Phrase</li>
                  <li v-for="song in Object.keys(this.songData)" v-bind:key="song">
                    <a class="dropdown-item dropdown-toggle">Song {{song}} {{this.songData[song]['key']}}</a>
                      <ul class="dropdown-menu">
                        <div v-for="segment in Object.keys(this.songData[song])" v-bind:key="segment">
                          <div v-if="segment != 'key'">
                            <li v-on:click="get_data"><a class="dropdown-item phraseSelect" 
                              v-bind:data-song="song"
                              v-bind:data-segment="segment">
                              Segment {{segment}} {{this.songData[song][segment]}}</a></li>
                          </div>
                        </div>
                      </ul>
                  </li>
              </ul>
          </li>
      </ul>
    <ul class="navbar-nav">
      <li class="nav-item">
        <button class="btn" disabled>Phrase ID: {{this.songID.slice(0,3)}}: {{this.songname}} {{this.songID.slice(4)}} | {{this.songkey}}</button><br> 
        <!-- <button class="btn" v-on:click="test">test</button><br>  -->
      </li>
      <li class="nav-item">
        <a tabindex="0" class="btn" role="button" data-toggle="popover" data-trigger="focus" title="Help" rel="popover"
        data-content="
        Playback: <br> 
        <ul>
          <li>e: reset player</li>
          <li>r: replay</li>
          <li>t: test</li>
          <li>a: a to test</li>
          <li>s: show answer</li>
          <li>n: new sample</li>
        </ul>
        Input-Fixed: <br> 
        <ul>
          <li>Mouse</li>
          <ul>
            <li>left click: select a major triad</li>
            <li>right click: select a minor triad</li>
            <li>middle click or (shift + left click): select a dominant 7th chord</li>
            <li>alt + left/right click: select a major/minor 7th chord</li>
          </ul>
          <li>Keyboard</li>
          <ul>
            <li>'1'-'=': select root</li>
            <li>shift + root: major triad</li>
            <li>ctrl + root: minor triad</li>
            <li>alt + root: moninant 7th chord</li>
            <li>alt+ shift/ctrl + root: major/minor 7th chord</li>
          </ul>
        </ul>
        Input-Movable: <br> 
        <ul>
          <li>Mouse</li>
          <ul>
            <li>left click: select a triad corresponding the the scale degree</li>
            <li>shift + left click: select a major triad</li>
            <li>ctrl + left click: select a minor triad</li>
            <li>alt + left click: select a dominant seventh chord</li>
            <li>alt + shift/ctrl + left click: select a major/minor seventh chord</li>
          </ul>
          <li>Keyboard</li>
          <ul>
            <li>1-7: select a triad corresponding the the scale degree</li>
            <li>shift + 1-7: select a major triad</li>
            <li>ctrl + 1-7: select a minor triad</li>
            <li>alt + 1-7: select a dominant seventh chord</li>
            <li>alt + shift/ctrl + 1-7: select a major/minor seventh chord</li>
          </ul>
        </ul>
        "  data-html="true">
          Help
        </a><br>
      </li>
    </ul>
  </div>
</nav>


<div class="container-fluid pt-3 pb-5" id="main_app">
  <!-- Original -->
  <!-- Time steps: Original -->
  <table id=time_steps class="table table-fixed prog_table">
    <thead class="thead-light">
    <tr>
      <th class="prog_head table_cell"></th>
      <div>
        <th class="time_cell" v-for="i in 16" v-bind:key="i" v-bind:id="'time'+(i-1)"> {{ (i+3-(i-1)%4)/4 + "." + ((i-1)%4+1)}} </th>
        <th class="time_cell"></th><th class="time_cell"></th>
      </div>
    </tr>
    </thead>
  </table> 

  <midi-visualizer type="piano-roll" class="right" id="original_vis" v-bind:noteSequence="this.original_noteseq" v-bind:config="this.cfg"></midi-visualizer>
  <div class="up">
  <midi-visualizer type="piano-roll" class="right" id="original_vis_overlay" v-bind:noteSequence="this.original_noteseq_overlay" v-bind:config="this.cfg_mel"></midi-visualizer>
  <svg class="original_svg svg right" height="0px"></svg>
  
  
  <div class="up">

  <!-- Original Progression -->
  <table id="original_prog" class="table table-fixed table-striped prog_table">
    <tbody>
    <tr>
        <th id=play_prog_original class="prog_head" v-on:click="play_prog_original">Original</th>
        <div>
        <td v-for="i in 16" v-bind:key="i" v-bind:id="'original_prog'+(i-1)" class="table_cell" style="font-weight:normal;" v-on:click="play_chord('original', i-1)" > {{ original_chd_str[i-1] }} </td>
        <th></th><th></th>
        </div>
    </tr>
    </tbody>  
  </table>

  <!-- Altered -->
  <!-- Time steps -->
  <table id=altered_time_steps class="table table-fixed prog_table">
    <thead class="thead-light">
    <tr>
        <div>
          <th class = "prog_head table_cell" v-on:click="replay_all"></th>
          <th class="time_cell" v-for="i in 16" v-bind:key="i" v-bind:id="'time_altered'+(i-1)" v-on:click="replay_bar(i-1)"> {{ (i+3-(i-1)%4)/4 + "." + ((i-1)%4+1)}} </th>
          <th class="time_cell" v-on:click="replay_all">Replay</th><th class="time_cell" v-on:click="replay_all"></th>
        </div>
    </tr>
    </thead>
  </table> 

  <canvas id="altered_canvas" class="right"></canvas>
  <svg class="swapped_svg svg right" id="swapped_svg" height="0px"></svg>

  <div class="up">
  <!-- Altered Progression -->
  <table id=saved_prog class="table table-fixed table-striped prog_table">
    <tbody>
      <tr>
        <div>
        <th id=play_prog_original class="prog_head" v-on:click="play_prog_altered">Altered</th>
        <td v-for="i in 16" v-bind:key="i" v-bind:id="'altered'+(i-1)" class="table_cell" style="font-weight:normal;" v-on:click="play_chord('altered',i-1)">
          <span v-if="! hide_vis_input">{{altered_chd_str[i-1]}}</span>
        </td>
        <th><span class="table_tail" v-on:click="test_add" v-if="! this.playing">Add to test</span></th>
        </div>
    </tr>
    </tbody>
  </table> 

  <!-- Interfacing -->
  <div class="row">
    <div class="col-4">
    <button id="altered_reset" class="btn btn-light" v-on:click="player_reset">Reset</button>
    <br>
    Bpm: <span id=bpm_text>{{this.bpm}}</span><div class=slider_container><input type="range" class="form-control-range slider" min=30 max=200 v-model="bpm" v-on:pointerout="follow_tempo"></div>
    Next bpm: <span id=bpm_text>{{this.next_bpm}}</span><div class=slider_container><input type="range" class="form-control-range slider" min=30 max=200 v-model="next_bpm"></div>
    Velocity: <span id=bpm_text>{{this.velocity_scale}}%</span><div class=slider_container><input type="range" class="form-control-range slider" id=vel_slider min=5 max=100 v-model="velocity_scale"></div>
    Expressive dynamics: <span >{{this.expressiveness_vel}}% <div class=slider_container><input type="range" class="form-control-range slider" min=0 max=300 v-model="expressiveness_vel"></div></span>
    Expressive timing: <span >{{this.expressiveness_tempo}}% <div class=slider_container><input type="range" class="form-control-range slider" min=0 max=300 v-model="expressiveness_tempo"></div></span>

    <div class="input-group-prepend">
    <div class="input-group-text" style="width:160px">
      <input type="checkbox" id="root_overlay" v-bind:checked="root_overlay" v-on:click="this.root_on_click()"> <span> &nbsp; Root overlay</span>
    </div>
    </div>
    <div class="input-group-prepend">
      <div class="input-group-text" style="width:160px">
        <input type="checkbox" id="chord_overlay" v-bind:checked="chord_overlay" v-on:click="this.chord_on_click()"> <span> &nbsp; Chord overlay</span>
      </div>
    </div>

    <br>
    <div>
    <button class="btn btn-light" v-on:click="test_clear" :disabled="this.test_chd_strs.length < 1 || playing">Clear Test</button><br>
    <br>
    <button class="btn btn-light" v-on:click="test_apply" :disabled="this.test_chd_strs.length < 1 || playing">Test</button><br>
    <button class="btn btn-light" v-on:click="test_show_answer" :disabled="! hide_vis_input || playing">Show answer</button><br>
    </div>
    
    <div v-for="i in this.test_chd_strs.length" :key="i">
      <div v-if="i == this.test_idx + 1 && ! hide_vis_input" class="test_correct no_click">
        <span v-for="j in 4" :key="j">
          {{this.test_chd_strs[i-1][4*(j-1)]}}
          <span v-if="j<4"> &nbsp;-&nbsp;</span>
        </span>
      </div>
      <div v-else class="no_click">
        <span v-for="j in 4" :key="j">
          {{this.test_chd_strs[i-1][4*(j-1)]}}
          <span v-if="j<4"> &nbsp;-&nbsp;</span>
        </span>
      </div>
    </div>
    
    <br><button class="btn btn-light" v-on:click="connect_midi">Connect MIDI output device (Chrome only)</button>
    <div class="dropdown">
      <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Channel {{this.midi_channel}}
      </button>
      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
      <div v-for="i in 16" :key="i">
        <a class="dropdown-item" href="#" v-on:click="change_midi_channel(i)">Channel {{i}}</a>
      </div>
      </div>
    </div>
      
    <br>
    <p v-if="this.show_midi_devices">{{this.midi_device_names}}</p><br>
    <p v-if="!this.phrasebank_loaded">Loading phrase bank {{n_loaded}}/{{n_songs}} ... This could take around a minute.</p>
    <p v-if="this.demo.name == 'hst-performance anthem'">Anthem demo: phrase {{this.demo.line}} bar {{this.demo.bar}} <span v-if="this.demo.locked">locked</span><span v-if="this.demo.locked1">locked</span></p>

  </div>

  <div class="col-6">
    <div class="btn-group">
      <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">{{"Input type: "+this.input_type}}
      <span class="caret"></span></button>
      <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#" v-on:click="change_input_type('movable')">Movable</a></li>
        <li><a class="dropdown-item" href="#" v-on:click="change_input_type('fixed')">Fixed</a></li>
      </ul>

    <div class="dropdown" v-if="this.input_type == 'movable'">
      <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">{{"Key: "+this.key+" major"}}
      <span class="caret"></span></button>
      <ul class="dropdown-menu">
        <li><a v-for="key in this.scales_major" 
        v-bind:key="key" class="dropdown-item" href="#" v-on:click="change_key(key)">{{key + " major"}}</a></li>
      </ul>
    </div>
    </div>

    <!-- Interface UIs -->  
    <div v-if="this.loaded && ! this.hide_vis_input">
    <InterfaceFixed v-if="input_type == 'fixed'" v-on:update_current_chord="update_current_chord"/>
    <InterfaceMovable ref="dial" v-if="input_type == 'movable' && !this.wheel.connected" v-bind:interface_key="this.key" v-bind:roots="scales_major" v-on:update_current_chord="update_current_chord"/>
    <InterfaceMovableWheel ref="dial_wheel" v-if="input_type == 'movable' && this.wheel.connected" v-bind:interface_key="this.key" v-bind:roots="scales_major" v-on:update_current_chord="update_current_chord"/>
    </div>

  </div>

  <!-- Next phrase -->
  <div class="col-1">
    <p>Next phrase:</p>
    <PhraseFilter v-if="this.demo.name == 'none' && !this.wheel.connected" v-on:set_filter="set_filter"/>
    <PhraseFilterWheel ref="phrase_filter_wheel" v-if="this.demo.name == 'none' && this.wheel.connected" v-on:set_filter="set_filter"/>
    <PhraseSelectDemo v-if="this.demo.name != 'none'" ref="phrase_selector_demo" v-bind:noteseqs="this.next_phrases" v-on:update_next_phrase="update_next_phrase"/>
    <PhraseSelect v-if="this.demo.name == 'none' && !this.wheel.connected" ref="phrase_selector" v-bind:noteseqs="this.next_phrases" v-on:update_next_phrase="update_next_phrase"/>
    <PhraseSelect v-if="this.demo.name == 'none' && this.wheel.connected" id="phrase_select_wheel" ref="phrase_selector" v-bind:noteseqs="this.next_phrases" v-on:update_next_phrase="update_next_phrase"/>
  </div>
</div>
</div>
</div>
</div>
</div>

<!-- Barlines -->
<svg id=original_barline class="barline_svg"></svg><br>
<svg id=altered_barline class="barline_svg"></svg>

<!-- Player -->
<midi-player v-bind:noteSequence="this.original_noteseq" sound-font visualizer="#original_vis" id="original_player"></midi-player>

<!-- Mel/Acc Toggle -->
<div id="melacc_toggle">
<div class="input-group-prepend">
  <div class="input-group-text" style="width:160px">
    <input type="checkbox" id="root_overlay" v-bind:checked="mel" v-on:click="this.mel_on_click()"> <span> &nbsp; Melody</span>
  </div>
</div>
<div class="input-group-prepend">
  <div class="input-group-text" style="width:160px">
    <input type="checkbox" id="chord_overlay" v-bind:checked="acc" v-on:click="this.acc_on_click()"> <span> &nbsp; Accompaniment</span>
  </div>
</div>
</div>

</div>
</template>

<script>
// import { NoteSequence } from '@magenta/music'
import { createQuantizedNoteSequence, unquantizeSequence } from '@magenta/music/esm/core/sequences'
import InterfaceFixed from './components/InterfaceFixed.vue'
import InterfaceMovable from './components/InterfaceMovable.vue'
import PhraseFilter from './components/PhraseFilter.vue'
import PhraseSelect from './components/PhraseSelect.vue'
import PhraseSelectDemo from './components/PhraseSelectDemo.vue'
import InterfaceMovableWheel from './components/InterfaceMovableWheel.vue'
import PhraseFilterWheel from './components/PhraseFilterWheel.vue'
const axios = require('axios').default
const d3 = require("d3")
const mm = require("@magenta/music")
const _ = require("html-midi-player")
const Tone = require("tone")
const {WebMidi} = require("webmidi")
const Faye = require('faye')
console.log(_)
var player = new mm.SoundFontPlayer('https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus')
// var debug_player = new mm.SoundFontPlayer('https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus')

export default {
  name: 'App',
  components: {
    InterfaceFixed,
    InterfaceMovable,
    PhraseFilter,
    PhraseSelect,
    PhraseSelectDemo,
    InterfaceMovableWheel,
    PhraseFilterWheel
},
  data: function(){
    return{
      // Constants (not really)
      BACKEND_PATH: "http://127.0.0.1:5000",//"" //"http://127.0.0.1:5000"
      DEBUG: false,
      STEP_SIZE: 4,
      scales_major: ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'],
      // Chord playback
      prog_step_duration: 0.5,
      octave_center: 48,

      // Song data (original)
      allData: {},

      n_songs: 0,
      n_loaded: 0,

      songID: "000",
      songname: '',
      songkey: '',
      songData: {},

      original_noteseq: 0,
      original_noteseq_mixed: 0,
      original_noteseq_mel: 0,
      original_noteseq_acc: 0,
      original_noteseq_overlay: {notes:[{pitch:30, start:0, end:16}], totalTime: 16},
      empty_noteseq: {notes:[{pitch:30, start:0, end:16}], totalTime: 16},

      original_chd_str: 0,
      original_chd_mat: 0,

      notedic: 0,
      notedic_mixed: 0,
      notedic_mel: 0,
      notedic_acc: 0,

      sustain: [],

      // Expressive performance
      expressiveness_vel: 100,
      expressiveness_tempo: 100,
      expressiveness_dur: 100,

      // Song data (altered)
      altered_noteseq: {notes:[], totalTime: 16},
      altered_noteseqs: [0,0,0,0],
      altered_chd_str: Array(16).fill(""),
      altered_chd_mat: Array(16).fill(Array(36).fill(0)),

      // Stored song data (test mode)
      chds: [],
      test_chd_strs: [],
      test_chds: [],
      altered_chd_str_hide: [],
      test_idx: -1,

      // Interfacing (outside)
      bpm: 60,
      next_bpm: 60,
      velocity_scale: 10,
      playing: false,
      loaded: false,
      phrasebank_loaded: false,
      hide_vis_input: false,
      input_type: "fixed",
      key: "C",
      
      mel: false,
      acc: true,

      // Interfacing (inside)
      t: 0,
      chord_seq: [], // Entered chords for the current window
      current_chd: '', // Queued chord for the next time step
      current_chd_text: '',

      // Altered visualiser
      altered_vis: 0,

      // Visualiser config
      cfg: {
        noteHeight: 4,
        pixelsPerTimeStep: 100,
        minPitch: 20,
        maxPitch: 90,
        noteSpacing: 1
      },
      cfg_mel: {
        noteHeight: 4,
        pixelsPerTimeStep: 100,
        minPitch: 20,
        maxPitch: 90,
        noteSpacing: 1,
        noteRGB: "255,0,0"
      },

      // Overlays
      root_overlay: true,
      chord_overlay: false,

      // Next phrase
      next_phrases_id: [0,0,0],
      next_phrases: [0,0,0],
      next_phrase_idx: -1,
      edge_weights: [],

      // Next phrase filtering
      filter_h: -1,
      filter_v: -1,

      // MIDI output device
      show_midi_devices: false,
      midi_device_names: [],
      midi_device: 0,
      midi_channel: 1,

      // Demos
      demo: {
        name: 'hst-performance anthem',//'hst-performance anthem', 'none'
        bar: -1,
        line: 0,
        chord_seq: ['1', '4', '5', '5', '5', '1', 'x5', '1', '6', 'x5', '5', 's6', '2', '1', '5', '1', '1', '4', '5', '5', '5', '1', 'x5', '1'],
        phrase_seq: ['038_B', '050_B', '000_A', '001_A', '002_A', '003_A', '004_A', '005_A', '005_A'],
        locked: true,
        lock_passed: false,
        locked1: true,
        tempo_curve: [[13.71      , 71.42857143],
       [14.55      , 80.        ],
       [15.3       , 82.19178082],
       [16.03      , 83.33333333],
       [16.75      , 81.08108108],
       [17.49      , 78.94736842],
       [18.25      , 83.33333333],
       [18.97      , 80.        ],
       [19.72      , 84.50704225],
       [20.43      , 77.92207792],
       [21.2       , 83.33333333],
       [21.92      , 81.08108108],
       [22.66      , 80.        ],
       [23.41      , 83.33333333],
       [24.13      , 83.33333333],
       [24.85      , 77.92207792],
       [25.62      , 83.33333333],
       [26.34      , 83.33333333],
       [27.06      , 83.33333333],
       [27.78      , 82.19178082],
       [28.51      , 82.19178082],
       [29.24      , 81.08108108],
       [29.98      , 81.08108108],
       [30.72      , 80.        ],
       [31.47      , 75.94936709],
       [32.26      , 85.71428571],
       [32.96      , 77.92207792],
       [33.73      , 84.50704225],
       [34.44      , 84.50704225],
       [35.15      , 81.08108108],
       [35.89      , 75.        ],
       [36.69      , 81.08108108],
       [37.43      , 81.08108108],
       [38.17      , 86.95652174],
       [38.86      , 84.50704225],
       [39.57      , 83.33333333],
       [40.29      , 89.55223881],
       [40.96      , 84.50704225],
       [41.67      , 80.        ],
       [42.42      , 84.50704225],
       [43.13      , 83.33333333],
       [43.85      , 85.71428571],
       [44.55      , 84.50704225],
       [45.26      , 85.71428571],
       [45.96      , 83.33333333],
       [46.68      , 82.19178082],
       [47.41      , 76.92307692],
       [48.19      , 80.        ],
       [48.94      , 77.92207792],
       [49.71      , 85.71428571],
       [50.41      , 81.08108108],
       [51.15      , 77.92207792],
       [51.92      , 82.19178082],
       [52.65      , 84.50704225],
       [53.36      , 81.08108108],
       [54.1       , 81.08108108],
       [54.84      , 78.94736842],
       [55.6       , 81.08108108],
       [56.34      , 80.        ],
       [57.09      , 78.94736842],
       [57.85      , 81.08108108],
       [58.59      , 81.08108108],
       [59.33      , 84.50704225],
       [60.04      , 68.96551724],
       [60.91      , 73.17073171],
       [61.73      , 81.08108108],
       [62.47      , 76.92307692],
       [63.25      , 80.        ],
       [64.        , 73.17073171],
       [64.82      , 77.92207792],
       [65.59      , 75.94936709],
       [66.38      , 81.08108108],
       [67.12      , 81.08108108],
       [67.86      , 75.94936709],
       [68.65      , 77.92207792],
       [69.42      , 78.94736842],
       [70.18      , 80.        ],
       [70.93      , 78.94736842],
       [71.69      , 80.        ],
       [72.44      , 76.92307692],
       [73.22      , 77.92207792],
       [73.99      , 81.08108108],
       [74.73      , 77.92207792],
       [75.5       , 76.92307692],
       [76.28      , 80.        ],
       [77.03      , 80.        ],
       [77.78      , 80.        ],
       [78.53      , 77.92207792],
       [79.3       , 74.07407407],
       [80.11      , 76.92307692],
       [80.89      , 82.19178082],
       [81.62      , 75.        ],
       [82.42      , 80.        ],
       [83.17      , 81.08108108],
       [83.91      , 76.92307692],
       [84.69      , 15.34526854]],

        sustain:
          [[0.00909090909090909, 4.0],
          [4.013636363636364, 6.0],
          [6.013636363636364, 7.995454545454545],
          [8.018181818181818, 18.0],
          [18.013636363636362, 20.0],
          [20.009090909090908, 23.995454545454546],
          [24.013636363636362, 26.0],
          [26.009090909090908, 28.0],
          [28.013636363636362, 34.0],
          [34.013636363636365, 36.0],
          [36.01363636363636, 37.99545454545454],
          [38.01363636363636, 44.0],
          [44.00909090909091, 46.0],
          [46.00909090909091, 48.0],
          [48.01363636363636, 51.99545454545454],
          [52.018181818181816, 53.0],
          [53.01363636363636, 54.0],
          [54.00909090909091, 55.0],
          [55.01363636363636, 56.0],
          [56.01363636363636, 59.0],
          [59.01363636363636, 60.0],
          [60.01363636363636, 68.0],
          [68.0090909090909, 70.0],
          [70.01363636363637, 71.99545454545454],
          [72.01818181818182, 82.00454545454545],
          [82.01363636363637, 84.00454545454545],
          [84.01363636363637, 88.0],
          [88.0090909090909, 90.0],
          [90.01363636363637, 91.99545454545454],
          [92.01363636363637, 95.0]],
        },

      wheel:{
        conncected: false,

        // Pedals
        gas: 0,
        brake: 0,
        acc_ratio: 30,
        clutched: false,

        // Wheel
        turn_idx: 0,
      
        // wheel_shift
        wheel_shift: 0,
        wheel_shift_offset: 0,
      }
    }
  },
  computed: {
  },
  methods: {
    // Helpers
    list_to_noteseq(notes_in, filter_start=0, filter_end=16){
      let notes_out = []
      for (let i=0; i<notes_in.length; i++){
          let start = notes_in[i][0]
          let end = notes_in[i][1]
          let pit = notes_in[i][2]
          if (filter_start >= 8){
              start += 8
              end += 8
          }
              if (start>=filter_start && start<filter_end){
                  notes_out.push({pitch:pit, startTime:start, endTime:end})
              }
      }
      return notes_out
    },

    chords_to_noteseq(chords, relative=true){ 
      
      let mod_chords = []
      for (let i=0; i<chords.length; i++){
        let chord = chords[i]
        let chroma = []
        for (let j=0; j<12; j++){
          if (chord[12+j] == 1){
            chroma.push(j)
          }
        }
        if (chord.slice(0,13).indexOf(1) == -1){
          break
        }
        if (relative){
          mod_chords.push([chord.slice(0,13).indexOf(1),chroma,0])
        }
        else{
          mod_chords.push([chord.slice(0,13).indexOf(1),chroma,chord.slice(24,36).indexOf(1)])
        }
      }
      chords = mod_chords
      

      let prog_notes = [];

      if (chords.length > 0){
        let cur_chord = chords[0];
        let cur_dur = this.prog_step_duration;
        
        for (let i=1; i<chords.length; i++){
            if (JSON.stringify(chords[i])==JSON.stringify(cur_chord)){
                cur_dur += this.prog_step_duration;
            }
            else {
                let root = parseInt(cur_chord[0]);
                let chroma = cur_chord[1];
                let bass = parseInt(cur_chord[2]);
                for (let j=0; j<chroma.length; j++){
                  if (relative){
                    prog_notes.push({pitch: parseInt(chroma[j])+root+this.octave_center, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                  }
                  else{
                    prog_notes.push({pitch: parseInt(chroma[j])+this.octave_center, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                  }
                }
                prog_notes.push({pitch:bass+root+this.octave_center-12, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                cur_chord = chords[i];
                cur_dur = this.prog_step_duration;
            }
        }
        let root = parseInt(cur_chord[0]);
        let chroma = cur_chord[1];
        let bass = parseInt(cur_chord[2]);
        for (let j=0; j<chroma.length; j++){
          if (relative){
            prog_notes.push({pitch: parseInt(chroma[j])+root+this.octave_center, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});
          }
          else{
            prog_notes.push({pitch: parseInt(chroma[j])+this.octave_center, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});
          }
        }
        prog_notes.push({pitch:bass+root+this.octave_center-12, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});

        return {notes: prog_notes, totalTime: this.prog_step_duration*chords.length};
      }
    },

    // Fetch data from the backend
    get_songdata(){
      let backend_path = this.BACKEND_PATH
      if (this.DEBUG){
        backend_path = 'http://127.0.0.1:5000'
      }
      axios.get(backend_path + '/get_songdata')
        .then(response => {
              let data = response.data
              if (! data.songData){
                data = JSON.parse(response.data)
              }
              this.songData = data.songData
        })
    },
    
    get_data(id="000", reset=true){
      if(typeof(id) != "string"){
        if (id.target.dataset.song != undefined){
          id = id.target.dataset.song.slice(0,3) + "_" + id.target.dataset.segment
        }
        else{
          id = "000"
        }
      }
      if (id == "000"){
        let keys = Object.keys(this.allData).slice(1)
        id = keys[Math.floor(Math.random() * keys.length)]
      }
      if (this.demo.name != "none"){
        id = this.demo.phrase_seq[this.demo.line]
      }
      let data = this.allData[id]
      this.songID = data.songID
      this.original_noteseq_mixed = data.original_noteseq_mixed
      this.original_noteseq_mel = data.original_noteseq_mel
      this.original_noteseq_acc = data.original_noteseq_acc
      this.original_chd_str = data.original_chd_str
      this.original_chd_mat = data.original_chd_mat
      this.notedic_mixed = data.notedic_mixed
      this.notedic_mel = data.notedic_mel
      this.notedic_acc = data.notedic_acc
      this.sustain = data.sustain
      this.songname = data.name
      this.songkey = data.key

      this.update_melacc_toggle()
      // Modify the sustain status to include the onset of every measure
      for (let bar=1; bar<4; bar++){
        for (let i=0; i<this.sustain.length; i++){
          let start = this.sustain[i][0]
          let end = this.sustain[i][1]
          if (start < bar*4 && end > bar*4){
            break
          }
          if (start > bar*4){
            if (i > 0){
              this.sustain[i-1][1] = bar*4 + 1
            }
            else{
            this.sustain.push([bar*4 - 1, bar*4 + 1])
            }
            break
          }
        }
      }

      // Fetch a placeholder notesequence
      // this.altered_vis = new mm.PianoRollCanvasVisualizer({notes: this.list_to_noteseq(this.notedic[0]["0M3,0M3"]), totalTime:16}, document.getElementById('altered_canvas'), this.cfg)
      
      this.altered_vis = new mm.PianoRollCanvasVisualizer({notes: [{pitch: 30, start:0, end:8}], totalTime:16}, document.getElementById('altered_canvas'), this.cfg)
      this.update_overlay()

      this.test_show_answer()
      if (reset){
        this.player_reset()
      }
      this.place_barlines_and_player()
      setTimeout(() => {  this.place_barlines_and_player(); }, 1000)
      setTimeout(() => {  this.place_barlines_and_player(); }, 3000)

      // Update next phrases
      if (this.demo.name == 'hst-performance anthem'){
        this.update_next_phrases_demo()
      }
      else{
        this.update_next_phrases()
      }
    },

    get_data_all(){
      let n_songs = 0
      let backend_path = this.BACKEND_PATH
      if (this.DEBUG){
        backend_path = 'http://127.0.0.1:5000'
      }
      axios.get(backend_path + '/get_data_all')
        .then(response => {
              let data_in = response.data
              if (!(data_in[0] > 0)){
                data_in = JSON.parse(response.data)
              }
              this.allData = {'edge_weights': data_in[1][1]}
              this.edge_weights = data_in[1][1]
              n_songs = data_in[0]
              if (this.DEBUG){
                n_songs = 1
              }
              this.n_songs = n_songs

              for (let i=0; i<n_songs; i++){
                if (this.DEBUG){
                  axios.get(backend_path + '/get_data_all_idx', {params: {idx: 5}})
                  .then(response => {
                    this.n_loaded ++
                    let data_in = response.data
                    if (data_in[0] != 0){
                      data_in = JSON.parse(response.data)
                    }
                    let key = data_in[1][0]
                    let val = data_in[1][1]
                    this.allData[key] = val
                    if (Object.keys(this.allData).length == n_songs+1){
                      this.get_data()
                      this.phrasebank_loaded = true
                      this.apply_filter_anchors()
                    }
              })
                  continue
                }
                axios.get(backend_path + '/get_data_all_idx', {params: {idx: i}})
                  .then(response => {
                    this.n_loaded ++
                    let data_in = response.data
                    if (data_in[0] != 0){
                      data_in = JSON.parse(response.data)
                    }
                    let key = data_in[1][0]
                    let val = data_in[1][1]
                    this.allData[key] = val
                    if (Object.keys(this.allData).length == n_songs+1){
                      this.get_data()
                      this.phrasebank_loaded = true
                      this.apply_filter_anchors()
                    }
              })
              }
        })
    },

    get_data_anthem(){
      let n_songs = 0
      let backend_path = this.BACKEND_PATH
      axios.get(backend_path + '/get_data_anthem')
        .then(response => {
              let data_in = response.data
              if (!(data_in[0] > 0)){
                data_in = JSON.parse(response.data)
              }
              this.allData = {'edge_weights': data_in[1][1]}
              this.edge_weights = data_in[1][1]
              n_songs = data_in[0]
              this.n_songs = n_songs

              for (let i=0; i<n_songs; i++){
                axios.get(backend_path + '/get_data_anthem_idx', {params: {idx: i}})
                  .then(response => {
                    this.n_loaded ++
                    let data_in = response.data
                    if (data_in[0] != 0){
                      data_in = JSON.parse(response.data)
                    }
                    let key = data_in[1][0]
                    let val = data_in[1][1]
                    this.allData[key] = val
                    if (Object.keys(this.allData).length == n_songs+1){
                      this.get_data()
                      this.phrasebank_loaded = true
                    }
              })
              }
        })
    },

    // Interfacing (player)
    player_play(){
      if (this.loaded){
        if (this.playing){
          if (this.t % this.STEP_SIZE == 0){
            // Reset at t = 0
            if (this.t == 0){
              
              // Next phrase
              if (this.next_phrase_idx != -1){
                this.get_data(this.next_phrases_id[this.next_phrase_idx], false)
                this.next_phrase_idx = -1
                if (this.demo.name == 'hst-performance anthem'){
                  this.update_next_phrases_demo()
                }
                else{
                  this.update_next_phrases()
                  this.$refs.phrase_selector.reset()
                }
              }
            }
            this.player_query_step()
          }
          if (!this.playing){
            return
          }

          // Next time step
          this.t += 4;
          if (this.t == 16){
              this.t = 0
              
              if (!this.demo.locked && !this.demo.locked1 && this.demo.line < this.demo.phrase_seq.length - 1){
                this.demo.line ++
                this.next_phrase_idx = 0
              }
              if (!this.demo.locked && this.demo.locked1 && !this.demo.lock_passed){
                this.demo.lock_passed = true
                this.demo.line ++
                this.next_phrase_idx = 0
              }
          }
        }
      }
      
    },

    player_reset(){
      this.playing = false
      this.loaded = true
      this.t = 0
      this.altered_noteseq.notes = []
      this.altered_noteseqs = [0,0,0,0]
      this.chord_seq = []
      this.altered_chd_str = Array(16).fill("")
      this.altered_chd_mat =  Array(16).fill(Array(36).fill(0))
      this.altered_vis.redraw()
      this.update_overlay()
    }, 

    player_query_step(){

      // Chord input behaviors
      if (this.demo.name != 'none' && this.demo.line > 1){
        if (this.demo.bar >= this.demo.chord_seq.length){
          this.playing = false
          return
        }
        this.demo.bar ++
        if (this.current_chd == ''){
          if (this.demo.chord_seq[this.demo.bar].includes('s')){
              this.$refs.dial.keydown_functions(
              new KeyboardEvent('keydown', {
                'key': 'z'
              })
            )
            this.$refs.dial.keydown_functions(
              new KeyboardEvent('keydown', {
                'key': this.demo.chord_seq[this.demo.bar].slice(1)
              })
            )
            this.$refs.dial.keyup_functions(
              new KeyboardEvent('keydown', {
                'key': 'z'
              })
            )
          }
          else if (this.demo.chord_seq[this.demo.bar].includes('x')){
              this.$refs.dial.keydown_functions(
              new KeyboardEvent('keydown', {
                'key': 'x'
              })
            )
            this.$refs.dial.keydown_functions(
              new KeyboardEvent('keydown', {
                'key': this.demo.chord_seq[this.demo.bar].slice(1)
              })
            )
            this.$refs.dial.keyup_functions(
              new KeyboardEvent('keydown', {
                'key': 'x'
              })
            )
          }
          else{
            this.$refs.dial.keydown_functions(
              new KeyboardEvent('keydown', {
                'key': this.demo.chord_seq[this.demo.bar]
              })
            )
          }
        }
      }
      if (this.current_chd == ''){
        this.playing = false
        return
      }
      this.playing = true

      // tempo
      let tempo_changes = []
      let window_len
      if (this.demo.bar > -1){
        let slice = this.demo.tempo_curve.slice(this.demo.bar * 4, this.demo.bar * 4 + 4)
        window_len = slice[3][0] - slice[0][0] + 60 / slice[3][1]
        for (let i=0; i<4; i++){
          tempo_changes[i] = [slice[i][0] - slice[0][0] + 0.001, slice[i][1]]
        }
      }
      else{
        [tempo_changes, window_len] = this.get_tempo_changes()
      }
      setTimeout(() => {  this.player_play(); }, window_len * 1000)
      // Update cell highlighting
      for (let i=this.t; i<this.t+4; i++){
        this.highlight_cell("altered"+i, window_len)
      }
      const high_light_step = (time) => {
        this.highlight_cell("time_altered"+time, window_len / 4)
        if (time % 4 == 3){
          return
        }
        setTimeout(() => {
          high_light_step(time+1)
        }, window_len * 250);
      }
      high_light_step(this.t)

      this.bpm = this.next_bpm

      // Clean up at song start
      if (this.t == 0){
        this.altered_chd_str = Array(16).fill("")
        this.altered_chd_mat =  Array(16).fill(Array(36).fill(0))
        this.altered_noteseq.notes = []
        this.altered_noteseqs = [0,0,0,0]
        this.chds = []
      }

      // Clean up at window start
      if (this.t % this.STEP_SIZE == 0){
        this.chord_seq = []
      }
      this.chds.push(this.current_chd)
      this.chord_seq.push(this.current_chd)
      let root = parseInt(this.current_chd.slice(0,-2))
      let chroma = this.current_chd.slice(-2)
      this.altered_chd_str[this.t] = this.current_chd_text

      if (!this.wheel.clutched || !this.wheel.connected){
        // Stop the player at the next query step unless a new chord is entered
        this.current_chd = ''
        this.current_chd_text = ''
      }
      
      // Query and update noteseq
      let chord_seq_maxlen = 8 / this.STEP_SIZE
      let query = []
      for (let i=0; i<this.chord_seq.length; i++){
        query.push(this.chord_seq[i])
      }
      while (query.length < chord_seq_maxlen){
        query.push(query[query.length-1])
      }
      query = query.join(',')
      let note_list = this.notedic[(this.t - this.t%8)/8][query]
      let new_notes = this.list_to_noteseq(note_list, this.t, this.t+this.STEP_SIZE, true)
      new_notes = this.apply_dynamics(new_notes)
      this.altered_noteseq.notes = this.altered_noteseq.notes.concat(new_notes)  
      let quant_note_seq = this.notes_to_quant_noteseq(new_notes)
      let noteseq = unquantizeSequence(quant_note_seq)
      // noteseq = this.apply_articulation(noteseq)

      let This = this
      
      console.log(noteseq)

      if (This.demo.bar >= 0){
        for (let i=0; i<noteseq.notes.length; i++){
          for (let j=0; j<This.demo.sustain.length; j++){
            let sus_start = This.demo.sustain[j][0] - 16 * (This.demo.line - 2)
            let sus_end = This.demo.sustain[j][1] - 16 * (This.demo.line - 2)
            if (noteseq.notes[i].endTime > sus_start && noteseq.notes[i].endTime < sus_end){
              noteseq.notes[i].endTime = sus_end
              break
            }
            if (noteseq.notes[i].endTime < sus_start){
              break
            }
          }
        }
      }

      
      for (let i=0; i<noteseq.notes.length; i++){
        for (let j=0; j<noteseq.notes.length; j++){
          if (noteseq.notes[i].startTime < noteseq.notes[j].startTime && noteseq.notes[i].endTime >= noteseq.notes[j].startTime && noteseq.notes[i].pitch == noteseq.notes[j].pitch){
            noteseq.notes[i].endTime = noteseq.notes[j].startTime - 0.15
          }
        }
        if (noteseq.notes[i].endTime >= 3.9){
          noteseq.notes[i].endTime = 5
        }
      }

      console.log(noteseq)

      // Set tompo curve
      Tone.Transport.bpm.setValueAtTime(60, Tone.Transport.now())
      for (let i=0; i<tempo_changes.length; i++){
        Tone.Transport.bpm.setValueAtTime(tempo_changes[i][1], Tone.Transport.now() + tempo_changes[i][0])
      }
      

      // Restart the player
      if (player.isPlaying()){
        player.stop()
      }
      noteseq.totalTime = 6 
      player.start(noteseq)
      this.altered_noteseqs[(this.t-this.t%4)/4] = this.altered_noteseq


      // Canvas and noteseq
      if (! this.hide_vis_input){
        this.altered_vis.noteSequence = this.altered_noteseq
        this.altered_vis.redraw()
      }

      // Overlay and notemat
      if (this.current_chd.includes('sd') || this.current_chd.includes('xd')){
        root = parseInt(this.current_chd.slice(0,-4))
        chroma = this.current_chd.slice(-2)
      }
      let new_chd_mat = Array(36).fill(0)
      new_chd_mat[root] = 1
      new_chd_mat[24] = 1

      let M3 = [0,4,7]
      let m3 = [0,3,7]
      let M7 = [0,4,7,11]
      let m7 = [0,3,7,10]
      let D7 = [0,4,7,10]
      let chm = 0

      if (chroma == 'M3'){
        chm = M3
      }
      if (chroma == 'm3'){
        chm = m3
      }
      if (chroma == 'M7'){
        chm = M7
      }
      if (chroma == 'm7'){
        chm = m7
      }
      if (chroma == 'D7'){
        chm = D7
      }
      
      let s = 0
      for (let i=0; i<12; i++){
        s = s + new_chd_mat[i]
      }
      if (s == 0){
        new_chd_mat[0] = 1
      }

      for (let i=0; i<chm.length; i++){
        new_chd_mat[(root+chm[i])%12 + 12] = 1
      }
      for (let i=this.t; i<this.t+this.STEP_SIZE; i++)[
        this.altered_chd_mat[i] = new_chd_mat
      ]
      this.update_overlay()

      // Wheel
      if (this.wheel.connected){
        this.$refs.dial_wheel.update_offest(this.wheel.turn_idx)
        this.next_bpm = this.bpm + (this.wheel.gas - this.wheel.brake) * this.wheel.acc_ratio
        this.wheel.wheel_shift_offset = 4 - this.wheel.sheel_shift
        this.wheel.sheel_shift = 0
      }
    },

    notes_to_quant_noteseq(notes){
      let out = createQuantizedNoteSequence(4, 60)
      out.tempos = [{time: 0, qpm: 60}]
      let This = this
      for (let i=0; i<notes.length; i++){
        let note = notes[i]
        let note_start = note.startTime
        let note_end = note.endTime
        if (This.demo.bar >= 0){
          for (let j=0; j<This.demo.sustain.length; j++){
            let sus_start = This.demo.sustain[j][0] - 16 * (This.demo.line - 2)
            let sus_end = This.demo.sustain[j][1] - 16 * (This.demo.line - 2)
            if (note.endTime > sus_start && note.endTime < sus_end){
              note_end = sus_end
              break
            }
            if (note.endTime < sus_start){
              break
            }
          }
        }
        else{
            for (let j=0; j<This.sustain.length; j++){
            let sus_start = This.sustain[j][0]
            let sus_end = This.sustain[j][1]
            if (note.endTime > sus_start && note.endTime < sus_end){
              note_end = sus_end
              break
            }
            if (note.endTime < sus_start){
              break
            }
          }
        }
        
        out.notes.push({pitch:note.pitch, quantizedStartStep:(note_start-this.t)*4, quantizedEndStep:Math.round((note_end-this.t)*4), velocity: note.velocity})
      }
      // Fix note overlaps
      for (let i=0; i<out.notes.length; i++){
        for (let j=0; j<out.notes.length; j++){
          if (out.notes[i].quantizedStartStep < out.notes[j].quantizedStartStep && out.notes[i].quantizedEndStep > out.notes[j].quantizedStartStep){
            out.notes[i].quantizedEndStep = out.notes[j].quantizedStartStep
          }
        }
      }
      return out
    },

    canvas_update_note(note){
      let t = this.t
      if (t == 0){
        t = 16
      }
      let canvas_note = {pitch: note.pitch, startTime: note.startTime + t - 4, endTime: note.endTime + t - 4}
      // console.log(canvas_note)
      if (note.expressive){
        canvas_note = {pitch: note.pitch, startTime: note.quant_startTime*this.bpm/60/4+t-4, endTime: note.quant_endTime*this.bpm/60/4+t-4}
      }
      this.altered_vis.redraw(canvas_note)
    },

    // Expressive dynamics / timing
    apply_dynamics(noteseq){
      let original_notes = this.original_noteseq.notes
      let altered_notes = noteseq

      // Sort everything by start time
      original_notes.sort(function (a,b){return a.startTime - b.startTime})
      altered_notes.sort(function (a,b){return a.startTime - b.startTime})

      // Find the average vel of the original noteseq
      let avg_vel = 0
      for (let i=0; i<original_notes.length; i++){
        avg_vel = avg_vel + original_notes[i].velocity
      }
      avg_vel = Math.floor(avg_vel / original_notes.length)

      // Put notes into time-quantized buckeds
      let original_buckets = [] // of velocities
      let altered_buckets = [] // of indices
      for (let i=0; i<16; i++){
        original_buckets.push([])
        altered_buckets.push([])
      }
      for (let i=0; i<original_notes.length; i++){
        let note = original_notes[i]
        if (note.startTime < this.t || note.startTime >= this.t + 4){
          continue
        }
        original_buckets[Math.round(note.startTime / 0.25) % 16].push(note.velocity)
      }

      for (let i=0; i<altered_notes.length; i++){
        let note = altered_notes[i]
        altered_buckets[note.startTime / 0.25 % 16].push(i)
      }

      for (let i=0; i<16; i++){
        let altered_bucket = altered_buckets[i]
        let original_bucket = original_buckets[i]
        for (let j=0; j<altered_bucket.length; j++){
          let idx = altered_bucket[j]
          if (original_bucket.length == 0){
            if (idx == 0){
              altered_notes[0].velocity = 1
            }
            else{
              altered_notes[idx].velocity = altered_notes[idx - 1].velocity
            }
          }
          else if (altered_bucket.length == original_bucket.length){
            altered_notes[idx].velocity = original_bucket[j]
          }
          else if (j == altered_bucket.length - 1){
            altered_notes[idx].velocity = original_bucket[original_bucket.length - 1]
          }
          else{
            // Interpolate between the closest 2 velo
            let pos = j / altered_bucket.length * original_bucket.length
            let bottom_vel = original_bucket[Math.floor(pos)]
            let top_vel = original_bucket[Math.floor(pos) + 1]
            let bottom_weight = pos % 1
            altered_notes[idx].velocity = bottom_vel * bottom_weight + top_vel * (1 - bottom_weight)
          }
        }
      }

      // Adjust for spread and scale
      for (let i=0; i<altered_notes.length; i++){
        altered_notes[i].velocity = Math.floor(((altered_notes[i].velocity / avg_vel - 1)* this.expressiveness_vel / 100 + 1 ) * 127 * this.velocity_scale/100)
        if (altered_notes[i].velocity > 127){
          altered_notes[i].velocity = 127
        }
        if (altered_notes[i].velocity < 10){
          altered_notes[i].velocity = 38
        }
      }
      return noteseq
    },

    apply_articulation(noteseq){
      let original_notes = this.original_noteseq.notes
      let altered_notes = noteseq.notes

      // Sort everything by start time
      original_notes.sort(function (a,b){return a.startTime - b.startTime})
      altered_notes.sort(function (a,b){return a.startTime - b.startTime})

      // Put notes into time-quantized buckeds
      let original_buckets = [] // of note lengths 
      let altered_buckets = [] // of indices
      for (let i=0; i<16; i++){
        original_buckets.push([])
        altered_buckets.push([])
      }
      for (let i=0; i<original_notes.length; i++){
        let note = original_notes[i]
        if (note.startTime < this.t || note.startTime >= this.t + 4){
          continue
        }
        original_buckets[Math.round(note.startTime / 0.25) % 16].push(note.endTime - note.startTime)
      }

      for (let i=0; i<altered_notes.length; i++){
        let note = altered_notes[i]
        altered_buckets[note.startTime / 0.25 % 16].push(i)
      }

      for (let i=0; i<16; i++){
        let altered_bucket = altered_buckets[i]
        let original_bucket = original_buckets[i]
        for (let j=0; j<altered_bucket.length; j++){
          let idx = altered_bucket[j]
          if (original_bucket.length != 0){
            let dur = altered_notes[idx].endTime - altered_notes[idx].startTime
            if (altered_bucket.length == original_bucket.length){
              altered_notes[idx].endTime = ((original_bucket[j]/dur - 1) * this.expressiveness_dur / 100 + 1) * dur + altered_notes[idx].startTime
            }
            else if (j == altered_bucket.length - 1){
              altered_notes[idx].endTime = ((original_bucket[original_bucket.length - 1]/dur - 1) * this.expressiveness_dur / 100 + 1) * dur + altered_notes[idx].startTime
            }
            else{
              // Interpolate between the closest 2 dur
              let pos = j / altered_bucket.length * original_bucket.length
              let bottom_vel = original_bucket[Math.floor(pos)]
              let top_vel = original_bucket[Math.floor(pos) + 1]
              let bottom_weight = pos % 1
              let dur_rate = bottom_vel * bottom_weight + top_vel * (1 - bottom_weight)
              altered_notes[idx].endTime = ((dur_rate/dur - 1) * this.expressiveness_dur / 100 + 1) * dur + altered_notes[idx].startTime
            }
          }
        }
      }

      // Sustain the notes who end at step end
      for (let i=0; i<altered_notes.length; i++){
        if (altered_notes[i].endTime == 4){
          altered_notes[i].endTime = 8
        }
      }
      return noteseq
    },

    get_tempo_changes(){
      // Calculate the tempo changes for the phrase, then return the relative part

      // let notes = this.original_noteseq_mel.notes
      // notes.sort(function (a,b){return a.startTime - b.startTime})

      // let out = [] //[[onset_step, lengthened], ...]
      // for (let i=0; i<notes.length; i++){
      //   let note = notes[i]
      //   let dur = Math.round((note.endTime - note.startTime)/0.25)
      //   let lengthened = false
        
      //   // TL1
      //   if (i > 0 && i < notes.length - 1){
      //     let pre_dur = Math.round((notes[i-1].endTime - notes[i-1].startTime)/0.25)
      //     let next_dur = Math.round((notes[i+1].endTime - notes[i+1].startTime)/0.25)
      //     if (pre_dur == dur && next_dur > dur){
      //       lengthened = true
      //     }
      //   }

      //   // TL2
      //   if (i < notes.length - 1){
      //     let next_dur = Math.round((notes[i+1].endTime - notes[i+1].startTime)/0.25)
      //     if (next_dur >= dur * 3){
      //       lengthened = true
      //     }
      //   }

      //   out.push([Math.round(note.startTime/0.25), lengthened])
      // }

      let notes = this.original_noteseq.notes
      notes.sort(function (a,b){return a.startTime - b.startTime})

      let out = [] //[[onset_step, lengthened], ...]
      let bins = []
      let sum_velo = 0
      for (let i=0; i<65; i++){
        bins.push([])
      }
      for (let i=0; i<notes.length; i++){
        let note = notes[i]
        sum_velo = sum_velo + note.velocity
        bins[Math.round(note.startTime/0.25)].push(note.velocity)
      }
      let avg_velo = sum_velo / notes.length

      for (let i=0; i<65; i++){
        let sum = bins[i].reduce((a, b) => a + b, 0);
        if (sum < avg_velo * bins[i].length){
          out.push([i, true])
        }
        else if(bins[i].length > 0){
          out.push([i, false])
        }
      }

      // convert out to bpm changes
      let bpm_changes = [[0.001, this.bpm]] // [[time(second), bpm, step], ...]
      let t = 0
      let cur_step = 0
      let slowed = 0
      let bpm = this.bpm
      let slice_len = [-1, -1, -1, -1]

      for (let i=0; i<out.length; i++){
        let step = out[i][0]
        let lengthened = out[i][1]
        
        for (let j=0; j<4; j++){
          if (slice_len[j] == -1 && step > 16 + 16 * j){
            slice_len[j] = t + (16 + 16 * j - cur_step) * 15 / bpm
          }
        }

        t += (step - cur_step) * 60 / bpm / 4

        if (i == out.length - 1){
          slice_len[3] = t + 15 / bpm * (64 - step)
        }

        if (lengthened){
          // Slow down
          bpm /= (0.015 * this.expressiveness_tempo / 100) + 1
          slowed += 1
          bpm_changes.push([t, bpm, step])
        }
        else if(!lengthened && slowed > 0){
          // Speed up
          bpm *= ((0.015 * this.expressiveness_tempo / 100) + 1) ** slowed
          slowed = 0
          bpm_changes.push([t, bpm, step])
        }
        cur_step = step
      }

      for (let j=0; j<4; j++){
        if (slice_len[j] == -1){
          slice_len[j] = slice_len[j-1] + 240 / bpm
        }
      }
      
      let changes_out = [[0.001, this.bpm, 0]]
      for (let i=0; i<bpm_changes.length; i++){
        let [t, bpm, step] = bpm_changes[i]
        
        if (this.t == 0){
          if (t < slice_len[0] && t != 0.001){
            changes_out.push([t, bpm, step % 16])
          } 
        }
        else{
          if (t <= slice_len[this.t / 4 - 1]){
            changes_out[0][1] = bpm
          }
          if (t > slice_len[this.t / 4 - 1] && t < slice_len[this.t / 4]){
            t -= slice_len[this.t / 4 - 1]
            changes_out.push([t, bpm, step % 16])
          }
        }
      }

      for (let j=3; j > 0; j--){
        slice_len[j] -= slice_len[j-1]
      }

      changes_out.push([0, this.next_bpm, 16])

      for (let i=0; i<changes_out.length; i++){
        let step = changes_out[i][2]
        let ratio = ((this.next_bpm - this.bpm) / this.bpm) * (step / 16) + 1
        changes_out[i][1] *= ratio
      }
      let dense_changes = [] //[bpm, ...]
      // Interpolate 
      for (let i=0; i < 16; i++){
        let before_step = 0
        let before_bpm = 0
        let after_step = 0
        let after_bpm = 0
        for (let j=0; j < changes_out.length; j++){
          let step = changes_out[j][2]
          let bpm = changes_out[j][1]

          if (step <= i){
            before_step = step
            before_bpm = bpm
          }
          if (step >= i){
            after_step = step
            after_bpm = bpm
            break
          }
        }
        if (before_step == after_step){
          dense_changes.push(before_bpm)
        }
        else{
          let r_before = (i - before_step) / (after_step - before_step)
          dense_changes.push(before_bpm * r_before + (1 - r_before) * after_bpm)
        }
      }

      let out_out = [[0.001, this.bpm]]
      // Convert into continuous changes
      let cur_t = 0
      for (let i = 1; i < 16; i ++){
        let prev_bpm = out_out[i-1][1]
        cur_t += 15 / prev_bpm
        out_out.push([cur_t, dense_changes[i]])
      }
      cur_t += 15 / dense_changes[15]
        
      return [out_out, cur_t]
    },

    // Interfacing (input type)
    change_input_type(type){
      this.input_type = type
    },
    change_key(key){
      this.key = key
      this.$refs.dial.draw_dial(this.$refs.dial.outer_text(key))
    },
    update_current_chord(chd, text){
      this.current_chd = chd
      this.current_chd_text = text
      if (!this.playing){
        this.playing = true
        this.player_play()
      }
      else{
        // Pre-update overlays and chord texts
        // Overlay and notemat
        let root
        let chroma
        if (this.current_chd.includes('sd') || this.current_chd.includes('xd')){
          root = parseInt(this.current_chd.slice(0,-4))
          chroma = this.current_chd.slice(-2)
        }
        else{
          root = parseInt(this.current_chd.slice(0,-2))
          chroma = this.current_chd.slice(-2)
        }
        let new_chd_mat = Array(36).fill(0)
        let t = this.t
        new_chd_mat[root] = 1
        new_chd_mat[root+24] = 1

        let M3 = [0,4,7]
        let m3 = [0,3,7]
        let M7 = [0,4,7,11]
        let m7 = [0,3,7,10]
        let D7 = [0,4,7,10]
        let chm = 0

        if (chroma == 'M3'){
          chm = M3
        }
        if (chroma == 'm3'){
          chm = m3
        }
        if (chroma == 'M7'){
          chm = M7
        }
        if (chroma == 'm7'){
          chm = m7
        }
        if (chroma == 'D7'){
          chm = D7
        }

        for (let i=0; i<chm.length; i++){
          new_chd_mat[(root+chm[i])%12 + 12] = 1
        }
        for (let i=t; i<t+this.STEP_SIZE; i++)[
          this.altered_chd_mat[i] = new_chd_mat
        ]
        this.update_overlay()

        // Text
        this.altered_chd_str[t] = this.current_chd_text
        }
    },

    // Overlays
    draw_overlay_bar(svg, x, pitch, color){
      x *= 100;
      while (pitch <= 90){
          if (pitch >= 30){
              svg.append('rect')
              .attr('fill', color)
              .attr('opacity', 0.3)
              .attr('x', x)
              .attr('y', this.cfg.noteHeight * (this.cfg.maxPitch - pitch))
              .attr('width', 100)
              .attr('height', 4)
              .attr('class', 'overlay');
          }
          pitch += 12;
      }
    },
    clear_overlay(){
      d3.selectAll(".overlay").remove().exit()
    },
    get_color(pitch){
      return d3.interpolateSinebow((pitch/12+0.6)%1)
    },
    draw_root_overlay(){
      for (let i=0; i<this.original_chd_mat.length; i++){
        let chd = this.original_chd_mat[i];
        let root = chd.slice(0,12).indexOf(1);
        this.draw_overlay_bar(d3.select(".original_svg"), i, root, this.get_color(0));
        if (this.altered_chd_mat[i].slice(0,12).indexOf(1) >= 0 && ! this.hide_vis_input){
            this.draw_overlay_bar(d3.select(".swapped_svg"), i, this.altered_chd_mat[i].slice(0,12).indexOf(1), this.get_color(0));
        }
      }
    },
    draw_chord_overlay(){
      for (let i=0; i<this.original_chd_mat.length; i++){
        let chd = this.original_chd_mat[i];
        let root = chd.slice(0,12).indexOf(1);
        for (let j=0; j<12; j++){
          if (chd[12+j] == 1){
              this.draw_overlay_bar(d3.select(".original_svg"), i, j, this.get_color((j-root)%12));
          }
          if (this.altered_chd_mat[i][12+j] == 1  && ! this.hide_vis_input){
              this.draw_overlay_bar(d3.select(".swapped_svg"), i, j, this.get_color((j-this.altered_chd_mat[i].slice(0,12).indexOf(1))%12));
          }
        }
      }
    },
    update_overlay(){
      this.clear_overlay()
      if (this.chord_overlay){
        this.draw_chord_overlay()
      }
      else if (this.root_overlay){
        this.draw_root_overlay()
      }
    },
    root_on_click(){
      if (this.root_overlay){
        this.root_overlay = false
      }
      else {
        this.root_overlay = true
      }
      this.update_overlay()
    },
    chord_on_click(){
      if (this.chord_overlay){
        this.chord_overlay = false
      }
      else {
        this.chord_overlay = true
      }
      this.update_overlay()
    },

    // Place barlines / original player
    draw_barlines_original(){
      d3.selectAll(".barline_original").remove().exit()
      let top_rect = document.getElementById("time0").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog0").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.bottom + window.pageYOffset || document.documentElement.scrollTop

      for (let i=1; i<4; i++){
          d3.selectAll("#original_barline")
          .append('rect')
          .attr('x', l1 + i*4*(l2-l1))
          .attr('y', t)
          .attr('width', 3)
          .attr('height', b-t)
          .attr('class', 'barline barline_original')
      }
    },
    draw_barlines_altered(){
      d3.selectAll(".barline_altered").remove().exit()

      let top_rect = document.getElementById("time_altered0").getBoundingClientRect();
      let bottom_rect = document.getElementById("altered10").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.bottom + window.pageYOffset || document.documentElement.scrollTop

      for (let i=1; i<4; i++){
          d3.selectAll("#altered_barline")
          .append('rect')
          .attr('x', l1 + i*4*(l2-l1))
          .attr('y', t)
          .attr('width', 3)
          .attr('height', b-t)
          .attr('class', 'barline barline_altered')
        }
    },
    place_player_original(){
      let top_rect = document.getElementById("time15").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog15").getBoundingClientRect();

      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.top + window.pageYOffset || document.documentElement.scrollTop

      d3.select("#original_player")
      .style("position","absolute")
      .style("left",l2+"px")
      .style("top", (t+2.5*b)/3.5+"px")
      .style("-webkit-transform","scale(0.75)")
      .raise()
    },
    place_barlines_and_player(){
      this.draw_barlines_original()
      this.draw_barlines_altered()
      this.place_player_original()
      this.place_melacc_toggle()
    },

    // Mel/Acc toggle
    mel_on_click(){
      this.mel = ! this.mel
      if (! this.mel && ! this.acc){
        this.acc = true
      }
      this.update_melacc_toggle()
    },
    acc_on_click(){
      this.acc = ! this.acc
      if (! this.acc && ! this.mel){
        this.mel = true
      }
      this.update_melacc_toggle()
    },
    update_melacc_toggle(){
      if (this.mel && this.acc){
        this.notedic = this.notedic_mixed
        this.original_noteseq = this.original_noteseq_mixed
        this.original_noteseq_overlay = this.original_noteseq_mel
      }
      else if (this.mel){
        this.notedic = this.notedic_mel
        this.original_noteseq = this.original_noteseq_mel
        this.original_noteseq_overlay = this.empty_noteseq
      }
      else{
        this.notedic = this.notedic_acc
        this.original_noteseq = this.original_noteseq_acc
        this.original_noteseq_overlay = this.empty_noteseq
      }
    },
    place_melacc_toggle(){
      let top_rect = document.getElementById("time15").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog15").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.top + window.pageYOffset || document.documentElement.scrollTop

      d3.select("#melacc_toggle")
      .style("position","absolute")
      .style("left",l2+(l2-l1)/4+"px")
      .style("top", (1.15*t+b)/2.15+"px")
      .style("-webkit-transform","scale(0.6)")
      .raise()
    },

    // Chord playback
    play_chord(track, i){
      player.stop()
      let highlight_start = 0
      let highlight_end = 16
      if (track == 'original'){
        player.start(this.chords_to_noteseq([this.original_chd_mat[i]], false))
        for (let j=0; j<16; j++){
          if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") != '' && j > i){
            highlight_end = j
            break
          }
          if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") != ''){
            highlight_start = j
          }
        }
        for (let j=highlight_start; j<highlight_end; j++){
          this.highlight_cell("original_prog"+j, 0.5)
        }
      }
      if (track == 'altered'){
        highlight_start = i - i%4
        for (let j=highlight_start; j<highlight_start+4; j++){
          this.highlight_cell("altered"+j, 0.5)
        }
        player.start(this.chords_to_noteseq([this.altered_chd_mat[i]], false))
      }

      
    },

    play_prog_original(){
      player.stop()
      player.start(this.chords_to_noteseq(this.original_chd_mat, false))
      let i = 0
      const high_light_step = () => {
        if (i < 16){
          this.highlight_cell("time"+i, this.prog_step_duration)
          if (document.getElementById("original_prog"+i).innerHTML.replace(/\s/g,"") != ''){
            let t = 1
            for (let j=i+1; j<16; j++){
              if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") == ''){
                t++
              }
              else{
                break
              }
            }
            for (let j=i; j<i+t; j++){
              this.highlight_cell("original_prog"+j, t*this.prog_step_duration)
            }
          }
          i++
          setTimeout(() => {
            high_light_step()
          }, this.prog_step_duration*1000);
        }
      }
      high_light_step()
      
    },

    play_prog_altered(){
      player.stop()
      player.start(this.chords_to_noteseq(this.altered_chd_mat, false))
      let i = 0
      const high_light_step = () => {
        if (i < 16){
          if (i%4 == 0 && this.altered_chd_str[i] == ''){return}
          this.highlight_cell("time_altered"+i, this.prog_step_duration)
          if (this.altered_chd_str[i] != ''){
            for (let j=i; j<i+4; j++){
              this.highlight_cell("altered"+j, 4*this.prog_step_duration)
            }
          }
          i++
          setTimeout(() => {
            high_light_step()
          }, this.prog_step_duration*1000);
        }
      }
      high_light_step()
    },

    // Chord/Time cell highlighting
    highlight_cell(id, t){
      document.getElementById(id).classList.add("cell_active")
      setTimeout(() => {
        document.getElementById(id).classList.remove("cell_active")
      }, t*1000);
    },

    // Time cell click
    replay_bar(step, len=1, bypass_check=false){
      if ((! this.loaded || this.playing) && ! bypass_check){
        return
      } 
      let t = this.t
      let bar = (step - step%4) / 4
      if (this.altered_noteseqs[bar] == 0){
        this.loaded = true
        return
      }
      // Lock this.t
      this.loaded = false
      this.t = (bar+1) * 4
      this.altered_noteseqs[bar].totalQuantizedSteps = 16
      if (player.isPlaying()){
        player.stop()
      }
      player.start(this.altered_noteseqs[bar], this.bpm)

      // Dirty fix
      setTimeout(() => {
        if (!player.isPlaying()){
          player.start(this.altered_noteseqs[bar], this.bpm)
        }
      }, 5)
      setTimeout(() => {
        if (!player.isPlaying()){
          player.start(this.altered_noteseqs[bar], this.bpm)
        }
      }, 10)
      setTimeout(() => {
        if (!player.isPlaying()){
          player.start(this.altered_noteseqs[bar], this.bpm)
        }
      }, 15)
      setTimeout(() => {
        if (!player.isPlaying()){
          player.start(this.altered_noteseqs[bar], this.bpm)
        }
      }, 30)
      setTimeout(() => {
        if (!player.isPlaying()){
          player.start(this.altered_noteseqs[bar], this.bpm)
        }
      }, 50)

      // Time/prog cell highlighting
      const high_light_step = (time) => {
        this.highlight_cell("time_altered"+time, 4*250*60/this.bpm/1000)
        if (time % 4 == 3){
          return
        }
        setTimeout(() => {
          high_light_step(time+1)
        }, 4*250*60/this.bpm);
      }
      high_light_step(this.t-4)

      for (let i=this.t-4; i<this.t; i++){
        this.highlight_cell("altered"+i, 16*250*60/this.bpm/1000)
      }
      
      // Unlock this.t
      setTimeout(() => {
        this.t = t
        len --
        if (len > 0){
          if (player.isPlaying()){
            player.stop()
          }
          this.replay_bar(step+4, len, true)
        }
        else{
          this.loaded = true
        }
      }, 16*250*60/this.bpm)
    },

    replay_all(){
      this. replay_bar(2, 4)
    },

    // Test mode
    test_add(){
      if (this.altered_noteseqs[3] == 0){
        return
      }
      this.test_chd_strs.push(this.altered_chd_str)
      this.test_chds.push(this.chds)
    },

    test_apply(){
      if (this.playing || this.test_chd_strs.length == 0){
        return
      }
      let idx = Math.floor(Math.random() * this.test_chd_strs.length)

      // Hide things
      this.hide_vis_input = true
      this.altered_chd_str_hide = this.test_chd_strs[idx].slice()
      this.altered_vis.noteSequence = {notes: [{pitch: 30, start:0, end:8}], totalTime:16}
      this.test_idx = idx

      const step = (i) => {
        this.update_current_chord(this.test_chds[idx][i], this.test_chd_strs[idx][i*4])
        if (i == 0){
            setTimeout(() => {
            step(i + 1)
          }, 15*250*60/this.bpm);
        }
        else if (i < 3){
          setTimeout(() => {
            step(i + 1)
          }, 16*250*60/this.bpm);
        }
      }

      this.player_reset()
      step(0)
    },

    test_show_answer(){
      if (! this.hide_vis_input || this.playing){
        return
      }
      this.hide_vis_input = false
      this.altered_chd_str = this.altered_chd_str_hide.slice()
      this.update_overlay()
      this.altered_vis.noteSequence = this.altered_noteseq
      this.altered_vis.redraw()
    },
    
    test_clear(){
      this.test_chd_strs = []
      this.test_chds = []
      this.altered_chd_str_hide = []
      this.test_idx = -1
      this.hide_vis_input = false
    },

    // Next phrase selector
    update_next_phrases(){
      if (this.filter_h == -1){
        // Get the index for the current phrase
        let samples = this.edge_weights.samples
        let song_idx = 0
        for (let i=0; i<samples.length; i++){
          if (samples[i] == this.songID){
            song_idx = i
            break
          } 
        }

        let weights = []
        for (let i=0; i<this.edge_weights.mat[song_idx].length; i++){
          weights.push(this.edge_weights.mat[song_idx][i])
        }

        for (let i=0; i<3; i++){
          // Select next phrases with the highest transition scores
          let next_idx = weights.indexOf(Math.max(...weights))
          weights[next_idx] = -999

          let id = samples[next_idx]
          if (id == this.songID){
            i --
            continue
          }
          this.next_phrases_id[i] = id
          this.next_phrases[i] = this.allData[id].original_noteseq_acc
        }
      }
      
      else{
        // Rank the phrases by the L2 distnce to the filter values
        let dist_dic = {}
        let dists = []
        for (let i=0; i<this.edge_weights.samples.length; i++){
          let sample = this.allData[this.edge_weights.samples[i]]
          let dist = (sample['hd'] - this.filter_h) ** 2 + (sample['vd'] - this.filter_v) ** 2
          if (! (dist in dist_dic) ){
            dist_dic[dist] = [i]
            dists.push(dist)
          }
          else{
            dist_dic[dist].push(i)
          }
        }

        let c = 0
        dists.sort()
        for (let i=0; i<dists.length; i++){
          for (let j=0; j<dist_dic[dists[i]].length; j++){
            let id = this.edge_weights.samples[dist_dic[dists[i]][j]]
            this.next_phrases_id[c] = id
            this.next_phrases[c] = this.allData[id].original_noteseq_acc
            c ++
            if (c > 3){
              return
            }
          }
        }
      }

      // for (let i=0; i<5; i++){
      //   // Randomly select a next phrase
      //   let keys = Object.keys(this.allData).slice(1)
      //   let id = keys[Math.floor(Math.random() * keys.length)]
      //   this.next_phrases_id[i] = id
      //   this.next_phrases[i] = this.allData[id].original_noteseq_acc
      // }
    },

    update_next_phrase(i){
      this.next_phrase_idx = i
    },

    update_next_phrases_demo(){
      let id = this.demo.phrase_seq[this.demo.line + 1]
      this.next_phrases_id[0] = id
      this.next_phrases[0] = this.allData[id].original_noteseq_acc
    },

    // Next phrase filter
    set_filter(filter){
      this.filter_h = filter[0]
      this.filter_v = filter[1]
      this.update_next_phrases()
    },

    apply_filter_anchors(){
      let vds = []
      let hds = []
      for (let i=0; i<this.edge_weights.samples.length; i++){
        let sample = this.allData[this.edge_weights.samples[i]]
        vds.push(sample['vd'])
        hds.push(sample['hd'])
      }
      vds.sort()
      hds.sort()
      let anchors_v = [vds[6], vds[12], vds[18], vds[24]]
      let anchors_h = [hds[6], hds[12], hds[18], hds[24]]
      for (let i=0; i<this.edge_weights.samples.length; i++){
        let vd_q = 4
        let hd_q = 4
        let sample = this.allData[this.edge_weights.samples[i]]
        let vd = sample['vd']
        let hd = sample['hd']
        for (let i=3; i>=0; i--){
          if (vd < anchors_v[i]){
            vd_q = i
          }
          if (hd < anchors_h[i]){
            hd_q = i
          }
        }
        sample['vd'] = vd_q
        sample['hd'] = hd_q
      }
    },

    // MIDI output
    connect_midi(){
      WebMidi
        .enable()
        .then(()=>{
          this.midi_device_names = []
          this.show_midi_devices = true
          WebMidi.outputs.forEach(output => this.midi_device_names.push(output.name))
          this.midi_device = WebMidi.outputs[1]
        })
        .catch(err => alert(err));
    },

    output_midi(note){
        console.log(Tone.Transport.bpm.value)
        let dur = (note.endTime - note.startTime)*60000/Tone.Transport.bpm.value
        if (dur > 2 *60000/Tone.Transport.bpm.value){
          dur = 2 *60000/Tone.Transport.bpm.value
        }
        if (this.show_midi_devices){
          this.midi_device.channels[this.midi_channel].playNote(note.pitch, {duration: dur, attack: note.velocity/128})
        }
        console.log(note.pitch, {duration: dur, attack: note.velocity/128})
      },

    change_midi_channel(i){
      this.midi_channel = i
    },

    follow_tempo(){
      this.next_bpm = this.bpm
    },

    // Wheel
    apply_velo(){
      // // Adjust velo
      // this.next_bpm += (this.wheel.gas - this.wheel.brake)
      
      // // if (this.wheel.velo < 0){
      // //   this.wheel.velo += this.wheel.drag
      // //   if (this.wheel.velo > 0){
      // //     this.wheel.velo = 0
      // //   }
      // // }

      // // if (this.wheel.velo > 0){
      // //   this.wheel.velo -= this.wheel.drag
      // //   if (this.wheel.velo < 0){
      // //     this.wheel.velo = 0
      // //   }
      // // }

      // // this.next_bpm += this.wheel.velo
      // if (this.next_bpm < 30){
      //   this.next_bpm = 30
      // }
      // if (this.next_bpm > 200){
      //   this.next_bpm = 200
      // }
      // // console.log(this.wheel.velo)

      // setTimeout(() => {  this.apply_velo(); },  100)
      
    },

    apply_wheel_shift(){
      let idx = this.wheel.wheel_shift - 1
      if (idx > -1){
        this.$refs.phrase_selector.phrase_on_click(idx)
      }
      else{
        this.$refs.phrase_selector.reset()
      }
    }

  },


  mounted(){
    // Demo versions
    if (this.demo.name == 'none'){
      this.demo.name = document.querySelector('title').innerHTML
      if (this.demo.name != 'hst-performance anthem'){
        this.demo.name = 'none'
      }
    }

    this.get_songdata()

    if (this.demo.name == 'hst-performance anthem'){
      this.get_data_anthem()
    }
    else{
      this.get_data_all()
    }
    player.loadAllSamples().then(()=>{ 
        this.loaded = true
        this.altered_noteseq.notes = []
    })
    
    let This = this
    player.callbackObject = {
        run: (note) => {
          This.canvas_update_note(note)
          This.output_midi(note)
          },
        stop: () => {return}
        };

    // Barlines and player positioning
    window.onresize = this.place_barlines_and_player
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (event) => {
      let key = event.key
      if (['e','E'].includes(key)){
        this.player_reset()
      }
      if (['n','N'].includes(key)){
        this.get_data()
      }
      if (['t','T'].includes(key)){
        this.test_apply()
      }
      if (['s','S'].includes(key)){
        this.test_show_answer()
      }
      if (['a','A'].includes(key)){
        this.test_add()
      }
      if (['r','R'].includes(key)){
        this.replay_all()
      }
      if (['l','L'].includes(key)){
        if (this.demo.locked){
          this.demo.locked = false
        }
      }
      if (['k','K'].includes(key)){
        if (this.demo.locked1 && ! this.demo.locked){
          this.demo.locked1 = false
        }
      }
      if ([' '].includes(key)){
        event.preventDefault()
      }
      if (['m'].includes(key)){
        console.log = function() {}
        this.midi_device = 0
      }
    })

    // Mouse wheel
    // document.addEventListener('wheel', (event) => {
    //   if (this.next_bpm > 30 && this.next_bpm < 200){
    //     event.preventDefault()
    //     this.next_bpm -= event.deltaY / 102
    //   }
    // },
    // {
    //   passive: false 
    // })

    // Cell highlighting - original (copied form educational)
    const mutationObserver_config = { childList: true, subtree: true, attributes:true };
    let original_timer = document.getElementById("original_player").shadowRoot.querySelector(".current-time")
    let original_controls = document.getElementById("original_player").shadowRoot.querySelector(".controls")

    function original_cell_highlight(time_cell, prog_cell, step=1){
        if (time_cell){
            time_cell.classList.add("time_cell_active")
            setTimeout(() => {
                if (time_cell.classList.contains("time_cell_active")){
                    time_cell.classList.remove("time_cell_active")
                }
            }, step*1000);
            if (! prog_cell.classList.contains("table_cell_active")){
                prog_cell.classList.add("table_cell_active")
                let lighted_cells = [prog_cell]
                let timeout = step
                let temp_cell = document.getElementById("original_prog"+(lighted_cells[lighted_cells.length-1].id.slice(13,15)*1+1))
                
                while (temp_cell && temp_cell.innerHTML.replace(/\s/g, '')==""){
                    temp_cell.classList.add("table_cell_active")
                    lighted_cells.push(temp_cell)
                    temp_cell = document.getElementById("original_prog"+(lighted_cells[lighted_cells.length-1].id.slice(13,15)*1+1))
                    timeout += step
                }
                setTimeout(() => {
                    while (lighted_cells.length > 0){
                        let cell = lighted_cells.pop()
                        if (cell.classList.contains("table_cell_active")){
                            cell.classList.remove("table_cell_active")
                        }
                    }
                }, timeout*1000);
            }
        }
    }

    let original_callback = function(mutationsList, observer) {
        observer == observer
        for(var mutation of mutationsList) {
          mutation == mutation
            if (original_controls.classList.contains("playing")){
                let time_cell = document.getElementById("time"+(original_timer.innerHTML.slice(2,4)*1))
                let prog_cell = document.getElementById("original_prog"+(original_timer.innerHTML.slice(2,4)*1))
                original_cell_highlight(time_cell, prog_cell)
            }
        }
    };

    let original_observer = new MutationObserver(original_callback);
    original_observer.observe(original_controls, mutationObserver_config);

    // Wheel
    This.apply_velo()
    var faye_client = new Faye.Client('http://127.0.0.1:8001/');
    faye_client.subscribe('/messages', function(message){

      This.wheel.connected = true
      This.change_input_type('movable')

      // Pedal
      if (message.type == 'gas'){
        This.wheel.gas = message.value 
        This.next_bpm = This.bpm + (This.wheel.gas - This.wheel.brake) * This.wheel.acc_ratio
      }

      if (message.type == 'brake'){
        This.wheel.brake = message.value 
        This.next_bpm = This.bpm + (This.wheel.gas - This.wheel.brake) * This.wheel.acc_ratio
      }

      if (message.type == 'clutch'){
        This.wheel.clutched = !This.wheel.clutched
        if (!This.wheel.clutched){
          // Stop the player at the next query step unless a new chord is entered
          This.current_chd = ''
          This.current_chd_text = ''
        }
        else if (!This.playing && This.input_type == 'movable'){
          This.$refs.dial_wheel.outer_on_click(0)
        }
      }

      // Wheel
      if (message.type == 'wheel_turn'){
        if (This.input_type == 'movable'){
          This.wheel.turn_idx = message.value
          This.$refs.dial_wheel.outer_on_click(message.value)
        }
      }

      // Shift
      if (message.type == 'shift'){
        let val = message.value
        if (val == 1){
          This.$refs.phrase_filter_wheel.set_circle(50, 50)
        }
        if (val == 2){
          This.$refs.phrase_filter_wheel.set_circle(50, 150)
        }
        if (val == 3){
          This.$refs.phrase_filter_wheel.set_circle(150, 50)
        }
        if (val == 4){
          This.$refs.phrase_filter_wheel.set_circle(150, 150)
        }
        if (val == 5){
          This.$refs.phrase_filter_wheel.set_circle(250, 50)
        }
        if (val == 6){
          This.$refs.phrase_filter_wheel.set_circle(250, 150)
        }
        if (val == 0){
          This.$refs.phrase_filter_wheel.reset()
        }
      }

      if (message.type == 'wheel_shift'){
        This.wheel.wheel_shift = (message.value + This.wheel.wheel_shift_offset) % 4
        This.apply_wheel_shift()
      }
    })
 },

}


</script>

<style>
/* General / Misc */
#main_app{
  transform-origin: top left;
  -webkit-transform: scale(0.6);
  position: relative;
  left: 100px;
}

.right{
    position: relative;
    left: 100px;
}

.popover{
  max-width: 100% !important;
}

/* Prog Table */
.prog_table{
    width: 1900px !important;
}

.prog_head{
    text-align: center;
    vertical-align: text-top;
    width:100px;
    font-weight: bold;
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

.prog_repos{
    position: relative;
    top: 5px;}

.time_cell{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    text-align: left;
    width: 100px;
}

.time_cell_active{
    background-color: #80b8f5 !important
}

.table_cell{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    text-align: left;
    width: 100px;
}

.table_tail{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    text-align: left;
}

.table_cell_active{
    background-color: #80b8f5 !important;
    animation-name: table_cell_active_ani;
    animation-duration: 1s;
}

/* Barlines //////////////////////////////////////////////////////////////////////////////// */
.barline_svg{
    position: absolute;
    top: 0px;
    left: 0px;
    width: 1600px;
    height: 1000px;
    pointer-events: none;
}

.barline{
    fill: black;
    opacity: 0.1;
}

/* Piano Roll Overlay //////////////////////////////////////////////////////////////////// */
canvas{
    display: block;
}

.svg{
    position: relative;
    top: -280px;
    width: 1600px;
    height: 280px;
}

.up{
    position:relative;
    top: -280px
}

#original_vis_overlay{
  opacity: 0.85;
}

/* Bpm and vel_scale slider ////////////////////////////////////////////////////////////////////////////////// */
.slider{
    position: relative;
    top: 15px;
    -webkit-appearance: none;
    width: 300px;
    height: 10px;
    background: #d3d3d3;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
}

.slider:hover {
    opacity: 1;
  }
  
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 25px;
    height: 25px;
    background: #80b8f5;
    cursor: pointer;
    stroke-width: 0px;
}
  
.slider::-moz-range-thumb {
    width: 25px;
    height: 25px;
    background: #80b8f5;
    cursor: pointer;
    stroke-width: 0px;
}

.slider_container{
    height: 50px;
}

/* hover dropdown menus //////////////////////////////////////////////////////////////////////////////////////*/
@media only screen and (max-width: 991px) {
    .navbar-hover .show > .dropdown-toggle::after{
        transform: rotate(-90deg);
    }
}
@media only screen and (min-width: 992px) {
    .navbar-hover .collapse ul li{position:relative;}
    .navbar-hover .collapse ul li:hover> ul{display:block}
    .navbar-hover .collapse ul ul{position:absolute;top:100%;left:0;min-width:250px;display:none}
    .navbar-hover .collapse ul ul ul{position:absolute;top:0;left:100%;min-width:250px;display:none}
}

#resample{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    padding-left: 10%;
}

#browse_samples{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

.dropdown{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

/* Cell highlighting //////////////////////////////////////////////////////////////// */
.cell_active{
  background-color: #80b8f5 !important
}

/* Test //////////////////////////////////*/
.test_correct{
  color: #0c9600
}

.no_click{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

#phrase_select_wheel{
    position:relative;
    top: -1170px
}
</style>
