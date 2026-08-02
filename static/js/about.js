document.addEventListener("DOMContentLoaded", () => {

    const revealElements = document.querySelectorAll(".reveal");

    function revealOnScroll() {

        const trigger = window.innerHeight * 0.85;

        revealElements.forEach((el) => {

            const top = el.getBoundingClientRect().top;

            if (top < trigger) {
                el.classList.add("active");
            }

        });

    }

    revealOnScroll();

    window.addEventListener("scroll", revealOnScroll);

});