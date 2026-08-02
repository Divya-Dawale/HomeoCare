document.addEventListener("DOMContentLoaded",()=>{

    /* ==========================
       REVEAL
    ========================== */

    const items=document.querySelectorAll(
        ".status-form-card,.status-result-card"
    );

    function reveal(){

        const trigger=window.innerHeight*0.85;

        items.forEach(item=>{

            if(item.getBoundingClientRect().top<trigger){

                item.classList.add("active");

            }

        });

    }

    reveal();

    window.addEventListener("scroll",reveal);



    /* ==========================
       HERO PARALLAX
    ========================== */

    const c1=document.querySelector(".circle-1");
    const c2=document.querySelector(".circle-2");

    document.addEventListener("mousemove",(e)=>{

        const x=(window.innerWidth/2-e.clientX)/40;
        const y=(window.innerHeight/2-e.clientY)/40;

        if(c1)
            c1.style.transform=`translate(${x}px,${y}px)`;

        if(c2)
            c2.style.transform=`translate(${-x}px,${-y}px)`;

    });



    /* ==========================
       INPUT EFFECT
    ========================== */

    document.querySelectorAll("input").forEach(input=>{

        input.addEventListener("focus",()=>{

            input.parentElement.classList.add("focused");

        });

        input.addEventListener("blur",()=>{

            input.parentElement.classList.remove("focused");

        });

    });



    /* ==========================
       BUTTON LOADING
    ========================== */

    const form=document.querySelector("form");

    if(form){

        form.addEventListener("submit",()=>{

            const btn=document.querySelector(".status-btn");

            btn.innerHTML="Checking...";

            btn.disabled=true;

        });

    }

});