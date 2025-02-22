document
  .getElementById("surveyForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevents default form submission

    let formData = new FormData(this);

    fetch("/submit", {
      method: "POST",
      body: new URLSearchParams(new FormData(this)),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => response.json())
      .then((data) => alert("Response received: " + JSON.stringify(data)))
      .catch((error) => console.error("Error:", error));
  });
