<template>
  <div>
    <svg id="filter_svg" height="200px" width="300px"></svg>
    <img src='accFilter_icons/vSparse.svg' height='300' width='300' class='filter_icon' id='vSparse' />
    <img src='accFilter_icons/vDense.svg' height='300' width='300' class='filter_icon' id='vDense' />
    <img src='accFilter_icons/hSparse.svg' height='300' width='300' class='filter_icon' id='hSparse' />
    <img src='accFilter_icons/hDense.svg' height='300' width='300' class='filter_icon' id='hDense' />
    <button class="btn btn-light up" v-on:click="reset">Reset</button>
  </div>
</template>

<script>
const d3 = require("d3")

export default {
  name: 'PhraseFilterWheel',

  data: function(){
    return{
      x: -1,
      y: 201,
      filter_h: -1,
      filter_v: -1,
    }
  },

  computed: {
  },

  methods: {
    reset(){
      this.x = -1
      this.y = 201
      d3.selectAll(".circle").remove().exit()
      this.set_filter()
    },

    set_filter(){
      let x_quant = (this.x - this.x % 100) / 100
      let y_quant = 1 - (this.y - this.y % 100) / 100
      if (this.x < 0){
        x_quant = -1
      }
      if (x_quant != this.filter_h || y_quant != this.filter_v){
        this.filter_h = x_quant
        this.filter_v = y_quant
        this.$emit('set_filter', [this.filter_h*2, this.filter_v*2])
      }
    },

    set_circle(new_x, new_y){
      d3.selectAll('.circle').remove().exit()

      d3.select('#filter_svg').append('circle')
        .attr('cx', new_x)
        .attr('cy', new_y)
        .attr('r', 10)
        .attr('fill', '#00a2ff')
        .classed('circle', true)

      this.x = new_x
      this.y = new_y
      this.set_filter()
    }
  },

  mounted(){
    const canvas_size_h = 300
    const canvas_size_v = 200
    const n_bins_h = 3
    const n_bins_v = 2
    const line_width = 2

    let this_ = this

    const dragHandler = d3.drag()
    .on("drag", function (e) {
      let rect = document.getElementById("filter_svg").getBoundingClientRect()
      let new_x = (e.sourceEvent.clientX - rect.x)/0.6
      let new_y = (e.sourceEvent.clientY - rect.y)/0.6
      if (new_x > canvas_size_h){
        new_x = canvas_size_h - 1
      }
      if (new_x < 0){
        new_x = 1
      }
      if (new_y > canvas_size_v){
        new_y = canvas_size_v - 1
      }
      if (new_y < 0){
        new_y = 1
      }
      this_.x = new_x
      this_.y = new_y
      d3.selectAll(".circle")
          .attr("cx", new_x)
          .attr("cy", new_y)
      this_.set_filter()
    })
    let svg = d3.select('#filter_svg')

    // Set up the background and selector movement
    svg.append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', canvas_size_h)
      .attr('height', canvas_size_v)
      .attr('fill', 'black')
      .attr('opacity', 0.3)

    svg.append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', canvas_size_h)
      .attr('height', canvas_size_v)
      .attr('fill', 'black')
      .attr('opacity', 0)
      .classed("background", true)
      .on('mousedown', function(e){
        let rect = document.getElementById("filter_svg").getBoundingClientRect()
        
        d3.selectAll('.circle').remove().exit()

        svg.append('circle')
          .attr('cx', (e.clientX - rect.x)/0.6)
          .attr('cy', (e.clientY - rect.y)/0.6)
          .attr('r', 10)
          .attr('fill', '#00a2ff')
          .classed('circle', true)

          dragHandler(svg.selectAll(".circle"))
          this_.x = (e.clientX - rect.x)/0.6
          this_.y = (e.clientY - rect.y)/0.6
          this_.set_filter()
      })
      
    dragHandler(svg.selectAll(".background"));

    // Add lines
    for (let i=1; i<n_bins_h; i++){
      svg.append('rect')
      .attr('x', i * canvas_size_h / n_bins_h)
      .attr('y', 0)
      .attr('width', line_width)
      .attr('height', canvas_size_v)
      .attr('fill', 'white')
      .attr('opacity', 0.3)
    }

    for (let i=1; i<n_bins_v; i++){
      svg.append('rect')
      .attr('x', 0)
      .attr('y', i * canvas_size_v / n_bins_v)
      .attr('width', canvas_size_h)
      .attr('height', line_width)
      .attr('fill', 'white')
      .attr('opacity', 0.3)
    }

    d3.selectAll('.background').raise()


  },
  
  beforeUnmount() {
  }

}
</script>

<style scoped>
.filter_icon{
  position: relative;
  opacity: 0.6;
  pointer-events: none;
}

#vSparse{
  left: 190px;
  top: -10px;
  -webkit-transform: scale(2);
  transform-origin: center;
}

#vDense{
  left: 135px;
  top: -465px;
  -webkit-transform: scale(1.4);
  transform-origin: center;
}

#hSparse{
  left: 80px;
  top: -677px;
  -webkit-transform: scale(2);
  transform-origin: center;
}

#hDense{
  left: 180px;
  top: -1030px;
  -webkit-transform: scale(1.3);
  transform-origin: center;
}

.up{
  position: relative;
  top: -1200px;
}

</style>
