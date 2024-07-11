function validateDates() {
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaFin = document.getElementById('fechaFin').value;
    const today = new Date().toISOString().split('T')[0];

    if (fechaInicio < today || fechaFin < today) {
        alert('Las fechas deben ser actuales o futuras.');
        return false;
    }

    if (fechaFin < fechaInicio) {
        alert('La fecha de fin no puede ser anterior a la fecha de inicio.');
        return false;
    }

    return true;
}

