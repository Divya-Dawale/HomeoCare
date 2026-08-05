document.addEventListener("DOMContentLoaded", function () {

    initializeDarkMode();

});

function initializeDarkMode() {

    const toggle = document.getElementById("themeToggle");

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {

        document.body.classList.add("dark-theme");

        if (toggle) {
            toggle.checked = true;
        }

    }

    if (!toggle) return;

    toggle.addEventListener("change", function () {

        if (this.checked) {

            document.body.classList.add("dark-theme");
            localStorage.setItem("theme", "dark");

        } else {

            document.body.classList.remove("dark-theme");
            localStorage.setItem("theme", "light");

        }

    });

}