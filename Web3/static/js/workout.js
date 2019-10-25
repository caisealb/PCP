// color palette:
// grey: #282e3a
// yellow/orange: #eca72c
// Green: #2dcb74
// red: #ad343e
// Lightgrey: #bcabae



function draw(speed)
{
      var  canvas = document.getElementById("myCanvas");
      var  context = canvas.getContext("2d");
      context.clearRect(0,0,canvas.width, canvas.height);
      var centerX = canvas.width / 2;
      var centerY = canvas.height / 2;
      var radius = canvas.height / 2 - 20;

      context.beginPath();
      context.arc(centerX, centerY, radius, Math.PI, Math.PI*-1.1, true);

      var gradience = context.createRadialGradient(centerX, centerY, radius, centerX, centerY, radius-radius/8);
       gradience.addColorStop(0, '#282e3a');
       gradience.addColorStop(1, '#bcabae');

       context.fillStyle = gradience;
       context.fill();
       context.closePath();
       context.restore();

	context.beginPath();
	context.strokeStyle = '#FFFFFF';
	context.translate(centerX,centerY);
  // context.transform.rotate(-90deg);
  // context.transform(0);
	var increment = 1;
	context.font="15px Helvetica";
	for (var i=-5; i<=5; i++)
	{
		angle = Math.PI/10*i;
		sineAngle = Math.sin(angle);
		cosAngle = -Math.cos(angle);

		if (i % 5 == 0) {
		context.lineWidth = 5;
		iPointX = sineAngle *(radius -radius/4);
		iPointY = cosAngle *(radius -radius/4);
		oPointX = sineAngle *(radius -radius/7);
		oPointY = cosAngle *(radius -radius/7);

		wPointX = sineAngle *(radius -radius/2.5);
		wPointY = cosAngle *(radius -radius/2.5);
		context.fillText((i+5)*increment,wPointX-2,wPointY+4);
		}
		else
		{
		context.lineWidth = 2;
		iPointX = sineAngle *(radius -radius/5.5);
		iPointY = cosAngle *(radius -radius/5.5);
		oPointX = sineAngle *(radius -radius/7);
		oPointY = cosAngle *(radius -radius/7);
		}
		context.beginPath();
		context.moveTo(iPointX,iPointY);
		context.lineTo(oPointX,oPointY);
		context.stroke();
		context.closePath();
	}

	var numOfSegments = speed/increment;
	numOfSegments = numOfSegments -18;
	angle = Math.PI/30*numOfSegments;
	sineAngle = Math.sin(angle);
	cosAngle = -Math.cos(angle);
	pointX = sineAngle *(3/4*radius);
	pointY = cosAngle *(3/4*radius);

}


function pauseFunction(){
  document.getElementById("overlay").style.visibility = "visible";
}

function continueFunction(){
  document.getElementById("overlay").style.visibility = "hidden";
}

//stop button
function hoverFunction(){
  document.getElementById("stopCircle").style.opacity = "0.5";
}

function hoverOutFunction(){
  document.getElementById("stopCircle").style.opacity = "1";
}

//pausebutton
function hoverPause(){
  document.getElementById('pauseCircle').style.opacity = "0.5";
}

function hoverOutPause(){
  document.getElementById('pauseCircle').style.opacity = "1"
}

function redraw()
{
	draw(document.getElementById("myList").value);
}
