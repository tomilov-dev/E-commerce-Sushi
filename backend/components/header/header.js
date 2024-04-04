let mobileMenuOpen = false;
let mobileMenuEl = document.getElementById("mobileMenu");
let mobileOpenButton = document.getElementById("mobileOpenButton");
let mobileCloseButton = document.getElementById("mobileCloseButton");

let flyoutContactMobileEl = document.getElementById("flyoutContactMobile");
let flyoutContactMobileIcon = document.getElementById(
  "flyoutContactMobileIcon"
);

let flyoutContactDesktopEl = document.getElementById("flyoutContactDesktop");
let flyoutContactDesktopIcon = document.getElementById(
  "flyoutContactDesktopIcon"
);

function openMobile() {
  mobileMenuEl.hidden = !mobileMenuEl.hidden;
  mobileOpenButton.hidden = !mobileOpenButton.hidden;
  mobileCloseButton.hidden = !mobileCloseButton.hidden;
}

function openMobileFlyout() {
  flyoutContactMobileEl.hidden = !flyoutContactMobileEl.hidden;
  flyoutContactMobileIcon.classList.toggle("rotate-180");
}

function openDesktopFlyout() {
  flyoutContactDesktopEl.hidden = !flyoutContactDesktopEl.hidden;
  flyoutContactDesktopIcon.classList.toggle("rotate-180");
}
