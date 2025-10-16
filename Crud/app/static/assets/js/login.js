document.addEventListener('DOMContentLoaded', function() {
    
    // Elementos del formulario
    const passwordInput = document.getElementById('passwordInputRegister');
    const confirmPasswordInput = document.getElementById('confirmPasswordInput');
    const errorDisplay = document.getElementById('passwordMatchError');
    const registerForm = document.getElementById('registerForm');

    // =======================================
    // 1. FUNCIONALIDAD MOSTRAR/OCULTAR CONTRASEÑA (Toggle Eye)
    // =======================================

    /**
     * Configura el comportamiento de 'mostrar/ocultar' para un campo de contraseña.
     * @param {string} inputId - ID del campo de entrada (input).
     * @param {string} toggleId - ID del icono de "ojo".
     */
    function setupPasswordToggle(inputId, toggleId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(toggleId);

        if (input && icon) {
            icon.addEventListener('click', function() {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            });
        }
    }

    // Aplicar a ambos campos de contraseña
    setupPasswordToggle('passwordInputRegister', 'togglePasswordRegister');
    setupPasswordToggle('confirmPasswordInput', 'toggleConfirmPassword');

    // =======================================
    // 2. VALIDACIÓN DE COINCIDENCIA DE CONTRASEÑAS
    // =======================================

    /**
     * Verifica si el valor del campo Contraseña y Confirmar Contraseña son iguales.
     * Muestra o oculta el mensaje de error correspondiente.
     * @returns {boolean} True si coinciden, False si no.
     */
    function validatePasswords() {
        if (!passwordInput || !confirmPasswordInput) return true; // Si los campos no existen, no hay error.

        if (passwordInput.value !== confirmPasswordInput.value) {
            errorDisplay.style.display = 'block';
            
            // Usa la API de Validación de HTML5 para bloquear el envío del formulario
            confirmPasswordInput.setCustomValidity('Las contraseñas deben coincidir.'); 
            return false;
        } else {
            errorDisplay.style.display = 'none';
            confirmPasswordInput.setCustomValidity(''); // Borra cualquier mensaje de error previo
            return true;
        }
    }

    // 2.1. Validar en tiempo real (mientras el usuario escribe)
    if (passwordInput && confirmPasswordInput) {
        passwordInput.addEventListener('keyup', validatePasswords);
        confirmPasswordInput.addEventListener('keyup', validatePasswords);
    }

    // 2.2. Validar al intentar enviar el formulario
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            // Asegura que la validación se ejecute antes de enviar
            if (!validatePasswords()) {
                event.preventDefault(); // Detiene el envío si no coinciden
                // Si la validación falla, Chrome/Firefox mostrará el mensaje de error de HTML5
            }
        });
    }
});