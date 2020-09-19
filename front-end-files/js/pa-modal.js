// SF 
var modal = document.getElementById("myModal-1");
var trigger = document.getElementById("modal-1");
var span = document.getElementsByClassName("pa-close")[0]; 

trigger.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
});


//SOC
  var modal2 = document.getElementById("myModal-2");
  var trigger2 = document.getElementById("modal-2");
  var span2 = document.getElementsByClassName("pa-close")[1]; 

trigger2.onclick = function() {
  modal2.style.display = "block";
}

span2.onclick = function() {
  modal2.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal2) {
    modal2.style.display = "none";
  }
});


//SHC
var modal3 = document.getElementById("myModal-3");
var trigger3 = document.getElementById("modal-3");
var span3 = document.getElementsByClassName("pa-close")[2]; 

trigger3.onclick = function() {
modal3.style.display = "block";
}

span3.onclick = function() {
modal3.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal3) {
    modal3.style.display = "none";
  }
});

//PGA 

var modal4 = document.getElementById("myModal-4");
var trigger4 = document.getElementById("modal-4");
var span4 = document.getElementsByClassName("pa-close")[3]; 

trigger4.onclick = function() {
modal4.style.display = "block";
}

span4.onclick = function() {
modal4.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal4) {
    modal4.style.display = "none";
  }
});

//LLL
var modal5 = document.getElementById("myModal-5");
var trigger5 = document.getElementById("modal-5");
var span5 = document.getElementsByClassName("pa-close")[4]; 

trigger5.onclick = function() {
modal5.style.display = "block";
}

span5.onclick = function() {
modal5.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal5) {
    modal5.style.display = "none";
  }
});


//EC

var modal6 = document.getElementById("myModal-6");
var trigger6 = document.getElementById("modal-6");
var span6 = document.getElementsByClassName("pa-close")[5]; 

trigger6.onclick = function() {
modal6.style.display = "block";
}

span6.onclick = function() {
modal6.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == modal6) {
    modal6.style.display = "none";
  }
});
