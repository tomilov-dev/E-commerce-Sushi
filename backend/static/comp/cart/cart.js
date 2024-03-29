function cartPriceChanges(itemsPrice, deliveryPrice, totalPrice) {
  let itemsPriceEl = document.querySelector("#cart-items-price");
  let deliveryPriceEl = document.querySelector("#cart-delivery-price");
  let totalPriceEl = document.querySelector("#cart-total-price");

  itemsPriceEl.textContent = itemsPrice + " ₽";
  deliveryPriceEl.textContent = deliveryPrice + " ₽";
  totalPriceEl.textContent = totalPrice + " ₽";
}

function addToCart(button) {
  let form = button.closest("form");
  let data = new FormData(form);

  let cartItem = form.parentNode.parentNode.parentNode.parentNode;
  let cartItemTPV = cartItem.querySelector(".item-total-price-value");
  let itemQ = cartItem.querySelector(".item-quantity-value");

  let itemQV = parseInt(itemQ.textContent);
  itemQ.textContent = itemQV + 1;

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
        throw new Error("Error with item add");
      }
    })
    .then((data) => {
      showToast("Добавлен товар: " + data["added_item"]);
      cartPriceChanges(
        data["items_price"],
        data["delivery_price"],
        data["cart_price"]
      );
      cartItemTPV.textContent = data["unit_total_price"];
    });

  cartBadgeChanges(1);
  return false;
}

function removeFromCart(button) {
  let form = button.closest("form");
  let data = new FormData(form);

  let cartItem = form.parentNode.parentNode.parentNode.parentNode;
  let cartItemTPV = cartItem.querySelector(".item-total-price-value");
  let itemQ = cartItem.querySelector(".item-quantity-value");

  let itemQV = parseInt(itemQ.textContent);
  itemQ.textContent = itemQV - 1;

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
      cartPriceChanges(
        data["items_price"],
        data["delivery_price"],
        data["cart_price"]
      );
      utp = data["unit_total_price"];
      if (utp === null) {
        cartItem.remove();
      } else {
        cartItemTPV.textContent = utp;
      }
    });

  cartBadgeChanges(-1);
  return false;
}

function deleteFromCart(button) {
  let form = button.closest("form");
  let data = new FormData(form);
  let cartItem = button.parentNode.parentNode.parentNode.parentNode;

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
      showToast("Убраны товары: " + data["deleted_item"]);
      cartBadgeSetValue(data["units_count"], data["units_count_text"]);
      cartPriceChanges(
        data["items_price"],
        data["delivery_price"],
        data["cart_price"]
      );
      cartItem.remove();
    });

  return false;
}
