// =========================================
// Sidebar Active Link
// =========================================

const currentPath = window.location.pathname;

document.querySelectorAll(".sidebar nav a").forEach(link => {

    if (link.getAttribute("href") === currentPath) {

        link.classList.add("active");

    }

});

// =========================================
// Fade Animation
// =========================================

window.addEventListener("load", () => {

    document.body.classList.add("loaded");

});

// =========================================
// Notification Button
// =========================================

const notificationBtn = document.querySelector(".notification");

if(notificationBtn){

    notificationBtn.addEventListener("click",()=>{

        notificationBtn.classList.toggle("ring");

    });

}

// =========================================
// Dark Mode
// =========================================

const darkBtn = document.getElementById("darkModeToggle");

if(darkBtn){

    if(localStorage.getItem("theme")==="dark"){

        document.body.classList.add("dark");

    }

    darkBtn.addEventListener("click",()=>{

        document.body.classList.toggle("dark");

        if(document.body.classList.contains("dark")){

            localStorage.setItem("theme","dark");

        }

        else{

            localStorage.setItem("theme","light");

        }

    });

}

// =========================================
// Mobile Sidebar
// =========================================

const sidebar = document.querySelector(".sidebar");
const menuBtn = document.getElementById("menuBtn");
const sidebarOverlay = document.getElementById("sidebarOverlay");

if(menuBtn && sidebar){

    menuBtn.addEventListener("click", () => {

        sidebar.classList.toggle("show");

        if(sidebarOverlay){
            sidebarOverlay.classList.toggle("show");
        }

    });

}


if(sidebarOverlay){

    sidebarOverlay.addEventListener("click", () => {

        sidebar.classList.remove("show");
        sidebarOverlay.classList.remove("show");

    });

}