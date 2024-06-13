const singUpButton = document.getElementById('signUp');
const singInButton = document.getElementById('signIn');
const main = document.getElementById('main');

singUpButton.addEventListener('click', () =>{
    main.classList.add("right-panel-active");
})
singInButton.addEventListener('click', () =>{
    main.classList.remove("right-panel-active");
})
