//ADDAPTED FROM W3 Schools Examole

// Get the navbar and the placeholder
var navbar = document.getElementById("navbar");
var navbarPlaceholder = document.getElementById("navbar-placeholder");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Function to add the sticky class to the navbar and adjust the placeholder
function addSticky() {
    navbarPlaceholder.style.height = navbar.offsetHeight - 1;
    navbar.classList.add("sticky");
}

// Function to remove the sticky class from the navbar and reset the placeholder height
function removeSticky() {
    navbarPlaceholder.style.height = 0;
    navbar.classList.remove("sticky");
}

// When the user scrolls the page, execute myFunction
window.onscroll = function() {
  if (window.scrollY >= sticky - 15) {
    addSticky();
  } else {
    removeSticky();
  }
};