
var N_DANCER = 0;
window.addEventListener("keydown", handleKeydown);
var DELAY = 0;
var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
ctx.lineWidth = 3;
var colors=[];
Pos = JSON.parse(Pos);
var darr = Array(N_DANCER);
var arrow = 0;
var postime=[]

async function initializeSettings() {
  try {
    const data = await window.fetchData('../data/setting.json');
    N_DANCER = data.dancersname.length;
    audiopath = data.audio; // 使用全局变量，不再重新声明
    console.log('N_DANCER:', N_DANCER);
    // 初始化 darr 数组
    darr = Array(N_DANCER);
    for (let i = 0; i < N_DANCER; i++) {
      darr[i] = new Dancer(i, 50 + 100 * i, 59);
    }
  } catch (error) {
    console.error('Error initializing settings:', error);
  }
}

async function initializeData() {
  return window.fetchData('../data/data.json').then(data => {
    alllight = data.frames;
    frametime = data.frametimes;
    colors = data.color;
    startAnimation();
  });
}
async function initializeposData() {
  return window.fetchData('../data/pos.json').then(data => {
    pos = data.pos;
    postime=data.postimes;
  });
}
async function reloadDataAndRedraw() {
  await initializeposData();
  await initializeData();
  
  loadDataFromJSON();
  reloadRegions(); // 新增這行
  getCurrentTime();
}

function dragdancer(x,y){
    handler.updatepos(arrow,x,y);

}
function handleKeydown(e) {
  const currentTime = window.wavesurfer.getCurrentTime();
  switch (e.keyCode) {
    case 32:
      window.wavesurfer.playPause();
      break;
    case 37:
      window.setTime(currentTime - 5);
      break;
    case 39:
      window.setTime(currentTime + 5);
      break;
    case 190:
      window.setTime(currentTime + 0.1);
      break;
    case 188:
      window.setTime(currentTime - 0.1);
      break;
    case 75: // 'k' or 'K'
      window.wavesurfer.playPause();
      console.log("play/pause");
      break;
    case 85://"U"
    if (!isdragging) {
      nowPos=getTimeSegmentIndex(postime,wavesurfer.getCurrentTime());
      window.setTime(postime[nowPos])
      isdragging = true;

  }
}}
function color(c, x) {
  var percent = (-1) * (1.0 - (x / 255.0));
  return c;
}
// 将需要在全局作用域使用的函数添加到 window 对象
window.initializeSettings = initializeSettings;
window.initializeData = initializeData;
window.handleKeydown = handleKeydown;


function getPos(idx, time,nowPos) {
  var bx = 0, by = 0;
  S=postime.length;

  var t1 = postime[nowPos];
  var x1 = pos[nowPos][idx][0];
  var y1 = pos[nowPos][idx][1];
  if(nowPos == S-1) return [x1, y1];
  
  var t2 = postime[nowPos+1];
  var x2 = pos[nowPos+1][idx][0];
  var y2 = pos[nowPos+1][idx][1];

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
  if (!window.wavesurfer) {
    console.error('WaveSurfer is not initialized');
  }
  var time = wavesurfer.getCurrentTime() + DELAY;
  ctx.clearRect(0, 0, canvas.width, canvas.height);


  nowPos=getTimeSegmentIndex(postime,time);

  for(var i=0; i<N_DANCER; i++) {

      var pos = getPos(i, time,nowPos);
      darr[i].setBasePos(pos[0], pos[1]);

  }
  if(isdragging){
    darr[arrow].setBasePos(lastX-30, lastY-10);
  }
  //決定要怎麼畫
  for(var i=0; i<N_DANCER; i++){

      
    darr[i].draw(time);
      
   
    if (i == arrow){
      darr[i].drawArrow();
    }}


  segment = getTimeSegmentIndex(frametime, time * 1000);
  draw_time(time, segment);
  
  requestAnimFrame(function() {
    getCurrentTime();
    animate(darr, canvas, ctx, startTime);
  });
}


function getcolor(dancer, segment, part) {
  return colors[alllight[dancer][segment][part]];
}



function startAnimation() {
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
      function(callback) {
        window.setTimeout(callback, 1000/60);
      };
  })();
}

function setArrow(arrowN) {
  arrow = arrowN;
  reloadDataAndRedraw();
}

function setTime(time) {
  const duration = wavesurfer.getDuration();
  const progress = time / duration;
  wavesurfer.seekTo(progress);
}





for(var i = 0; i < N_DANCER; i++)
  darr[i] = new Dancer(i, 50 + 100 * i, 59);


