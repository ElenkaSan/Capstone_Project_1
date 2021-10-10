window.onload = choosePic;

const myPix = new Array("/static/images/h1.png",
"/static/images/h2.png",
"/static/images/h3.png",
"/static/images/h4.png",
"/static/images/h5.png",
"/static/images/h6.png",
"/static/images/h7.png",
"/static/images/h8.png",
"/static/images/h9.png",
"/static/images/h10.png",
"/static/images/h12.png",
"/static/images/h13.png",
"/static/images/h14.png",
"/static/images/h15.png",
"/static/images/h16.png",
);

function choosePic() {
     var randomNum = Math.floor(Math.random() * myPix.length);
     document.getElementById("execise").src = myPix[randomNum];
}

