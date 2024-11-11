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
    //貓耳
    ctx.strokeStyle = getcolor(this.id, segment,0);
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius, head_radius - 3, Math.PI, Math.PI * 2);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 - 1, this.base_y + 3);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 + 1, this.base_y + 3);
    ctx.stroke();
    //帽子
    ctx.strokeStyle = getcolor(this.id, segment,1 );
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius+2, head_radius - 5, Math.PI,2 * Math.PI );
    ctx.moveTo(this.base_x+this.width / 2-head_radius + 5 , this.base_y +head_radius + 2);
    ctx.lineTo(this.base_x+this.width / 2+head_radius - 5 , this.base_y +head_radius + 2);
    ctx.ellipse(this.base_x + this.width / 2, this.base_y + head_radius+2, head_radius-5, 5,0, Math.PI, 2 * Math.PI,true);
    ctx.stroke();
  //手臂
    var hand_w = 10;
    var hand_h = 20;
  
    ctx.strokeStyle = getcolor(this.id, segment, 4);
    ctx.strokeRect(this.base_x, this.base_y + head_radius - 8 + hand_h + 5, hand_w, hand_h * 2);
    ctx.strokeStyle = getcolor(this.id, segment, 5);
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + head_radius - 8 + hand_h + 5, hand_w, hand_h * 2);
  //手環
    var hand_radius = 6;
    ctx.strokeStyle = getcolor(this.id, segment, 4);
    ctx.beginPath();
    ctx.strokeRect(this.base_x, this.base_y + 3 * head_radius + hand_h , hand_w, 3);
    ctx.stroke();
  
    ctx.strokeStyle = getcolor(this.id, segment, 5);
    ctx.beginPath();
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + 3 * head_radius + hand_h , hand_w, 3);
    ctx.stroke();
  //手套
  ctx.lineWidth=2;
    ctx.strokeStyle = getcolor(this.id, segment, 6);
    ctx.beginPath();
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
    ctx.strokeStyle = getcolor(this.id, segment, 7);
    ctx.beginPath();
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
  //西裝外套
  ctx.lineWidth=3;
    ctx.strokeStyle = getcolor(this.id, segment, 3);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius-3);
    ctx.lineTo(this.base_x + this.width / 2 - 6, this.base_y + 2 * head_radius-3 );
    ctx.lineTo(this.base_x + this.width / 2 - 6, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 2 * head_radius +20);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius-3);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 7, this.base_y + 2 * head_radius-3); 
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 8, this.base_y + 2 * head_radius+11);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 10, this.base_y + 2 * head_radius+10);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 12, this.base_y + 2 * head_radius+20);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 1, this.base_y + 2 * head_radius); 
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius-3);
    ctx.lineTo(this.base_x + this.width / 2 +6, this.base_y + 2 * head_radius-3 );
    ctx.lineTo(this.base_x+ this.width / 2 +6, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 2 * head_radius +20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius-3);
    ctx.moveTo(this.base_x+ this.width / 2 + head_radius - 7, this.base_y + 2 * head_radius-3); 
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 8, this.base_y + 2 * head_radius+11);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 10, this.base_y + 2 * head_radius+10);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 12, this.base_y + 2 * head_radius+20);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 1, this.base_y + 2 * head_radius);    
    ctx.stroke();
    
  //裡面衣服
  ctx.strokeStyle = getcolor(this.id, segment, 0)
  ctx.beginPath();
  ctx.moveTo(this.base_x + this.width / 2 +6, this.base_y + 2 * head_radius+1 );
  ctx.lineTo(this.base_x + this.width / 2 , this.base_y + 2 * head_radius+3 );
  ctx.lineTo(this.base_x + this.width / 2-6, this.base_y + 2 * head_radius+1 );
  ctx.moveTo(this.base_x + this.width / 2 +6, this.base_y + 2 * head_radius +25);
  ctx.lineTo(this.base_x + this.width / 2 -6, this.base_y + 2 * head_radius +25);
  ctx.stroke();
  //裙子
    var belt_w = 2 * head_radius - 6;
    var belt_h = 10;
    var pants_w = 12;
    var pants_h = 35;
    ctx.lineWidth=2;
    ctx.strokeStyle = getcolor(this.id, segment, 8);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 4, this.base_y + 3 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 2, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 2, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 4, this.base_y + 3 * head_radius + 20);
    ctx.moveTo(this.base_x + this.width / 2 +5, this.base_y + 2 * head_radius +35);
    ctx.lineTo(this.base_x + this.width / 2 -5, this.base_y + 2 * head_radius +35);
    ctx.stroke();
  
  //左襪套
    ctx.strokeStyle = getcolor(this.id, segment, 9);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 65);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 +pants_w, this.base_y + 4 * head_radius + 65);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5+pants_w, this.base_y + 4 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 40);
    ctx.stroke();
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 10, this.base_y + 4 * head_radius + 45);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius +pants_w, this.base_y + 4 * head_radius + 60);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius +pants_w+1, this.base_y + 4 * head_radius + 45);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius +9, this.base_y + 4 * head_radius + 60);
    ctx.stroke();
    
  //右襪套
    ctx.strokeStyle = getcolor(this.id, segment, 10);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 65);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 -pants_w, this.base_y + 4 * head_radius + 65);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5-pants_w, this.base_y + 4 * head_radius + 40);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 40);
    ctx.stroke();
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius -9, this.base_y + 4 * head_radius + 45);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius -pants_w, this.base_y + 4 * head_radius + 60);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius -pants_w, this.base_y + 4 * head_radius + 45);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius -10, this.base_y + 4 * head_radius + 60);
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
   
     ctx.strokeStyle = getcolor(this.id, segment, 11);
     ctx.beginPath();
     ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
     ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30);
     ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30 + pants_h);
     ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
     ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30);
     ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
     ctx.stroke();
   
     ctx.strokeStyle = getcolor(this.id, segment, 12);
     ctx.beginPath();
     ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30 + pants_h);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30);
     ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
     ctx.stroke();
   };
  