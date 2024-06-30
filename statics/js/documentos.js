$('#actividadTutorial').DataTable({
    responsive: true,
    language: {
      "decimal": "",
      "emptyTable": "No hay información",
      "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
      "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
      "infoFiltered": "(Filtrado de _MAX_ total entradas)",
      "infoPostFix": "",
      "thousands": ",",
      "lengthMenu": "Mostrar _MENU_ Entradas",
      "loadingRecords": "Cargando...",
      "processing": "Procesando...",
      "search": "Buscar: ",
      "zeroRecords": "Sin resultados encontrados",
      "paginate": {
          "first": "Primero",
          "last": "Ultimo",
          "next": "Siguiente",
          "previous": "Anterior"
      }
  },
  
});



function confirmarEliminacion() {
    if (confirm("¿Desea borrar la actividad?")) {
      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }

  function confirmarAgregar() {
    if (confirm("¿Desea guardar el registro?")) {

      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }

  function confirmarEditar() {
    if (confirm("¿Desea guardar los cambios?")) {

      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }


   // Cierra los mensajes automáticamente después de 5 segundos
   document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
      setTimeout(function() {
        alert.classList.add('fade-out');
        setTimeout(function() {
          alert.remove();
        }, 500); // espera 0.5 segundos después de desvanecerse para eliminarlo del DOM
      }, 5000); // 5 segundos antes de desvanecerse
    });
  });