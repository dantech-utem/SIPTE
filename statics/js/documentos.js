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
      // Aquí va el código que ejecutará la acción de eliminación
      alert("Elemento eliminado exitosamente.");
      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }

  function confirmarAgregar() {
    if (confirm("¿Desea guardar el registro?")) {
      // Aquí va el código que ejecutará la acción de eliminación
      alert("Registro guardado");
      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }

  function confirmarEditar() {
    if (confirm("¿Desea guardar los cambios?")) {
      // Aquí va el código que ejecutará la acción de eliminación
      alert("Registro guardado");
      return true; // Permite que se complete la acción
    } else {
      return false; // Cancela la acción
    }
  }