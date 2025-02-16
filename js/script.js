
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("results").style.display = "none"; // Hide results section on page load
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("getRecommendation").addEventListener("click", function () {
        // Get user input values
        const soilType = document.getElementById("soil").value;
        const weather = document.getElementById("weather").value;
        const humidity = document.getElementById("market").value;
        const rainfall = document.getElementById("rainfall").value;

        // Check if inputs are empty
        if (!soilType || !weather || !humidity || !rainfall) {
            alert("⚠️ Please fill all the fields before submitting!");
            return;
        }

        // Data to send in POST request
        const requestData = {
            soil_type: soilType,
            weather: weather,
            humidity: humidity,
            rainfall:rainfall
        };

        // Call API using Fetch
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())  
        .then(data => {
            console.log("Response from server:", data);
            displayResults(data);
            document.getElementById("results").style.display = "block";
        })
        .catch(error => {
            console.error("Error:", error);
            alert("❌ Failed to fetch recommendations. Please try again!");
            document.getElementById("results").style.display = "none";
        });
    });
});

// Function to display results
function displayResults(data) {
    const cropList = document.getElementById("crop-list");
    cropList.innerHTML = "<h3>🌾 Recommended Crops:</h3>";

    if (data.prediction) {
        cropList.innerHTML += `
            <div class="crop-card">
                <span class="crop-name">${data.prediction}</span>
            </div>
        `;
    } else {
        cropList.innerHTML += "<p class='no-result'>🚫 No recommendations found.</p>";
    }
}


