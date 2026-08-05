// ===================================================
//              WEBSOCKET CONNECTION
// ===================================================

const socket = new WebSocket(
    "ws://" +
    window.location.host +
    "/ws/notifications/"
);

socket.onopen = function () {

    console.log(
        "✅ Notification WebSocket Connected"
    );

};

socket.onmessage = function (event) {

    console.log(
        "🔥 Notification Received:",
        event.data
    );

    const data =
    JSON.parse(event.data);

    showNotification(
        data.message
    );

    updateNotificationCount(
        data.count
    );

    addNotificationToDropdown(
        data
    );

};

socket.onerror = function (error) {

    console.error(
        "WebSocket Error:",
        error
    );

};

socket.onclose = function () {

    console.log(
        "❌ Notification WebSocket Closed"
    );

};



// ===================================================
//              TOAST NOTIFICATION
// ===================================================

function showNotification(message){

    const container =
    document.getElementById(
        "notification-container"
    );

    if(!container) return;


    const toast =
    document.createElement("div");

    toast.className =
    "notification-toast";


    toast.innerHTML = `

        <div class="toast-header">

            <div class="toast-title">

                <i class="fa-solid fa-bell"></i>

                <span>

                    New Notification

                </span>

            </div>

            <div class="toast-time">

                Just now

            </div>

            <button class="toast-close">

                <i class="fa-solid fa-xmark"></i>

            </button>

        </div>


        <div class="toast-body">

            <div class="toast-message">

                ${message}

            </div>

        </div>


        <div class="toast-progress"></div>

    `;


    container.prepend(
        toast
    );


    const closeButton =
    toast.querySelector(
        ".toast-close"
    );

    closeButton.addEventListener(
        "click",
        function(){

            toast.remove();

        }
    );


    setTimeout(function(){

        toast.classList.add(
            "hide"
        );

        setTimeout(function(){

            toast.remove();

        },400);

    },7000);

}

// ===================================================
//          UPDATE NOTIFICATION COUNT
// ===================================================

function updateNotificationCount(count){

    if(count === undefined) return;


    const badge =
    document.querySelector(
        ".notification-count"
    );


    const total =
    document.querySelector(
        ".notification-total"
    );


    if(badge){

        badge.textContent = count;

    }


    if(total){

        total.textContent = count;

    }

}



// ===================================================
//      ADD NEW NOTIFICATION TO DROPDOWN
// ===================================================

function addNotificationToDropdown(data){

    const list =
    document.getElementById(
        "notificationList"
    );

    if(!list) return;


    const empty =
    list.querySelector(
        ".empty-notification"
    );

    if(empty){

        empty.remove();

    }


    const item =
    document.createElement(
        "div"
    );

    item.className =
    "notification-item";


    item.innerHTML = `

        <div class="notification-icon">

            <i class="fa-solid fa-bell"></i>

        </div>

        <div class="notification-content">

            <div class="notification-message">

                ${data.message}

            </div>

            <div class="notification-time">

                Just now

            </div>

        </div>

    `;


    list.prepend(item);

}

// ===================================================
//          DROPDOWN OPEN / CLOSE
// ===================================================

const bell =
document.getElementById(
    "notificationBell"
);

const dropdown =
document.getElementById(
    "notificationDropdown"
);


if(bell && dropdown){

    // ---------------------------
    // Open / Close Dropdown
    // ---------------------------

    bell.addEventListener(
        "click",
        function(e){

            e.stopPropagation();

            dropdown.classList.toggle(
                "show"
            );

        }
    );


    // ---------------------------
    // Close when clicking outside
    // ---------------------------

    document.addEventListener(
        "click",
        function(e){
            console.log("Document clicked");

            if(

                !bell.contains(e.target) &&
                !dropdown.contains(e.target)
                

            ){
                console.log("Outside click");

                if(

                    dropdown.classList.contains(
                        "show"
                    )

                ){

                    dropdown.classList.remove(
                        "show"
                    );


                    // -----------------------
                    // Mark Notifications Read
                    // -----------------------
                    console.log("Calling mark-read");
                    fetch(
                        "/notifications/mark-read/"
                    )
                    .then(
                        response => response.json()
                    )
                    .then(function(){

                        // Bell badge

                        const badge =
                        document.querySelector(
                            ".notification-count"
                        );

                        if(badge){

                            badge.textContent = "0";

                        }


                        // Header badge

                        const total =
                        document.querySelector(
                            ".notification-total"
                        );

                        if(total){

                            total.textContent = "0";

                        }


                        // Clear dropdown

                        const list =
                        document.getElementById(
                            "notificationList"
                        );

                        if(list){

                            list.innerHTML = `

                                <div class="empty-notification">

                                    <i class="fa-regular fa-bell-slash"></i>

                                    <p>

                                        No new notifications

                                    </p>

                                </div>

                            `;

                        }

                    });

                }

            }

        }
    );

}