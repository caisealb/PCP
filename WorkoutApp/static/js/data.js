
   var socket = io();

    //Distance & Speed
    var totalDis = 0;
    var currentSpeed = 0;
    var speedDisplay = 0;
    var disDisplay = 0;

    //GPS latitude & longitude
    var currentLat = 0;
    var latDisplay;
    var currentLong = 0;
    var longDisplay;
    var loc = {};
    var locations = [];
    //window.map = undefined;

    socket.on('connect', function() {
      // socket.emit('json', {data: 'I\'m connected!'});
    });

    socket.on('distance', function(dist_obj) {
        const json = JSON.parse(dist_obj);
        console.log(json);
        //console.log(json.distance);

        if (json.distance !== undefined) {
            totalDis = parseFloat(json.distance);
            disDisplay = totalDis.toString();
            console.log(totalDis);
            console.log(disDisplay);
            setDistance();
            }
        });
    function setDistance(){
      var disttext = document.getElementById("distanceText");
      disttext.innerHTML = (disDisplay);
    }

    socket.on('speed', function(speed_obj) {
        const json = JSON.parse(speed_obj);
        console.log(json);
        //console.log(json.distance);

        if (json.speed !== undefined) {
            currentSpeed = parseFloat(json.speed);
            speedDisplay = currentSpeed.toString();
            console.log(currentSpeed);
            console.log(speedDisplay);
            setSpeed();
            }
        });
      function setSpeed(){
        var speedtext = document.getElementById("speedText");
        speedtext.innerHTML = (speedDisplay);
      }

    socket.on('latitude', function(lat_obj) {
        const json = JSON.parse(lat_obj);
        console.log(json);
        //console.log(json.distance);

        if (json.latitude !== undefined) {
            currentLat = parseFloat(json.latitude);
            latDisplay = currentLat.toString();
            console.log(currentLat);
            console.log(latDisplay);
            // setLat();
            }
          });
        // function setLat(){
        //   var lattext = document.getElementById("latText");
        //   speedtext.innerHTML = (latDisplay); }

    socket.on('longitude', function(long_obj) {
        const json = JSON.parse(long_obj);
        console.log(json);
        //console.log(json.distance);

        if (json.longitude !== undefined) {
            currentLong = parseFloat(json.longitude);
            longDisplay = currentLong.toString();
            console.log(currentLong);
            console.log(longDisplay);
            // setLong();
            }
          });
        // function setLong(){
        //   var longtext = document.getElementById("longText");
        //   longtext.innerHTML = (longDisplay);


        function initMap() {
            center = {lat:currentLat, lng:currentLong};
            var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 17,
            center: center,
            styles: [
                {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
                {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
                {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
                {
                  featureType: 'administrative.locality',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'poi',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'poi.park',
                  elementType: 'geometry',
                  stylers: [{color: '#263c3f'}]
                },
                {
                  featureType: 'poi.park',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#6b9a76'}]
                },
                {
                  featureType: 'road',
                  elementType: 'geometry',
                  stylers: [{color: '#38414e'}]
                },
                {
                  featureType: 'road',
                  elementType: 'geometry.stroke',
                  stylers: [{color: '#212a37'}]
                },
                {
                  featureType: 'road',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#9ca5b3'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'geometry',
                  stylers: [{color: '#746855'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'geometry.stroke',
                  stylers: [{color: '#1f2835'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#f3d19c'}]
                },
                {
                  featureType: 'transit',
                  elementType: 'geometry',
                  stylers: [{color: '#2f3948'}]
                },
                {
                  featureType: 'transit.station',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'water',
                  elementType: 'geometry',
                  stylers: [{color: '#17263c'}]
                },
                {
                  featureType: 'water',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#515c6d'}]
                },
                {
                  featureType: 'water',
                  elementType: 'labels.text.stroke',
                  stylers: [{color: '#17263c'}]
                }
              ]
            });

            // var dot = new google.maps.Circle({
            //   strokeColor: '#ad343e',
            //   strokeOpacity: 0.8,
            //   strokeWeight: 1,
            //   fillColor: '#ad343e',
            //   fillOpacity: 0.8,
            //   map:map,
            //   center: center,
            //   radius: 3
            // })

          // locations.push(center);

        function updatePosition(){
            loc = {lat:currentLat,lng:currentLong};
            locations.push(loc);
            console.log(loc);
            map.setCenter(loc);
            var path = new google.maps.Polyline({
              path: locations,
              geodesic: true,
              strokeColor: '#ad343e',
              strokeOpacity: 1.0,
              strokeWeight: 2
            })
            if ((currentLat != 0) && (currentLong != 0)){
            path.setMap(map);
          }
        }

        // function moveToLocation(currenLat, currentLong){
        //   const center = {lat:currentLat, lng: currentLong};
        //   // using global variable:
        //   window.map.panTo(center);
        // }

        setInterval(updatePosition,1000);
        // setInterval(moveToLocation,1000);
      }
