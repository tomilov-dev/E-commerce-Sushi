let toastCounter = 0;
let toastComponentHTML = document
  .querySelector("#toast-template")
  .querySelector(".toast").outerHTML;
let toastContainer = document.querySelector(".toast-container");

function showToast(content) {
  let newToast = document.createElement("div");
  newToast.innerHTML = toastComponentHTML;
  if (!newToast.classList.contains("toast-element")) {
    newToast.classList.add("toast-element");
  }

  let toastId = toastCounter;
  let newToastCloseButton = newToast.querySelector("button");

  newToast.setAttribute("toast-id", toastId);
  newToastContent = newToast.querySelector(".toast-content");
  newToastContent.textContent = content;
  newToastCloseButton.setAttribute("toast-id", toastId);

  toastCounter++;
  toastContainer.appendChild(newToast);

  setTimeout(function () {
    closeToast(newToastCloseButton);
  }, 3000);
}

function closeToast(toastCloseButton) {
  let toastId = toastCloseButton.getAttribute("toast-id");
  let toastElement = toastContainer.querySelector(
    `.toast-element[toast-id="${toastId}"]`
  );

  if (toastElement) {
    toastElement.remove();
  }
}
