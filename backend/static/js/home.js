document.addEventListener("DOMContentLoaded", function () {
    const arrow = document.getElementById("scroll-arrow");
    const loginSection = document.getElementById("login-section");

    if (arrow && loginSection) {
        arrow.addEventListener("click", function () {
            loginSection.scrollIntoView({ behavior: "smooth" });
        });
    }
});
