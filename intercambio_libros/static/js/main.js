/**
 * Script principal para la plataforma de intercambio de libros.
 * Incluye funcionalidades generales como:
 * - Confirmación de acciones importantes (eliminar libro, etc.)
 * - Validación de formularios
 * - Efectos de interfaz
 */

document.addEventListener('DOMContentLoaded', function() {
    // Confirmación para acciones importantes
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres realizar esta acción? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // Efecto hover para tarjetas de libros
    const bookCards = document.querySelectorAll('.card.book-card');
    bookCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.querySelector('.card-img-top').style.transform = 'scale(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.querySelector('.card-img-top').style.transform = 'scale(1)';
        });
    });
    
    // Validación de formularios
    const forms = document.querySelectorAll('form.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Mostrar/ocultar contraseña
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.querySelector('#id_password1, #id_password2');
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
    
    // Cerrar automáticamente las alertas después de 10 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 10000);
    });
});
