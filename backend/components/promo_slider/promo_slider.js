document.addEventListener("DOMContentLoaded", function () {
  new Splide("#promo-carousel", {
    type: "loop",
    perPage: 3,
    perMove: 1,
    breakpoints: {
      1024: {
        perPage: 2,
      },
      768: {
        perPage: 1,
      },
    },
  }).mount();
});
