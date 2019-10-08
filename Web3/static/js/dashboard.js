var dist;
var socket = io();
socket.on('connect', function() {
  // socket.emit('json', {data: 'I\'m connected!'});
});

socket.on('json', function(msg) {

  function rotate {
    // map(speed, ..., ..., ..., ...);
    var speed = parseFloat(msg['speed']);
    document.getElementById("needle").'angle' = speed;
  }
});
