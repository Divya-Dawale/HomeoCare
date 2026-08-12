document.addEventListener("DOMContentLoaded", function () {

    /*
    =========================================================
    HOMEOCARE CHATBOT
    =========================================================
    */

    const chatButton =
        document.getElementById("homeocare-chat-button");

    const chatWindow =
        document.getElementById("homeocare-chat-window");

    const closeButton =
        document.getElementById("homeocare-chat-close");

    const messages =
        document.getElementById("homeocare-chat-messages");

    const input =
        document.getElementById("homeocare-chat-input");

    const sendButton =
        document.getElementById("homeocare-chat-send");


    /*
    =========================================================
    CHECK CHATBOT ELEMENTS
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
    */

    const chatTitle =
        document.querySelector(".homeocare-chat-title h3");

    const patientMode =
        chatTitle &&
        chatTitle.textContent
            .toLowerCase()
            .includes("patient assistant");


    console.log("Patient chatbot mode:", patientMode);


    /*
    =========================================================
    PATIENT DATA
    =========================================================
    */

    let patientAppointmentData = null;
    let patientPrescriptionData = null;
    let patientMedicalRecordData = null;
    let patientBillData = null;
    let patientHistoryData = null;


    /*
    =========================================================
    LOAD PATIENT APPOINTMENT DATA
    =========================================================
    */

    async function loadPatientAppointmentData() {

        if (!patientMode) {
            return;
        }

        try {

            const response =
                await fetch("/patient/chatbot/appointment/");

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


    /*
    =========================================================
    LOAD PATIENT BILL DATA
    =========================================================
    */

    async function loadPatientBillData() {

        if (!patientMode) {
            return;
        }

        try {

            const response =
                await fetch("/patient/chatbot/bills/");

            if (!response.ok) {
                throw new Error(
                    "Bill request failed: " +
                    response.status
                );
            }

            patientBillData =
                await response.json();

            console.log(
                "Patient bill data loaded:",
                patientBillData
            );

        } catch (error) {

            console.error(
                "Could not load patient bill information:",
                error
            );

            patientBillData = null;
        }
    }


    /*
    =========================================================
    LOAD PATIENT MEDICAL HISTORY
    =========================================================
    */

    async function loadPatientHistoryData() {

        if (!patientMode) {
            return;
        }

        try {

            const response =
                await fetch("/patient/chatbot/history/");

            if (!response.ok) {
                throw new Error(
                    "Medical history request failed: " +
                    response.status
                );
            }

            patientHistoryData =
                await response.json();

            console.log(
                "Patient medical history loaded:",
                patientHistoryData
            );

        } catch (error) {

            console.error(
                "Could not load patient medical history:",
                error
            );

            patientHistoryData = null;
        }
    }


    /*
    =========================================================
    LOAD PATIENT MEDICAL RECORD
    =========================================================
    */

    async function loadPatientMedicalRecordData() {

        if (!patientMode) {
            return;
        }

        try {

            const response =
                await fetch(
                    "/patient/chatbot/medical-records/"
                );

            if (!response.ok) {
                throw new Error(
                    "Medical record request failed: " +
                    response.status
                );
            }

            patientMedicalRecordData =
                await response.json();

            console.log(
                "Patient medical record data loaded:",
                patientMedicalRecordData
            );

        } catch (error) {

            console.error(
                "Could not load patient medical record information:",
                error
            );

            patientMedicalRecordData = null;
        }
    }


    /*
    =========================================================
    LOAD PATIENT PRESCRIPTION DATA
    =========================================================
    */

    async function loadPatientPrescriptionData() {

        if (!patientMode) {
            return;
        }

        try {

            const response =
                await fetch(
                    "/patient/chatbot/prescriptions/"
                );

            if (!response.ok) {
                throw new Error(
                    "Prescription request failed: " +
                    response.status
                );
            }

            patientPrescriptionData =
                await response.json();

            console.log(
                "Patient prescription data loaded:",
                patientPrescriptionData
            );

        } catch (error) {

            console.error(
                "Could not load patient prescription information:",
                error
            );

            patientPrescriptionData = null;
        }
    }


    /*
    =========================================================
    LOAD ALL PATIENT DATA
    =========================================================
    */

    loadPatientAppointmentData();
    loadPatientMedicalRecordData();
    loadPatientPrescriptionData();
    loadPatientBillData();
    loadPatientHistoryData();


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

        message.textContent =
            text;

        messages.appendChild(
            message
        );

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

        messages.appendChild(
            typing
        );

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
            message
                .toLowerCase()
                .trim();


        /*
        =====================================================
        PATIENT-ONLY INFORMATION
        =====================================================
        */

        if (patientMode) {


            /*
            =================================================
            APPOINTMENT — NEXT / UPCOMING
            =================================================
            */

            if (
                text.includes("next appointment") ||
                text.includes("upcoming appointment") ||
                text.includes("upcoming appointments") ||
                text.includes("when is my next appointment") ||
                text.includes("when is my upcoming appointment")
            ) {

                if (
                    !patientAppointmentData ||
                    !patientAppointmentData.upcoming
                ) {
                    return (
                        "You don't currently have an upcoming appointment. 😊"
                    );
                }

                const appointment =
                    patientAppointmentData.upcoming;

                return (
                    "📅 Your next appointment is on " +
                    (
                        appointment.date ||
                        "Date not recorded"
                    ) +
                    " at " +
                    (
                        appointment.time ||
                        "Time not recorded"
                    ) +
                    ".\n\n" +

                    "📋 Appointment No: " +
                    (
                        appointment.appointment_no ||
                        "Not assigned"
                    ) +
                    "\n" +

                    "🩺 Reason: " +
                    (
                        appointment.reason ||
                        "Not specified"
                    ) +
                    "\n" +

                    "📌 Status: " +
                    (
                        appointment.status ||
                        "Not available"
                    )
                );
            }


            /*
            =================================================
            APPOINTMENT — STATUS
            =================================================
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
                    (
                        appointment.status ||
                        "Not available"
                    ) +
                    ".\n\n" +

                    "📅 Date: " +
                    (
                        appointment.date ||
                        "Not recorded"
                    ) +
                    "\n" +

                    "🕐 Time: " +
                    (
                        appointment.time ||
                        "Not recorded"
                    )
                );
            }


            /*
            =================================================
            APPOINTMENT — SHOW
            =================================================
            */

            if (
                text.includes("show my appointment") ||
                text.includes("show my latest appointment") ||
                text.includes("view my appointment") ||
                text.includes("see my appointment") ||
                text.includes("latest appointment") ||
                text.includes("check my appointment")
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
                    "\n\n" +

                    "📅 Date: " +
                    (
                        appointment.date ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "🕐 Time: " +
                    (
                        appointment.time ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "🩺 Reason: " +
                    (
                        appointment.reason ||
                        "Not specified"
                    ) +
                    "\n\n" +

                    "📌 Status: " +
                    (
                        appointment.status ||
                        "Not available"
                    )
                );
            }


            /*
            =================================================
            APPOINTMENT — NUMBER
            =================================================
            */

            if (
                text.includes("appointment number") ||
                text.includes("appointment no") ||
                text.includes("appointment id")
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
                    "📋 Your appointment number is " +
                    (
                        appointment.appointment_no ||
                        "Not assigned"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            APPOINTMENT — LAST
            =================================================
            */

            if (
                text.includes("last appointment") ||
                text.includes("my last appointment")
            ) {

                if (
                    !patientAppointmentData ||
                    !patientAppointmentData.latest
                ) {
                    return (
                        "I couldn't find any previous appointment " +
                        "associated with your account."
                    );
                }

                const appointment =
                    patientAppointmentData.latest;

                return (
                    "📅 Your last appointment was on " +
                    (
                        appointment.date ||
                        "Date not recorded"
                    ) +
                    " at " +
                    (
                        appointment.time ||
                        "Time not recorded"
                    ) +
                    ".\n\n" +

                    "📋 Appointment No: " +
                    (
                        appointment.appointment_no ||
                        "Not assigned"
                    ) +
                    "\n" +

                    "🩺 Reason: " +
                    (
                        appointment.reason ||
                        "Not specified"
                    ) +
                    "\n" +

                    "📌 Status: " +
                    (
                        appointment.status ||
                        "Not available"
                    )
                );
            }


            /*
            =================================================
            BILL — TOTAL
            =================================================
            */

            if (
                text.includes("how much do i owe") ||
                text.includes("amount do i owe") ||
                text.includes("total bill") ||
                text.includes("total amount") ||
                text.includes("how much is my bill") ||
                text === "my bill" ||
                text === "bill"
            ) {

                if (
                    !patientBillData ||
                    !patientBillData.latest
                ) {
                    return (
                        "I couldn't find any bill " +
                        "associated with your account."
                    );
                }

                const bill =
                    patientBillData.latest;

                return (
                    "💰 Your total bill amount is: ₹" +
                    Number(
                        bill.total_amount || 0
                    ).toFixed(2) +
                    "."
                );
            }


            /*
            =================================================
            BILL — CONSULTATION FEE
            =================================================
            */

            if (
                text.includes("consultation fee") ||
                text.includes("consultation charge") ||
                text.includes("doctor fee") ||
                text.includes("doctor charge")
            ) {

                if (
                    !patientBillData ||
                    !patientBillData.latest
                ) {
                    return (
                        "I couldn't find any bill " +
                        "associated with your account."
                    );
                }

                const bill =
                    patientBillData.latest;

                return (
                    "🩺 Your consultation fee is: ₹" +
                    Number(
                        bill.consultation_fee || 0
                    ).toFixed(2) +
                    "."
                );
            }


            /*
            =================================================
            BILL — MEDICINE FEE
            =================================================
            */

            if (
                text.includes("medicine fee") ||
                text.includes("medicine charge") ||
                text.includes("medicine cost") ||
                text.includes("medicine fees") ||
                text.includes("medicien fee")
            ) {

                if (
                    !patientBillData ||
                    !patientBillData.latest
                ) {
                    return (
                        "I couldn't find any bill " +
                        "associated with your account."
                    );
                }

                const bill =
                    patientBillData.latest;

                return (
                    "💊 Your medicine fee is: ₹" +
                    Number(
                        bill.medicine_fee || 0
                    ).toFixed(2) +
                    "."
                );
            }


            /*
            =================================================
            BILL — COMPLETE
            =================================================
            */

            if (
                text.includes("show my bill") ||
                text.includes("show my bills") ||
                text.includes("view my bill") ||
                text.includes("view my bills") ||
                text.includes("what is my bill") ||
                text.includes("what's my bill") ||
                text.includes("how is my bill")
            ) {

                if (
                    !patientBillData ||
                    !patientBillData.latest
                ) {
                    return (
                        "I couldn't find any bill " +
                        "associated with your account."
                    );
                }

                const bill =
                    patientBillData.latest;

                return (
                    "💰 Your latest bill:\n\n" +

                    "📅 Date: " +
                    (
                        bill.date ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "💵 Total Amount: ₹" +
                    Number(
                        bill.total_amount || 0
                    ).toFixed(2) +
                    "\n\n" +

                    "🩺 Consultation Fee: ₹" +
                    Number(
                        bill.consultation_fee || 0
                    ).toFixed(2) +
                    "\n\n" +

                    "💊 Medicine Fee: ₹" +
                    Number(
                        bill.medicine_fee || 0
                    ).toFixed(2) +
                    "\n\n" +

                    "📌 Status: " +
                    (
                        bill.status ||
                        "Not recorded"
                    )
                );
            }


            /*
            =================================================
            MEDICAL HISTORY
            =================================================
            */

            if (
                text.includes("medical history") ||
                text.includes("my history") ||
                text.includes("how many visits") ||
                text.includes("how many appointments") ||
                text.includes("total visits") ||
                text.includes("completed visits") ||
                text.includes("last visit") ||
                text.includes("previous visit") ||
                text.includes("latest visit")
            ) {

                if (!patientHistoryData) {
                    return (
                        "I couldn't load your medical history " +
                        "information right now."
                    );
                }


                /*
                =============================================
                TOTAL VISITS
                =============================================
                */

                if (
                    text.includes("how many visits") ||
                    text.includes("how many appointments") ||
                    text.includes("total visits")
                ) {

                    return (
                        "📚 You have had " +
                        (
                            patientHistoryData.total_visits ||
                            0
                        ) +
                        " visit(s) at HomeoCare."
                    );
                }


                /*
                =============================================
                COMPLETED VISITS
                =============================================
                */

                if (
                    text.includes("completed visits")
                ) {

                    return (
                        "✅ You have completed " +
                        (
                            patientHistoryData.completed_visits ||
                            0
                        ) +
                        " visit(s)."
                    );
                }


                /*
                =============================================
                LAST VISIT
                =============================================
                */

                if (
                    text.includes("last visit") ||
                    text.includes("previous visit") ||
                    text.includes("latest visit")
                ) {

                    if (
                        !patientHistoryData.latest
                    ) {
                        return (
                            "I couldn't find any previous visit " +
                            "associated with your account."
                        );
                    }

                    const visit =
                        patientHistoryData.latest;

                    return (
                        "📅 Your last visit was on " +
                        (
                            visit.date ||
                            "Date not recorded"
                        ) +
                        (
                            visit.time
                                ? " at " + visit.time
                                : ""
                        ) +
                        ".\n\n" +

                        "📋 Appointment No: " +
                        (
                            visit.appointment_no ||
                            "Not assigned"
                        ) +
                        "\n" +

                        "🩺 Reason: " +
                        (
                            visit.reason ||
                            "Not specified"
                        ) +
                        "\n" +

                        "📌 Status: " +
                        (
                            visit.status ||
                            "Not available"
                        )
                    );
                }


                /*
                =============================================
                COMPLETE MEDICAL HISTORY
                =============================================
                */

                if (
                    text.includes("medical history") ||
                    text.includes("my history")
                ) {

                    return (
                        "📚 Your HomeoCare medical history:\n\n" +

                        "📋 Total Visits: " +
                        (
                            patientHistoryData.total_visits ||
                            0
                        ) +
                        "\n\n" +

                        "✅ Completed Visits: " +
                        (
                            patientHistoryData.completed_visits ||
                            0
                        )
                    );
                }
            }


            /*
            =================================================
            PRESCRIPTION — DOSAGE
            =================================================
            */

            if (
                text.includes("dosage") ||
                text.includes("dose")
            ) {

                if (
                    !patientPrescriptionData ||
                    !patientPrescriptionData.latest
                ) {
                    return (
                        "I couldn't find any prescription " +
                        "associated with your account."
                    );
                }

                const prescription =
                    patientPrescriptionData.latest;

                return (
                    "💊 Your prescribed dosage is: " +
                    (
                        prescription.dosage ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            PRESCRIPTION — FREQUENCY
            =================================================
            */

            if (
                text.includes("frequency") ||
                text.includes("how often should i take")
            ) {

                if (
                    !patientPrescriptionData ||
                    !patientPrescriptionData.latest
                ) {
                    return (
                        "I couldn't find any prescription " +
                        "associated with your account."
                    );
                }

                const prescription =
                    patientPrescriptionData.latest;

                return (
                    "🔄 Your prescribed medicine frequency is: " +
                    (
                        prescription.frequency ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            PRESCRIPTION — COMPLETE
            =================================================
            */

            if (
                text.includes("my prescription") ||
                text.includes("show my prescription") ||
                text.includes("show my prescriptions") ||
                text.includes("view my prescription") ||
                text.includes("my medicine") ||
                text.includes("my medicines") ||
                text.includes("what medicine") ||
                text.includes("what medicines") ||
                text.includes("medicine was prescribed") ||
                text.includes("medicines were prescribed") ||
                text.includes("which medicine") ||
                text.includes("which medicines")
            ) {

                if (
                    !patientPrescriptionData ||
                    !patientPrescriptionData.latest
                ) {
                    return (
                        "I couldn't find any prescription " +
                        "associated with your account."
                    );
                }

                const prescription =
                    patientPrescriptionData.latest;

                return (
                    "💊 Your latest prescription:\n\n" +

                    "📅 Date: " +
                    (
                        prescription.date ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "💊 Medicine: " +
                    (
                        prescription.medicine_name ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "💊 Dosage: " +
                    (
                        prescription.dosage ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "🔄 Frequency: " +
                    (
                        prescription.frequency ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "📅 Duration: " +
                    (
                        prescription.duration ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "📝 Instructions: " +
                    (
                        prescription.instructions ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "📌 Status: " +
                    (
                        prescription.status ||
                        "Not recorded"
                    )
                );
            }


            /*
            =================================================
            MEDICAL RECORD — DIAGNOSIS
            =================================================
            */

            if (
                text.includes("diagnosis") ||
                text.includes("diagnoses") ||
                text.includes("diagnossi")
            ) {

                if (
                    !patientMedicalRecordData ||
                    !patientMedicalRecordData.latest
                ) {
                    return (
                        "I couldn't find any medical record " +
                        "associated with your account."
                    );
                }

                const record =
                    patientMedicalRecordData.latest;

                return (
                    "🔎 Your latest diagnosis was: " +
                    (
                        record.diagnosis ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            MEDICAL RECORD — SYMPTOMS
            =================================================
            */

            if (
                text.includes("symptom") ||
                text.includes("symptoms")
            ) {

                if (
                    !patientMedicalRecordData ||
                    !patientMedicalRecordData.latest
                ) {
                    return (
                        "I couldn't find any medical record " +
                        "associated with your account."
                    );
                }

                const record =
                    patientMedicalRecordData.latest;

                return (
                    "🩺 Your latest recorded symptoms were: " +
                    (
                        record.symptoms ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            MEDICAL RECORD — OBSERVATIONS
            =================================================
            */

            if (
                text.includes("observation") ||
                text.includes("observations")
            ) {

                if (
                    !patientMedicalRecordData ||
                    !patientMedicalRecordData.latest
                ) {
                    return (
                        "I couldn't find any medical record " +
                        "associated with your account."
                    );
                }

                const record =
                    patientMedicalRecordData.latest;

                return (
                    "👨‍⚕️ Your latest observations were: " +
                    (
                        record.observations ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            MEDICAL RECORD — FOLLOW-UP
            =================================================
            */

            if (
                text.includes("follow up") ||
                text.includes("follow-up") ||
                text.includes("followup")
            ) {

                if (
                    !patientMedicalRecordData ||
                    !patientMedicalRecordData.latest
                ) {
                    return (
                        "I couldn't find any medical record " +
                        "associated with your account."
                    );
                }

                const record =
                    patientMedicalRecordData.latest;

                return (
                    "📌 Your latest follow-up instructions were: " +
                    (
                        record.follow_up ||
                        "Not recorded"
                    ) +
                    "."
                );
            }


            /*
            =================================================
            MEDICAL RECORD — COMPLETE
            =================================================
            */

            if (
                text.includes("medical record") ||
                text.includes("medical records") ||
                text.includes("show my record") ||
                text.includes("show my medical record") ||
                text.includes("view my medical record") ||
                text.includes("show my records") ||
                text.includes("view my records")
            ) {

                if (
                    !patientMedicalRecordData ||
                    !patientMedicalRecordData.latest
                ) {
                    return (
                        "I couldn't find any medical record " +
                        "associated with your account."
                    );
                }

                const record =
                    patientMedicalRecordData.latest;

                return (
                    "📄 Your latest medical record:\n\n" +

                    "📅 Date: " +
                    (
                        record.date ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "🩺 Symptoms: " +
                    (
                        record.symptoms ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "🔎 Diagnosis: " +
                    (
                        record.diagnosis ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "👨‍⚕️ Observations: " +
                    (
                        record.observations ||
                        "Not recorded"
                    ) +
                    "\n\n" +

                    "📌 Follow-up: " +
                    (
                        record.follow_up ||
                        "Not recorded"
                    )
                );
            }

        }


        /*
        =====================================================
        GENERAL GREETING
        =====================================================
        */

        if (
            text === "hello" ||
            text === "hi" ||
            text === "hey" ||
            text.startsWith("hello ") ||
            text.startsWith("hi ") ||
            text.startsWith("hey ")
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
                "📅 You can request an appointment through " +
                "the Book Appointment section of the HomeoCare " +
                "website. Our receptionist reviews the request " +
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
                "👋 Welcome to HomeoCare! If you are a new " +
                "patient, you can request an appointment through " +
                "the Book Appointment section. Please provide " +
                "the requested details so our receptionist can " +
                "review your request."
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
                "📋 You can check your patient or appointment " +
                "status from the Patient Status section using " +
                "your Patient ID and registered phone number."
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
                "For personal health concerns, please consult " +
                "your qualified healthcare professional."
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
                "consultations, personalized treatment, follow-up " +
                "care, prescriptions, digital medical records and " +
                "appointment management."
            );
        }


        /*
        =====================================================
        PRESCRIPTION — PUBLIC
        =====================================================
        */

        if (
            text.includes("prescription") ||
            text.includes("medicine") ||
            text.includes("medicines")
        ) {

            return (
                "You can view your prescriptions and prescribed " +
                "medicines from the Prescriptions section of your " +
                "patient panel."
            );
        }


        /*
        =====================================================
        BILLS — PUBLIC
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
                "You can check your clinic bills and payment " +
                "information from the Bills section of your " +
                "patient panel."
            );
        }


        /*
        =====================================================
        MEDICAL HISTORY — PUBLIC
        =====================================================
        */

        if (
            text.includes("medical history") ||
            text.includes("history")
        ) {

            return (
                "You can view your medical history from the " +
                "Medical History section of your patient panel."
            );
        }


        /*
        =====================================================
        PROFILE — PUBLIC
        =====================================================
        */

        if (
            text.includes("profile") ||
            text.includes("account")
        ) {

            return (
                "You can manage your personal information from " +
                "the Profile section of your patient panel."
            );
        }


        /*
        =====================================================
        CONTACT CLINIC
        =====================================================
        */

        if (
            text.includes("contact") ||
            text.includes("phone") ||
            text.includes("email") ||
            text.includes("address") ||
            text.includes("how can i contact") ||
            text.includes("how do i contact") ||
            text.includes("contact clinic")
        ) {

            return (
                "📞 You can contact HomeoCare Clinic using the " +
                "details below:\n\n" +

                "📱 Phone: +91 8600696292\n\n" +

                "📧 Email: homeocare@gmail.com\n\n" +

                "🏥 You can also visit the Contact Clinic " +
                "section of the HomeoCare website for more information."
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
        PATIENT DEFAULT
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


        /*
        =====================================================
        HOMEPAGE DEFAULT
        =====================================================
        */

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

                try {

                    const response =
                        await getBotResponse(text);

                    addMessage(
                        response,
                        "bot"
                    );

                } catch (error) {

                    console.error(
                        "Chatbot response error:",
                        error
                    );

                    addMessage(
                        "Sorry, something went wrong. Please try again.",
                        "bot"
                    );
                }

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

                        if (!question) {
                            return;
                        }

                        input.value =
                            question;

                        sendButton.click();
                    }
                );
            }
        );


    console.log(
        "HomeoCare chatbot fully initialized."
    );

});


