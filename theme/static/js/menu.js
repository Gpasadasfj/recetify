document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("hamburger");
  const menu = document.getElementById("mobile-menu");

  // Abrir / cerrar al pulsar el botón
  menuBtn.addEventListener("click", (e) => {
    e.stopPropagation(); // evita que el click cierre inmediatamente
    menu.classList.remove("pointer-events-none");
    menu.classList.remove("opacity-0");
    menu.classList.add("opacity-100");
    menu.classList.remove("translate-x-full"); // fuera de pantalla
    menu.classList.add("translate-x-0"); // visible en su sitio
  });

  // Cerrar al hacer click fuera del menú
  document.addEventListener("click", (e) => {
    const clickInsideMenu = menu.contains(e.target);

    if (!clickInsideMenu) {
      menu.classList.add("pointer-events-none");
      menu.classList.remove("opacity-100"); // cerrar el menú
      menu.classList.add("opacity-0");
      menu.classList.add("translate-x-full"); // fuera de pantalla
      menu.classList.remove("translate-x-0"); // visible en su sitio
    }
  });
});
