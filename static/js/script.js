document.addEventListener('DOMContentLoaded', function() {

    const grid = document.getElementById("drawingGrid"); //get grid
    const resetButton = document.getElementById("resetButton"); //get button
    const runButton = document.getElementById("runButton");



    let isDrawing = false; //flag variable
    

    for (let i = 0; i < 28; i++) {
        for (let j = 0; j < 28; j++) {
            //create div
            const cell = document.createElement("div");
            //style div as cell
            cell.className = "cell";

            //listener
            cell.addEventListener("mousedown", () => cell.classList.add("active")); //mousedown on the cell
            cell.addEventListener("mouseenter", () => {
                if (isDrawing) cell.classList.add("active"); // mouseenter on the cell
            });

            //add to grid
            grid.appendChild(cell);

        }
    };

    //flag mousedown as drawing mode aka isDrawing = true
    document.addEventListener("mousedown", e => {
        if (e.target.classList.contains("cell")) { // prevent text selection ONLY FOR CELL
            e.preventDefault();
            isDrawing = true;
        };
    });

    //mouseup isDrawing = false
    document.addEventListener ("mouseup", () => {
    isDrawing = false;
    });

    resetButton.addEventListener("click", () => {   
        document.querySelectorAll(".cell.active").forEach(cell => {
                cell.classList.remove("active");
        });
    });


    runButton.addEventListener("click", () => {
        
        const gridData = []; //copy of the part above.. just saving the grid..

        for (let i = 0; i < 28; i++) {
            for (let j = 0; j < 28; j++) {
                const index = i * 28 + j;
                const cell = grid.children[index];
                gridData.push(cell.classList.contains("active") ? 1 : 0); //? means => if true 1 else 0
            }
        }
        console.log(gridData.slice(0,10));
        console.log(gridData.length);

        //send to server
        fetch("/run_model", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ grid_data: gridData})
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
            updateChart(data.prediction);           
        })
        .catch(error => {
            console.error("Error:", error);
        });


    })

    
    //plot
    const ctx = document.getElementById('myChart').getContext('2d');
       const chart = new Chart(ctx, {
           type: 'bar',
           data: {
               labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
               datasets: [{
                    label : "Prediction Distribuition",
                   data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   backgroundColor: 'rgba(54, 162, 235, 0.6)'
               }]
           },
            options: {
                    responsive: false,
                    plugins: { legend: { display: false }, tooltip: {enabled : false} },
                    scales: {
                        x: {grid: {display: false}},
                        y: { beginAtZero: true, max: 1 ,grid : {display: false}}
                    }
                }
       });

       function updateChart(probabilities) {
           chart.data.datasets[0].data = probabilities;
           chart.update();
       };

});
