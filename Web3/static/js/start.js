
function hoverFunction(){
  document.getElementById("playButton").style.backgroundColor = "grey";
}

function hoverOutFunction(){
  document.getElementById("playButton").style.backgroundColor = "transparent";
}


function startFunction(){
  document.getElementById("playButton").style.visibility = "hidden";
  document.getElementById("del-countdown").style.display = "block";

  for (var i=3; i > 0; i--){
    var timerText = document.getElementById("clock");
    timerText.innerHTML = (i);
  }
    setTimeout(10000);
}


//
// function updateTimer(deadline){
//   var time = deadline - new Date();
//   return {
//     // 'days': Math.floor( time/(1000*60*60*24) ),
//     // 'hours': Math.floor( (time/(1000*60*60)) % 24 ),
//     // 'minutes': Math.floor( (time/1000/60) % 60 ),
//     'seconds': Math.floor( (time/1000) % 60 ),
//     'total' : time
//   };
// }

// window.onload = startTimer();
//
// function startTimer(){
//     for (var i=3; i > 0; i--){
//       var timerText = document.getElementById("clock");
//       timerText.innerHTML = (i);
//       setTimeout(1000);
//     }
//   }






// function animateClock(span){
//   span.className = "turn";
//   setTimeout(function(){
//     span.className = "";
//   },700);
// }

// function startTimer(id, deadline){
//   var timerInterval = setInterval(function(){
//     var clock = document.getElementById(id);
//     var timer = updateTimer(deadline);
//
//     clock.innerHTML = '<span>' + timer.seconds + '</span>';
//
//     //animations
//     var spans = clock.getElementsByTagName("span");
//     animateClock(spans[3]);
//     if(timer.seconds == 59) animateClock(spans[2]);
//     if(timer.minutes == 59 && timer.seconds == 59) animateClock(spans[1]);
//     if(timer.hours == 23 && timer.minutes == 59 && timer.seconds == 59) animateClock(spans[0]);
//
//     //check for end of timer
//     if(timer.total < 1){
//       clearInterval(timerInterval);
//       clock.innerHTML = '<span>0</span><span>0</span><span>0</span><span>0</span>';
//     }
//
//
//   }, 1000);
// }
