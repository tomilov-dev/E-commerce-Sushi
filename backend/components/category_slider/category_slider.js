const slideWidth = 100;

let widthBPs = {
  1200: 1190,
  1024: 800,
  768: 600,
  640: 480,
  400: 300,
};

let slidesBPs = {
  1200: 12,
  1024: 8,
  768: 6,
  640: 4,
  400: 3,
};

function setMaxWidth(slides, categoryCarousel) {
  let width = slideWidth * slides;
  categoryCarousel.style.width = width + "px";
}

function getSlidesPerPage(maxSlides, categoryCarousel) {
  let spp = slidesBPs[400];
  let width = window.innerWidth;

  let keys = Object.keys(slidesBPs)
    .map(Number)
    .sort((a, b) => b - a);

  let widthBP;
  for (let bp of keys) {
    if (width >= bp) {
      widthBP = bp;
      spp = slidesBPs[bp];
      break;
    }
  }

  if (spp > maxSlides) {
    setMaxWidth(maxSlides, categoryCarousel);
  }

  return Math.min(spp, maxSlides);
}

let categoryCarousel = document.getElementById("category-carousel");
let slidesCount = categoryCarousel.getAttribute("slides-count");
let slidesPerPage = getSlidesPerPage(slidesCount, categoryCarousel);

let goToIndex = 0;
let selectedCategory = document.getElementById("selected-category");

if (selectedCategory) {
  let currentIndex = selectedCategory.getAttribute("category-index");
  let spread = currentIndex - slidesPerPage;
  if (spread > 0) {
    goToIndex = spread + 1;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  new Splide("#category-carousel", {
    type: "loop",
    perPage: slidesPerPage,
    perMove: 1,
    pagination: false,
  })
    .mount()
    .go(goToIndex);
});
