export function barplot(ctx, x, y) {
    let c = new Chart(ctx, {
        responsive: true,
        type: "bar",
        data: {
            labels: x,
            datasets: [
                {
                    label: "",
                    data: y,
                    backgroundColor: "teal"
                }
            ]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                xAxes: [
                    {
                        gridLines: {
                            display: true,
                            drawTicks: false
                        },
                        ticks: {
                            beginAtZero: false,
                            padding: 5
                        }
                    }
                ],
                yAxes: [
                    {
                        gridLines: {
                            display: true,
                            drawTicks: false
                        },
                        ticks: {
                            beginAtZero: true,
                            padding: 5,
                            callback: value => {
                                if (value % 1 == 0) {
                                    return value;
                                }
                            }
                        }
                    },
                    {
                        position: "right",
                        gridLines: {
                            display: false,
                            drawTicks: false
                        },
                        ticks: {
                            display: false
                        }
                    }
                ]
            }
        }
    });

    c.render();

    return c;
}
