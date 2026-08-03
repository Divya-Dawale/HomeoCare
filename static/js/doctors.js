console.log("Doctor JS Loaded");
/*=========================================
        HomeoCare Doctor Panel
=========================================*/

document.addEventListener("DOMContentLoaded", () => {

    initializeSidebar();

    initializeNotification();

    initializeProfile();

    initializeActiveMenu();

});
/*=========================================
        MOBILE SIDEBAR
=========================================*/

function initializeSidebar(){

    const menuButton =
    document.querySelector(".menu-toggle");

    const sidebar =
    document.querySelector(".sidebar");

    if(!menuButton || !sidebar) return;

    menuButton.addEventListener("click",function(e){

        e.stopPropagation();

        sidebar.classList.toggle("show-sidebar");

    });

}



/*=========================================
        CLOSE SIDEBAR
=========================================*/

document.addEventListener("click",function(e){

    const sidebar =
    document.querySelector(".sidebar");

    const menuButton =
    document.querySelector(".menu-toggle");

    if(!sidebar || !menuButton) return;

    if(

        window.innerWidth <= 992 &&

        sidebar.classList.contains("show-sidebar") &&

        !sidebar.contains(e.target) &&

        !menuButton.contains(e.target)

    ){

        sidebar.classList.remove("show-sidebar");

    }

});
/*=========================================
        ACTIVE SIDEBAR MENU
=========================================*/

function initializeActiveMenu(){

    const currentPath =
    window.location.pathname;

    const menuItems =
    document.querySelectorAll(".menu-item");

    menuItems.forEach(item=>{

        const itemPath =
        new URL(item.href).pathname;

        if(itemPath === currentPath){

            item.classList.add("active");

        }

    });

}
/*=========================================
        NOTIFICATION EFFECT
=========================================*/

function initializeNotification() {

    const bell = document.querySelector(".notification");

    if (!bell) return;

    bell.addEventListener("click", () => {

        bell.classList.add("ring");

        setTimeout(() => {

            bell.classList.remove("ring");

        }, 600);

    });

}



/*=========================================
        PROFILE EFFECT
=========================================*/

function initializeProfile(){

    const profile =
    document.querySelector(".profile");

    if(!profile) return;

    profile.addEventListener("mouseenter",()=>{

        profile.classList.add("active");

    });

    profile.addEventListener("mouseleave",()=>{

        profile.classList.remove("active");

    });

}