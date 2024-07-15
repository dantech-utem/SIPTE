(function(){
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    let deleteUrl;

    btnEliminacion.forEach(btn =>{
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            deleteUrl = btn.getAttribute('href');
            $('#confirmModal').modal('show');
        });
    });

    document.getElementById('confirmDelete').addEventListener('click', () => {
        window.location.href = deleteUrl;
    });
})();
