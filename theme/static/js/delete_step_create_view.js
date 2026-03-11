document.addEventListener("click", function (e) {
  if (!e.target.classList.contains("delete-step")) return;

  const item = e.target.closest(".step-item");

  // no eliminar si es el único paso
  const container = document.getElementById("steps-container");
  // contar solo los pasos visibles
  const visibleSteps = container.querySelectorAll(".step-item:not(.hidden)");
  if (visibleSteps.length <= 1) {
    alert("La receta debe tener al menos un paso.");
    return;
  }

  // si el paso ya tiene ID -> marcar DELETE
  const idInput = item.querySelector('input[name$="-id"]');
  if (idInput && idInput.value) {
    let deleteInput = item.querySelector('input[name$="-DELETE"]');
    if (!deleteInput) {
      deleteInput = document.createElement("input");
      deleteInput.type = "hidden";
      deleteInput.name = idInput.name.replace("-id", "-DELETE");
      deleteInput.value = "on";
      item.appendChild(deleteInput);
    } else {
      deleteInput.value = "on";
    }

    // ocultar visualmente
    item.classList.add("hidden");
  } else {
    // paso nuevo -> eliminar del DOM
    item.remove();
  }

  // actualizar labels solo visualmente
  reorder();
});

function reorder() {
  const container = document.getElementById("steps-container");
  const visibleSteps = container.querySelectorAll(".step-item:not(.hidden)");

  visibleSteps.forEach((step, index) => {
    const label = step.querySelector(".step-label");
    label.innerText = index + 1; // actualizar solo el número visual
  });
}
