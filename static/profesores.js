document.addEventListener("DOMContentLoaded", () => {

    console.log("profesores.js cargado correctamente"); // DEBUG

    const btnFiltro = document.getElementById("abrirFiltro");
    const panel = document.getElementById("panelFiltro");

    if (!btnFiltro) {
        console.error("NO SE ENCONTRÓ EL BOTÓN DE FILTRO");
        return;
    }
    if (!panel) {
        console.error("NO SE ENCONTRÓ EL PANEL DE FILTRO");
        return;
    }

    // ABRIR / CERRAR PANEL
    btnFiltro.addEventListener("click", () => {
        console.log("Click en el botón de filtro");
        panel.classList.toggle("activo");
    });

    // ACORDEONES
    const titulos = document.querySelectorAll(".filtro-titulo");

    titulos.forEach(titulo => {
        titulo.addEventListener("click", () => {
            const contenido = titulo.nextElementSibling;
            contenido.style.display =
                contenido.style.display === "flex" ? "none" : "flex";
        });
    });

});
