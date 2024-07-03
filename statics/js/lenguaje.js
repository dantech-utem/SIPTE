
$(document).ready(function() {
  /*Script para inicializar DataTables en la tabla con ID 'informeTable'*/
    $('#informeTable').DataTable({
      "language": {
          "url": "/statics/js/Spanish.json",
      }
    });

     /*Script para inicializar DataTables en la tabla con ID 'avisoAlum'*/
    $('#avisoAlum').DataTable({
      "language": {
        "url": "/statics/js/Spanish.json"
      }
    });

    /*Script para inicializar DataTables en la tabla con ID 'avisosTable'*/
    $('#avisosTable').DataTable({
      "language": {
        "url": "/statics/js/Spanish.json"
      }
    });

});