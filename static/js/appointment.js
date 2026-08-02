document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       SCROLL REVEAL
    =============================== */

    const elements = document.querySelectorAll(
        ".info-box, .form-card, .success-card"
    );

    function reveal() {

        const trigger = window.innerHeight * 0.85;

        elements.forEach(el => {

            if (el.getBoundingClientRect().top < trigger) {
                el.classList.add("active");
            }

        });

    }

    reveal();

    window.addEventListener("scroll", reveal);



    /* ===============================
       HERO PARALLAX
    =============================== */

    const circle1 = document.querySelector(".circle-1");
    const circle2 = document.querySelector(".circle-2");

    document.addEventListener("mousemove", e => {

        const x = (window.innerWidth / 2 - e.clientX) / 40;
        const y = (window.innerHeight / 2 - e.clientY) / 40;

        if(circle1)
            circle1.style.transform=`translate(${x}px,${y}px)`;

        if(circle2)
            circle2.style.transform=`translate(${-x}px,${-y}px)`;

    });



    /* ===============================
       INPUT ANIMATION
    =============================== */

    document.querySelectorAll("input, textarea, select").forEach(input=>{

        input.addEventListener("focus",()=>{

            input.parentElement.classList.add("focused");

        });

        input.addEventListener("blur",()=>{

            input.parentElement.classList.remove("focused");

        });

    });



    /* ===============================
       SUBMIT BUTTON
    =============================== */

    document.querySelectorAll("form").forEach(form=>{

        form.addEventListener("submit",()=>{

            const btn=form.querySelector(".appointment-btn");

            if(btn){

                btn.innerHTML="Please Wait...";

                btn.disabled=true;

            }

        });

    });

});