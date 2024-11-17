const dancemovementstarttime=15.08


function getScaledNormalVector2D(x, y, targetLength) {
  // 計算法向量（逆時針）
  const normal = [-y, x];

  // 計算原始法向量的長度
  const length = Math.sqrt(normal[0] ** 2 + normal[1] ** 2);

  // 歸一化並調整至目標長度
  const scaledNormal = [
      (normal[0] / length) * targetLength,
      (normal[1] / length) * targetLength
  ];

  return scaledNormal;
}
function getVectorlength(x,y){
  currentLength = Math.sqrt(x * x + y * y);
  return currentLength;
}
function getScaledVector(x, y, scaleFactor) {
 
  // Scale the vector components
  const scaledX = x * scaleFactor;
  const scaledY = y * scaleFactor;
  
  return [scaledX,scaledY];
}
function getAngleBisector(v1,v2) {
  // 歸一化第一個向量
  x1=v1[0];
  x2=v2[0];
  y1=v1[0];
  y2=v2[0];
  const length1 = Math.sqrt(x1 * x1 + y1 * y1);
  const unitVector1 = { x: x1 / length1, y: y1 / length1 };
  
  // 歸一化第二個向量
  const length2 = Math.sqrt(x2 * x2 + y2 * y2);
  const unitVector2 = { x: x2 / length2, y: y2 / length2 };
  
  // 計算角平分向量，將兩個單位向量相加
  const bisectorX = unitVector1.x + unitVector2.x;
  const bisectorY = unitVector1.y + unitVector2.y;
  
  // 歸一化角平分向量
  const bisectorLength = Math.sqrt(bisectorX * bisectorX + bisectorY * bisectorY);
  const unitBisectorX = bisectorX / bisectorLength;
  const unitBisectorY = bisectorY / bisectorLength;
  
  // 使角平分向量的長度與原向量一致
  const originalLength = length1;  // 假設兩向量長度相同，所以使用其中一個的長度
  const scaledBisectorX = unitBisectorX * originalLength;
  const scaledBisectorY = unitBisectorY * originalLength;
  
  return [scaledBisectorX,scaledBisectorY];
}

function getcolor(dancer, segment, part) {
  return colors[alllight[dancer][segment][part]];
}
function Dancer(id, bx, by) {
    this.id = id;
    this.base_x = bx;
    this.base_y = by;
    this.height = 160;
    this.width = 64;
  };
Dancer.prototype.isClicked = function(mouseX, mouseY) {
    return mouseX >= this.base_x && mouseX <= this.base_x + this.width &&
           mouseY >= this.base_y && mouseY <= this.base_y + this.height;
};
Dancer.prototype.setBasePos = function(bx, by) {
    this.base_x = bx;
    this.base_y = by;
  }
Dancer.prototype.drawArrow=function(){
 
    ctx.strokeStyle = "#a0e0aa";
    //draw an arrow on the top of dencer
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2, this.base_y - 10);
    ctx.lineTo(this.base_x + this.width / 2 + 10, this.base_y - 10 - 20);
    ctx.lineTo(this.base_x + this.width / 2 - 10, this.base_y - 10 - 20);
    ctx.lineTo(this.base_x + this.width / 2 , this.base_y - 10);
    ctx.stroke();
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
    ctx.lineWidth=1.5;
    if(((time-dancemovementstarttime)*30>movementNum )|| (time<dancemovementstarttime)){
      this.originaldraw(head_radius,segment);
    }
    else{
      cX=this.base_x+32
      cY=this.base_y+65
      nf=Math.trunc((time-dancemovementstarttime)*30)
      
      NowMovement=dancemovement[nf]

      nowdepth= depthdata[nf]


      drawpart=[this.Head,this.RightUpperArm,this.LeftUpperArm,this.RightForeArm,this.LeftForeArm,this.RightLeg,this.LeftLeg,this.Body]
      //繪製關節
      this.drawjoint(NowMovement,segment,cX,cY);
      //繪製部位
      for(i=drawpart.length;i>0;i--){
        drawpart[nowdepth[i-1]](NowMovement,segment,this.id,cX,cY)
      }
      //繪製骨架
      //this.movementskeleton(NowMovement,cX,cY);
    }


  }
Dancer.prototype.originaldraw = function(head_radius,segment) {
    //貓耳
    ctx.strokeStyle = getcolor(this.id, segment,0);
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius - 10, head_radius - 3, Math.PI, Math.PI * 2);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 0.5 * head_radius -5);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 4, this.base_y -9);
    ctx.lineTo(this.base_x + this.width / 2 - 1, this.base_y -7);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 0.5 * head_radius -5);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 4, this.base_y -9);
    ctx.lineTo(this.base_x + this.width / 2 + 1, this.base_y -7);
    ctx.stroke();
    //帽子
    ctx.strokeStyle = getcolor(this.id, segment,1 );
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius-8, head_radius - 5, Math.PI,2 * Math.PI );
    ctx.moveTo(this.base_x+this.width / 2-head_radius + 5 , this.base_y +head_radius -8);
    ctx.lineTo(this.base_x+this.width / 2+head_radius - 5 , this.base_y +head_radius -8);
    ctx.ellipse(this.base_x + this.width / 2, this.base_y + head_radius-8, head_radius-5, 5,0, Math.PI, 2 * Math.PI,true);
    ctx.stroke();

    // 眼鏡部分
    ctx.strokeStyle = getcolor(this.id, segment, 2);
    ctx.lineWidth = 2;
    ctx.beginPath();
    var glass_width = 14; 
    var glass_height = 10; 
    var glass_y_offset = head_radius + 10; 
    var bridge_width = 6; 
    ctx.rect(
      this.base_x + this.width / 2 - head_radius / 2 - glass_width / 2,
      this.base_y + glass_y_offset -10,
      glass_width,
      glass_height
    );
    ctx.rect(
      this.base_x + this.width / 2 + head_radius / 2 - glass_width / 2,
      this.base_y + glass_y_offset-10,
      glass_width,
      glass_height
    );
    ctx.moveTo(
      this.base_x + this.width / 2 - bridge_width / 2,
      this.base_y + glass_y_offset + glass_height / 2-10);
    ctx.lineTo(
      this.base_x + this.width / 2 + bridge_width / 2,
      this.base_y + glass_y_offset + glass_height / 2-10);

    ctx.stroke(); 


  //手臂
    var hand_w = 10;
    var hand_h = 20;
  
    ctx.strokeStyle = getcolor(this.id, segment, 5);
    ctx.strokeRect(this.base_x, this.base_y + head_radius - 8 + hand_h + 5, hand_w, hand_h * 2);
    ctx.strokeStyle = getcolor(this.id, segment, 6);
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + head_radius - 8 + hand_h + 5, hand_w, hand_h * 2);
  
  //手套
<<<<<<< HEAD
    ctx.lineWidth=2;
    ctx.strokeStyle = getcolor(this.id, segment, 7);
=======
  ctx.lineWidth=2;
    ctx.strokeStyle = getcolor(this.id, segment, 6);
>>>>>>> fe47307778de5aa63a902f7ca2c7395cec1bf705
    ctx.beginPath();
    ctx.strokeRect(this.base_x, this.base_y + 3 * head_radius + hand_h , hand_w, 3);
    ctx.moveTo(this.base_x , this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x,this.base_y + 3 * head_radius + hand_h+13);
    ctx.moveTo(this.base_x +3, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x +3,this.base_y + 3 * head_radius + hand_h+16);
    ctx.moveTo(this.base_x +6, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x +6,this.base_y + 3 * head_radius + hand_h+17);
    ctx.moveTo(this.base_x +9, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x +9,this.base_y + 3 * head_radius + hand_h+16);
    ctx.moveTo(this.base_x +12, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x +12,this.base_y + 3 * head_radius + hand_h+11);
    ctx.stroke();
    ctx.strokeStyle = getcolor(this.id, segment, 8);
    ctx.beginPath();
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + 3 * head_radius + hand_h , hand_w, 3);
    ctx.moveTo(this.base_x- 1+this.width - hand_w , this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x- 1+this.width - hand_w,this.base_y + 3 * head_radius + hand_h+11);
    ctx.moveTo(this.base_x- 1+this.width - hand_w +3, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x- 1+this.width - hand_w +3,this.base_y + 3 * head_radius + hand_h+16);
    ctx.moveTo(this.base_x- 1+this.width - hand_w +6, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x- 1+this.width - hand_w +6,this.base_y + 3 * head_radius + hand_h+17);
    ctx.moveTo(this.base_x- 1+this.width - hand_w +9, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x- 1+this.width - hand_w +9,this.base_y + 3 * head_radius + hand_h+16);
    ctx.moveTo(this.base_x- 1+this.width - hand_w +12, this.base_y + 3 * head_radius + hand_h+5);
    ctx.lineTo(this.base_x- 1+this.width - hand_w +12,this.base_y + 3 * head_radius + hand_h+13);
    ctx.stroke();
<<<<<<< HEAD
    // 左外套
    ctx.lineWidth = 3;
    ctx.strokeStyle = getcolor(this.id, segment, 3);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 2, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius - 3);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 8, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 15, this.base_y + 2 * head_radius + 4); 
    ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius - 3);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 7); //口袋
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 7);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 17);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 17);
    ctx.closePath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 11);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 11
    );

    ctx.stroke();

    // 右外套
    ctx.lineWidth = 3;
    ctx.strokeStyle = getcolor(this.id, segment, 4);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius - 3);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 8, this.base_y + 2 * head_radius - 3);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 15, this.base_y + 2 * head_radius + 4); 
    ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius - 3);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 7); //口袋
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 7);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 17);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 17);
    ctx.closePath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 11);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 11);

    ctx.stroke();



        
        
    var belt_w = 2 * head_radius - 6;
    var belt_h = 10;
    var pants_w = 8;  // 褲管的寬度
    var pants_h = 60; // 褲管的高度
    // 左褲管部分 (包含左褲管、左口袋和左裝飾線)
    ctx.strokeStyle = getcolor(this.id, segment, 9);
    ctx.beginPath();

    // 左褲管
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 5 * head_radius + pants_h); // 褲管高度
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 10, this.base_y + 3 * head_radius+25); // 口袋起始點
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 3 * head_radius+25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 3 * head_radius + 35);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 10, this.base_y + 3 * head_radius + 35);
    ctx.closePath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 12, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 10, this.base_y + 5 * head_radius + pants_h);
    ctx.moveTo(this.base_x + this.width / 2 - 1, this.base_y + 3 * head_radius + 38); 
    ctx.lineTo(this.base_x + this.width / 2 - 5, this.base_y + 5 * head_radius + pants_h); 

    ctx.stroke();

    // 右褲管
    ctx.strokeStyle = getcolor(this.id, segment, 10);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 5 * head_radius + pants_h); // 褲管高度
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 10, this.base_y + 3 * head_radius +25); // 口袋起始點
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius+25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius + 35);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 10, this.base_y + 3 * head_radius + 35);
    ctx.closePath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 12, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 10, this.base_y + 5 * head_radius + pants_h);
    ctx.moveTo(this.base_x + this.width / 2 + 1, this.base_y + 3 * head_radius + 38); 
    ctx.lineTo(this.base_x + this.width / 2 + 5, this.base_y + 5 * head_radius + pants_h); 
    ctx.stroke(); 
=======
// 左外套
ctx.lineWidth = 3;
ctx.strokeStyle = getcolor(this.id, segment, 2);
ctx.beginPath();
ctx.moveTo(this.base_x + this.width / 2 - head_radius + 2, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius + 40);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius + 40);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 2 * head_radius + 20);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius - 3);
ctx.moveTo(this.base_x + this.width / 2 - head_radius + 8, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 15, this.base_y + 2 * head_radius + 4); 
ctx.lineTo(this.base_x + this.width / 2 - 2, this.base_y + 2 * head_radius - 3);
ctx.moveTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 7); //口袋
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 7);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 17);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 17);
ctx.closePath();
ctx.moveTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius + 11);
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 14, this.base_y + 2 * head_radius + 11
);

ctx.stroke();

// 右外套
ctx.lineWidth = 3;
ctx.strokeStyle = getcolor(this.id, segment, 3);
ctx.beginPath();
ctx.moveTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius + 40);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius + 40);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 2 * head_radius + 20);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius - 3);
ctx.moveTo(this.base_x + this.width / 2 + head_radius - 8, this.base_y + 2 * head_radius - 3);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 15, this.base_y + 2 * head_radius + 4); 
ctx.lineTo(this.base_x + this.width / 2 + 2, this.base_y + 2 * head_radius - 3);
ctx.moveTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 7); //口袋
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 7);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 17);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 17);
ctx.closePath();
ctx.moveTo(this.base_x + this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius + 11);
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 14, this.base_y + 2 * head_radius + 11);

ctx.stroke();



    
    
    //褲子
     var belt_w = 2 * head_radius - 6;
     var belt_h = 10;
     var pants_w = 12;
     var pants_h = 35;
   
     ctx.strokeStyle = getcolor(this.id, segment, 10);
     ctx.beginPath();
     ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius + 25);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 5 * head_radius);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 7 - pants_w, this.base_y + 5 * head_radius);
     ctx.stroke();
   
     ctx.strokeStyle = getcolor(this.id, segment, 9);
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
>>>>>>> fe47307778de5aa63a902f7ca2c7395cec1bf705
   };
Dancer.prototype.movementskeleton = function(NowMovement,cX,cY){
  
  ctx.strokeStyle = "#2c2c2c";
  //ctx.strokeStyle = "#000000";
  ctx.beginPath();
  headcenter=[(cX+NowMovement[1][0]+cX+NowMovement[2][0]+cX+NowMovement[0][0])/3,(cY+NowMovement[1][1]+cY+NowMovement[2][1]+cY+NowMovement[0][1])/3]
  //ctx.arc(headcenter[0], headcenter[1], 13, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  
  ctx.moveTo((cX+NowMovement[0][0])*3-2*headcenter[0],(cY+NowMovement[0][1])*3-2*headcenter[1]);
  ctx.lineTo((cX+NowMovement[1][0])*3-2*headcenter[0],(cY+NowMovement[1][1])*3-2*headcenter[1]);
  ctx.lineTo((cX+NowMovement[2][0])*3-2*headcenter[0],(cY+NowMovement[2][1])*3-2*headcenter[1]);
  ctx.lineTo((cX+NowMovement[0][0])*3-2*headcenter[0],(cY+NowMovement[0][1])*3-2*headcenter[1]);
  
 
  ctx.moveTo(cX+NowMovement[1+2][0],cY+NowMovement[1+2][1]);
  ctx.lineTo(cX+NowMovement[2+2][0],cY+NowMovement[2+2][1]);
  ctx.lineTo(cX+NowMovement[14+2][0],cY+NowMovement[14+2][1]);
  ctx.lineTo(cX+NowMovement[13+2][0],cY+NowMovement[13+2][1]);
  ctx.lineTo(cX+NowMovement[1+2][0],cY+NowMovement[1+2][1]);

  ctx.lineTo(cX+NowMovement[3+2][0],cY+NowMovement[3+2][1]);
  ctx.lineTo(cX+NowMovement[5+2][0],cY+NowMovement[5+2][1]);

  ctx.moveTo(cX+NowMovement[2+2][0],cY+NowMovement[2+2][1]);
  ctx.lineTo(cX+NowMovement[4+2][0],cY+NowMovement[4+2][1]);
  ctx.lineTo(cX+NowMovement[6+2][0],cY+NowMovement[6+2][1]);

  ctx.moveTo(cX+NowMovement[14+2][0],cY+NowMovement[14+2][1]);
  ctx.lineTo(cX+NowMovement[16+2][0],cY+NowMovement[16+2][1]);
  ctx.lineTo(cX+NowMovement[18+2][0],cY+NowMovement[18+2][1]);

  ctx.moveTo(cX+NowMovement[13+2][0],cY+NowMovement[13+2][1]);
  ctx.lineTo(cX+NowMovement[15+2][0],cY+NowMovement[15+2][1]);
  ctx.lineTo(cX+NowMovement[17+2][0],cY+NowMovement[17+2][1]);
  ctx.stroke();
}
Dancer.prototype.drawjoint = function(NowMovement,segment,cX,cY){
  //左手關節
  ctx.strokeStyle = getcolor(this.id, segment, 5);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[4][0],cY+NowMovement[4][1],5, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(cX+NowMovement[6][0],cY+NowMovement[6][1],5, 0, Math.PI * 2);
  ctx.stroke();
  ctx.strokeStyle = getcolor(this.id, segment, 7);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[8][0],cY+NowMovement[8][1],5, 0, Math.PI * 2);
  ctx.stroke();
  //右手關節
  ctx.strokeStyle = getcolor(this.id, segment, 6);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[3][0],cY+NowMovement[3][1],5, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(cX+NowMovement[5][0],cY+NowMovement[5][1],5, 0, Math.PI * 2);
  ctx.stroke();
  ctx.strokeStyle = getcolor(this.id, segment, 8);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[7][0],cY+NowMovement[7][1],5, 0, Math.PI * 2);
  ctx.stroke();
  //左腳關節
  ctx.strokeStyle = getcolor(this.id, segment,9);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[18][0],cY+NowMovement[18][1],6, 0, Math.PI * 2);
  ctx.stroke();
  //右腳關節
  ctx.strokeStyle = getcolor(this.id, segment,10);
  ctx.beginPath();
  ctx.arc(cX+NowMovement[17][0],cY+NowMovement[17][1],6, 0, Math.PI * 2);
  ctx.stroke();
}
Dancer.prototype.LeftUpperArm = function(NowMovement,segment,id,cX,cY){
  ctx.strokeStyle = getcolor(id, segment, 5);
  
  shoulder=[cX+NowMovement[4][0],cY+NowMovement[4][1]];
  elbow=[cX+NowMovement[6][0],cY+NowMovement[6][1]];
  v=getScaledNormalVector2D(shoulder[0]-elbow[0],shoulder[1]-elbow[1],6);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(shoulder[0]+v[0],shoulder[1]+v[1]);
  ctx.lineTo(shoulder[0]-v[0],shoulder[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(shoulder[0]+v[0],shoulder[1]+v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.moveTo(shoulder[0]-v[0],shoulder[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(elbow[0],elbow[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
}
Dancer.prototype.LeftForeArm = function(NowMovement,segment,id,cX,cY){
  //繪製手臂
  ctx.strokeStyle = getcolor(id, segment, 5);
  
  wrist=[cX+NowMovement[8][0],cY+NowMovement[8][1]];
  elbow=[cX+NowMovement[6][0],cY+NowMovement[6][1]];
  thumb=[cX+NowMovement[14][0],cY+NowMovement[14][1]];  
  index=[cX+NowMovement[12][0],cY+NowMovement[12][1]];
  pinky=[cX+NowMovement[10][0],cY+NowMovement[10][1]];


  v=getScaledNormalVector2D(wrist[0]-elbow[0],wrist[1]-elbow[1],5);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.moveTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(elbow[0],elbow[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
  //繪製手指
  
  ctx.strokeStyle = getcolor(id, segment, 7);

  /*
  thumbVector=[wrist[0]-thumb[0],wrist[1]-thumb[1]];
  //LtV=getVectorlength(thumbVector[0],thumbVector[1]);
  thumbVector=getScaledVector(thumbVector[0],thumbVector[1],0.5);
  indexVector=[wrist[0]-index[0],wrist[1]-index[1]];
  indexVector=getScaledVector(indexVector[0],indexVector[1],0.5);
  pinkyVector=[wrist[0]-pinky[0],wrist[1]-pinky[1]];
  indexVector=getScaledVector(pinkyVector[0],pinkyVector[1],0.5);
  mVector=getAngleBisector(indexVector,pinkyVector);
  middleVector=getAngleBisector(indexVector,mVector);
  ringVector=getAngleBisector(pinkyVector,mVector);

  ctx.beginPath();
  ctx.moveTo(wrist[0]-thumbVector[0],wrist[1]-thumbVector[1]);
  ctx.lineTo(wrist[0]-2*thumbVector[0],wrist[1]-2*thumbVector[1]);
  ctx.moveTo(wrist[0]-indexVector[0],wrist[1]-indexVector[1]);
  ctx.lineTo(wrist[0]-2*indexVector[0],wrist[1]-2*indexVector[1]);
  ctx.moveTo(wrist[0]-middleVector[0],wrist[1]-middleVector[1]);
  ctx.lineTo(wrist[0]-2*middleVector[0],wrist[1]-2*middleVector[1]);
  ctx.moveTo(wrist[0]-ringVector[0],wrist[1]-ringVector[1]);
  ctx.lineTo(wrist[0]-2*ringVector[0],wrist[1]-2*ringVector[1]);
  ctx.moveTo(wrist[0]-pinkyVector[0],wrist[1]-pinkyVector[1]);
  ctx.lineTo(wrist[0]-2*pinkyVector[0],wrist[1]-2*pinkyVector[1]);
  ctx.stroke();
  */
  //

}
Dancer.prototype.RightUpperArm = function(NowMovement,segment,id,cX,cY){
  ctx.strokeStyle = getcolor(id, segment, 6);
  shoulder=[cX+NowMovement[3][0],cY+NowMovement[3][1]];
  elbow=[cX+NowMovement[5][0],cY+NowMovement[5][1]];
  v=getScaledNormalVector2D(shoulder[0]-elbow[0],shoulder[1]-elbow[1],6);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(shoulder[0]+v[0],shoulder[1]+v[1]);
  ctx.lineTo(shoulder[0]-v[0],shoulder[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(shoulder[0]+v[0],shoulder[1]+v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.moveTo(shoulder[0]-v[0],shoulder[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(elbow[0],elbow[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
}
Dancer.prototype.RightForeArm = function(NowMovement,segment,id,cX,cY){
  //繪製手臂
  ctx.strokeStyle = getcolor(id, segment, 6);
  
  wrist=[cX+NowMovement[8-1][0],cY+NowMovement[8-1][1]];
  elbow=[cX+NowMovement[6-1][0],cY+NowMovement[6-1][1]];
  thumb=[cX+NowMovement[14-1][0],cY+NowMovement[14-1][1]];  
  index=[cX+NowMovement[12-1][0],cY+NowMovement[12-1][1]];
  pinky=[cX+NowMovement[10-1][0],cY+NowMovement[10-1][1]];


  v=getScaledNormalVector2D(wrist[0]-elbow[0],wrist[1]-elbow[1],5);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(elbow[0]+v[0],elbow[1]+v[1]);
  ctx.moveTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.lineTo(elbow[0]-v[0],elbow[1]-v[1]);
  ctx.moveTo(wrist[0]+v[0],wrist[1]+v[1]);
  ctx.lineTo(wrist[0]-v[0],wrist[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(elbow[0],elbow[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
  //繪製手指
  /*
  ctx.strokeStyle = getcolor(id, segment, 7);

  
  thumbVector=[wrist[0]-thumb[0],wrist[1]-thumb[1]];
  //LtV=getVectorlength(thumbVector[0],thumbVector[1]);
  thumbVector=getScaledVector(thumbVector[0],thumbVector[1],0.5);
  indexVector=[wrist[0]-index[0],wrist[1]-index[1]];
  indexVector=getScaledVector(indexVector[0],indexVector[1],0.5);
  pinkyVector=[wrist[0]-pinky[0],wrist[1]-pinky[1]];
  indexVector=getScaledVector(pinkyVector[0],pinkyVector[1],0.5);
  mVector=getAngleBisector(indexVector,pinkyVector);
  middleVector=getAngleBisector(indexVector,mVector);
  ringVector=getAngleBisector(pinkyVector,mVector);

  ctx.beginPath();
  ctx.moveTo(wrist[0]-thumbVector[0],wrist[1]-thumbVector[1]);
  ctx.lineTo(wrist[0]-2*thumbVector[0],wrist[1]-2*thumbVector[1]);
  ctx.moveTo(wrist[0]-indexVector[0],wrist[1]-indexVector[1]);
  ctx.lineTo(wrist[0]-2*indexVector[0],wrist[1]-2*indexVector[1]);
  ctx.moveTo(wrist[0]-middleVector[0],wrist[1]-middleVector[1]);
  ctx.lineTo(wrist[0]-2*middleVector[0],wrist[1]-2*middleVector[1]);
  ctx.moveTo(wrist[0]-ringVector[0],wrist[1]-ringVector[1]);
  ctx.lineTo(wrist[0]-2*ringVector[0],wrist[1]-2*ringVector[1]);
  ctx.moveTo(wrist[0]-pinkyVector[0],wrist[1]-pinkyVector[1]);
  ctx.lineTo(wrist[0]-2*pinkyVector[0],wrist[1]-2*pinkyVector[1]);
  ctx.stroke();
  */
}
Dancer.prototype.Head = function(NowMovement,segment,id,cX,cY){
  //nose=[cX+NowMovement[0][0],cY+NowMovement[0][1]];
  Leye=[cX+NowMovement[1][0],cY+NowMovement[1][1]];
  Reye=[cX+NowMovement[2][0],cY+NowMovement[2][1]];
  nose=[(Leye[0]+Reye[0])/2,(Leye[1]+Reye[1])/2+2];
   //帽子
  ctx.strokeStyle = getcolor(id, segment,1 );
   ctx.beginPath();
   ctx.arc(nose[0],nose[1], 12, Math.PI,2 * Math.PI );
   ctx.moveTo(nose[0]-12,nose[1]);
   ctx.lineTo(nose[0]+12, nose[1]);
   //ctx.ellipse(this.base_x + this.width / 2, this.base_y + head_radius+2, head_radius-5, 5,0, Math.PI, 2 * Math.PI,true);
   ctx.stroke();
   ctx.beginPath();
   ctx.moveTo(nose[0]-12 + 3, nose[1]- 0.5 * 15 -1);
   ctx.lineTo(nose[0]-12 + 4, nose[1]- 0.5 * 15 - 7);
   ctx.lineTo(nose[0]-12 + 10, nose[1]- 0.5 * 15 -4);
   ctx.moveTo(nose[0]+12 - 3, nose[1]- 0.5 * 15 -1);
   ctx.lineTo(nose[0]+12 - 4, nose[1]- 0.5 * 15 - 7);
   ctx.lineTo(nose[0]+12 - 10, nose[1]- 0.5 * 15 -4);
   ctx.moveTo(nose[0]+12 , nose[1]+2);
   ctx.lineTo(nose[0]-12 , nose[1]+2);
   ctx.moveTo(nose[0]+12 , nose[1]+4);
   ctx.lineTo(nose[0]+10 , nose[1]+4);
   ctx.lineTo(nose[0]+9 , nose[1]+7);
   ctx.lineTo(nose[0]+4 , nose[1]+7);
   ctx.lineTo(nose[0]+2 , nose[1]+4);
   ctx.lineTo(nose[0] , nose[1]+4);
   ctx.moveTo(nose[0]-12 , nose[1]+4);
   ctx.lineTo(nose[0]-10 , nose[1]+4);
   ctx.lineTo(nose[0]-9 , nose[1]+7);
   ctx.lineTo(nose[0]-4 , nose[1]+7);
   ctx.lineTo(nose[0]-2 , nose[1]+4);
   ctx.lineTo(nose[0] , nose[1]+4);
   ctx.stroke();
}
Dancer.prototype.Body = function(NowMovement,segment,id,cX,cY){
  
  Lhip=[cX+NowMovement[16][0],cY+NowMovement[16][1]];
  Rhip=[cX+NowMovement[15][0],cY+NowMovement[15][1]];
  Lshoulder=[cX+NowMovement[4][0],cY+NowMovement[4][1]];
  Rshoulder=[cX+NowMovement[3][0],cY+NowMovement[3][1]]; 
  vshoulder=getVectorlength(Lshoulder[0]-Rshoulder[0],Lshoulder[1]-Rshoulder[1]);
  //左半身
  ctx.strokeStyle = getcolor(id, segment, 3);
  v=getScaledVector(Lshoulder[0]-Rshoulder[0],Lshoulder[1]-Rshoulder[1],0.4);
  v1=getScaledNormalVector2D(Lshoulder[0]-Rshoulder[0],Lshoulder[1]-Rshoulder[1],5);
  dv=getScaledVector(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],0.4);
  dv1=getScaledNormalVector2D(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],6);
  ctx.beginPath();
  ctx.moveTo(Lshoulder[0]+v1[0],Lshoulder[1]+v1[1]);
  ctx.lineTo(Lshoulder[0]+v1[0]-v[0],Lshoulder[1]+v1[1]-v[1]);
  ctx.lineTo(Lhip[0]-dv1[0]-dv[0],Lhip[1]-dv1[1]-dv[1]);
  ctx.lineTo(Lhip[0]-dv1[0]+dv[0],Lhip[1]-dv1[1]+dv[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(Lshoulder[0]+v1[0],Lshoulder[1]+v1[1]);
  ctx.lineTo(Lshoulder[0]+v1[0]-v[0],Lshoulder[1]+v1[1]-v[1]);
  ctx.lineTo(Lhip[0]-dv1[0]-dv[0],Lhip[1]-dv1[1]-dv[1]);
  ctx.lineTo(Lhip[0]-dv1[0]+dv[0],Lhip[1]-dv1[1]+dv[1]);
  ctx.lineTo(Lshoulder[0]+v1[0],Lshoulder[1]+v1[1]);
  ctx.stroke();
  //右半身
  ctx.strokeStyle = getcolor(id, segment, 4);
  v=getScaledVector(Lshoulder[0]-Rshoulder[0],Lshoulder[1]-Rshoulder[1],0.4);
  v1=getScaledNormalVector2D(Lshoulder[0]-Rshoulder[0],Lshoulder[1]-Rshoulder[1],5);
  dv=getScaledVector(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],0.4);
  dv1=getScaledNormalVector2D(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],6);
  ctx.beginPath();
  ctx.moveTo(Rshoulder[0]+v1[0],Rshoulder[1]+v1[1]);
  ctx.lineTo(Rshoulder[0]-v1[0]+v[0],Rshoulder[1]+v1[1]+v[1]);
  ctx.lineTo(Rhip[0]+dv1[0]+dv[0],Rhip[1]-dv1[1]+dv[1]);
  ctx.lineTo(Rhip[0]+dv1[0]-dv[0],Rhip[1]-dv1[1]-dv[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(Rshoulder[0]+v1[0],Rshoulder[1]+v1[1]);
  ctx.lineTo(Rshoulder[0]+v1[0]+v[0],Rshoulder[1]+v1[1]+v[1]);
  ctx.lineTo(Rhip[0]-dv1[0]+dv[0],Rhip[1]-dv1[1]+dv[1]);
  ctx.lineTo(Rhip[0]+dv1[0]-dv[0],Rhip[1]-dv1[1]-dv[1]);
  ctx.lineTo(Rshoulder[0]-v1[0],Rshoulder[1]-v1[1]);
  ctx.stroke();
}
Dancer.prototype.LeftLeg = function(NowMovement,segment,id,cX,cY){
  ctx.strokeStyle = getcolor(id, segment, 9);
  mh=[(cX+NowMovement[16][0]+cX+NowMovement[15][0])/2,(cY+NowMovement[16][1]+cY+NowMovement[15][1])/2]
  Lhip=[cX+NowMovement[16][0],cY+NowMovement[16][1]];
  Rhip=[cX+NowMovement[15][0],cY+NowMovement[15][1]];
  knee=[cX+NowMovement[18][0],cY+NowMovement[18][1]];
  ankle=[cX+NowMovement[20][0],cY+NowMovement[20][1]];
  v=getScaledNormalVector2D(Lhip[0]-knee[0],Lhip[1]-knee[1],6);
  //handler.debug(v.join(","))
 
  ctx.beginPath();

  mp1=getScaledNormalVector2D(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],-10);


  if(Lhip[0]<Rhip[0]){
    ctx.moveTo(mh[0]+mp1[0],mh[1]+mp1[1]);
    ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
    ctx.moveTo(knee[0]-v[0],knee[1]-v[1]);
    ctx.lineTo(Lhip[0]-v[0],Lhip[1]-v[1]);
    ctx.lineTo(mh[0],mh[1]);
    ctx.stroke();
  }else{
    ctx.moveTo(mh[0]-mp1[0],mh[1]-mp1[1]);
    ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
    ctx.moveTo(knee[0]+v[0],knee[1]+v[1]);
    ctx.lineTo(Lhip[0]+v[0],Lhip[1]+v[1]);
    ctx.lineTo(mh[0],mh[1]);
    ctx.stroke();
  }
  v=getScaledNormalVector2D(knee[0]-ankle[0],knee[1]-ankle[1],6);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.lineTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.lineTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.moveTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.moveTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.lineTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(knee[0],knee[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
  v=getScaledNormalVector2D(Lhip[0]-knee[0],Lhip[1]-knee[1],6);
  v1=getScaledVector(Lhip[0]-knee[0],Lhip[1]-knee[1],0.3)
  ctx.beginPath();
  ctx.moveTo(Lhip[0]+v[0]-v1[0],Lhip[1]+v[1]-v1[1]);
  ctx.lineTo(Lhip[0]-v[0]-v1[0],Lhip[1]-v[1]-v1[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.strokeStyle = getcolor(id, segment, 11);
  
  v=getScaledNormalVector2D(knee[0]-ankle[0],knee[1]-ankle[1],4);
  v1=getScaledNormalVector2D(v[0],v[1],2);
  foot=[ankle[0]+v1[0],ankle[1]+v1[1]];
  ctx.moveTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0],foot[1]-1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0]+3*v1[0],foot[1]-1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0]+3*v1[0],foot[1]+1.5*v[1]+3*v1[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0],foot[1]-1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0]+3*v1[0],foot[1]-1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0]+3*v1[0],foot[1]+1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.stroke();
}
Dancer.prototype.RightLeg = function(NowMovement,segment,id,cX,cY){
  ctx.strokeStyle = getcolor(id, segment, 9);
  mh=[(cX+NowMovement[16][0]+cX+NowMovement[15][0])/2,(cY+NowMovement[16][1]+cY+NowMovement[15][1])/2]
  Lhip=[cX+NowMovement[15][0],cY+NowMovement[15][1]];
  Rhip=[cX+NowMovement[16][0],cY+NowMovement[16][1]];
  knee=[cX+NowMovement[17][0],cY+NowMovement[17][1]];
  ankle=[cX+NowMovement[19][0],cY+NowMovement[19][1]];
  v=getScaledNormalVector2D(Lhip[0]-knee[0],Lhip[1]-knee[1],6);
  //handler.debug(v.join(","))
 
  ctx.beginPath();

  mp1=getScaledNormalVector2D(Lhip[0]-Rhip[0],Lhip[1]-Rhip[1],-10);


  if(Lhip[0]<Rhip[0]){
    ctx.moveTo(mh[0]+mp1[0],mh[1]+mp1[1]);
    ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
    ctx.moveTo(knee[0]-v[0],knee[1]-v[1]);
    ctx.lineTo(Lhip[0]-v[0],Lhip[1]-v[1]);
    ctx.lineTo(mh[0],mh[1]);
    ctx.stroke();
  }else{
    ctx.moveTo(mh[0]-mp1[0],mh[1]-mp1[1]);
    ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
    ctx.moveTo(knee[0]+v[0],knee[1]+v[1]);
    ctx.lineTo(Lhip[0]+v[0],Lhip[1]+v[1]);
    ctx.lineTo(mh[0],mh[1]);
    ctx.stroke();
  }
  v=getScaledNormalVector2D(knee[0]-ankle[0],knee[1]-ankle[1],6);
  //handler.debug(v.join(","))
  ctx.beginPath();
  ctx.moveTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.lineTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.lineTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.moveTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.moveTo(ankle[0]+v[0],ankle[1]+v[1]);
  ctx.lineTo(ankle[0]-v[0],ankle[1]-v[1]);
  ctx.stroke();
  //填滿關節
  ctx.beginPath();  
  ctx.arc(knee[0],knee[1],5.2, 0, Math.PI * 2);
  ctx.closePath();  // 關閉路徑
  ctx.fillStyle = "#000000";  // 這裡可以換成任何你想要的顏色
  ctx.fill();  // 填滿圓形
  v=getScaledNormalVector2D(Lhip[0]-knee[0],Lhip[1]-knee[1],6);
  v1=getScaledVector(Lhip[0]-knee[0],Lhip[1]-knee[1],0.3)
  ctx.beginPath();
  ctx.moveTo(Lhip[0]+v[0]-v1[0],Lhip[1]+v[1]-v1[1]);
  ctx.lineTo(Lhip[0]-v[0]-v1[0],Lhip[1]-v[1]-v1[1]);
  ctx.lineTo(knee[0]-v[0],knee[1]-v[1]);
  ctx.lineTo(knee[0]+v[0],knee[1]+v[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.strokeStyle = getcolor(id, segment, 12);

  v=getScaledNormalVector2D(knee[0]-ankle[0],knee[1]-ankle[1],4);
  v1=getScaledNormalVector2D(v[0],v[1],2);
  foot=[ankle[0]+v1[0],ankle[1]+v1[1]];
  ctx.beginPath();
  ctx.moveTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0],foot[1]-1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0]+3*v1[0],foot[1]-1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0]+3*v1[0],foot[1]+1.5*v[1]+3*v1[1]);
  ctx.closePath();
  ctx.fillStyle = "#000000"; // 黑色
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0],foot[1]-1.5*v[1]);
  ctx.lineTo(foot[0]-1.5*v[0]+3*v1[0],foot[1]-1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0]+3*v1[0],foot[1]+1.5*v[1]+3*v1[1]);
  ctx.lineTo(foot[0]+1.5*v[0],foot[1]+1.5*v[1]);
  ctx.stroke();
}