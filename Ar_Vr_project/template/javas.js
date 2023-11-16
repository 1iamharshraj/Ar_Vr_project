var timer;
var seconds = 0;

function checkt() {
    var checkbox = document.getElementById("btn");
    var timerDisplay = document.getElementById("timer");

    if (checkbox.checked) {
        // Start the timer
        timer = setInterval(function () {
            seconds++;
            timerDisplay.innerText = seconds;

            if (seconds >= 5) {
                // Stop the timer after 10 seconds
                clearInterval(timer);
                checkbox.checked = false; // Uncheck the checkbox
            }
        }, 1000); // Update every 1 second
    } else {
        // Stop the timer if the checkbox is unchecked
        clearInterval(timer);
        seconds = 0; // Reset the timer value
        timerDisplay.innerText = seconds;
    }
}