  var dist;
  var socket = io();
  socket.on('connect', function() {
    // socket.emit('json', {data: 'I\'m connected!'});
  });

  socket.on('json', function(msg) {

    switch(color) {
      dist = parseFloat(msg['distance']);
      case x:
        dist => 33;
      document.getElementById("myCircle").'background-color' = #FFFFFF;
      case y:
        dist => 66;
        document.getElementById("myCircle").'background-color' = #AAAAAA;
      default:
        document.getElementById("myCircle").'background-color' = #BBBBBB;

    }
  });
