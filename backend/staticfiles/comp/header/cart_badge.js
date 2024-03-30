function cartBadgeChanges(change) {
  let cartBadge = document.querySelector("#cart-units-count-badge");
  let count = parseInt(cartBadge.getAttribute("count"));

  count += change;

  let countText = count;
  if (count > 9) {
    countText = "9+";
  }

  cartBadge.textContent = countText;
  cartBadge.setAttribute("count", count);
}

function cartBadgeSetValue(value, valueText) {
  let cartBadge = document.querySelector("#cart-units-count-badge");

  cartBadge.textContent = valueText;
  cartBadge.setAttribute("count", value);
}
