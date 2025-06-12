// Confirmação para deletar
document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.querySelectorAll('form[onsubmit*="return confirm"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // A confirmação já está no onsubmit, mas isso é uma boa prática
            // para adicionar lógicas mais complexas no futuro, se necessário.
            const userConfirmed = confirm('Tem certeza que deseja deletar este gestor? Esta ação não pode ser desfeita.');
            if (!userConfirmed) {
                event.preventDefault();
            }
        });
    });
});