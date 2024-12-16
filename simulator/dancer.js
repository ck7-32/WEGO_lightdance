
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
  ctx.lineWidth=1.5;

  this.originaldraw(head_radius,segment);
  var head_radius = 20;
  ctx.font = "20px sans-serif";
  ctx.fillStyle = "#FF0000";
  ctx.fillText(this.id, this.base_x + this.width / 2 - 5, this.base_y -head_radius + 6);
};
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
  var glass_width = 12; 
  var glass_height = 8; 
  var glass_y_offset = head_radius + 10; 
  var bridge_width = 6; 
  ctx.rect(
    this.base_x + this.width / 2 - head_radius / 2 - glass_width / 2,
    this.base_y + glass_y_offset -12,
    glass_width,
    glass_height
  );
  ctx.rect(
    this.base_x + this.width / 2 + head_radius / 2 - glass_width / 2,
    this.base_y + glass_y_offset-12,
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
  ctx.lineWidth=2;
  ctx.strokeStyle = getcolor(this.id, segment, 7);
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
  // 左鞋
ctx.beginPath();
ctx.strokeStyle = getcolor(this.id, segment, 11); // 設定左鞋的顏色

ctx.moveTo(this.base_x + this.width / 2 - head_radius - 2, this.base_y + 3 * head_radius + 100); // 左鞋起點
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 26, this.base_y + 3 * head_radius + 100); // 左鞋底邊
ctx.lineTo(this.base_x + this.width / 2 + head_radius - 25, this.base_y + 3 * head_radius + 108); // 左鞋後跟
ctx.lineTo(this.base_x + this.width / 2 - head_radius - 6, this.base_y + 3 * head_radius + 108); // 左鞋前端
ctx.closePath();

ctx.stroke();

// 右鞋
ctx.beginPath();
ctx.strokeStyle = getcolor(this.id, segment, 12); // 設定右鞋的顏色

ctx.moveTo(this.base_x + this.width / 2 + head_radius + 2, this.base_y + 3 * head_radius + 100); // 右鞋起點
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 26, this.base_y + 3 * head_radius + 100); // 右鞋底邊
ctx.lineTo(this.base_x + this.width / 2 - head_radius + 25, this.base_y + 3 * head_radius + 108); // 右鞋後跟
ctx.lineTo(this.base_x + this.width / 2 + head_radius + 6, this.base_y + 3 * head_radius + 108); // 右鞋前端
ctx.closePath();

ctx.stroke();

};
