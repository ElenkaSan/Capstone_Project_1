window.onload = choosePic;

const myPix = new Array("/static/images/h1.jpeg",
"/static/images/h2.jpeg",
"/static/images/h3.jpeg",
"/static/images/h4.jpeg",
"/static/images/h5.jpeg",
"/static/images/h6.jpeg",
"/static/images/h7.jpeg",
"/static/images/h8.jpeg",
"/static/images/h9.jpeg",
"/static/images/h10.jpeg",
"/static/images/h12.jpeg",
"/static/images/h13.jpeg",
"/static/images/h14.jpeg",
"/static/images/h15.jpeg",
"/static/images/h16.jpeg",
);

function choosePic() {
     var randomNum = Math.floor(Math.random() * myPix.length);
     document.getElementById("execise").src = myPix[randomNum];
}

