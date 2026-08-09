document.addEventListener("DOMContentLoaded", function () {

    const chatButton = document.getElementById("homeocare-chat-button");
    const chatWindow = document.getElementById("homeocare-chat-window");
    const closeButton = document.getElementById("homeocare-chat-close");
    const messages = document.getElementById("homeocare-chat-messages");
    const input = document.getElementById("homeocare-chat-input");
    const sendButton = document.getElementById("homeocare-chat-send");
    let patientAppointmentData = null;

    if (!chatButton || !chatWindow || !messages || !input || !sendButton) {
        console.log("HomeoCare chatbot elements not found.");
        return;
    }
    loadPatientAppointmentData();
    console.log("HomeoCare chatbot loaded.");
  
    /* ==============================
       OPEN CHAT
    ============================== */

    chatButton.addEventListener("click", function () {

        chatWindow.classList.toggle("chatbot-open");

        if (chatWindow.classList.contains("chatbot-open")) {
            input.focus();
        }

    });


    /* ==============================
       CLOSE CHAT
    ============================== */

    if (closeButton) {

        closeButton.addEventListener("click", function () {

            chatWindow.classList.remove("chatbot-open");

        });

    }


    /* ==============================
       ADD MESSAGE
    ============================== */

    function addMessage(text, sender) {

        const message = document.createElement("div");

        message.classList.add(
            "homeocare-chat-message",
            sender
        );

        message.textContent = text;

        messages.appendChild(message);

        messages.scrollTop = messages.scrollHeight;

    }


    /* ==============================
       TYPING INDICATOR
    ============================== */

    function showTypingIndicator() {

        const typing = document.createElement("div");

        typing.id = "homeocare-typing-indicator";

        typing.classList.add(
            "homeocare-chat-message",
            "bot",
            "homeocare-typing"
        );

        typing.textContent =
            "HomeoCare Assistant is typing...";

        messages.appendChild(typing);

        messages.scrollTop = messages.scrollHeight;

    }


    function removeTypingIndicator() {

        const typing =
            document.getElementById(
                "homeocare-typing-indicator"
            );

        if (typing) {
            typing.remove();
        }

    }


    /* ==============================
       PATIENT CHATBOT RESPONSE
    ============================== */

    function getBotResponse(message) {

        const text = message.toLowerCase().trim();


        /* GREETING */

        if (
            text.includes("hello") ||
            text.includes("hi") ||
            text.includes("hey")
        ) {

            return "Hello! 👋 Welcome back to HomeoCare. How can I help you today?";

        }

        /* ==============================
   REAL APPOINTMENT INFORMATION
============================== */

if (
    text.includes("next appointment") ||
    text.includes("upcoming appointment") ||
    text.includes("my next appointment")
) {

    if (
        !patientAppointmentData ||
        !patientAppointmentData.upcoming
    ) {

        return "You don't currently have an upcoming appointment.";

    }

    const appointment =
        patientAppointmentData.upcoming;

    return `📅 Your next appointment is on ${appointment.date} at ${appointment.time}. Reason: ${appointment.reason}. Status: ${appointment.status}. Appointment No: ${appointment.appointment_no || "Not assigned"}.`;

}


if (
    text.includes("appointment status") ||
    text.includes("status of my appointment") ||
    text.includes("check my appointment status")
) {

    if (
        !patientAppointmentData ||
        !patientAppointmentData.latest
    ) {

        return "I couldn't find an appointment associated with your account.";

    }

    return `📋 Your latest appointment status is ${patientAppointmentData.latest.status}.`;

}


if (
    text.includes("check my appointment") ||
    text.includes("show my appointment") ||
    text.includes("view my appointment") ||
    text.includes("see my appointment")
) {

    if (
        !patientAppointmentData ||
        !patientAppointmentData.latest
    ) {

        return "I couldn't find an appointment associated with your account.";

    }

    const appointment =
        patientAppointmentData.latest;

    return `📅 Appointment No: ${appointment.appointment_no || "Not assigned"} | Date: ${appointment.date} | Time: ${appointment.time} | Reason: ${appointment.reason} | Status: ${appointment.status}.`;

}
        



        /* MEDICAL RECORDS */

        if (
            text.includes("medical record") ||
            text.includes("medical records") ||
            text.includes("records")
        ) {

            return "You can view your medical records from the Medical Records section of your patient panel.";

        }


        /* PRESCRIPTION */

        if (
            text.includes("prescription") ||
            text.includes("medicine") ||
            text.includes("medicines")
        ) {

            return "You can view your prescriptions and prescribed medicines from the Prescriptions section of your patient panel.";

        }


        /* BILLS */

        if (
            text.includes("bill") ||
            text.includes("bills") ||
            text.includes("billing") ||
            text.includes("payment") ||
            text.includes("fee")
        ) {

            return "You can check your clinic bills and payment information from the Bills section of your patient panel.";

        }


        /* HOMEOPATHY */

        if (
            text.includes("homeopathy") ||
            text.includes("homeopathic")
        ) {

            return "Homeopathy is a complementary healthcare system based on highly diluted substances. For personal health concerns, please consult your qualified healthcare professional.";

        }


        /* SERVICES */

        if (
            text.includes("service") ||
            text.includes("services")
        ) {

            return "HomeoCare provides homeopathy-focused consultations, prescriptions, medical records, appointment management and follow-up care.";

        }


        /* PROFILE */

        if (
            text.includes("profile") ||
            text.includes("account")
        ) {

            return "You can manage your personal information from the Profile section of your patient panel.";

        }


        /* CONTACT */

        if (
            text.includes("contact") ||
            text.includes("phone") ||
            text.includes("email") ||
            text.includes("address")
        ) {

            return "You can find the clinic's contact information in the Contact section of HomeoCare.";

        }


        /* THANK YOU */

        if (
            text.includes("thank") ||
            text.includes("thanks")
        ) {

            return "You're welcome! 😊";

        }


        /* DEFAULT */

        return "I'm sorry, I didn't quite understand that. You can ask me about your appointment, medical records, prescriptions, bills, homeopathy, services, profile or contacting the clinic.";

    }


    /* ==============================
       SEND MESSAGE
    ============================== */

    function sendMessage() {

        const text = input.value.trim();

        if (!text) {
            return;
        }

        addMessage(text, "user");

        input.value = "";

        showTypingIndicator();

        setTimeout(function () {

            removeTypingIndicator();

            const response =
                getBotResponse(text);

            addMessage(response, "bot");

        }, 700);

    }


    /* SEND BUTTON */

    sendButton.addEventListener(
        "click",
        sendMessage
    );


    /* ENTER KEY */

    input.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {
                sendMessage();
            }

        }
    );


    /* ==============================
       QUICK QUESTIONS
    ============================== */

    document
        .querySelectorAll(".homeocare-quick-question")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const question =
                        this.dataset.question;

                    input.value = question;

                    sendButton.click();

                }
            );

        });

});
async function loadPatientAppointmentData() {

    try {

        const response = await fetch(
            "/patient/chatbot/appointment/"
        );

        if (!response.ok) {
            return;
        }

        patientAppointmentData = await response.json();

    } catch (error) {

        console.error(
            "Could not load appointment information:",
            error
        );

    }
}