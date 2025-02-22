let mediaRecorder;
        let audioChunks = [];
        let recordTimeout;

        document.getElementById("startBtn").addEventListener("click", async function () {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = async () => {
                    if (audioChunks.length === 0) {
                        console.error("No audio recorded.");
                        return;
                    }

                    const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    document.getElementById("audioPlayer").src = audioUrl;

                    // Optional: Upload to server
                    const formData = new FormData();
                    formData.append("audio", audioBlob, "recording.webm");

                    fetch("/upload", {
                        method: "POST",
                        body: formData,
                    })
                    .then((response) => response.text())
                    .then((data) => console.log("Upload success:", data))
                    .catch((error) => console.error("Error uploading:", error));
                };

                mediaRecorder.start();
                document.getElementById("startBtn").disabled = true;
                document.getElementById("stopBtn").disabled = false;

                // Automatically stop recording after 30 seconds
                recordTimeout = setTimeout(() => stopRecording(), 30000);
            } catch (error) {
                console.error("Error accessing microphone:", error);
                alert("Microphone access denied or unavailable.");
            }
        });

        document.getElementById("stopBtn").addEventListener("click", function () {
            stopRecording();
        });

        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state === "recording") {
                mediaRecorder.stop();
                clearTimeout(recordTimeout);
                document.getElementById("startBtn").disabled = false;
                document.getElementById("stopBtn").disabled = true;
            }
        }