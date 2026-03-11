document.addEventListener("DOMContentLoaded", () => {
  const recipesBtn = document.getElementById("recipes-btn");
  const savedBtn = document.getElementById("saved-btn");
  const recipes = document.getElementById("recipes");
  const savedRecipes = document.getElementById("saved_recipes");
  const slider = document.getElementById("slider");
  const myRecipesMessage = document.querySelector(".my-recipes-default-message")
  const savedRecipesMessage = document.querySelector(".saved-recipes-default-message")

  savedBtn.addEventListener("click", () => {
    if (savedBtn.classList.contains("active-slider")) return;

    savedBtn.classList.add("active-slider");
    recipesBtn.classList.remove("active-slider");

    if (recipes) {
      recipes.classList.add("hidden");
      recipes.classList.remove("grid");
    }

    if (myRecipesMessage) {
      myRecipesMessage.classList.remove("flex")
      myRecipesMessage.classList.add("hidden")
    }

    if (savedRecipesMessage) {
      savedRecipesMessage.classList.add("flex")
      savedRecipesMessage.classList.remove("hidden")
    }

    if (savedRecipes) {
      savedRecipes.classList.add("grid")
      savedRecipes.classList.remove("hidden")
    }

    slider.style.left = "50%";
  });

  recipesBtn.addEventListener("click", () => {
    if (recipesBtn.classList.contains("active-slider")) return;

    recipesBtn.classList.add("active-slider");
    savedBtn.classList.remove("active-slider");

    if (recipes) {
      recipes.classList.remove("hidden");
      recipes.classList.add("grid");
    }

    if (myRecipesMessage) {
      myRecipesMessage.classList.add("flex")
      myRecipesMessage.classList.remove("hidden")
    }

    if (savedRecipesMessage) {
      savedRecipesMessage.classList.remove("flex")
      savedRecipesMessage.classList.add("hidden")
    }
    
    if (savedRecipes) {
      savedRecipes.classList.add("hidden");
      savedRecipes.classList.remove("grid");
    }

    slider.style.left = "0%";
  });
});
