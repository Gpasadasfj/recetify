document.addEventListener("click", function (e) {
  // Seleccionar unidad
  const option = e.target.closest(".ingredient-unit-options li");
  if (option) {
    const select = option.closest(".ingredient-unit-select");
    const selected = select.querySelector(".ingredient-unit-selected");

    // Cambiar aquí: usar el <select> real del formset
    const realSelect = select.querySelector('select[name$="-unit"]');

    selected.textContent = option.textContent.trim();
    if (realSelect) {
      realSelect.value = option.dataset.value; // <- Esto es clave
      realSelect.dispatchEvent(new Event("change")); // opcional, si necesitas disparar listeners
    }

    select.querySelector(".ingredient-unit-options").classList.add("hidden");
    e.stopPropagation();
    return;
  }

  // Abrir / cerrar dropdown
  const select = e.target.closest(".ingredient-unit-select");
  if (select) {
    e.stopPropagation();

    const options = select.querySelector(".ingredient-unit-options");

    document.querySelectorAll(".ingredient-unit-options").forEach((ul) => {
      if (ul !== options) ul.classList.add("hidden");
    });

    options.classList.toggle("hidden");
    return;
  }

  // Click fuera → cerrar todos
  document
    .querySelectorAll(".ingredient-unit-options")
    .forEach((ul) => ul.classList.add("hidden"));
});
