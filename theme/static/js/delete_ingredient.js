document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".ingredients-container");
  const form = container.closest("form");

  function getTotalFormsInput() {
    return form.querySelector('input[name$="-TOTAL_FORMS"]');
  }

  function updateIndexes() {
    const items = container.querySelectorAll(".ingredient-item");
    const totalFormsInput = getTotalFormsInput();

    items.forEach((item, index) => {
      item.querySelectorAll("input, select").forEach((field) => {
        if (!field.name) return;
        field.name = field.name.replace(/-\d+-/, `-${index}-`);
        field.id = field.id.replace(/-\d+-/, `-${index}-`);
      });
    });

    if (totalFormsInput) {
      totalFormsInput.value = items.length;
    }
  }

  container.addEventListener("click", (e) => {
    const removeBtn = e.target.closest(".material-symbols-outlined");
    if (!removeBtn) return;

    const item = removeBtn.closest(".ingredient-item");
    const items = container.querySelectorAll(".ingredient-item");

    if (items.length <= 1) {
      alert("Debe haber al menos un ingrediente");
      return;
    }

    // 1️⃣ Buscar input id para ver si es ingrediente existente
    const idInput = item.querySelector('input[name$="-id"]');

    if (idInput && idInput.value) {
      // ingrediente existente -> marcar DELETE
      let deleteInput = item.querySelector('input[name$="-DELETE"]');
      if (!deleteInput) {
        deleteInput = document.createElement("input");
        deleteInput.type = "hidden";
        deleteInput.name = idInput.name.replace("-id", "-DELETE");
        deleteInput.value = "on"; // marcar para eliminar
        item.appendChild(deleteInput);
      } else {
        deleteInput.value = "on";
      }

      // ocultamos visualmente
      item.style.display = "none";

    } else {
      // ingrediente nuevo -> eliminar del DOM
      item.remove();
    }

    // actualizar índices y TOTAL_FORMS
    updateIndexes();
  });
});
