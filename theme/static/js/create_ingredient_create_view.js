document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.querySelector(".add-ingredient");
  const container = document.querySelector(".ingredients-container");
  const totalForms = document.querySelector(
    'input[name="ingredient-TOTAL_FORMS"]',
  );

  addButton.addEventListener("click", () => {
    const ingredientCount = parseInt(totalForms.value);

    const template = document.querySelector(".ingredient-template");
    const newIngredient = template.content.cloneNode(true);

    newIngredient.querySelectorAll("[name]").forEach((input) => {
      input.name = input.name.replace("__prefix__", ingredientCount);
      input.id = input.id.replace("__prefix__", ingredientCount);

    });

    container.appendChild(newIngredient);
    totalForms.value = ingredientCount + 1;
  });
});
