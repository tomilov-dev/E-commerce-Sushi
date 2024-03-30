let slidesPerPage = 8;
let goToIndex = 0;
let categoryCarousel = document.getElementById("category-carousel");
let selectedCategory = document.getElementById("selected-category");
let slidesCount = categoryCarousel.getAttribute("slides-count");

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
