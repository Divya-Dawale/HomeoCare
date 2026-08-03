const labels = JSON.parse(
    document.getElementById("revenue-labels").textContent
);

const values = JSON.parse(
    document.getElementById("revenue-values").textContent
);

const canvas = document.getElementById("revenueChart");

if (canvas) {

    const ctx = canvas.getContext("2d");

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

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(value) {

                            return "₹" + value;

                        }

                    }

                }

            }

        }

    });

}