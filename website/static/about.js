const carouselSlide = document.querySelector(".carousel-slide");
const images = document.querySelectorAll(".carousel-slide img");
const imageWidth = images[0].clientWidth;
let counter = 1;

setInterval(() => {
  carouselSlide.style.transition = "transform 0.5s ease-in-out";
  carouselSlide.style.transform = `translateX(${-imageWidth * counter}px)`;
  counter++;
  if (counter === images.length) {
    setTimeout(() => {
      carouselSlide.style.transition = "none";
      carouselSlide.style.transform = `translateX(0)`;
      counter = 1;
    }, 1000);
  }
}, 10000);
