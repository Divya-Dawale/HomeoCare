document.addEventListener("DOMContentLoaded", () => {

    // Reveal Animation

    const revealItems = document.querySelectorAll(".reveal");

    function reveal() {

        const trigger = window.innerHeight * 0.85;

        revealItems.forEach(item => {

            if (item.getBoundingClientRect().top < trigger) {
                item.classList.add("active");
            }

        });

    }

    reveal();

    window.addEventListener("scroll", reveal);




    // FAQ

    const questions = document.querySelectorAll(".faq-question");

    questions.forEach(question => {

        question.addEventListener("click", function(){

            const item = this.parentElement;

            item.classList.toggle("active");

            const icon = this.querySelector("span");

            icon.textContent = item.classList.contains("active") ? "−" : "+";

        });

    });

});