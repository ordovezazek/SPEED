var modal = document.getElementById("modal-content");

// var img = document.getElementById("myImg");
// var img2 = document.getElementById("myImg2");
// var img3 = document.getElementById("myImg3");

var modalImg = document.getElementById("img01");

var images = document.getElementsByClassName("myImg")

for(var i = 0; i < images.length; i++) {
    let img = images[i];
    console.log(img);
    img.onclick = function() {
        modal.style.display = "block";
        modalImg.src = this.src;
    }
}

var span = document.getElementsByClassName("ap-close")[0];

span.onclick = function() {
    modal.style.display = "none";
}

window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});