/**
 * Pede confirmacao em acoes destrutivas (logout, cancelar chamado).
 * Marca elementos com data-confirm="mensagem opcional".
 */
export function initConfirmActions() {
    const forms = document.querySelectorAll('form[data-confirm]');
    forms.forEach((form) => {
        form.addEventListener('submit', (event) => {
            const msg = form.dataset.confirm || 'Tem certeza?';
            if (!window.confirm(msg)) {
                event.preventDefault();
            }
        });
    });
}