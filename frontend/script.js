document.getElementById("submit").addEventListener("click", function () {
  const review = document.getElementById("review").value;

  fetch("http://127.0.0.1:5000/review", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ review: review }),
  })
    .then((response) => response.json())
    .then((data) => {
      const rating = data.rating;
      displayRating(rating);
    })
    .catch((error) => console.error("Error:", error));
});

function displayRating(rating) {
  const starsContainer = document.getElementById("stars");
  const emotionContainer = document.getElementById("emotion");

  starsContainer.innerHTML = "";
  for (let i = 0; i < rating; i++) {
    starsContainer.innerHTML += "⭐";
  }

  rating *= 1;
  let emotion = "";
  switch (rating) {
    case 1:
      emotion = "😞";
      break;
    case 2:
      emotion = "😕";
      break;
    case 3:
      emotion = "😐";
      break;
    case 4:
      emotion = "🙂";
      break;
    case 5:
      emotion = "😃";
      break;
    default:
      emotion = "";
  }

  emotionContainer.innerHTML = emotion;
}
