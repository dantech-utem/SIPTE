document.addEventListener('DOMContentLoaded', function() {
    const tabs = Array.from(document.querySelectorAll('#myTab button'));
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const submitBtn = document.getElementById('submitBtn'); 

    function updateButtons() {
        const activeTab = document.querySelector('#myTab .active');
        const activeIndex = tabs.indexOf(activeTab);

        prevButton.style.display = activeIndex === 0 ? 'none' : 'inline-block';
        nextButton.style.display = activeIndex === tabs.length - 1 ? 'none' : 'inline-block';

        // Deshabilitar el botón "Anterior" en la primera sección
        prevButton.disabled = activeIndex === 0;

        // Mostrar el botón de enviar solo en la última pestaña
        if (activeIndex === tabs.length - 1) {
            submitBtn.style.display = 'inline-block';
        } else {
            submitBtn.style.display = 'none';
        }
    }

    prevButton.addEventListener('click', function() {
        const activeTab = document.querySelector('#myTab .active');
        const activeIndex = tabs.indexOf(activeTab);
        if (activeIndex > 0) {
            tabs[activeIndex - 1].click();
        }
    });

    nextButton.addEventListener('click', function() {
        const activeTab = document.querySelector('#myTab .active');
        const activeIndex = tabs.indexOf(activeTab);
        if (activeIndex < tabs.length - 1) {
            tabs[activeIndex + 1].click();
        }
    });

    tabs.forEach(tab => {
        tab.addEventListener('click', updateButtons);
    });

    updateButtons();
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('submitBtn').addEventListener('click', function(event) {
        // Validar si todos los campos requeridos están llenos
        var form = document.getElementById('formDatos');
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            $('#warningModal').modal('show'); // Mostrar el modal de advertencia
        }
        form.classList.add('was-validated');
    }, false);
});