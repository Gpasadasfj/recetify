const halfStars = document.querySelectorAll(".half-star");
const preview = document.getElementById("rating-preview");
const input = document.getElementById("rating-input");
const stars = document.querySelectorAll(".star");

let currentRating = null;

halfStars.forEach((half) => {
  half.addEventListener("mouseenter", () => {
    const star = parseInt(half.dataset.star);
    const value = half.dataset.half === "left" ? star - 0.5 : star;

    preview.textContent = formatRatingForDisplay(value);
    updateStars(value);
  });

  half.addEventListener("click", () => {
    const star = parseInt(half.dataset.star);
    currentRating = half.dataset.half === "left" ? star - 0.5 : star;

    input.value = currentRating.toFixed(1); // <-- siempre string con decimal
    preview.textContent = formatRatingForDisplay(currentRating); // <-- solo mostrar
    updateStars(currentRating);
  });
});

document.getElementById("rating-stars").addEventListener("mouseleave", () => {
  if (currentRating !== null) {
    preview.textContent = formatRatingForDisplay(currentRating);
    updateStars(currentRating);
  } else {
    preview.textContent = "—";
    stars.forEach((s) => s.classList.remove("active"));
  }
});

function updateStars(value) {
  stars.forEach((star, index) => {
    star.classList.remove("full", "half");

    const starValue = index + 1;

    if (value >= starValue) {
      star.classList.add("full");
    } else if (value >= starValue - 0.5) {
      star.classList.add("half");
    }
  });
}

// Solo para mostrar
function formatRatingForDisplay(value) {
  return value % 1 === 0 ? value : value.toFixed(1);
}
