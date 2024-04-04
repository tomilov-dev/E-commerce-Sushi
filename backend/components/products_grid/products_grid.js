function selectUnit(button) {
  unitId = button.getAttribute("unit-id");

  let unitSelector = button.parentNode;
  let unitsSelectors = unitSelector.parentNode;
  let unitsCards = unitsSelectors.nextElementSibling;

  let unitsSelectorsElements =
    unitsSelectors.querySelectorAll(".unit-selector");
  let unitsCardsElements = unitsCards.querySelectorAll(".unit-card");

  for (let unitSelectorElement of unitsSelectorsElements) {
    if (unitSelectorElement.getAttribute("unit-id") === unitId) {
      unitSelectorElement.classList.add("selected");
    } else {
      unitSelectorElement.classList.remove("selected");
    }
  }

  for (let unitCardElement of unitsCardsElements) {
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

  let unitForms = button.parentNode.parentNode.parentNode;
  let unitQuantity = unitForms.querySelector(".unit-quantity");
  let unitRemoveForm = unitForms.querySelector(".unit-remove-form");

  let unitQuantityValueElement = unitForms.querySelector(
    ".unit-quantity-value"
  );
  let unitQuantityValue = parseInt(unitQuantityValueElement.textContent);

  if (unitQuantityValue === 0) {
    unitQuantity.removeAttribute("hidden");
    unitRemoveForm.removeAttribute("hidden");
  }
  unitQuantityValueElement.textContent = unitQuantityValue + 1;

  cartBadgeChanges(1);

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
      showToast("Добавлен товар: " + data["added_item"]);
    });

  return false;
}

function removeFromCart(button) {
  let form = button.closest("form");
  let data = new FormData(form);

  let unitForms = button.parentNode.parentNode.parentNode;
  let unitQuantity = unitForms.querySelector(".unit-quantity");
  let unitRemoveForm = unitForms.querySelector(".unit-remove-form");

  let unitQuantityValueElement = unitForms.querySelector(
    ".unit-quantity-value"
  );
  let unitQuantityValue = parseInt(unitQuantityValueElement.textContent);

  unitQuantityValueElement.textContent = unitQuantityValue - 1;
  if (unitQuantityValue === 1) {
    unitQuantity.setAttribute("hidden", true);
    unitRemoveForm.setAttribute("hidden", true);
  }

  cartBadgeChanges(-1);

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
        throw new Error("Error with unit remove");
      }
    })
    .then((data) => {
      showToast("Удален товар: " + data["removed_item"]);
    });

  return false;
}
