  const modal = document.getElementById("deleteModal");
  const openBtn = document.getElementById("openDeleteModal");
  const closeBtn = document.getElementById("closeDeleteModal");

  openBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  });

  closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  })