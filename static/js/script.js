document.addEventListener('DOMContentLoaded', function() {

    const grid = document.getElementById("drawingGrid"); //get grid
    const resetButton = document.getElementById("resetButton"); //get button
    const exportButton = document.getElementById("exportButton");
    const recordButton = document.getElementById("recordButton");
    const labelInput = document.getElementById("labelInput");
    const statusDiv = document.getElementById("statusDiv");
    
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

    //save grid
    recordButton.addEventListener("click", () => {
        const label = labelInput.value.trim() || "unlabeled";

        const gridData = [];

        for (let i = 0; i < 28; i++) {
            for (let j = 0; j < 28; j++) {
                const index = i * 28 + j;
                const cell = grid.children[index];
                gridData.push(cell.classList.contains("active" ? 1 : 0)); //? means => if true 1 else 0
            }
        }

        //send to server
        fetch("/save_drawing", {
            method: "POST",
            headers: {"Content-Type" : "application/json" },
            body: JSON.stringify({ grid_data: gridData, label: label})
        })
        .then(response => {
            if (response.status === 201) {
                console.log("sucess");
            } else {
                console.log("something went wrong");
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
        })
    });


});
