// Espera a que el contenido del DOM se haya cargado completamente
document.addEventListener('DOMContentLoaded', () => {
    // Obtiene el botón de inicio de sesión por su ID
    const loginButton = document.getElementById('login-button');

    // Añade un evento de clic al botón
    loginButton.addEventListener('click', () => {
        // Cambia el color de fondo del botón temporalmente al hacer clic
        loginButton.style.backgroundColor = '#003d99';
        setTimeout(() => {
            // Vuelve a cambiar el color de fondo del botón después de 200 ms
            loginButton.style.backgroundColor = '#007bff';
        }, 200);
    });
});
