
function hoverFunction(){
  document.getElementById("playButton").style.backgroundColor = "grey";
}

function hoverOutFunction(){
  document.getElementById("playButton").style.backgroundColor = "transparent";
}


function startFunction() {
  document.getElementById("playButton").style.visibility = "hidden";
  document.getElementById("del-countdown").style.display = "block";
  document.getElementById("header").innerHTML = "Workout begins in:";


  document.getElementById('clock').innerHTML =
    00 + ":" + 6;
  startTimer();

}

function startTimer() {
  var presentTime = document.getElementById('clock').innerHTML;
  var timeArray = presentTime.split(/[:]+/);
  var m = timeArray[0];
  var s = checkSecond((timeArray[1] - 1));
  if(s==59){m=m-1}
  //if(m<0){alert('timer completed')}

  document.getElementById('clock').innerHTML =
    m + ":" + s;
  console.log(m)
  setTimeout(startTimer, 1000);
}

function checkSecond(sec) {
  if (sec < 10 && sec >= 0) {sec = "0" + sec}; // add zero in front of numbers < 10
  if (sec == 0) {
    window.location.href = "Workout";
  };
  return sec;
}
