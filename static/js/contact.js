document.addEventListener("DOMContentLoaded", () => {

    const elements = document.querySelectorAll(".info-card, .map-card");

    function reveal() {

        const trigger = window.innerHeight * 0.85;

        elements.forEach(el => {

            if (el.getBoundingClientRect().top < trigger) {

                el.style.opacity = "1";
                el.style.transform = "translateY(0)";
            }

        });

    }

    elements.forEach(el => {

        el.style.opacity = "0";
        el.style.transform = "translateY(40px)";
        el.style.transition = "all .7s ease";

    });

    reveal();

    window.addEventListener("scroll", reveal);

});