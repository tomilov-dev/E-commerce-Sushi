function selectUnit(button) {
  unitId = button.getAttribute("id");

  let unitSelector = button.parentNode;
  let unitsSelectors = unitSelector.parentNode;
  let unitsCards = unitsSelectors.nextElementSibling;

  let unitsSelectorsElements = unitsSelectors.querySelectorAll(".unit");
  let unitsCardsElements = unitsCards.querySelectorAll(".unit-card");

  for (unitSelectorElement of unitsSelectorsElements) {
    if (unitSelectorElement.getAttribute("unit-id") === unitId) {
      unitSelectorElement.classList.add("selected");
    } else {
      unitSelectorElement.classList.remove("selected");
    }
  }

  for (unitCardElement of unitsCardsElements) {
    if (unitCardElement.getAttribute("unit-id") === unitId) {
      unitCardElement.removeAttribute("hidden");
    } else {
      unitCardElement.setAttribute("hidden", true);
    }
  }
}

function addToCart(button) {
  let form = button.closest("form");
  let data = new FormData(form);

  fetch(form.action, {
    method: "POST",
    body: data,
    headers: {
      "X-CSRFToken": data.get("csrfmiddlewaretoken"),
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error with unit add");
      }
    })
    .then((data) => {
      console.log(data);
    });

  return false;
}
