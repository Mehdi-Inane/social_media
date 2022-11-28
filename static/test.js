const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signUpButton_1 = document.getElementById('signUp_1');
const signInButton_1 = document.getElementById('signIn_1');


signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});


signUpButton_1.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});


signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});


signInButton_1.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});
