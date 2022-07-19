const g = require('logitech-g29')

var http = require('http'),
    faye = require('faye');

var server = http.createServer(),
    bayeux = new faye.NodeAdapter({mount: '/'});

bayeux.attach(server);
server.listen(8001);

let turn_idx = -1
let wheel_shift = 0

g.connect(
    {
        autocenter: true,
        range: 360
    },
  function(err) {
    console.log('WHEEL CONNECTED')

    bayeux.getClient().publish('/messages', {
        type: 'connected',
        val: 0,
    });

    g.on('pedals-gas', function(val) {
        bayeux.getClient().publish('/messages', {
            type: 'gas',
            value: val,
        });
    })

    g.on('pedals-brake', function(val) {
        bayeux.getClient().publish('/messages', {
            type: 'brake',
            value: val,
        });
    })

    g.on('pedals-clutch', function(val) {
        if (val == 0){
            bayeux.getClient().publish('/messages', {
                type: 'clutch',
                value: val,
            });
        }
    })

    g.on('wheel-turn', function(val) {
        let idx = Math.floor((val - 0.001) / 100 * 7)
        if (idx < 0){
          idx = 0
        }
        idx = (idx - 3 + 7) % 7
        
        if (turn_idx != idx){
            turn_idx = idx
            bayeux.getClient().publish('/messages', {
                type: 'wheel_turn',
                value: idx,
            });
        }

    })

    g.on('shifter-gear', function(val) {
        console.log(val)
        bayeux.getClient().publish('/messages', {
            type: 'shift',
            value: val,
        });
    })

    g.on('wheel-shift_left', function(val) {
        if (val == 1){
            wheel_shift = wheel_shift + 3
            console.log(wheel_shift)
            bayeux.getClient().publish('/messages', {
                type: 'wheel_shift',
                value: wheel_shift,
            });
        }
    })
    
    g.on('wheel-shift_right', function(val) {
        if (val == 1){
            wheel_shift = wheel_shift + 1
            console.log(wheel_shift)
            bayeux.getClient().publish('/messages', {
                type: 'wheel_shift',
                value: wheel_shift,
            });
        }
    })


})