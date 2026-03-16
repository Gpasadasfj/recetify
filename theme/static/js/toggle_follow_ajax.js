const followButtons = document.querySelectorAll(".follow-btn");

followButtons.forEach((btn) => {
  btn.addEventListener("click", async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const csrfToken = document
      .querySelector('meta[name="csrf-token"]')
      .getAttribute("content");

    try {
      const response = await fetch(btn.dataset.url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      if (response.status === 403) {
        // Usuario no logueado → redirigir a login
        window.location.href = "/login/?next=" + window.location.pathname;
        return;
      }

      if (!response.ok) throw new Error("Error en la petición");

      const data = await response.json();

      // Cambia texto del botón
      btn.textContent = btn.textContent.trim() === "Seguir" ? "Siguiendo" : "Seguir";

      // Actualiza contador de seguidores
      const followersCount = document.getElementById("followers-count");
      if (followersCount) {
        followersCount.textContent = data.followers;
      }
    } catch (err) {
      console.error("Error toggle follow:", err);
    }
  });
});
