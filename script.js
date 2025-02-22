let mediaRecorder;
let audioChunks = [];
let recordButton = document.getElementById("recordButton");
let audioPlayback = document.getElementById("audioPlayback");
let audioElement = audioPlayback.querySelector("audio");
let timerDisplay = document.getElementById("timer");
let startTime;
let timerInterval;

// Function to format time as MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Function to update the timer display
function updateTimer() {
    const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
    timerDisplay.textContent = formatTime(elapsedTime);
}

// Function to start recording
async function startRecording() {
    audioChunks = []; // Clear previous recording
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioElement.src = audioUrl;
        audioPlayback.style.display = "block"; // Show playback controls
    };

    mediaRecorder.start();
    recordButton.textContent = "Stop Recording";
    recordButton.onclick = stopRecording;

    // Start the timer
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);

    // Automatically stop recording after 30 seconds
    setTimeout(() => {
        if (mediaRecorder.state === "recording") {
            stopRecording();
        }
    }, 30000); // 30 seconds
}

// Function to stop recording
function stopRecording() {
    mediaRecorder.stop();
    recordButton.textContent = "Start Recording";
    recordButton.onclick = startRecording;

    // Stop the timer
    clearInterval(timerInterval);
    timerDisplay.textContent = "00:00";
}

// Initialize button click event
recordButton.onclick = startRecording;