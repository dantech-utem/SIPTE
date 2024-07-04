const singUpButton = document.getElementById('signUp');
const singInButton = document.getElementById('signIn');
const main = document.getElementById('main');
const returnButton = document.getElementById('boton-regreso');
singUpButton.addEventListener('click', () =>{

    var email = $('#email').val();
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: 'POST',
        url: '/validar_email/',
        data: {
            'email': email,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            if (response.exists) {
                document.getElementById('emailSSO').value = email;
                main.classList.add("right-panel-active");
            } else {
                $('#error-container').html('<div class="mt-3"><div class="alert alert-danger" role="alert">El correo electrónico no está registrado.</div></div>');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al validar el correo electrónico:', error);
        }
    });

})

returnButton.addEventListener('click', () => {
    main.classList.remove("right-panel-active");
});

// Evento que se ejecuta al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    var token = localStorage.getItem('sso_token');

    if (token) {
        // Realiza una solicitud al servidor para validar el token
        $.ajax({
            type: 'POST',
            url: '/validate_token/',
            data: {
                'token': token,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                console.log(response.valid);
                if (response.valid == true) {

                    // El token es válido, realiza la acción deseada (por ejemplo, remover una clase)
                    window.location.href = '/prueba2';
                } else {
                    // El token no es válido, limpia el localStorage y redirige al login
                    localStorage.removeItem('sso_token');
                      // Ajusta la URL según tu aplicación
                }
            },
            error: function(xhr, status, error) {
                console.error('Error al validar el token:', error);
                // Maneja el error apropiadamente si es necesario
            }
        });
    } else {
        // Si no hay token en localStorage, realiza la acción deseada (por ejemplo, remover una clase)
        main.classList.remove("right-panel-active");
    }
});



