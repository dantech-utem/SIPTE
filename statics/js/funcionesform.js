document.addEventListener('DOMContentLoaded', (event) => {
    const fechaInicioEditInput = document.getElementById('fechaInicioE');
    const fechaFinEditInput = document.getElementById('fechaFinE');

    // Obtener la fecha actual
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedToday = `${year}-${month}-${day}`

    // Obtener las fechas guardadas desde Django
    const savedFechaInicio = fechaInicioEditInput.value;
    const savedFechaFin = fechaFinEditInput.value;

    // Establecer la fecha mínima para fechaInicio basada en la fecha actual o la fecha guardada (la mayor)
    const minFechaInicio = (new Date(savedFechaInicio) > new Date(formattedToday)) ? savedFechaInicio : formattedToday;
    fechaInicioEditInput.setAttribute('min', minFechaInicio);

    // Establecer la fecha mínima para fechaFin como el día siguiente a la fecha guardada en fechaInicio
    const savedDateInicio = new Date(savedFechaInicio);
    savedDateInicio.setDate(savedDateInicio.getDate() + 1);
    const nextDay = savedDateInicio.toISOString().split('T')[0];
    fechaFinEditInput.setAttribute('min', nextDay);

    // Asegurar que fechaFin no sea anterior a fechaInicio y no sea el mismo día
    fechaInicioEditInput.addEventListener('change', function() {
      const selectedDate = new Date(this.value);
      selectedDate.setDate(selectedDate.getDate() + 1);
      const nextDay = selectedDate.toISOString().split('T')[0];
      fechaFinEditInput.setAttribute('min', nextDay);

      // Si la fecha seleccionada para inicio es igual a la fecha final, resetear la fecha final
      if (fechaInicioEditInput.value >= fechaFinEditInput.value) {
        fechaFinEditInput.value = '';
      }
    });

    fechaFinEditInput.addEventListener('change', function() {
      if (new Date(fechaFinEditInput.value) <= new Date(formattedToday)) {
        fechaFinEditInput.value = '';
      } else if (fechaInicioEditInput.value === fechaFinEditInput.value) {
        fechaFinEditInput.value = '';
      } else if (new Date(fechaFinEditInput.value) <= new Date(fechaInicioEditInput.value)) {
        fechaFinEditInput.value = '';
      }
    });
  });

  document.addEventListener('DOMContentLoaded', (event) => {
    const fechaInicioInput = document.getElementById('fechaInicio');
    const fechaFinInput = document.getElementById('fechaFin');
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); 
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;

    // Establecer la fecha mínima para ambos campos como la fecha actual
    fechaInicioInput.setAttribute('min', formattedDate);
    fechaFinInput.setAttribute('min', formattedDate);

    // Asegurar que fechaFin no sea anterior a fechaInicio y que no sea el mismo día
    fechaInicioInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        selectedDate.setDate(selectedDate.getDate() + 1);
        const nextDay = selectedDate.toISOString().split('T')[0];
        fechaFinInput.setAttribute('min', nextDay);
      });


     // Asegurar que fechaInicio no sea posterior a fechaFin
     fechaFinInput.addEventListener('change', function() {
        fechaInicioInput.setAttribute('max', this.value);
      });
  });

  window.onload = function(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
      dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
      mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaR').value=ano+"-"+mes+"-"+dia;
  }