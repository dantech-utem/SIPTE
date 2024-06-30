const singUpButton = document.getElementById('signUp');
const singInButton = document.getElementById('signIn');
const main = document.getElementById('main');
const returnButton = document.getElementById('boton-regreso');
singUpButton.addEventListener('click', () =>{

    var email = document.getElementById('email').value;
    // Ajax para validar el email
    $.ajax({
        type: 'POST',
        url: '/validar_email/',
        data: {
            'email': email,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            console.log(response)
            if (response.exists) {
                document.getElementById('emailSSO').value = email;
                main.classList.add("right-panel-active");

            } else {
                alert('El email no existe. Inténtalo de nuevo.');
            }
        },
        error: function() {
            alert('Error en la validación del email.');
        }
    });

})

returnButton.addEventListener('click', () => {
    main.classList.remove("right-panel-active");
});
