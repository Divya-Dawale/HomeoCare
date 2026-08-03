const labels = JSON.parse(
    document.getElementById("revenue-labels").textContent
);

const values = JSON.parse(
    document.getElementById("revenue-values").textContent
);

const canvas = document.getElementById("revenueChart");

if (canvas) {

    const ctx = canvas.getContext("2d");
    const isDark = document.body.classList.contains("dark-theme");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Revenue",

                    data: values,

                    borderColor: "#22c55e",

                    backgroundColor: "rgba(34,197,94,0.15)",

                    fill: true,

                    tension: 0.4,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#16a34a",

                    borderWidth: 3

                }

            ]

        },

        const isDark = document.body.classList.contains("dark-theme");

options: {

    responsive: true,

    maintainAspectRatio: false,

    plugins: {

        legend: {
            display: false
        },

        tooltip: {
            titleColor: isDark ? "#F8FAFC" : "#1E293B",
            bodyColor: isDark ? "#F8FAFC" : "#1E293B",
            backgroundColor: isDark ? "#1E293B" : "#FFFFFF"
        }

    },

    scales: {

        x: {

            ticks: {
                color: isDark ? "#F8FAFC" : "#64748B"
            },

            grid: {
                color: isDark ? "#334155" : "#EEF3F2"
            }

        },

        y: {

            beginAtZero: true,

            ticks: {

                color: isDark ? "#F8FAFC" : "#64748B",

                callback: function(value) {
                    return "₹" + value;
                }

            },

            grid: {
                color: isDark ? "#334155" : "#EEF3F2"
            }

        }

    }

}

    });

}