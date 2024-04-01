let resendCodeElement = document.getElementById("resend-code");
let resendCodeTimeElement = document.getElementById("resend-code-time-element");

let timeElement = document.getElementById("resend-code-time");
let timeValue = parseInt(timeElement.textContent);

let countDown = setInterval(function () {
  timeValue--;
  timeElement.textContent = timeValue;

  if (timeValue <= 0) {
    clearInterval(countDown);
    resendCodeElement.removeAttribute("hidden");
    resendCodeTimeElement.setAttribute("hidden", true);
  }
}, 1000);
