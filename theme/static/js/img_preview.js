function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById("image-preview");
  const label = document.getElementById("add-img");
  const actions = document.getElementById("image-actions");
  const container = document.getElementById("img-container")

  if (input.files && input.files[0]) {
    preview.src = URL.createObjectURL(input.files[0]);
    preview.classList.remove("hidden");
    label.classList.add("hidden");
    actions.classList.remove("hidden");
    container.classList.remove("h-[50dvh]")
  }
}