
/*=========================================
        HomeoCare Receptionist Panel
=========================================*/


document.addEventListener("DOMContentLoaded", () => {

    initializeSidebar();

    initializeNotification();

    initializeProfile();

    initializeDarkMode();

});



/*=========================================
        MOBILE SIDEBAR
=========================================*/

function initializeSidebar() {

    const menuButton = document.querySelector(".menu-toggle");

    const sidebar = document.querySelector(".sidebar");

    if (!menuButton || !sidebar) return;

    menuButton.addEventListener("click", () => {

        sidebar.classList.toggle("show-sidebar");

    });

}



/*=========================================
        CLOSE SIDEBAR ON MOBILE
=========================================*/

document.addEventListener("click", function (e) {

    const sidebar = document.querySelector(".sidebar");

    const button = document.querySelector(".menu-toggle");

    if (!sidebar || !button) return;

    if (

        window.innerWidth <= 992 &&

        !sidebar.contains(e.target) &&

        !button.contains(e.target)

    ) {

        sidebar.classList.remove("show-sidebar");

    }

});



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
        PROFILE HOVER
=========================================*/

function initializeProfile() {

    const profile = document.querySelector(".profile");

    if (!profile) return;

    profile.addEventListener("mouseenter", () => {

        profile.classList.add("active");

    });

    profile.addEventListener("mouseleave", () => {

        profile.classList.remove("active");

    });

}

/*=========================================
            DARK MODE
=========================================*/

function initializeDarkMode(){

    const toggle =
    document.getElementById("themeToggle");

    /* Restore saved theme */

    const savedTheme =
    localStorage.getItem("theme");

    if(savedTheme === "dark"){

        document.body.classList.add("dark-theme");

        if(toggle){

            toggle.checked = true;

        }

    }

    if(!toggle) return;

    toggle.addEventListener("change",function(){

        if(this.checked){

            document.body.classList.add("dark-theme");

            localStorage.setItem(
                "theme",
                "dark"
            );

        }

        else{

            document.body.classList.remove("dark-theme");

            localStorage.setItem(
                "theme",
                "light"
            );

        }

    });

}
