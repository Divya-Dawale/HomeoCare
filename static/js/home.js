console.log("HOME JS IS WORKING");
// ===============================
// FAQ ACCORDION
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const questions = document.querySelectorAll(".faq-question");

    questions.forEach(question => {

        question.addEventListener("click", function () {

            const item = this.parentElement;

            document.querySelectorAll(".faq-item").forEach(faq => {

                if (faq !== item) {
                    faq.classList.remove("active");
                    faq.querySelector("span").textContent = "+";
                }

            });

            item.classList.toggle("active");

            this.querySelector("span").textContent =
                item.classList.contains("active") ? "−" : "+";

        });

    });

});
   


// ===============================
// SCROLL REVEAL
// ===============================

const revealElements = document.querySelectorAll(

".trust-card, .service-card, .process-card, .testimonial-card, .stat-box"

);

function revealOnScroll(){

    const trigger = window.innerHeight * 0.85;

    revealElements.forEach(el=>{

        const top = el.getBoundingClientRect().top;

        if(top < trigger){

            el.classList.add("active","reveal");

        }

    });

}

window.addEventListener("scroll",revealOnScroll);

revealOnScroll();


// ===============================
// NUMBER COUNT ANIMATION
// ===============================

const counters = document.querySelectorAll(".stat-box h2");

let counted = false;

function animateCounters(){

    if(counted) return;

    const stats = document.querySelector(".stats");

    if(!stats) return;

    const top = stats.getBoundingClientRect().top;

    if(top < window.innerHeight-100){

        counted = true;

        counters.forEach(counter=>{

            const text = counter.innerText;

            const number = parseInt(text);

            if(isNaN(number)) return;

            let current = 0;

            const increment = Math.ceil(number/80);

            const timer = setInterval(()=>{

                current += increment;

                if(current>=number){

                    current = number;

                    clearInterval(timer);

                }

                if(text.includes("%")){

                    counter.innerText = current+"%";

                }

                else if(text.includes("+")){

                    counter.innerText = current+"+";

                }

                else{

                    counter.innerText=current;

                }

            },20);

        });

    }

}

window.addEventListener("scroll",animateCounters);

animateCounters();


// ===============================
// PARALLAX HERO
// ===============================

const doctor = document.querySelector(".doctor-card");

window.addEventListener("mousemove",(e)=>{

    if(!doctor) return;

    const x = (window.innerWidth/2 - e.clientX)/40;

    const y = (window.innerHeight/2 - e.clientY)/40;

    doctor.style.transform=`translate(${x}px,${y}px)`;

});


// ===============================
// SMOOTH BUTTON RIPPLE
// ===============================

const buttons=document.querySelectorAll(".btn-primary,.btn-secondary");

buttons.forEach(button=>{

button.addEventListener("click",function(e){

const ripple=document.createElement("span");

const rect=this.getBoundingClientRect();

const size=Math.max(rect.width,rect.height);

ripple.style.width=size+"px";

ripple.style.height=size+"px";

ripple.style.left=e.clientX-rect.left-size/2+"px";

ripple.style.top=e.clientY-rect.top-size/2+"px";

ripple.classList.add("ripple");

this.appendChild(ripple);

setTimeout(()=>{

ripple.remove();

},600);

});

});


// ===============================
// NAVBAR SHADOW
// ===============================

const navbar = document.querySelector(".navbar");

if (navbar) {

    window.addEventListener("scroll", () => {

        if (window.scrollY > 40) {
            navbar.classList.add("nav-scrolled");
        } else {
            navbar.classList.remove("nav-scrolled");
        }

    });

}


// ===============================
// FLOATING CARDS
// ===============================

const floatingCards=document.querySelectorAll(".floating-card");

floatingCards.forEach((card,index)=>{

card.animate(

[

{

transform:"translateY(0px)"

},

{

transform:"translateY(-15px)"

},

{

transform:"translateY(0px)"

}

],

{

duration:3000+(index*700),

iterations:Infinity

}

);

});


// ===============================
// ACTIVE NAV LINK
// ===============================

const sections=document.querySelectorAll("section");

const navLinks=document.querySelectorAll(".nav-links a");

window.addEventListener("scroll",()=>{

let current="";

sections.forEach(section=>{

const top=section.offsetTop-150;

if(pageYOffset>=top){

current=section.getAttribute("class");

}

});

navLinks.forEach(link=>{

link.classList.remove("active");

});

});


// ===============================
// PAGE FADE IN
// ===============================

window.addEventListener("load",()=>{

document.body.classList.add("loaded");

});
const backToTop = document.getElementById("backToTop");

if (backToTop) {

    window.addEventListener("scroll", () => {

        if (window.scrollY > 300) {

            backToTop.classList.add("show");

        } else {

            backToTop.classList.remove("show");

        }

    });

    backToTop.addEventListener("click", () => {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });

}