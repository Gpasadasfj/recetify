function removeImage() {
  const input = document.getElementById("id_image");
  const preview = document.getElementById("image-preview");
  const label = document.getElementById("add-img");
  const actions = document.getElementById("image-actions");

  input.value = "";
  preview.src = "";
  preview.classList.add("hidden");

  label.classList.remove("hidden");
  actions.classList.add("hidden");
}