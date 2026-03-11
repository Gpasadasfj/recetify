document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".check-toggle").forEach(toggle => {
    toggle.addEventListener("click", () => {
      toggle.querySelector(".empty-check").classList.toggle("hidden");
      toggle.querySelector(".checked").classList.toggle("hidden");
    });
  });
});
