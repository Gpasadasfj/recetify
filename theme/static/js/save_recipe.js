document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".saveButton");
  const filled = document.getElementById("filled_save");
  const empty = document.getElementById("empty_save");

  if (!btn) return;

  btn.addEventListener("click", (e) => {
    fetch(btn.dataset.url)
      .then((res) => res.json())
      .then((data) => {
        if (data.saved) {
          filled.classList.remove("hidden");
          empty.classList.add("hidden");
        } else {
          filled.classList.add("hidden");
          empty.classList.remove("hidden");
        }
      });
  });
});
