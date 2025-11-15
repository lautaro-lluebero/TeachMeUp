document.addEventListener("DOMContentLoaded", () => {
  const btnAbrir = document.getElementById("abrirFiltro");
  const panel = document.getElementById("panelFiltro");

  if (!btnAbrir || !panel) return;

  btnAbrir.addEventListener("click", (e) => {
    e.stopPropagation();
    panel.classList.toggle("open");
  });

  document.addEventListener("click", () => {
    panel.classList.remove("open");
  });

  panel.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  // Acordeón para cada sección
  document.querySelectorAll(".filtro-titulo").forEach((btn) => {
    btn.addEventListener("click", () => {
      const contenido = btn.nextElementSibling;
      contenido.classList.toggle("open");
    });
  });

  // 🔹 OPCIONAL: si una sección tiene algo tildado, la abrimos al cargar
  document.querySelectorAll(".filtro-section").forEach((section) => {
    const contenido = section.querySelector(".filtro-contenido");
    const inputs = contenido ? contenido.querySelectorAll("input") : [];

    const algunoMarcado = Array.from(inputs).some((input) => input.checked);

    if (algunoMarcado && contenido) {
      contenido.classList.add("open");
    }
  });
});
