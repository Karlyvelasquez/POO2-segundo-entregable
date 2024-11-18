document.addEventListener("DOMContentLoaded", () => {
    // Selecciona los enlaces de la barra lateral y las secciones del contenido principal
    const links = document.querySelectorAll(".sidebar a");
    const sections = document.querySelectorAll(".main-content > div");

    // Función para cambiar entre secciones
    links.forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();
            const targetId = link.getAttribute("href").substring(1);

            // Muestra la sección seleccionada y oculta las demás
            sections.forEach(section => {
                section.style.display = section.id === targetId ? "block" : "none";
            });

            // Marca el enlace activo en la barra lateral
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
        });
    });

    // Muestra la primera sección por defecto
    links[0].click();

    // Función para mostrar formularios de agregar o editar
    function toggleForm(formId, show) {
        const form = document.getElementById(formId);
        form.style.display = show ? "block" : "none";
    }

    // Ejemplo de funcionalidad CRUD: abrir/cerrar formularios y enviar datos
    const addProductButton = document.getElementById("addProductButton");
    const productForm = document.getElementById("productForm");

    if (addProductButton && productForm) {
        addProductButton.addEventListener("click", () => {
            toggleForm("productForm", true);
        });

        productForm.addEventListener("submit", event => {
            event.preventDefault();
            // Aquí puedes añadir la lógica para enviar datos al backend
            alert("Producto agregado exitosamente");
            toggleForm("productForm", false);
            productForm.reset();
        });
    }

    // Alertas de confirmación para operaciones de eliminación
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach(button => {
        button.addEventListener("click", event => {
            const confirmed = confirm("¿Estás seguro de que deseas eliminar este elemento?");
            if (!confirmed) event.preventDefault();
        });
    });
});
