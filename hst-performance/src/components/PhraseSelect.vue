<template>
  <div class="up">
     <table id="phrase_table" class="table table-bordered table-fixed">
      <tbody>
        <tr v-for="i in 3" v-bind:key="i" v-bind:id="'phrase_'+i"
          v-on:click="phrase_on_click(i-1)" 
          v-bind:class="{'phrase_cell':true, 
                          'selected': i-1 == next_phrase_idx
                          }" >
          <td>
            <midi-visualizer type="piano-roll" id="vis[i-1]" v-bind:noteSequence="noteseqs[i-1]" v-bind:config="cfg"></midi-visualizer>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
export default {
  name: 'PhraseSelect',

  props:{
    noteseqs: Array,
  },

  data: function(){
    return{
      next_phrase_idx: -1,

      cfg: {
        noteHeight: 2,
        pixelsPerTimeStep: 40,
        minPitch: 35,
        maxPitch: 80,
        noteSpacing: 0.5
      },
    }
  },

  computed: {
  },

  methods: {
    reset(){
      this.next_phrase_idx=-1
    },

    // Clicks
    phrase_on_click(i){
      this.next_phrase_idx = i
      this.$emit('update_next_phrase', i)
    },

    // Keyboard inputs
    keyboard_functions(event){ 
      let key = event.key
      // console.log(key)
      return key
    }
  },

  mounted(){
    // Handle keyboard inputs
    document.addEventListener('keydown', this.keyboard_functions)
  },
  
  beforeUnmount() {
    document.removeEventListener('keydown', this.keyboard_functions);
  }

}
</script>

<style scoped>
#phrase_table{
    width: 650px !important;
}

.phrase_cell{
    width: 60px;
    text-anchor: middle;
    text-align: left;
    vertical-align: middle !important;
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

.phrase_cell:hover{
    background-color: #a2cbf7;
}

.selected{
  background-color: #64abf7;
}

.selected:hover{
  background-color: #64abf7;
}

.up{
  position: relative;
  top: -800px;
}

</style>
