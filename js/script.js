// Image Carousel Infinite Scroll
let currentSlide = 1;
const carousel = document.querySelector('.carousel');
const totalSlides = document.querySelectorAll('.carousel img').length - 2; // Excluding Clones
const slideWidth = 100; // Each slide takes 100% width
let autoScroll;

// Move Slide Function
function moveSlide(direction) {
    clearInterval(autoScroll); // Stop auto scroll temporarily

    currentSlide += direction;
    carousel.style.transition = "transform 0.5s ease-in-out";
    carousel.style.transform = `translateX(-${currentSlide * slideWidth}%)`;

    // Handle Infinite Scroll Transition
    setTimeout(() => {
        if (currentSlide >= totalSlides + 1) {
            currentSlide = 1;
            carousel.style.transition = "none";
            carousel.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
        } else if (currentSlide <= 0) {
            currentSlide = totalSlides;
            carousel.style.transition = "none";
            carousel.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
        }
    }, 500);

    startAutoScroll(); // Restart auto-scroll
}

// Auto Scroll Function
function startAutoScroll() {
    autoScroll = setInterval(() => moveSlide(1), 4000);
}

// Initialize Carousel
window.onload = () => {
    carousel.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
    startAutoScroll();
};
