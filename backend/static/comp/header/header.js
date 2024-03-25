/* Desktop menu section */
const flyoutContactDesktop = document.querySelector('#flyoutContactDesktop');
const flyoutContactButtonDesktop = document.querySelector('#flyoutContactButtonDesktop');
const flyoutContactExpandMoreDesktop = document.querySelector('#flyoutContactExpandMoreDesktop');
const flyoutContactExpandLessDesktop = document.querySelector('#flyoutContactExpandLessDesktop');

flyoutContactDesktop.classList.toggle('hidden');
flyoutContactExpandMoreDesktop.classList.toggle('hidden');

flyoutContactButtonDesktop.addEventListener('click', function () {
    if (flyoutContactExpandMoreDesktop.classList.contains('hidden')) {
        flyoutContactExpandMoreDesktop.classList.remove('hidden');
        flyoutContactExpandLessDesktop.classList.toggle('hidden');
    } else {
        flyoutContactExpandMoreDesktop.classList.toggle('hidden');
        flyoutContactExpandLessDesktop.classList.remove('hidden');
    }

    if (flyoutContactDesktop.classList.contains('hidden')) {
        flyoutContactDesktop.classList.remove('hidden');
    } else {
        flyoutContactDesktop.classList.toggle('hidden');
    }
});
/* Desktop menu section END */


/* Mobile menu section */
/* Mobile menu toggle section */
const mobileMenuOpenButton = document.querySelector('#mobileMenuOpenButton');
const mobileMenuCloseButton = document.querySelector('#mobileMenuCloseButton');
const mobileMenu = document.querySelector("#mobileMenu");

mobileMenu.classList.toggle('hidden');

mobileMenuOpenButton.addEventListener('click', function() {
    mobileMenu.classList.remove('hidden');
})
mobileMenuCloseButton.addEventListener('click', function() {
    mobileMenu.classList.toggle('hidden');
})
/* Mobile menu toggle section END */

/* Mobile menu flyout section */
const flyoutContactMobile = document.querySelector('#flyoutContactMobile');
const flyoutContactButtonMobile = document.querySelector('#flyoutContactButtonMobile');
const flyoutContactExpandMoreMobile = document.querySelector('#flyoutContactExpandMoreMobile');
const flyoutContactExpandLessMobile = document.querySelector('#flyoutContactExpandLessMobile');

flyoutContactMobile.classList.toggle('hidden');
flyoutContactExpandLessMobile.classList.toggle('hidden');

flyoutContactButtonMobile.addEventListener('click', function () {
    if (flyoutContactExpandMoreMobile.classList.contains('hidden')) {
        flyoutContactExpandMoreMobile.classList.remove('hidden');
        flyoutContactExpandLessMobile.classList.toggle('hidden');
    } else {
        flyoutContactExpandMoreMobile.classList.toggle('hidden');
        flyoutContactExpandLessMobile.classList.remove('hidden');
    }

    if (flyoutContactMobile.classList.contains('hidden')) {
        flyoutContactMobile.classList.remove('hidden');
    } else {
        flyoutContactMobile.classList.toggle('hidden');
    }
});
/* Mobile menu flyout section END */
/* Mobile menu section END*/
