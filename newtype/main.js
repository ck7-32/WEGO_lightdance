var N_PART = 16;
var N_DANCER = 3;

document.addEventListener('DOMContentLoaded', function() {
  var audioElement = document.getElementById('myAudio');
  wavesurfer.play();
});
var DELAY = 0.0;

var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
ctx.lineWidth = 3;

var BLUE = "#00FFFF";
var ORANGE = "#FF9400";
var YELLOW = "#FFFF00";
var PURPLE = "#AA00FF";
var RED = "#FF0000";
var WHITE = "#FFFFFF";
var GREEN = "#99FF33";
var BLACK = "#000000";
var PINK = "#FFC0CB";
var COLOR=[BLACK,RED,PINK,ORANGE,GREEN,BLUE,PURPLE,WHITE]

function color(c, x) {
  var percent = (-1) * (1.0 - (x / 255.0));
  return c;
}
Pos = JSON.parse(Pos);

function fetchDataAndInitialize() {
  fetch('data.json')
    .then(response => response.json())
    .then(data => {
      alllight = data.frames;
      frametime = data.frametimes;

      startAnimation();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}
function reloadDataAndRedraw() {
  fetchDataAndInitialize();
}
function setTime(time) {
  const duration = wavesurfer.getDuration();
  const progress = time / duration;
  wavesurfer.seekTo(progress);
}
function startAnimation() {
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
      function(callback) {
        window.setTimeout(callback, 1000);
      };
  })();

  window.addEventListener("keydown", (e) => {
    if(e.keyCode === 32){
      if(wavesurfer.isPlaying()) wavesurfer.pause();
      else wavesurfer.play();
    }
    else if(e.keyCode === 37){
      setTime(wavesurfer.getCurrentTime() - 5);
    }
    else if(e.keyCode === 39){
      setTime(wavesurfer.getCurrentTime() + 5);
    }
    else if(e.keyCode === 190){
      setTime(wavesurfer.getCurrentTime() + 0.1);
    }
    else if(e.keyCode === 188){
      setTime(wavesurfer.getCurrentTime() - 0.1);
    }
  });

  function getPos(idx, time) {
    var bx = 0, by = 0;
    var S = Pos[idx].length;

    if(S == 0) return [0, 0];

    var lb = 0, rb = S-1;
    while(lb < rb) {
      var mb = (lb + rb + 1) >> 1;
      if(Pos[idx][mb][0] > time)
        rb = mb - 1;
      else
        lb = mb;
    }

    var t1 = Pos[idx][lb][0];
    var x1 = Pos[idx][lb][1];
    var y1 = Pos[idx][lb][2];

    if(lb == S-1) return [x1, y1];
    
    var t2 = Pos[idx][lb+1][0];
    var x2 = Pos[idx][lb+1][1];
    var y2 = Pos[idx][lb+1][2];

    bx = x1 + (x2-x1) * (time-t1) / (t2-t1);
    by = y1 + (y2-y1) * (time-t1) / (t2-t1);

    return [bx, by];
  }

  function getTimeSegmentIndex(timeSegments, currentTime) {
    let left = 0;
    let right = timeSegments.length - 1;

    while (left <= right) {
      const mid = Math.floor((left + right) / 2);
      const segment = timeSegments[mid];

      if (currentTime >= segment) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }
    return right;
  }

  function draw_time(time, frame) {
    ctx.font = "20px Monospace";
    ctx.fillStyle = "#FFFFFF";
    
    ctx.fillText(frame, 0, canvas.height - 40);
    ctx.fillText(time, 0, canvas.height - 20);
  }

  function animate(darr, canvas, ctx, startTime) {
    var time = wavesurfer.getCurrentTime() + DELAY;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for(var i=0; i<N_DANCER; i++) {
      for(var j=0; j<N_PART; j++) {
        var pos = getPos(i, time);
        darr[i].setBasePos(pos[0], pos[1]);
      }
    }

    for(var i=0; i<N_DANCER; i++)
      darr[i].draw(time);

    segment = getTimeSegmentIndex(frametime, time * 1000);
    draw_time(time, segment);

    requestAnimFrame(function() {
      animate(darr, canvas, ctx, startTime);
      getCurrentTime();
    });
  }

  function animate_test(dancer, canvas, ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(var j = 0; j < N_PART; j++) {
      dancer.setLight(j, 255);
    }
    dancer.setBasePos(canvas.width / 2, canvas.height / 2);
    dancer.draw();
  }

  function getcolor(dancer, segment, part) {
    return COLOR[alllight[dancer][segment][part]];
  }

  function Dancer(id, bx, by) {
    this.id = id;
    this.base_x = bx;
    this.base_y = by;
    this.height = 160;
    this.width = 64;
    this.light = Array(N_PART);
    for(var i=0; i<N_PART; i++)
      this.light[i] = 0;
  };

  Dancer.prototype.setBasePos = function(bx, by) {
    this.base_x = bx;
    this.base_y = by;
  }

  Dancer.prototype.draw = function(time) {
    var miltime = time * 1000;
    var segment = getTimeSegmentIndex(frametime, miltime);

    ctx.strokeStyle = "#FFFFFF";
    ctx.strokeRect(this.base_x, this.base_y, 1, 1);
    ctx.strokeRect(this.base_x + this.width, this.base_y, 1, 1);
    ctx.strokeRect(this.base_x, this.base_y + this.height, 1, 1);
    ctx.strokeRect(this.base_x + this.width, this.base_y + this.height, 1, 1);

    var head_radius = 20;
    ctx.font = "20px sans-serif";
    ctx.fillStyle = "#FF0000";
    ctx.fillText(this.id, this.base_x + this.width / 2 - 5, this.base_y + head_radius + 6);

    ctx.strokeStyle = getcolor(this.id, segment, 2);
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius, head_radius - 3, Math.PI, Math.PI * 2);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 - 1, this.base_y + 3);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 + 1, this.base_y + 3);
    ctx.stroke();

    var hand_w = 10;
    var hand_h = 25;

    ctx.strokeStyle = getcolor(this.id, segment, 5);
    ctx.strokeRect(this.base_x, this.base_y + head_radius - 10 + hand_h + 5, hand_w, hand_h * 2);
    ctx.strokeStyle = getcolor(this.id, segment, 6);
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + head_radius - 10 + hand_h + 5, hand_w, hand_h * 2);

    var hand_radius = 6;
    ctx.strokeStyle = getcolor(this.id, segment, 3);
    ctx.beginPath();
    ctx.strokeRect(this.base_x, this.base_y + 3 * head_radius + hand_h + 5, hand_w, 3);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 4);
    ctx.beginPath();
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + 3 * head_radius + hand_h + 5, hand_w, 3);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 0);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2, this.base_y + 2 * head_radius + 4);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2, this.base_y + 2 * head_radius + 4);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 1);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 25);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 30);
    ctx.stroke();

    var belt_w = 2 * head_radius - 6;
    var belt_h = 10;
    var pants_w = 12;
    var pants_h = 35;

    ctx.strokeStyle = getcolor(this.id, segment, 8);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 7 - pants_w, this.base_y + 5 * head_radius);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 7);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 7 + pants_w, this.base_y + 5 * head_radius);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 9);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 10);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.stroke();
  };

  var darr = Array(N_DANCER);
  for(var i = 0; i < N_DANCER; i++)
    darr[i] = new Dancer(i, 50 + 100 * i, 59);

  setTimeout(function() {
    var startTime = (new Date()).getTime();
    animate(darr, canvas, ctx, startTime);
  }, 500);

}

fetchDataAndInitialize();
