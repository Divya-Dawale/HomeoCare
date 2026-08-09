document.addEventListener("DOMContentLoaded", function () {

    const chatButton = document.getElementById("homeocare-chat-button");
    const chatWindow = document.getElementById("homeocare-chat-window");
    const closeButton = document.getElementById("homeocare-chat-close");
    const messages = document.getElementById("homeocare-chat-messages");
    const input = document.getElementById("homeocare-chat-input");
    const sendButton = document.getElementById("homeocare-chat-send");

    /*
    =========================================================
    CHECK CHATBOT
    =========================================================
    */

    if (
        !chatButton ||
        !chatWindow ||
        !messages ||
        !input ||
        !sendButton
    ) {
        console.log("HomeoCare chatbot elements not found.");
        return;
    }

    console.log("HomeoCare Chatbot Loaded.");


    /*
    =========================================================
    PATIENT PAGE DETECTION
    =========================================================

    The patient dashboard contains this element:

        homeocare patient assistant

    Homepage contains:

        homeocare assistant

    We detect patient mode from the page.
    */

    const patientMode =
        document.querySelector(
            ".homeocare-chat-title h3"
        )?.textContent
        ?.toLowerCase()
        .includes("patient assistant");


    let patientAppointmentData = null;


    /*
    =========================================================
    LOAD PATIENT APPOINTMENT DATA
    =========================================================
    */

    async function loadPatientAppointmentData() {

        /*
        Do NOT call the patient API on homepage.
        */

        if (!patientMode) {
            return;
        }

        try {

            const response = await fetch(
                "/patient/chatbot/appointment/"
            );

            if (!response.ok) {

                throw new Error(
                    "Appointment request failed: " +
                    response.status
                );

            }

            patientAppointmentData =
                await response.json();

            console.log(
                "Patient appointment data loaded:",
                patientAppointmentData
            );

        } catch (error) {

            console.error(
                "Could not load patient appointment information:",
                error
            );

            patientAppointmentData = null;

        }

    }


    loadPatientAppointmentData();


    /*
    =========================================================
    OPEN CHAT
    =========================================================
    */

    chatButton.addEventListener(
        "click",
        function () {

            chatWindow.classList.toggle(
                "chatbot-open"
            );

            if (
                chatWindow.classList.contains(
                    "chatbot-open"
                )
            ) {

                input.focus();

            }

        }
    );


    /*
    =========================================================
    CLOSE CHAT
    =========================================================
    */

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            function () {

                chatWindow.classList.remove(
                    "chatbot-open"
                );

            }
        );

    }


    /*
    =========================================================
    ADD MESSAGE
    =========================================================
    */

    function addMessage(text, sender) {

        const message =
            document.createElement("div");

        message.classList.add(
            "homeocare-chat-message",
            sender
        );

        message.textContent = text;

        messages.appendChild(message);

        messages.scrollTop =
            messages.scrollHeight;

    }


    /*
    =========================================================
    TYPING INDICATOR
    =========================================================
    */

    function showTypingIndicator() {

        const typing =
            document.createElement("div");

        typing.id =
            "homeocare-typing-indicator";

        typing.classList.add(
            "homeocare-chat-message",
            "bot",
            "homeocare-typing"
        );

        typing.textContent =
            "HomeoCare Assistant is typing...";

        messages.appendChild(typing);

        messages.scrollTop =
            messages.scrollHeight;

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


    /*
    =========================================================
    BOT RESPONSE
    =========================================================
    */

    async function getBotResponse(message) {

        const text =
            message.toLowerCase().trim();


        /*
        =====================================================
        PATIENT-SPECIFIC APPOINTMENT QUESTIONS
        =====================================================

        These ONLY work in patient mode.
        Homepage remains completely general.
        */

        if (patientMode) {

            /*
            NEXT APPOINTMENT
            */

            if (
                text.includes("next appointment") ||
                text.includes("upcoming appointment") ||
                text.includes("my next appointment")
            ) {

                if (
                    !patientAppointmentData ||
                    !patientAppointmentData.upcoming
                ) {

                    return (
                        "You don't currently have " +
                        "an upcoming appointment. 😊"
                    );

                }

                const appointment =
                    patientAppointmentData.upcoming;

                return (
                    "📅 Your next appointment is on " +
                    appointment.date +
                    " at " +
                    appointment.time +
                    ".\n\n" +

                    "📋 Appointment No: " +
                    (
                        appointment.appointment_no ||
                        "Not assigned"
                    ) +
                    "\n" +

                    "🩺 Reason: " +
                    appointment.reason +
                    "\n" +

                    "📌 Status: " +
                    appointment.status
                );

            }


            /*
            APPOINTMENT STATUS
            */

            if (
                text.includes("appointment status") ||
                text.includes("status of my appointment") ||
                text.includes("check my appointment status") ||
                text.includes("check my status")
            ) {

                if (
                    !patientAppointmentData ||
                    !patientAppointmentData.latest
                ) {

                    return (
                        "I couldn't find an appointment " +
                        "associated with your account."
                    );

                }

                const appointment =
                    patientAppointmentData.latest;

                return (
                    "📋 Your latest appointment status is " +
                    appointment.status +
                    ".\n\n" +

                    "📅 Date: " +
                    appointment.date +
                    "\n" +

                    "🕐 Time: " +
                    appointment.time
                );

            }


            /*
            SHOW MY APPOINTMENT
            */

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

                    return (
                        "I couldn't find an appointment " +
                        "associated with your account."
                    );

                }

                const appointment =
                    patientAppointmentData.latest;

                return (
                    "📋 Appointment No: " +
                    (
                        appointment.appointment_no ||
                        "Not assigned"
                    ) +
                    "\n" +

                    "📅 Date: " +
                    appointment.date +
                    "\n" +

                    "🕐 Time: " +
                    appointment.time +
                    "\n" +

                    "🩺 Reason: " +
                    appointment.reason +
                    "\n" +

                    "📌 Status: " +
                    appointment.status
                );

            }

        }


        /*
        =====================================================
        GENERAL GREETING
        =====================================================
        */

        if (
            text.includes("hello") ||
            text.includes("hi") ||
            text.includes("hey")
        ) {

            return (
                "Hello! 👋 Welcome to HomeoCare. " +
                "How can I help you today?"
            );

        }


        /*
        =====================================================
        BOOK APPOINTMENT
        =====================================================
        */

        if (
            text.includes("book appointment") ||
            text.includes("book an appointment") ||
            text.includes("how do i book") ||
            text.includes("how can i book") ||
            text.includes("appointment booking") ||
            text.includes("booking an appointment")
        ) {

            return (
                "📅 You can request an appointment " +
                "through the Book Appointment section " +
                "of the HomeoCare website. " +
                "Our receptionist reviews the request " +
                "and confirms the appointment."
            );

        }


        /*
        =====================================================
        NEW PATIENT
        =====================================================
        */

        if (
            text.includes("new patient") ||
            text.includes("i am a new patient") ||
            text.includes("i'm a new patient") ||
            text.includes("first visit") ||
            text.includes("first time")
        ) {

            return (
                "👋 Welcome to HomeoCare! " +
                "If you are a new patient, you can " +
                "request an appointment through the " +
                "Book Appointment section. " +
                "Please provide the requested details " +
                "so our receptionist can review your request."
            );

        }


        /*
        =====================================================
        PATIENT STATUS — PUBLIC WEBSITE
        =====================================================
        */

        if (
            text.includes("patient status") ||
            text.includes("check patient status") ||
            text.includes("my patient status")
        ) {

            return (
                "📋 You can check your patient or " +
                "appointment status from the Patient Status " +
                "section using your Patient ID and " +
                "registered phone number."
            );

        }


        /*
        =====================================================
        HOMEOPATHY
        =====================================================
        */

        if (
            text.includes("homeopathy") ||
            text.includes("homeopathic")
        ) {

            return (
                "Homeopathy is a complementary healthcare " +
                "system based on highly diluted substances. " +
                "For personal health concerns, please " +
                "consult your qualified healthcare professional."
            );

        }


        /*
        =====================================================
        SERVICES
        =====================================================
        */

        if (
            text.includes("service") ||
            text.includes("services") ||
            text.includes("what does homeocare provide")
        ) {

            return (
                "HomeoCare provides homeopathy-focused " +
                "consultations, personalized treatment, " +
                "follow-up care, prescriptions, digital " +
                "medical records and appointment management."
            );

        }


        /*
        =====================================================
        MEDICAL RECORDS
        =====================================================
        */

        if (
            text.includes("medical record") ||
            text.includes("medical records") ||
            text.includes("records")
        ) {

            return (
                "You can view your medical records " +
                "from the Medical Records section " +
                "of your patient panel."
            );

        }


        /*
        =====================================================
        PRESCRIPTION
        =====================================================
        */

        if (
            text.includes("prescription") ||
            text.includes("medicine") ||
            text.includes("medicines")
        ) {

            return (
                "You can view your prescriptions " +
                "and prescribed medicines from the " +
                "Prescriptions section of your patient panel."
            );

        }


        /*
        =====================================================
        BILLS
        =====================================================
        */

        if (
            text.includes("bill") ||
            text.includes("bills") ||
            text.includes("billing") ||
            text.includes("payment") ||
            text.includes("fee")
        ) {

            return (
                "You can check your clinic bills " +
                "and payment information from the " +
                "Bills section of your patient panel."
            );

        }


        /*
        =====================================================
        MEDICAL HISTORY
        =====================================================
        */

        if (
            text.includes("medical history") ||
            text.includes("history")
        ) {

            return (
                "You can view your medical history " +
                "from the Medical History section " +
                "of your patient panel."
            );

        }


        /*
        =====================================================
        PROFILE
        =====================================================
        */

        if (
            text.includes("profile") ||
            text.includes("account")
        ) {

            return (
                "You can manage your personal information " +
                "from the Profile section of your patient panel."
            );

        }


        /*
        =====================================================
        CONTACT
        =====================================================
        */

        if (
            text.includes("contact") ||
            text.includes("phone") ||
            text.includes("email") ||
            text.includes("address") ||
            text.includes("contact clinic")
        ) {

            return (
                "📞 You can find the clinic's phone number, " +
                "email address and other contact information " +
                "in the Contact section of HomeoCare."
            );

        }


        /*
        =====================================================
        THANK YOU
        =====================================================
        */

        if (
            text.includes("thank") ||
            text.includes("thanks")
        ) {

            return "You're welcome! 😊";

        }


        /*
        =====================================================
        DEFAULT
        =====================================================
        */

        if (patientMode) {

            return (
                "I'm sorry, I didn't quite understand that. " +
                "You can ask me about your appointment, " +
                "medical records, prescriptions, bills, " +
                "medical history, profile or contacting the clinic."
            );

        }


        return (
            "I'm sorry, I didn't quite understand that. " +
            "You can ask me about appointments, services, " +
            "homeopathy, patient status, new patient registration " +
            "or contacting the clinic."
        );

    }


    /*
    =========================================================
    SEND MESSAGE
    =========================================================
    */

    async function sendMessage() {

        const text =
            input.value.trim();

        if (!text) {
            return;
        }


        addMessage(
            text,
            "user"
        );

        input.value = "";

        showTypingIndicator();


        setTimeout(
            async function () {

                removeTypingIndicator();

                const response =
                    await getBotResponse(text);

                addMessage(
                    response,
                    "bot"
                );

            },
            700
        );

    }


    /*
    =========================================================
    SEND BUTTON
    =========================================================
    */

    sendButton.addEventListener(
        "click",
        sendMessage
    );


    /*
    =========================================================
    ENTER KEY
    =========================================================
    */

    input.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();

            }

        }
    );


    /*
    =========================================================
    QUICK QUESTIONS
    =========================================================
    */

    document
        .querySelectorAll(
            ".homeocare-quick-question"
        )
        .forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const question =
                            this.dataset.question;

                        input.value =
                            question;

                        sendButton.click();

                    }
                );

            }
        );

});