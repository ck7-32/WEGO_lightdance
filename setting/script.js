var circles = document.querySelectorAll('.circle');

let isDragging = false;
let offsetX, offsetY;
let currentCircle = null;

//�ˬd�O�_�I�쪫��
document.addEventListener('mousedown', (e) => {
  for (var i = 0; i < circles.length; i++) {
    var rect = circles[i].getBoundingClientRect();

    if (
      e.clientX >= rect.left &&
      e.clientX <= rect.right &&
      e.clientY >= rect.top &&
      e.clientY <= rect.bottom
    ) {
      //����
      isDragging = true;
      offsetX = e.clientX - circles[i].getBoundingClientRect().left;
      offsetY = e.clientY - circles[i].getBoundingClientRect().top;
      circles[i].style.cursor = 'grabbing';
      currentCircle = circles[i]; //�NcurrentCircle ���w���Ӫ���
      document.forms['form'].elements['x'].value = parseInt(currentCircle.style.left);
      document.forms['form'].elements['y'].value = parseInt(currentCircle.style.top);
    }
  }
});

//���ʸӪ���
document.addEventListener('mousemove', (e) => {
  if (isDragging && currentCircle) {
    let x = e.clientX - offsetX;
    let y = e.clientY - offsetY;
    if (x < 10) {
      currentCircle.style.left = 10 + 'px';
    } else if (x > 1125) {
      currentCircle.style.left = 1125 + 'px';
    } else if (y < 10) {
      currentCircle.style.top = 10 + 'px';
    } else if (y > 495) {
      currentCircle.style.top = 495 + 'px';
    } else {
      currentCircle.style.left = x + 'px';
      currentCircle.style.top = y + 'px';
      document.forms['form'].elements['x'].value = parseInt(currentCircle.style.left);
      document.forms['form'].elements['y'].value = parseInt(currentCircle.style.top);
    }
  }
});



//��������
document.addEventListener('mouseup', () => {
  isDragging = false;
  if (currentCircle) {
    currentCircle.style.cursor = 'grab';
  }
  }
);


//��x�Ay�y�Ч�s
function updateCirclePosition() {
  let Form = document.forms['form']
  let XValue = parseFloat(Form.elements['x'].value);
  let YValue = parseFloat(Form.elements['y'].value);
  if (XValue > 1125){
    Form.elements['x'].value = 1125;
  }
  if (XValue < 10){
    Form.elements['x'].value = 10;
  }
  if (YValue > 495){
    Form.elements['y'].value = 1125;
  }
  if (YValue < 0){
    Form.elements["y"].value = 0;
  }
  if (!isNaN(XValue)) {
    currentCircle.style.left = Math.max(10, Math.min(XValue, 1125)) + 'px';
  }

  if (!isNaN(YValue)) {
    currentCircle.style.top = Math.max(10, Math.min(YValue, 495)) + 'px';
  }
};
//��s�C��
function updateCircleColor() {
  let clothCheckbox = document.forms['form'].elements['cloth'];
  let clothColorInput = document.getElementById('clothColor');
  
  if (clothCheckbox.checked) {
    currentCircle.style.opacity = "1";
    currentCircle.style.backgroundColor = clothColorInput.value;
  } else {
    currentCircle.style.opacity = "0.001"; 
  }
}

//save���
function processFormData() {
  let Form = document.forms['form'];
  let xValue = Form.elements['x'].value;
  let yValue = orm.elements['y'].value;
  alert(xValue);

}

