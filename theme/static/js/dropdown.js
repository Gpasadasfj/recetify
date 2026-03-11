function setupDropdown(dropdownId, optionsId, selectedId, inputId) {
  const dropdown = document.querySelector(dropdownId);
  const options = document.querySelector(optionsId);
  const selected = document.querySelector(selectedId);
  const hiddenInput = document.querySelector(inputId);

  // Mostrar/ocultar opciones al hacer click
  dropdown.addEventListener("click", () => {
    options.classList.toggle("hidden");
  });

  // Seleccionar opción
  options.querySelectorAll("li").forEach((option) => {
    option.addEventListener("click", (e) => {
      selected.textContent = option.textContent;
      hiddenInput.value = option.dataset.value;
      options.classList.add("hidden");
      e.stopPropagation()
    });
  });

  // Cerrar si haces click fuera
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target) && !options.contains(e.target)) {
      options.classList.add("hidden");
    }
  });
}

setupDropdown(
  "#hours-dropdown",
  "#hours-options",
  "#hours-selected",
  "#hours-input",
);
setupDropdown(
  "#minutes-dropdown",
  "#minutes-options",
  "#minutes-selected",
  "#minutes-input",
);
setupDropdown(
  "#difficulty-select",
  "#difficulty-options",
  "#difficulty-selected",
  "#difficulty-input"
)
